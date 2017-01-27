#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Provides an interactive console with pytan available as handler'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.5'

import os  # noqa
import sys  # noqa
sys.dont_write_bytecode = True

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


def create_group_obj(filters=[], options=[], groupname=None):
    filter_defs = pytan.utils.dehumanize_question_filters(filters)
    option_defs = pytan.utils.dehumanize_question_options(options)
    filter_defs = handler._get_sensor_defs(defs=filter_defs)

    add_group_obj = pytan.utils.build_group_obj(filter_defs, option_defs)
    if groupname:
        add_group_obj.name = groupname
    return add_group_obj


def create_parent_group_obj(groups, name="", and_flag=True):
    parent_group = taniumpy.Group()
    parent_group.sub_groups = taniumpy.GroupList()

    parent_group.and_flag = 1 if and_flag else 0

    if name:
        parent_group.name = name

    for i in groups:
        parent_group.sub_groups.append(i)
    return parent_group


def check_preexisting(name, delete_preexisting):
    try:
        g = handler.get("group", name=name)[0]
    except:
        m = "No pre-existing group exists named: {}"
        m = m.format(name)
        print(m)
    else:
        m = "Found pre-existing group named: {} ({})"
        m = m.format(name, g)
        print(m)

        if delete_preexisting:
            handler.session.delete(g)
            m = "Deleted pre-existing group: {}"
            m = m.format(name)
            print(m)
        else:
            m = "delete_preexisting is False and group named '{}' already exists!"
            m = m.format(name)
            print(m)
            sys.exit()


parser = pytan.binsupport.setup_parser(desc=__doc__, help=True)
arggroup_name = 'Manual Create Group Options'
arggroup = parser.add_argument_group(arggroup_name)

arggroup.add_argument(
    '-n',
    '--name',
    required=True,
    action='store',
    dest='name',
    default=None,
    help='Name of parent group to create',
)

arggroup.add_argument(
    '-f1',
    '--filter1',
    required=False,
    action='append',
    dest='filters1',
    default=[],
    help='Filters to use for subgroup1',
)

arggroup.add_argument(
    '-o1',
    '--option1',
    required=False,
    action='append',
    dest='options1',
    default=[],
    help='Options to use for subgroup1',
)

arggroup.add_argument(
    '-f2',
    '--filter2',
    required=False,
    action='append',
    dest='filters2',
    default=[],
    help='Filters to use for subgroup2',
)

arggroup.add_argument(
    '-o2',
    '--option2',
    required=False,
    action='append',
    dest='options2',
    default=[],
    help='Options to use for subgroup2',
)

arggroup.add_argument(
    '--delete',
    required=False,
    action='store_true',
    dest='delete_preexisting',
    default=False,
    help='Delete parent group if it already exists',
)

arggroup.add_argument(
    '-g',
    '--groups',
    required=False,
    action='append',
    dest='groups',
    default=[],
    help='Pre-existing group names to use as part of parent group',
)

arggroup.add_argument(
    '--and_groups',
    required=False,
    action='store_true',
    dest='and_groups',
    default=False,
    help='Pre-existing groups should be and\'d',
)
arggroup.add_argument(
    '--and_parent',
    required=False,
    action='store_true',
    dest='and_parent',
    default=False,
    help='Parent group should be and\'d',
)

args = parser.parse_args()

handler = pytan.binsupport.process_handler_args(parser=parser, args=args)

# DEFINE THE STUFF
# delete_preexisting = True
# name = "ST0105"

# g1_filters = [
#     "Tanium Client Subnet, that contains:172.0.0.1/24",
#     "Tanium Client Subnet, that contains:172.0.0.1/22",
#     "Tanium Client Subnet, that contains:172.0.0.1/25",
# ]

# g2_filters = [
#     "Computer Name, that contains:DIAF"
# ]

# # ORRRRR....
# g2_existing_name = "Is Linux"

# DO THE WORK

check_preexisting(args.name, args.delete_preexisting)

groups = []
existing = []

if args.filters1:
    g = create_group_obj(filters=args.filters1, options=args.options1)
    groups.append(g)

if args.filters2:
    g = create_group_obj(filters=args.filters2, options=args.options2)
    groups.append(g)

if args.groups:
    existing = [handler.get("group", name=x)[0] for x in args.groups]

if existing:
    g = create_parent_group_obj(groups=existing, name="", and_flag=args.and_groups)
    groups.append(g)

parent_group = create_parent_group_obj(groups=groups, name=args.name, and_flag=args.and_parent)

created_group = handler._add(parent_group)
m = "Created Group: {}"
m = m.format(created_group)
print(m)
