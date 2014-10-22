# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.

import os
import sys
import time
import argparse
from argparse import ArgumentDefaultsHelpFormatter as A1
from argparse import RawDescriptionHelpFormatter as A2

pname = os.path.splitext(os.path.basename(sys.argv[0]))[0]


def get_now():
    return time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())


def fn_gen(ext):
    fn = "{}_{}.{}".format(get_now(), pname, ext)
    return fn


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
    # sw_group.add_argument(
    #     '-l',
    #     '--log',
    #     required=False,
    #     default=False,
    #     dest='logfile',
    #     const=fn_gen("log"),
    #     nargs='?',
    #     help='Save the log to a file (if no file supplied, will be saved '
    #     'to $date.$prog.log)',
    # )
    return parser
