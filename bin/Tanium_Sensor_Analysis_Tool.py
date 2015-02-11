#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Asks a question for every sensor and saves the results as a report format'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.3'

import os
import sys
import getpass
import logging
import time
import datetime
import csv
import io
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

OUTPUT_DIR = os.path.join(os.getcwd(), 'TSAT_OUTPUT', utils.get_now())
mylog = logging.getLogger(os.path.basename(my_file))
mylog.setLevel(logging.INFO)


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
    csv_io = io.BytesIO()
    headers = kwargs.get('headers', []) or get_all_headers(rows_list)
    writer = csv.DictWriter(
        csv_io, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC,
    )
    writer.writerow(dict((h, h) for h in headers))
    writer.writerows(rows_list)
    csv_str = csv_io.getvalue()
    return csv_str


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

    arggroup = parser.add_argument_group('TSAT Options')
    arggroup.add_argument(
        '--platform',
        required=False,
        default=[],
        action='append',
        dest='platforms',
        help='Only ask questions for sensors on a given platform',
    )
    arggroup.add_argument(
        '--category',
        required=False,
        default=[],
        action='append',
        dest='categories',
        help='Only ask questions for sensors in a given category',
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
        '--sleep',
        required=False,
        type=int,
        action='store',
        default=1,
        dest='sleep',
        help='Number of seconds to wait between asking questions',
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

    '''
    later:
        file with params to pass for paramaretrized sensors
        saved questions
        filters
    '''

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

    sensors = handler.get_all('sensor')

    # filter out all sensors that have a source_id (i.e. are created as temp sensors for params)
    sensors = [x for x in sensors if not x.source_id]
    mylog.info("Found {} sensors".format(len(sensors)))

    if not sensors:
        mylog.error("No sensors found!")
        sys.exit(1)

    sensors = filter_sensors(sensors, args.platforms, args.categories)
    mylog.info("Filtered down to {} sensors".format(len(sensors)))

    if not sensors:
        mylog.error("Platform/Category filters too restrictive, no sensors match!")
        sys.exit(1)

    reports_run = []

    for idx, sensor in enumerate(sensors):
        report_info = {
            'sensor': sensor.name,
            'msg': 'Not run',
            'report_file': 'N/A',
            'elapsed_seconds': -1,
            'question': 'N/A',
        }
        mylog.info(
            "NOW WORKING ON SENSOR: {} ({}/{})\n".format(sensor.name, idx + 1, len(sensors))
        )
        sensor_dir = os.path.join(args.report_dir, filter_filename(sensor.name))

        if not os.path.exists(sensor_dir):
            os.makedirs(sensor_dir)

        logfile = '{}_{}.log'.format(sensor.name, utils.get_now())
        logfile = filter_filename(logfile)
        logfile_path = os.path.join(sensor_dir, logfile)

        add_file_log(logfile_path, args.debugformat)
        mylog.info("++ Asking question for sensor: {}".format(sensor.name))

        try:
            start_time = datetime.datetime.now()
            ret = handler.ask_manual_human(
                sensors=sensor.name,
                timeout=args.timeout,
                pct_complete_threshold=args.pct_complete_threshold,
            )
        except taniumpy.question_asker.QuestionTimeoutException:
            m = "!! Question failed to complete due to timeout (timeout is {} seconds)".format(
                args.timeout
            )
            report_info['msg'] = m
            reports_run.append(report_info)
            mylog.error(m)
            remove_file_log(logfile_path)
            time.sleep(args.sleep)
            continue
        except Exception as e:
            m = "!! Question failed to complete: {}".format(e)
            report_info['msg'] = m
            reports_run.append(report_info)
            mylog.error(m)
            remove_file_log(logfile_path)
            time.sleep(args.sleep)
            continue

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        m = "++ Asked Question {!r} ID: {!r} in {} seconds".format(
            ret['question_object'].query_text, ret['question_object'].id, elapsed_time.seconds
        )
        report_info['question'] = ret['question_object'].query_text
        report_info['question_id'] = ret['question_object'].id
        report_info['elapsed_seconds'] = elapsed_time.seconds
        report_info['msg'] = m
        mylog.info(m)

        if not ret['question_results']:
            m = "Unable to export question results to report file, no ResultSet returned!"
            report_info['report_file'] = m
            reports_run.append(report_info)
            mylog.error(m)
            remove_file_log(logfile_path)
            time.sleep(args.sleep)
            continue

        if not ret['question_results'].rows:
            m = "Unable to export question results to report file, no rows returned!"
            report_info['report_file'] = m
            reports_run.append(report_info)
            mylog.error(m)
            remove_file_log(logfile_path)
            time.sleep(args.sleep)
            continue

        try:
            report_file, result = handler.export_to_report_file(
                obj=ret['question_results'], export_format='csv', report_dir=sensor_dir,
            )
            report_info['report_file'] = report_file
            m = "++ Report file {!r} written with {} bytes".format
            mylog.info(m(report_file, len(result)))
        except Exception as e:
            m = "Unable to export question results to report file, error: {}".format
            report_info['report_file'] = m
            reports_run.append(report_info)
            mylog.error(m(e))
            remove_file_log(logfile_path)
            time.sleep(args.sleep)
            continue

        reports_run.append(report_info)
        remove_file_log(logfile_path)
        time.sleep(args.sleep)

    headers = ['sensor', 'question', 'question_id', 'elapsed_seconds', 'msg', 'report_file']
    csv_str = csvdictwriter(reports_run, headers=headers)

    csv_file = '{}_{}.csv'.format(my_name, utils.get_now())
    csv_file = filter_filename(csv_file)
    csv_file_path = os.path.join(args.report_dir, csv_file)

    csv_fh = open(csv_file_path, 'wb')
    csv_fh.write(csv_str)
    csv_fh.close()

    mylog.info("Final CSV results of from all questions run written to: {}".format(csv_file_path))
