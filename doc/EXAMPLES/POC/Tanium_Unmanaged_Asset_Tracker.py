#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''TUAT: Compares Unmanaged Asset data against Tanium Clients in System Status'''

# TODO: FIX FOR 2.1.0
'''
Tanium Unmanaged Asset Tracker

How the Unmanaged Asset Tracking works in Tanium out of the box by default:
 - a saved action called "Unmanaged Asset Tracking - Deploy Scan Tools and Scan"
   runs every 50 minutes against every machine that matches the output of the
   question "Unmanaged Asset Scanner Exists is False". This saved action deploys
   a package called "Distribute Unmanaged Asset Tools and Scan", which deploys 4
   files, then runs copy-ua-scanner-and-scan.vbs
 - a saved action called "Unmanaged Asset Tracking - Run Scan"
   runs every 60 minutes against every machine that matches the output of the
   question "Is Windows is True". This saved action deploys
   a package called "Run Unmanaged Asset Scanner", which deploys no
   files, but runs ..\\..\\Tools\\run-ua-scan.vbs /RANDOM_WAIT_TIME_IN_SECONDS:240
 - run-ua-scan.vbs by default only scans for unmanaged assets that exist above the
   IP of the server running the scan. To have it scan the whole range of the last octet,
   the package "Run Unmanaged Asset Scanner" should have the Command modified to add
   "/SCAN_ENTIRE_SUBNET:True"
 - run-ua-scan.vbs can be run by hand to see the output of the unmanaged assets like so:

cd "C:\\Program Files (x86)\\Tanium\\Tanium Client\\Tools"
cscript run-ua-scan.vbs /SCAN_ENTIRE_SUBNET:True /IS_DEBUG:True

 - run-ua-scan.vbs saves the output of the scan to a file
   "C:\Program Files (x86)\Tanium\Tanium Client\Tools\Scans\uaresultsreadable.txt".
   This file is read by the sensor "Unmanaged Assets" and has contents that look
   like the following:

172.16.31.143|N/A|00-0c-29-c1-a1-38|VMware, Inc.
172.16.31.155|N/A|00-0c-29-5e-1d-4f|VMware, Inc.
172.16.31.156|WIN-A12SC6N6T7Q|00-0c-29-d6-43-6e|VMware, Inc.
172.16.31.255|N/A||Org Unavailable
172.16.31.2|N/A|00-50-56-e0-8c-fe|VMware, Inc.
132s - 255 IPs - 5 Unmanaged
132

 - The saved question "Unmanaged Assets" gathers the data from this file for all machines that match the question "Unmanaged Assets does not contain 'not found'"

'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.0'

import os
import sys
import getpass
import logging
import re
# import time
# import datetime
import csv
import StringIO
import string

sys.dont_write_bytecode = True

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
import taniumpy
from pytan import utils
from pytan import constants

examples = []

OUTPUT_DIR = os.path.join(os.getcwd(), 'TUAT_OUTPUT', utils.get_now())
mylog = logging.getLogger("TUAT")
mylog.setLevel(logging.INFO)


def fix_mac(m):
    return str(m).upper().replace('-', ':')


def dictify_resultset_row(rs_row):
    d = dict(zip(
        [x.display_name for x in rs_row.columns],
        [x[0] for x in rs_row.vals if type(x) == list]
    ))
    return d


def fix_newlines(val):
    if type(val) == str:
        # turn \n into \r\n
        val = re.sub(r"([^\r])\n", r"\1\r\n", val)
    return val


def join_list(l, j='\n'):
    if None in l:
        l = ""
    if type(l) == list:
        l = j.join(l)
    return l


def get_managed_assets(last_registration_hours=12, timeout=300, pct_complete_threshold=99,
                       report_dir=OUTPUT_DIR, max_data_age=60):
    kwargs = {}
    if last_registration_hours:
        cache_filter = taniumpy.CacheFilter()
        cache_filter.field = 'last_registration'
        cache_filter.type = 'Date'
        cache_filter.operator = 'Greater'
        cache_filter.not_flag = False
        last_registration = -(last_registration_hours * 60 * 60)
        cache_filter.value = utils.seconds_from_now(last_registration)

        cache_filter_list = taniumpy.CacheFilterList()
        cache_filter_list.append(cache_filter)
        cache_filter_list_body = cache_filter_list.toSOAPBody()
        kwargs['cache_filters'] = cache_filter_list_body

    search_spec = taniumpy.SystemStatusList()
    mas = handler.session.find(search_spec, **kwargs)
    if not mas:
        mylog.critical((
            "No managed assets found that have registered in the last {} hours"
        ).format(last_registration_hours))
        sys.exit(1)

    mylog.info(("Found {} managed assets").format(len(mas)))
    mas_out = handler.export_to_report_file(
        obj=mas,
        export_format='csv',
        report_dir=report_dir,
        prefix="mas_",
    )
    mylog.info(
        "Wrote Managed Assets to CSV file: {!r} ({} bytes)".format(mas_out[0], len(mas_out[1]))
    )
    # get mac address and computer ID of all mas
    client_macs = handler.ask_manual_human(
        sensors=[
            'MAC Address, opt:max_data_age:{}'.format(max_data_age),
            'Computer ID, opt:max_data_age:{}'.format(max_data_age),
        ],
        timeout=timeout,
        pct_complete_threshold=pct_complete_threshold,
    )
    client_macs_out = handler.export_to_report_file(
        obj=client_macs['question_results'],
        export_format='csv',
        report_dir=report_dir,
        prefix="ma_macs_",
    )
    mylog.info((
        "Wrote Client MACs output to CSV file: {!r} ({} bytes)"
    ).format(client_macs_out[0], len(client_macs_out[1])))

    # add the mac address to the ma objects
    for ma_mac in client_macs['question_results'].rows:
        ma_mac_dict = dictify_resultset_row(ma_mac)

        ma_mac_dict['MAC Address'] = fix_mac(ma_mac_dict['MAC Address'])

        if 'no results' in ma_mac_dict['MAC Address'].lower():
            mylog.debug(("Skipping 'no results' MAC result {}").format(ma_mac_dict))
            continue

        # find a matching computer ID for the rows return
        for x in mas:
            if x.computer_id == ma_mac_dict["Computer ID"]:
                mylog.debug((
                    "Adding MAC address '{}' to managed asset '{}' / computer_id: {} / ip_address: {}"
                ).format(ma_mac, str(x.host_name), x.computer_id, x.ipaddress_client))
                # add mac address to the ma
                x.mac_address = ma_mac

    for x in mas:
        v = getattr(x, 'mac_address', None)
        if not v:
            mylog.warning((
                "No MAC address associated with managed asset {}"
            ).format(str(x)))
            x.mac_address = "UNKNOWN"

    # turn it into a normal python list
    mas = [x for x in mas]
    return mas


def get_unmanaged_assets(saved=False, timeout=300, pct_complete_threshold=99,
                         report_dir=OUTPUT_DIR, max_data_age=60):
    if saved:
        uas_ret = handler.ask(
            qtype='saved',
            name="Unmanaged Assets",
            timeout=timeout,
            pct_complete_threshold=pct_complete_threshold,
        )

    else:
        uas_ret = handler.ask(
            qtype='manual_human',
            sensors="Unmanaged Assets, opt:max_data_age:{}".format(max_data_age),
            question_filters=[
                "is Windows, that is:True",
                "Unmanaged Assets, that does not contain:not found"
            ],
            question_options=["max_data_age:{}".format(max_data_age)],
            timeout=timeout,
            pct_complete_threshold=pct_complete_threshold,
        )

    uas_out = handler.export_to_report_file(
        obj=uas_ret['question_results'],
        export_format='csv',
        report_dir=report_dir,
        prefix="uas_",
    )

    mylog.info((
        "Wrote Unmanaged Assets output to CSV file: {!r} ({} bytes)"
    ).format(uas_out[0], len(uas_out[1])))

    uas = []

    # for each unmanaged asset row
    for ua in uas_ret['question_results'].rows:
        ua_dict = dictify_resultset_row(ua)

        if not ua_dict['MAC Address']:
            mylog.debug((
                "Skipping unmanaged asset {}, empty MAC address"
            ).format(ua_dict))
            continue

        # unmanaged asset uses dashes instead of colons, and does not
        # upper case everything, lets fix that
        ua_dict['MAC Address'] = fix_mac(ua_dict['MAC Address'])

        mylog.debug((
            "Found unmanaged asset {}"
        ).format(ua_dict))

        uas.append(ua_dict)

    mylog.info(("Found {} unmanaged assets").format(len(uas)))

    if not uas:
        mylog.critical((
            "No unmanaged assets found when asking question {}: {}"
        ).format(uas_ret['question_object'], uas_ret['question_object'].query_text))
        sys.exit(1)

    return uas


def diff_ua_ma(mas, uas):

    # list of truly unmanaged assets
    true_uas = []

    # for each unmanaged asset row
    for ua in uas:

        reason = None
        found = False

        # check if there is a ma that matches this MAC
        mac_match = [x for x in mas if x.mac_address == ua['MAC Address']]
        if not mac_match:
            reason = 'No matching MAC address in Managed Clients'
        else:
            # check if there is a ma that matches this IP Address
            ip_match = [x for x in mac_match if x.ipaddress_client == ua['IP Address']]
            if not ip_match:
                reason = 'Matching MAC address found, but IP address does not match'
            else:
                found = True

        mylog.debug(("Unmanaged asset {} reason: {}, found: {}").format(ua, reason, found))
        if reason:
            mylog.debug("Adding to truly unmanaged asset list")
            ua['reason'] = reason
            true_uas.append(ua)
        else:
            mylog.debug("Not adding to truly unmanaged asset list")

    mylog.info(("Found {} truly unmanaged assets").format(len(true_uas)))

    return true_uas


def filter_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename


def remove_file_log(logfile):
    basename = os.path.basename(logfile)
    root_logger = logging.getLogger()
    try:
        for x in root_logger.handlers:
            if x.name == basename:
                mylog.info(('Stopped file logging to: {}').format(logfile))
                root_logger.removeHandler(x)
    except:
        pass


def add_file_log(logfile, debug=False):
    remove_file_log(logfile)
    root_logger = logging.getLogger()
    basename = os.path.basename(logfile)
    try:
        file_handler = logging.FileHandler(logfile)
        file_handler.set_name(basename)
        if debug:
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(constants.DEBUG_FORMAT))
        else:
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(constants.INFO_FORMAT))
        root_logger.addHandler(file_handler)
        mylog.info(('Added file logging to: {}').format(logfile))
    except Exception as e:
        mylog.error((
            'Problem setting up file logging to {}: {}'
        ).format(logfile, e))


def process_handler_args(parser, all_args):
    handler_grp_names = ['Tanium Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args[k] for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception as e:
        print e
        sys.exit(99)
    return h


def get_all_headers(rows_list):
    headers = []
    for row_dict in rows_list:
        [headers.append(h) for h in row_dict.keys() if h not in headers]
    return headers


def csvdictwriter(rows_list, **kwargs):
    """returns the rows_list (list of dicts) as a CSV string"""
    csv_io = StringIO.StringIO()
    headers = kwargs.get('headers', []) or get_all_headers(rows_list)
    writer = csv.DictWriter(
        csv_io, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC,
    )
    writer.writerow(dict((h, h) for h in headers))
    writer.writerows(rows_list)
    csv_str = csv_io.getvalue()
    return csv_str


def write_csv(list_of_dicts, report_dir, my_name, story):
    headers = sorted(list_of_dicts[0].keys())
    csv_str = csvdictwriter(list_of_dicts, headers=headers)

    csv_file = '{}_{}.csv'.format(my_name, utils.get_now())
    csv_file = filter_filename(csv_file)
    csv_file_path = os.path.join(report_dir, csv_file)

    csv_fh = open(csv_file_path, 'wb')
    csv_fh.write(csv_str)
    csv_fh.close()

    mylog.info("Final CSV results of {} written to: {}".format(story, csv_file_path))


if __name__ == "__main__":

    utils.version_check(__version__)
    parser = utils.CustomArgParse(
        description=__doc__,
        add_help=True,
        formatter_class=utils.CustomArgFormat,
    )
    auth_group = parser.add_argument_group('Tanium Authentication')
    auth_group.add_argument(
        '-u',
        '--username',
        required=False,
        action='store',
        dest='username',
        default=None,
        help='Name of user',
    )
    auth_group.add_argument(
        '-p',
        '--password',
        required=False,
        action='store',
        default=None,
        dest='password',
        help='Password of user',
    )
    auth_group.add_argument(
        '--host',
        required=False,
        action='store',
        default=None,
        dest='host',
        help='Hostname/ip of SOAP Server',
    )
    auth_group.add_argument(
        '--port',
        required=False,
        action='store',
        default="444",
        dest='port',
        help='Port to use when connecting to SOAP Server',
    )

    opt_group = parser.add_argument_group('Handler Options')
    opt_group.add_argument(
        '-l',
        '--loglevel',
        required=False,
        action='store',
        type=int,
        default=0,
        dest='loglevel',
        help='Logging level to use, increase for more verbosity',
    )
    opt_group.add_argument(
        '--debugformat',
        required=False,
        action='store_true',
        dest='debugformat',
        help='Log with debug level to console and files',
    )

    arggroup = parser.add_argument_group('TUAT Options')
    arggroup.add_argument(
        '--output_dir',
        required=False,
        action='store',
        default=OUTPUT_DIR,
        dest='report_dir',
        help='Directory to save output to',
    )
    arggroup.add_argument(
        '--pct',
        required=False,
        type=float,
        action='store',
        default=99.00,
        dest='pct_complete_threshold',
        help='Percent to consider questions complete',
    )
    arggroup.add_argument(
        '--timeout',
        required=False,
        type=int,
        action='store',
        default=300,
        dest='timeout',
        help='How many seconds to wait before a question times out',
    )
    arggroup.add_argument(
        '--max_data_age',
        required=False,
        type=int,
        action='store',
        default=60,
        dest='max_data_age',
        help='Maximum age of client data in seconds, refresh if cached data is older than this',
    )
    arggroup.add_argument(
        '--saved',
        required=False,
        default=False,
        action='store_true',
        dest='saved',
        help='Used the saved question data for Unmanaged Assets instead of asking a brand new question',
    )
    arggroup.add_argument(
        '--last_registration_hours',
        required=False,
        action='store',
        default=12,
        type=int,
        dest='last_registration_hours',
        help='When fetching Managed Assets, fetch only clients that have reported in the last N hours',
    )

    args = parser.parse_args()

    all_args = args.__dict__

    if not args.username:
        username = raw_input('Tanium Username: ')
        all_args['username'] = username.strip()

    if not args.password:
        password = getpass.getpass('Tanium Password: ')
        all_args['password'] = password.strip()

    if not args.host:
        host = raw_input('Tanium Host: ')
        all_args['host'] = host.strip()

    handler = process_handler_args(parser, all_args)
    if args.debugformat or args.loglevel >= 1:
        mylog.setLevel(logging.DEBUG)
    else:
        mylog.setLevel(logging.INFO)

    if not os.path.exists(args.report_dir):
        os.makedirs(args.report_dir)

    my_name = os.path.splitext(os.path.basename(my_file))[0]
    whole_logfile = '{}_{}.log'.format(my_name, utils.get_now())
    whole_logfile = filter_filename(whole_logfile)
    whole_logfile_path = os.path.join(args.report_dir, whole_logfile)
    add_file_log(whole_logfile_path, args.debugformat)

    # get the managed assets (clients) (mas = managed assets)
    mas = get_managed_assets(
        last_registration_hours=args.last_registration_hours,
        timeout=args.timeout,
        pct_complete_threshold=args.pct_complete_threshold,
        report_dir=args.report_dir,
        max_data_age=args.max_data_age,
    )

    # get the unmanaged assets ( uas = unmanaged assets )
    uas = get_unmanaged_assets(
        saved=args.saved,
        timeout=args.timeout,
        pct_complete_threshold=args.pct_complete_threshold,
        report_dir=args.report_dir,
        max_data_age=args.max_data_age,
    )

    # diff the mas and uas and get a list of truly unmanaged assets
    true_uas = diff_ua_ma(mas, uas)

    write_csv(
        list_of_dicts=true_uas,
        report_dir=args.report_dir,
        my_name=my_name,
        story="truly unmanaged assets"
    )
