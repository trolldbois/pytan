# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.

import os
import sys
import argparse
from argparse import ArgumentDefaultsHelpFormatter as A1
from argparse import RawDescriptionHelpFormatter as A2

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

pname = os.path.splitext(os.path.basename(sys.argv[0]))[0]

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

# import SoapUtil
import SoapConstants


class CustomFormatter(A1, A2):
    pass


class CustomParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomFormatter
        #print kwargs
        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message):
        self.print_help()
        print('ERROR:{}:{}\n'.format(pname, message))
        sys.exit(2)


def setup_parser(desc, help=False):
    parser = CustomParser(
        description=desc,
        add_help=help,
        formatter_class=CustomFormatter,
    )
    auth_group = parser.add_argument_group('SOAP Connection')
    auth_group.add_argument(
        '-u',
        '--username',
        required=True,
        action='store',
        dest='username',
        default=None,
        help='Name of user',
    )
    auth_group.add_argument(
        '-p',
        '--password',
        required=True,
        action='store',
        default=None,
        dest='password',
        help='Password of user',
    )
    auth_group.add_argument(
        '--host',
        required=True,
        action='store',
        default=None,
        dest='host',
        help='Hostname/ip of SOAP Server',
    )
    auth_group.add_argument(
        '--protocol',
        required=False,
        action='store',
        default="https",
        dest='protocol',
        help='Protocol to use when connecting to SOAP Server',
    )
    auth_group.add_argument(
        '--port',
        required=False,
        action='store',
        default="443",
        dest='port',
        help='Port to use when connecting to SOAP Server',
    )
    auth_group.add_argument(
        '--path',
        required=False,
        action='store',
        default="/soap",
        dest='soap_path',
        help='SOAP Path to use when connecting to SOAP Server',
    )

    sw_group = parser.add_argument_group('Soap Wrapper')
    sw_group.add_argument(
        '-l',
        '--loglevel',
        required=False,
        action='store',
        type=int,
        default=0,
        dest='loglevel',
        help='Logging level to use, increase for more verbosity',
    )
    sw_group.add_argument(
        '--debugformat',
        required=False,
        action='store_true',
        default=False,
        dest='debugformat',
        help='Use debug format for log output',
    )

    return parser


def setup_transform_parser(parser):
    exp_group = parser.add_argument_group('Report Options')
    exp_group.add_argument(
        '--format',
        required=True,
        action='store',
        dest='ftype',
        choices=SoapConstants.TRANSFORM_FORMATS.keys(),
        help='Format to save response as',
    )

    exp_group.add_argument(
        '--filename',
        required=False,
        action='store',
        default=argparse.SUPPRESS,
        dest='fname',
        help='File name of report to create (will be automatically '
        'generated if not supplied)',
    )

    exp_group.add_argument(
        '--fileext',
        required=False,
        action='store',
        default=argparse.SUPPRESS,
        dest='fext',
        help='File name extension of report to create (--format used if not '
        'supplied)',
    )

    exp_group.add_argument(
        '--dirname',
        required=False,
        action='store',
        default=argparse.SUPPRESS,
        dest='fdir',
        help='Directory to create report in (current dir used if not '
        'supplied)',
    )

    exp_group.add_argument(
        '--filename_prefix',
        required=False,
        action='store',
        default=argparse.SUPPRESS,
        dest='fprefix',
        help='Prefix to add to the report filename',
    )
    exp_group.add_argument(
        '--filename_postfix',
        required=False,
        action='store',
        default=argparse.SUPPRESS,
        dest='fpostfix',
        help='Postfix to add to the report filename',
    )

    return parser


def setup_transform_resultxml_parser(parser):
    resultxml_group = parser.add_argument_group('Question Report Options')

    for TB, TB_DEF in SoapConstants.TRANSFORM_BOOL_KWARGS.iteritems():
        if TB_DEF is False:
            tb_action = "store_true"
        else:
            tb_action = "store_false"

        resultxml_group.add_argument(
            '--%s' % TB,
            required=False,
            action=tb_action,
            dest=TB,
            default=TB_DEF,
            help=SoapConstants.TRANSFORM_BOOL_HELP[TB],
        )
    return parser


def setup_transform_sort_parser(parser):
    sort_group = parser.add_argument_group('Report Sort Options')

    sort_group.add_argument(
        '--sort',
        required=False,
        action='append',
        dest='HEADER_SORT_PRIORITY',
        default=SoapConstants.TRANSFORM_HEADER_SORT_PRIORITY,
        help='Columns to sort first in output',
    )
    return parser
