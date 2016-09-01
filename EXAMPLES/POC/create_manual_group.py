#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a manual computer group'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.6'

# change me to the location of PyTan!
pytan_loc = '/github/pytan'

import os  # noqa
import re  # noqa
import sys  # noqa
import time  # noqa

sys.dont_write_bytecode = True
sys.path.append(os.path.join(os.path.expanduser(pytan_loc), 'lib'))

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan  # noqa
import pytan.binsupport  # noqa
import taniumpy  # noqa

ip_re = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')


def is_ip(t):
    if ip_re.match(t):
        ret = True
    else:
        ret = False
    return ret


pytan.binsupport.version_check(reqver=__version__)

setupmethod = getattr(pytan.binsupport, 'setup_pytan_shell_argparser')
responsemethod = getattr(pytan.binsupport, 'process_pytan_shell_args')

parser = setupmethod(doc=__doc__)
parser.add_argument(
    '-g',
    '--group_name',
    required=True,
    action='store',
    dest='group_name',
    type=str,
    default='',
    help='Name of manual computer group to create',
)

parser.add_argument(
    '-a',
    '--add',
    required=False,
    action='append',
    dest='adds',
    type=str,
    default=[],
    help='Name or IP of computer to add to manual computer group',
)

parser.add_argument(
    '-f',
    '--file',
    required=False,
    action='store',
    dest='file',
    type=str,
    default='',
    help='Name of file containing names or IPs of computers to add to manual computer group, one per line',
)

args = parser.parse_args()

handler = pytan.binsupport.process_handler_args(parser=parser, args=args)
response = responsemethod(parser=parser, handler=handler, args=args)

if args.file:
    try:
        v = open(args.file, 'r')
        fileadds = [x.strip() for x in v.readlines() if x.strip()]
        v.close()
    except Exception as e:
        m = "Unable to open file {}, error: {}".format
        print(m(args.file, e))
else:
    fileadds = []

all_adds = args.adds + fileadds
all_adds = list(set(all_adds))

computer_specs = taniumpy.ComputerSpecList()
for a in all_adds:
    spec = taniumpy.ComputerGroupSpec()
    if is_ip(a):
        spec.ip_address = a
    else:
        spec.computer_name = a
    computer_specs.append(spec)

computer_group = taniumpy.ComputerGroup()
computer_group.name = args.group_name
computer_group.computer_specs = computer_specs

m = "Adding {}".format
print(m(computer_group))
added_computer_group = handler.session.add(computer_group)
m = "Added {}".format
print(m(added_computer_group))

# m = "Sleeping 5 seconds..."
# print(m)
# time.sleep(5)

# m = "Verifying {} is searchable".format
# print(m(added_computer_group))
# verify_computer_group = handler.session.find(added_computer_group)
# m = "Verified {} is searchable".format
# print(m(verify_computer_group))

# actual_group_filter = 'Manual Group Membership, that =:{}'.format(added_computer_group.id)
# actual_group = handler.create_group(groupname=args.group_name, filters=[actual_group_filter])

# m = "Added {}".format
# print(m(actual_group))
