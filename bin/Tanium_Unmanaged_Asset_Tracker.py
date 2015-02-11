#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Compares Unmanaged Asset data against Tanium Clients in System Status'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.3'

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
mylog = logging.getLogger(os.path.basename(my_file))
mylog.setLevel(logging.INFO)


def fix_newlines(val):
    if type(val) == str:
        # turn \n into \r\n
        val = re.sub(r"([^\r])\n", r"\1\r\n", val)
    return val


def join_list(l, j='\n'):
    if type(l) == list:
        l = j.join(l)
    return l


def get_tanium_clients(last_registration_hours=12):
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

    clients = handler.get_all('client', **kwargs)
    return clients


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


def filter_sensors(sensors, platforms, categories):
    if not platforms and not categories:
        return sorted(sensors, key=lambda x: x.category)

    new_sensors = []
    for x in sorted(sensors, key=lambda x: x.category):
        if categories:
            if str(x.category).lower() not in [y.lower() for y in args.categories]:
                continue

        platforms = [
            q.platform for q in x.queries
            if q.script
            and 'THIS IS A STUB' not in q.script
            and 'echo Windows Only' not in q.script
        ]

        if platforms:
            match = [
                p for p in platforms
                if p.lower() in [y.lower() for y in args.platforms]
            ]
            if not match:
                continue
        new_sensors.append(x)
    return new_sensors


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


if __name__ == "__main__":
    print "THIS IS A WORK IN PROGRESS, NOT READY FOR USE"
    sys.exit(1)

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
        default=1,
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
        '--saved',
        required=False,
        default=False,
        action='store_true',
        dest='saved',
        help='Used the saved question data for Unmanaged Assets instead of asking a brand new question',
    )
    arggroup.add_argument(
        '--output_dir',
        required=False,
        action='store',
        default=OUTPUT_DIR,
        dest='report_dir',
        help='Directory to save output to',
    )
    arggroup.add_argument(
        '--last_registration_hours',
        required=False,
        action='store',
        default=12,
        type=int,
        dest='last_registration_hours',
        help='When fetching Tanium Client list, fetch only clients that have reported in the last N hours',
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
    if args.debugformat:
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

    # uas = unmanaged assets
    if args.saved:
        uas_ret = handler.ask(qtype='saved', name="Unmanaged Assets")
    else:
        uas_ret = handler.ask(
            qtype='manual_human',
            sensors="Unmanaged Assets",
            question_filters=[
                "is Windows, that is:True",
                "Unmanaged Assets, that does not contain:not found"
            ],
        )

    uas = uas_ret['question_results']

    # mas = managed assets
    # use question instead of client list??
    mas = get_tanium_clients(args.last_registration_hours)

    # list of truly unmanaged assets
    truly_ua = []

    # for each unmanaged asset row
    for ua in uas.rows:

        # check if there is a ma that matches this IP Address
        ip_match = [x for x in mas if x.ipaddress_client == ua['IP Address']]

        if not ip_match:
            reason = 'No matching IP address in Managed Clients'
            keys = [x.display_name for x in ua.columns]
            values = [fix_newlines(join_list(x)) for x in ua.vals]
            true_ua = dict(zip(keys, values))
            true_ua['reason'] = reason
            truly_ua.append(true_ua)
            continue

        hostname_match = []
