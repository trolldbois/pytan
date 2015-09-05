#!/usr/bin/env python -i
import os
import sys
import getpass
import traceback
import time

sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

pytan_loc = '~/gh/pytan'
sys.path.append(os.path.join(os.path.expanduser(pytan_loc), 'lib'))

import pytan
import taniumpy # noqa
import taniumpy as api # noqa
from pytan import utils
from pytan import constants  # noqa

sys.dont_write_bytecode = True


def process_handler_args(parser, all_args):
    my_args = dict(all_args)
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: my_args.pop(k) for k in handler_opts}
    # handler_args['session_lib'] = 'httplib'
    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception:
        traceback.print_exc()
        sys.exit(99)
    return h


parent_parser = utils.setup_parser(__doc__)
parser = utils.CustomArgParse(
    description=__doc__,
    parents=[parent_parser],
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


def get_rd(q, **kwargs):
    r = handler.get_result_data(q, **kwargs)
    print "*** GetResultData with args: {} returned {}".format(kwargs, r)
    return r


def get_status(r):
    status_url = 'export/{}.status'.format(r)
    status = handler.session.http_get(url=status_url).strip()
    print "*** Export status ({}): {}".format(status_url, status)
    return status


def get_export(r):
    data_url = 'export/{}.gz'.format(r)
    data = handler.session.http_get(url=data_url)
    print "*** Export data ({}):\n{}".format(data_url, data)

print "######### Asking question and not waiting for results"
v = handler.ask_manual(sensors='Computer Name', get_results=False)
q = v['question_object']

print "######### Doing CSV server side export"
start_csv_export = get_rd(q, export_flag=1, export_format=0)
csv_export_status = get_status(start_csv_export)
csv_export_data = get_export(start_csv_export)

print "######### Asking question and waiting for results"
v = handler.ask_manual(sensors='Computer Name', get_results=True)
q = v['question_object']

print "######### Doing CSV server side export"
start_csv_export = get_rd(q, export_flag=1, export_format=0)
csv_export_status = get_status(start_csv_export)
csv_export_data = get_export(start_csv_export)

time.sleep(1)

print "######### Doing XML server side export"
start_xml_export = get_rd(q, export_flag=1, export_format=1)
xml_export_status = get_status(start_xml_export)
xml_export_data = get_export(start_xml_export)

time.sleep(1)

print "######### Doing CEF server side export"
start_cef_export = get_rd(q, export_flag=1, export_format=2)
cef_export_status = get_status(start_cef_export)
cef_export_data = get_export(start_cef_export)

time.sleep(1)

print "######### Doing CEF server side export with trailing/leading"
start_cef_lt_export = get_rd(q, export_flag=1, export_format=2, export_leading_text="--LEADER--", export_trailing_text="--TRAILING--")
cef_lt_export_status = get_status(start_cef_lt_export)
cef_lt_export_data = get_export(start_cef_lt_export)
