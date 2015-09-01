#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Collection of classes and methods used throughout :mod:`pytan` for command line support"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import logging
import code
import atexit
import traceback
import pprint
import argparse
import getpass
import json
import string
import csv
import io
import datetime
import time
from argparse import ArgumentDefaultsHelpFormatter as A1 # noqa
from argparse import RawDescriptionHelpFormatter as A2 # noqa

try:
    import readline
    import rlcompleter
except:
    pass

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]
[sys.path.append(aa) for aa in path_adds if aa not in sys.path]

import pytan
import taniumpy

__version__ = pytan.__version__
pname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
mylog = logging.getLogger("pytan.handler")


class HistoryConsole(code.InteractiveConsole):
    """Class that provides an interactive python console with full auto complete, history, and history file support.

    Examples
    --------
        >>> console = pytan.binsupport.HistoryConsole()
    """
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        try:
            self.rldoc = rlcompleter.__doc__
        except:
            pass
        try:
            self.init_history(histfile)
        except:
            pass

    def init_history(self, histfile):
        if 'libedit' in readline.__doc__:
            # osx style readline
            readline.parse_and_bind("bind ^I rl_complete")
            readline.parse_and_bind("bind ^R em-inc-search-prev")
        else:
            # unix style readline
            readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    @staticmethod
    def save_history(histfile):
        try:
            readline.write_history_file(histfile)
        except:
            pass


class CustomArgFormat(A1, A2):
    """Multiple inheritance Formatter class for :class:`argparse.ArgumentParser`.

    If a :class:`argparse.ArgumentParser` class uses this as it's Formatter class, it will show the defaults for each argument in the `help` output
    """
    pass


class CustomArgParse(argparse.ArgumentParser):
    """Custom :class:`argparse.ArgumentParser` class which does a number of things:

        * Uses :class:`pytan.utils.CustomArgFormat` as it's Formatter class, if none was passed in
        * Prints help if there is an error
        * Prints the help for any subparsers that exist
    """
    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomArgFormat
        # print kwargs
        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message):
        self.print_help()
        print('ERROR:{}:{}\n'.format(pname, message))
        sys.exit(2)

    def print_help(self, **kwargs):
        super(CustomArgParse, self).print_help(**kwargs)
        subparsers_actions = [
            action for action in self._actions
            if isinstance(action, argparse._SubParsersAction)
        ]
        for subparsers_action in subparsers_actions:
            print ""
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                # print subparser
                # print(" ** {} '{}':".format(
                    # subparsers_action.dest, choice))
                print(subparser.format_help())


def setup_parser(desc, help=False):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts that use :mod:`pytan`. This establishes the basic arguments that are needed by all such scripts, such as:

        * --help
        * --username
        * --password
        * --host
        * --port
        * --loglevel
        * --debugformat
    """
    parser = CustomArgParse(description=desc, add_help=help, formatter_class=CustomArgFormat)
    arggroup_name = 'Handler Authentication'
    auth_group = parser.add_argument_group(arggroup_name)
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
        '--session_id',
        required=False,
        action='store',
        default=None,
        dest='session_id',
        help='Session ID to authenticate with instead of username/password',
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
        default="443",
        dest='port',
        help='Port to use when connecting to SOAP Server',
    )

    arggroup_name = 'Handler Options'
    opt_group = parser.add_argument_group(arggroup_name)
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
        default=False,
        dest='debugformat',
        help="Enable debug format for logging",
    )
    opt_group.add_argument(
        '--record_all_requests',
        required=False,
        action='store_true',
        default=False,
        dest='record_all_requests',
        help="Record all requests in handler.session.ALL_REQUESTS_RESPONSES",
    )
    opt_group.add_argument(
        '--stats_loop_enabled',
        required=False,
        action='store_true',
        default=False,
        dest='stats_loop_enabled',
        help="Enable the statistics loop",
    )
    opt_group.add_argument(
        '--http_auth_retry',
        required=False,
        action='store_false',
        default=True,
        dest='http_auth_retry',
        help="Disable retry on HTTP authentication failures",
    )
    opt_group.add_argument(
        '--http_retry_count',
        required=False,
        action='store',
        type=int,
        default=5,
        dest='http_retry_count',
        help="Retry count for HTTP failures/invalid responses",
    )

    return parser


def setup_parent_parser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser` and return a parser object for adding arguments to
    """
    parent_parser = setup_parser(desc=doc, help=False)
    parser = CustomArgParse(description=doc, parents=[parent_parser])
    return parser


def setup_tsat_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to get objects.
    """
    parser = setup_parent_parser(doc=doc)

    output_dir = os.path.join(os.getcwd(), 'TSAT_OUTPUT', pytan.utils.get_now())

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
        default=output_dir,
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
    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='question_filters',
        help='Whole question filter; pass --filters-help to get a full description',
    )
    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='question_options',
        help='Whole question option; pass --options-help to get a full description',
    )

    arggroup.add_argument(
        '--sensors-help',
        required=False,
        action='store_true',
        default=False,
        dest='sensors_help',
        help='Get the full help for sensor strings',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    return parser


def setup_get_object_argparser(obj, doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to get objects.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    get_object_group = parser.add_argument_group(arggroup_name)

    get_object_group.add_argument(
        '--all',
        required=False,
        default=False,
        action='store_true',
        dest='all',
        help='Get all {}s'.format(obj),
    )

    obj_map = pytan.utils.get_obj_map(obj)
    search_keys = obj_map['search']

    if 'id' not in search_keys:
        search_keys.append('id')

    if obj == 'whitelisted_url':
        search_keys.append('url_regex')

    for k in search_keys:
        get_object_group.add_argument(
            '--{}'.format(k),
            required=False,
            action='append',
            default=[],
            dest=k,
            help='{} of {} to get'.format(k, obj),
        )

    return parser


def setup_print_server_info_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to print sensor info.
    """
    parser = setup_parent_parser(doc=doc)
    output_group = parser.add_argument_group('Output Options')

    output_group.add_argument(
        '--json',
        required=False,
        default=False,
        action='store_true',
        dest='json',
        help='Show a json dump of the server information',
    )
    return parser


def setup_print_sensors_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to print server info.
    """
    parser = setup_get_object_argparser(obj='sensor', doc=__doc__)
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--category',
        required=False,
        default=[],
        action='append',
        dest='categories',
        help='Only show sensors in given category',
    )
    output_group.add_argument(
        '--platform',
        required=False,
        default=[],
        action='append',
        dest='platforms',
        help='Only show sensors for given platform',
    )
    output_group.add_argument(
        '--hide_params',
        required=False,
        default=False,
        action='store_true',
        dest='hide_params',
        help='Do not show parameters in output',
    )
    output_group.add_argument(
        '--params_only',
        required=False,
        default=False,
        action='store_true',
        dest='params_only',
        help='Only show sensors with parameters',
    )
    output_group.add_argument(
        '--json',
        required=False,
        default=False,
        action='store_true',
        dest='json',
        help='Show a json dump of the server information',
    )
    return parser


def setup_create_sensor_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a sensor.
    """
    parser = pytan.binsupport.setup_parser(desc=doc, help=True)
    arggroup_name = 'Create Sensor Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--unsupported',
        required=False,
        action='store',
        dest='unsupported',
        default=None,
        help='Creating sensors using this method not yet supported, use create_sensor_from_json instead!',
    )
    return parser


def setup_create_group_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a group.
    """
    parser = pytan.binsupport.setup_parser(desc=doc, help=True)
    arggroup_name = 'Create Group Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='groupname',
        default=None,
        help='Name of group to create',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        dest='filters',
        default=[],
        help='Filters to use for group, supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        dest='filter_options',
        default=[],
        help='Filter options to use for group, supply --options-help to see options'
        ' help',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    return parser


def setup_create_whitelisted_url_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a whitelisted_url.
    """
    parser = setup_parser(desc=doc, help=True)
    arggroup_name = 'Create Whitelisted URL Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--url',
        required=True,
        action='store',
        dest='url',
        default=None,
        help='Text of new Whitelisted URL',
    )

    arggroup.add_argument(
        '--regex',
        required=False,
        action='store_true',
        dest='regex',
        default=False,
        help='Whitelisted URL is a regex pattern',
    )

    arggroup.add_argument(
        '-d',
        '--download',
        required=False,
        action='store',
        dest='download_seconds',
        type=int,
        default=86400,
        help='Download Whitelisted URL every N seconds',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to Whitelisted URL',
    )
    return parser


def setup_create_package_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a package.
    """
    parser = pytan.binsupport.setup_parser(desc=doc, help=True)
    arggroup_name = 'Create Package Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of package to create',
    )

    arggroup.add_argument(
        '-c',
        '--command',
        required=True,
        action='store',
        dest='command',
        default='',
        help='Command to execute with package',
    )

    arggroup.add_argument(
        '-d',
        '--display-name',
        required=False,
        action='store',
        dest='display_name',
        default='',
        help='Display name of package',
    )

    arggroup.add_argument(
        '--command-timeout',
        required=False,
        action='store',
        dest='command_timeout_seconds',
        type=int,
        default=600,
        help='Command for this package timeout in N seconds',
    )

    arggroup.add_argument(
        '--expire-seconds',
        required=False,
        action='store',
        dest='expire_seconds',
        type=int,
        default=600,
        help='Expire actions created for this package in N seconds',
    )

    arggroup.add_argument(
        '-f',
        '--file-url',
        required=False,
        action='store',
        dest='file_urls',
        default=[],
        help='URL of file to include with package, can specify any of the '
        'following: "$url", or "$download_seconds::$url", or "$filename||$url",'
        ' or "$filename||$download_seconds::$url"',
    )

    arggroup.add_argument(
        '--parameters-file',
        required=False,
        action='store',
        dest='parameters_json_file',
        default='',
        help='JSON file describing parameters for this package, see '
        'doc/example_of_all_package_parameters.json for an example',
    )
    arggroup.add_argument(
        '-vf',
        '--verify-filter',
        required=False,
        action='append',
        dest='verify_filters',
        default=[],
        help='Filters to use for verifying the package after it is deployed, '
        ', supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-vo',
        '--verify-option',
        required=False,
        action='append',
        dest='verify_filter_options',
        default=[],
        help='Options to use for the verify filters, supply --options-help to see '
        'options help',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )

    arggroup.add_argument(
        '--verify-expire-seconds',
        required=False,
        action='store',
        dest='verify_expire_seconds',
        type=int,
        default=600,
        help='Expire the verify filters used by this package in N seconds',
    )
    return parser


def setup_pytan_shell_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a python shell.
    """
    parser = pytan.binsupport.setup_parser(desc=doc, help=True)
    return parser


def setup_create_user_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a user.
    """
    parser = pytan.binsupport.setup_parser(desc=doc, help=True)
    arggroup_name = 'Create User Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='username',
        default=None,
        help='Name of user to create',
    )

    arggroup.add_argument(
        '-rn',
        '--rolename',
        required=False,
        action='append',
        dest='rolename',
        default=[],
        help='Name of role to assign to new user',
    )

    arggroup.add_argument(
        '-ri',
        '--roleid',
        required=False,
        action='append',
        type=int,
        dest='roleid',
        default=[],
        help='ID of role to assign to new user',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to user',
    )
    return parser


def setup_create_json_object_argparser(obj, doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create objects from json files.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Create {} from JSON Options'.format(obj.replace('_', ' ').capitalize())
    arggroup = parser.add_argument_group(arggroup_name)
    arggroup.add_argument(
        '-j',
        '--json',
        required=True,
        action='store',
        default='',
        dest='json_file',
        help='JSON file to use for creating the object',
    )
    return parser


def setup_delete_object_argparser(obj, doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to delete objects.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    arggroup = parser.add_argument_group(arggroup_name)

    obj_map = pytan.utils.get_obj_map(obj)
    search_keys = obj_map['search']

    if obj == 'whitelisted_url':
        search_keys.append('url_regex')

    for k in search_keys:
        arggroup.add_argument(
            '--{}'.format(k),
            required=False,
            action='append',
            default=[],
            dest=k,
            help='{} of {} to get'.format(k, obj),
        )

    return parser


def setup_ask_saved_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask saved questions.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Saved Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup_name = 'Saved Question Selectors'
    arggroup = parser.add_argument_group(arggroup_name)
    arggroup.add_argument(
        '--refresh_data',
        required=False,
        action='store_true',
        default=False,
        dest='refresh_data',
        help='Refresh the data available for a saved question',
    )

    group = arggroup.add_mutually_exclusive_group()

    obj = 'saved_question'
    obj_map = pytan.utils.get_obj_map(obj)
    search_keys = obj_map['search']
    for k in search_keys:
        group.add_argument(
            '--{}'.format(k),
            required=False,
            action='store',
            dest=k,
            help='{} of {} to ask'.format(k, obj),
        )

    parser = add_ask_report_argparser(parser=parser)
    return parser


def setup_stop_action_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to stop actions.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Stop Action Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-i',
        '--id',
        required=True,
        type=int,
        action='store',
        dest='id',
        help='ID of Deploy Action to stop',
    )

    return parser


def setup_deploy_action_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to deploy actions.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Deploy Action Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--run',
        required=False,
        action='store_true',
        default=False,
        dest='run',
        help='Run the deploy action, if not supplied the deploy action will '
        'only ask the question that matches --filter and save the results to '
        'csv file for verification',
    )

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-results',
        action='store_false',
        dest='get_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not get the results after starting the deploy '
        'action'
    )
    group.add_argument(
        '--results',
        action='store_true',
        dest='get_results',
        default=True,
        required=False,
        help='Get the results after starting the deploy action '
        '(default)',
    )

    arggroup.add_argument(
        '-k',
        '--package',
        required=False,
        action='store',
        default='',
        dest='package',
        help='Package to deploy action with, optionally describe parameters, '
        'pass --package-help to get a full description',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='action_filters',
        help='Filter to deploy action against; pass --filters-help'
        'to get a full description',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='action_options',
        help='Options for deploy action filter; pass --options-help to get a '
        'full description',
    )

    arggroup.add_argument(
        '--start_seconds_from_now',
        required=False,
        action='store',
        type=int,
        default=None,
        dest='start_seconds_from_now',
        help='Start the action N seconds from now',
    )

    arggroup.add_argument(
        '--expire_seconds',
        required=False,
        action='store',
        type=int,
        default=None,
        dest='expire_seconds',
        help='Expire the action N seconds after it starts, if not supplied '
        'the packages own expire_seconds will be used',
    )

    arggroup.add_argument(
        '--package-help',
        required=False,
        action='store_true',
        default=False,
        dest='package_help',
        help='Get the full help for package string',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    parser = add_report_file_options(parser=parser)
    return parser


def setup_get_results_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to get results for questions or actions.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Get Result Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-o',
        '--object',
        action='store',
        default='question',
        choices=['saved_question', 'question', 'action'],
        dest='objtype',
        help='Type of object to get results for',
    )

    arggroup.add_argument(
        '-i',
        '--id',
        required=False,
        action='store',
        type=int,
        dest='id',
        help='id of object to get results for',
    )

    arggroup.add_argument(
        '-n',
        '--name',
        required=False,
        action='store',
        default='',
        dest='name',
        help='name of object to get results for',
    )
    parser = add_ask_report_argparser(parser)
    return parser


def setup_ask_parsed_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask parsed questions.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Parsed Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-q',
        '--question_text',
        required=True,
        action='store',
        default='',
        dest='question_text',
        help='The question text you want the server to parse into a list of parsed results',
    )

    arggroup.add_argument(
        '--picker',
        required=False,
        action='store',
        type=int,
        dest='picker',
        help='The index number of the parsed results that correlates to the actual question you wish to run -- you can get this by running this once without it to print out a list of indexes',
    )

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-results',
        action='store_false',
        dest='get_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not get the results after asking the quesiton '
        'action'
    )
    group.add_argument(
        '--results',
        action='store_true',
        dest='get_results',
        default=True,
        required=False,
        help='Get the results after asking the quesiton (default)',
    )
    parser = add_ask_report_argparser(parser=parser)
    return parser


def setup_ask_manual_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask manual questions.
    """
    parser = setup_parent_parser(doc=doc)
    arggroup_name = 'Manual Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-s',
        '--sensor',
        required=False,
        action='append',
        default=[],
        dest='sensors',
        help='Sensor, optionally describe parameters, options, and a filter'
        '; pass --sensors-help to get a full description',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='question_filters',
        help='Whole question filter; pass --filters-help to get a full description',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='question_options',
        help='Whole question option; pass --options-help to get a full description',
    )

    arggroup.add_argument(
        '--sensors-help',
        required=False,
        action='store_true',
        default=False,
        dest='sensors_help',
        help='Get the full help for sensor strings',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-results',
        action='store_false',
        dest='get_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not get the results after asking the quesiton '
        'action'
    )
    group.add_argument(
        '--results',
        action='store_true',
        dest='get_results',
        default=True,
        required=False,
        help='Get the results after asking the quesiton '
        '(default)',
    )
    parser = add_ask_report_argparser(parser=parser)
    return parser


def add_ask_report_argparser(parser):
    """Method to extend a :class:`pytan.utils.CustomArgParse` class for command line scripts with arguments for scripts that need to supply export format subparsers for asking questions.
    """
    parser = add_report_file_options(parser=parser)

    arggroup_name = 'Export Options'
    arggroup = parser.add_argument_group(arggroup_name)

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--enable_sse',
        action='store_true',
        dest='sse',
        default=True,
        required=False,
        help='Perform a server side export when getting data'
    )
    group.add_argument(
        '--disable_sse',
        action='store_false',
        dest='sse',
        required=False,
        help='Perform a normal get result data export when getting data'
    )

    arggroup.add_argument(
        '--sse_format',
        required=False,
        action='store',
        default='xml_obj',
        choices=['csv', 'xml', 'xml_obj', 'cef'],
        dest='sse_format',
        help='If sse = True, perform server side export in this format',
    )

    arggroup.add_argument(
        '--leading',
        required=False,
        action='store',
        default='',
        dest='leading',
        help='If sse = True, and sse_format = "cef", prepend each row with this text',
    )
    arggroup.add_argument(
        '--trailing',
        required=False,
        action='store',
        default='',
        dest='trailing',
        help='If sse = True, and sse_format = "cef", append each row with this text',
    )

    arggroup.add_argument(
        '--export_format',
        action='store',
        default='csv',
        choices=['csv', 'xml', 'json'],
        dest='export_format',
        help='Export Format to create report file in, only used if sse = False',
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='For export_format: csv, Sort headers by given names'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Sort the headers with a basic alphanumeric sort (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--add-sensor',
        action='store_true',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Add the sensor names to each header'
    )
    group.add_argument(
        '--no-add-sensor',
        action='store_false',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not add the sensor names to each header (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--add-type',
        action='store_true',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Add the result type to each header'
    )
    group.add_argument(
        '--no-add-type',
        action='store_false',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not add the result type to each header (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--expand-columns',
        action='store_true',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Expand multi-line cells into their own rows that have sensor correlated columns in the new rows'
    )
    group.add_argument(
        '--no-columns',
        action='store_false',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not add expand multi-line cells into their own rows (default)'
    )
    return parser


def add_report_file_options(parser):
    """Method to extend a :class:`pytan.utils.CustomArgParse` class for command line scripts with arguments for scripts that need to supply export file and directory options.
    """
    opt_group = parser.add_argument_group('Report File Options')
    opt_group.add_argument(
        '--file',
        required=False,
        action='store',
        default=None,
        dest='report_file',
        help='File to save report to (will be automatically generated if not '
        'supplied)',
    )
    opt_group.add_argument(
        '--dir',
        required=False,
        action='store',
        default=None,
        dest='report_dir',
        help='Directory to save report to (current directory will be used if '
        'not supplied)',
    )
    return parser


def add_get_object_report_argparser(parser):
    """Method to extend a :class:`pytan.utils.CustomArgParse` class for command line scripts with arguments for scripts that need to supply export format subparsers for getting objects.
    """
    parser = add_report_file_options(parser)
    arggroup_name = 'Export Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--export_format',
        action='store',
        default='csv',
        choices=['csv', 'xml', 'json'],
        dest='export_format',
        help='Export Format to create report file in, only used if sse = False',
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='Only for export_format csv, Sort headers by given names'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv, Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv, Sort the headers with a basic alphanumeric sort (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--no-explode-json',
        action='store_false',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv or json, Do not explode any embedded JSON into their own columns'
    )
    group.add_argument(
        '--explode-json',
        action='store_true',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv or json, Only for export_format csv, Explode any embedded JSON into their own columns (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--no-include_type',
        action='store_false',
        dest='include_type',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format json, Do not include SOAP type in JSON output'
    )
    group.add_argument(
        '--include_type',
        action='store_true',
        dest='include_type',
        required=False,
        default=argparse.SUPPRESS,
        help='Only for export_format json, Include SOAP type in JSON output (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--no-minimal',
        action='store_false',
        dest='minimal',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format xml, Produce the full XML representation, including empty attributes'
    )
    group.add_argument(
        '--minimal',
        action='store_true',
        dest='minimal',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format xml, Only include attributes that are not empty (default)'
    )

    return parser


def process_create_json_object_args(parser, handler, obj, args):
    """Process command line args supplied by user for create json object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    obj : str
        * Object type for create json object
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_from_json`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Create {} from JSON Options'.format(
            obj.replace('_', ' ').capitalize()
        )
    ]
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    try:
        response = handler.create_from_json(obj, **obj_grp_args)
    except Exception as e:
        print e
        sys.exit(100)
    for i in response:
        obj_id = getattr(i, 'id', 'unknown')
        print "Created item: {}, ID: {}".format(i, obj_id)
    return response


def process_tsat_args(parser, handler, args):
    """Process command line args supplied by user for tsat

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    '''
    TODO:
        file with params to pass for paramaretrized sensors
        saved questions
    '''
    mylog = logging.getLogger('TSAT')
    mylog.setLevel(logging.INFO)

    if args.debugformat:
        mylog.setLevel(logging.DEBUG)
    else:
        mylog.setLevel(logging.INFO)

    if any([args.sensors_help, args.filters_help, args.options_help]):
        handler.ask_manual(
            sensors_help=args.sensors_help,
            filters_help=args.filters_help,
            options_help=args.options_help,
        )
        sys.exit(99)

    if not os.path.exists(args.report_dir):
        os.makedirs(args.report_dir)

    my_name = os.path.splitext(os.path.basename(my_file))[0]
    whole_logfile = '{}_{}.log'.format(my_name, pytan.utils.get_now())
    whole_logfile = filter_filename(whole_logfile)
    whole_logfile_path = os.path.join(args.report_dir, whole_logfile)
    add_file_log(whole_logfile_path, args.debugformat)

    sensors = handler.get_all('sensor')
    mylog.info("Found {} total sensors".format(len(sensors)))

    # filter out all sensors that have a source_id (i.e. are created as temp sensors for params)
    real_sensors = filter_sourced_sensors(sensors=sensors)
    mylog.info("Filtered out sourced sensors: {}".format(len(real_sensors)))

    if not real_sensors:
        mylog.error("No sensors found!")
        sys.exit(1)

    filtered_sensors = filter_sensors(
        sensors=real_sensors, filter_platforms=args.platforms, filter_categories=args.categories,
    )
    mylog.info("Filtered out sensors based on user filters: {}".format(len(filtered_sensors)))

    if not filtered_sensors:
        mylog.error("Platform/Category filters too restrictive, no sensors match!")
        sys.exit(1)

    reports_run = []

    for idx, sensor in enumerate(filtered_sensors):
        report_info = {
            'sensor': sensor.name,
            'msg': 'Not run',
            'report_file': 'N/A',
            'elapsed_seconds': -1,
            'question': 'N/A',
        }
        mylog.info(
            "NOW WORKING ON SENSOR: {} ({}/{})\n".format(sensor.name, idx + 1, len(filtered_sensors))
        )
        sensor_dir = os.path.join(args.report_dir, filter_filename(sensor.name))

        if not os.path.exists(sensor_dir):
            os.makedirs(sensor_dir)

        logfile = '{}_{}.log'.format(sensor.name, pytan.utils.get_now())
        logfile = filter_filename(logfile)
        logfile_path = os.path.join(sensor_dir, logfile)

        add_file_log(logfile_path, args.debugformat)
        mylog.info("++ Asking question for sensor: {}".format(sensor.name))

        try:
            start_time = datetime.datetime.now()
            ret = handler.ask_manual(
                sensors=sensor.name,
                timeout=args.timeout,
                pct_complete_threshold=args.pct_complete_threshold,
                question_filters=args.question_filters,
                question_options=args.question_options,
            )
        # TODO: NO MORE EXCEPTION, ITS POLLER.STATUS
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

    csv_file = '{}_{}.csv'.format(my_name, pytan.utils.get_now())
    csv_file = filter_filename(csv_file)
    csv_file_path = os.path.join(args.report_dir, csv_file)

    csv_fh = open(csv_file_path, 'wb')
    csv_fh.write(csv_str)
    csv_fh.close()

    mylog.info("Final CSV results of from all questions run written to: {}".format(csv_file_path))


def process_delete_object_args(parser, handler, obj, args):
    """Process command line args supplied by user for delete object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    obj : str
        * Object type for delete object
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.delete`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    try:
        response = handler.delete(obj, **obj_grp_args)
    except Exception as e:
        print e
        sys.exit(100)
    for i in response:
        print "Deleted item: ", i
    return response


def process_stop_action_args(parser, handler, args):
    """Process command line args supplied by user for getting results

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args
        * args object from parsing `parser`

    Returns
    -------
    report_path, report_contents : tuple
        * results from :func:`pytan.handler.Handler.export_to_report_file` on the return of :func:`pytan.handler.Handler.get_result_data`
    """
    try:
        action_stop = handler.stop_action(**args.__dict__)
    except Exception as e:
        print e
        sys.exit(99)

    print "++ Action ID stopped successfully: {0.id!r}".format(action_stop)
    return action_stop


def process_get_results_args(parser, handler, args):
    """Process command line args supplied by user for getting results

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args
        * args object from parsing `parser`

    Returns
    -------
    report_path, report_contents : tuple
        * results from :func:`pytan.handler.Handler.export_to_report_file` on the return of :func:`pytan.handler.Handler.get_result_data`
    """
    try:
        obj = handler.get(**args.__dict__)[0]
    except Exception as e:
        print e
        sys.exit(99)

    m = "++ Found object: {}".format
    print(m(obj))

    if args.sse:
        try:
            results_obj = handler.get_result_data_sse(obj=obj, **args.__dict__)
        except Exception as e:
            print e
            sys.exit(99)

    else:
        try:
            results_obj = handler.get_result_data(obj=obj, **args.__dict__)
        except Exception as e:
            print e
            sys.exit(99)

    if isinstance(results_obj, taniumpy.object_types.result_set.ResultSet):
        if results_obj.rows:
            m = "++ Found results for object: {}".format
            print(m(results_obj))

            try:
                report_path, report_contents = handler.export_to_report_file(
                    obj=results_obj, **args.__dict__
                )
            except Exception as e:
                print e
                sys.exit(99)

            m = "++ Report file {!r} written with {} bytes".format
            print(m(report_path, len(report_contents)))

        else:
            report_contents = results_obj
            report_path = ''
            m = "++ No rows returned for results: {}".format
            print(m(results_obj))

    else:
        report_contents = results_obj
        report_path = handler.create_report_file(contents=report_contents, **args.__dict__)
        m = "++ Report file {!r} written with {} bytes".format
        print(m(report_path, len(report_contents)))

    return report_path, report_contents


def process_create_user_args(parser, handler, args):
    """Process command line args supplied by user for create user object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_user`
    """
    obj_grp_names = ['Create User Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_user(**obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    roles_txt = ', '.join([x.name for x in response.roles])

    m = "New user {0.name!r} created with ID {0.id!r}, roles: {1!r}".format
    print(m(response, roles_txt))
    return response


def process_create_package_args(parser, handler, args):
    """Process command line args supplied by user for create package object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_package`
    """
    obj_grp_names = ['Create Package Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_package(**obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    m = "New package {0.name!r} created with ID {0.id!r}, command: {0.command!r}".format
    print(m(response))
    return response


def process_create_sensor_args(parser, handler, args):
    """Process command line args supplied by user for create sensor object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_sensor`
    """
    obj_grp_names = ['Create Sensor Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_sensor(**obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    m = "New sensor {0.name!r} created with ID {0.id!r}".format
    print(m(response))
    return response


def process_create_whitelisted_url_args(parser, handler, args):
    """Process command line args supplied by user for create group object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_group`
    """
    obj_grp_names = ['Create Whitelisted URL Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_whitelisted_url(**obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    m = "New Whitelisted URL {0.url_regex!r} created with ID {0.id!r}".format
    print(m(response))
    return response


def process_create_group_args(parser, handler, args):
    """Process command line args supplied by user for create group object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_group`
    """
    obj_grp_names = ['Create Group Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_group(**obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    m = "New group {0.name!r} created with ID {0.id!r}, filter text: {0.text!r}".format
    print(m(response))
    return response


def process_print_server_info_args(parser, handler, args):
    """Process command line args supplied by user for printing server info

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    si = handler.session.get_server_info()

    if args.json:
        print pytan.utils.jsonify(si['diags_flat'])
    else:
        print str(handler)
        print_obj(si['diags_flat'])


def process_print_sensors_args(parser, handler, args):
    """Process command line args supplied by user for printing sensors

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    all_sensors = process_get_object_args(
        parser=parser, handler=handler, obj='sensor', args=args, report=False
    )

    real_sensors = filter_sourced_sensors(all_sensors)
    print "Filtered out sourced sensors: {}".format(len(real_sensors))

    filtered_sensors = filter_sensors(
        sensors=real_sensors, filter_platforms=args.platforms, filter_categories=args.categories,
    )
    print "Filtered out sensors based on user filters: {}".format(len(filtered_sensors))

    if args.json:
        for x in filtered_sensors:
            result = handler.export_obj(obj=x, export_format='json')
            print "{}:\n{}".format(x, result)
        sys.exit()

    for x in sorted(filtered_sensors, key=lambda x: x.category):
        platforms = parse_sensor_platforms(x)

        param_def = x.parameter_definition or {}
        if param_def:
            try:
                param_def = json.loads(param_def)
            except:
                print "Error loading JSON parameter definition {}".format(param_def)
                param_def = {}

        params = param_def.get('parameters', [])
        if args.params_only and not params:
            continue

        desc = (x.description or '').replace('\n', ' ').strip()
        print (
            "\n  * Sensor Name: '{0.name}', Platforms: {1}, Category: {0.category}"
        ).format(x, ', '.join(platforms))
        print "  * Description: {}".format(desc)

        if args.hide_params:
            continue

        skip_attrs = [
            'model',
            'parameterType',
            'snapInterval',
            'validationExpressions',
            'key',
        ]

        for param in params:
            print "  * Parameter '{}':".format(param['key'])
            for k, v in sorted(param.iteritems()):
                if k in skip_attrs:
                    continue
                if not v:
                    continue
                print "    - '{}': {}".format(k, v)


def process_get_object_args(parser, handler, obj, args, report=True):
    """Process command line args supplied by user for get object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    obj : str
        * Object type for get object
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.get`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    get_all = obj_grp_args.pop('all')
    if get_all:
        try:
            response = handler.get_all(obj)
        except Exception as e:
            print e
            sys.exit(100)
    else:
        try:
            response = handler.get(obj, **obj_grp_args)
        except Exception as e:
            print e
            sys.exit(100)

    print "Found items: ", response

    if report:
        report_file, result = handler.export_to_report_file(obj=response, **args.__dict__)

        m = "Report file {!r} written with {} bytes".format
        print(m(report_file, len(result)))

    return response


def process_ask_parsed_args(parser, handler, args):
    """Process command line args supplied by user for ask parsed

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response
        * response from :func:`pytan.handler.Handler.ask_parsed`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = ['Parsed Question Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    print "++ Asking parsed question:\n{}".format(pytan.utils.jsonify(obj_grp_args))

    try:
        response = handler.ask(qtype='parsed', **obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    question = response['question_object']
    results = response['question_results']
    print "++ Asked Question {0.query_text!r} ID: {0.id!r}".format(question)

    if results:
        try:
            report_file, report_contents = handler.export_to_report_file(obj=results, **args.__dict__)
        except Exception as e:
            print e
            sys.exit(99)

        m = "++ Report file {!r} written with {} bytes".format
        print(m(report_file, len(report_contents)))
    else:
        print "++ No action results returned, run get_results.py to get the results"

    return response


def process_ask_manual_args(parser, handler, args):
    """Process command line args supplied by user for ask manual

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response
        * response from :func:`pytan.handler.Handler.ask_manual`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = ['Manual Question Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    print "++ Asking manual question:\n{}".format(pytan.utils.jsonify(obj_grp_args))

    try:
        response = handler.ask(qtype='manual', **obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    question = response['question_object']
    results = response['question_results']
    print "++ Asked Question {0.query_text!r} ID: {0.id!r}".format(question)

    if results:
        try:
            report_file, report_contents = handler.export_to_report_file(obj=results, **args.__dict__)
        except Exception as e:
            print e
            sys.exit(99)

        m = "++ Report file {!r} written with {} bytes".format
        print(m(report_file, len(report_contents)))
    else:
        print "++ No action results returned, run get_results.py to get the results"

    return response


def process_deploy_action_args(parser, handler, args):
    """Process command line args supplied by user for deploy action

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response
        * response from :func:`pytan.handler.Handler.deploy_action`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = ['Deploy Action Options', 'Report File Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    print "++ Deploying action:\n{}".format(pytan.utils.jsonify(obj_grp_args))

    try:
        response = handler.deploy_action(**obj_grp_args)
    except Exception as e:
        print e
        sys.exit(99)

    action = response['action_object']
    print "++ Deployed Action {0.name!r} ID: {0.id!r}".format(action)
    print "++ Command used in Action: {0.package_spec.command!r}".format(action)

    if response['action_result_map']:
        print "++ Deploy action progress results:"
        for k, v in sorted(response['action_result_map'].iteritems()):
            print "Total {}: {}".format(k, v['total'])

    results = response['action_results']
    if results:
        if not obj_grp_args.get('report_file'):
            obj_grp_args['prefix'] = obj_grp_args.get('prefix', 'deploy_action_')

        try:
            report_file, report_contents = handler.export_to_report_file(
                obj=results, **obj_grp_args
            )
        except Exception as e:
            print e
            sys.exit(99)

        response['report_file'] = report_file
        response['report_contents'] = report_contents

        m = "++ Deploy results written to {!r} with {} bytes".format
        print(m(report_file, len(report_contents)))

    else:
        print (
            "++ No action results returned, run get_results.py to get the results"
        )

    return response


def process_pytan_shell_args(parser, handler, args):
    """Process command line args supplied by user for a python shell

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    console = pytan.binsupport.HistoryConsole()
    return console


def process_ask_saved_args(parser, handler, args):
    """Process command line args supplied by user for ask saved

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response
        * response from :func:`pytan.handler.Handler.ask_saved`
    """
    id_arg = args.id
    name_arg = args.name
    refresh_arg = args.refresh_data

    q_args = {}

    if id_arg:
        q_args['id'] = id_arg
    elif name_arg:
        q_args['name'] = name_arg
    else:
        parser.error("Must supply --id or --name")

    q_args['refresh_data'] = refresh_arg

    print "++ Asking saved question: {}".format(pytan.utils.jsonify(q_args))

    try:
        response = handler.ask(qtype='saved', **q_args)
    except Exception as e:
        print e
        sys.exit(99)

    question = response['question_object']
    results = response['question_results']
    print "++ Saved Question {0.query_text!r} ID: {0.id!r}".format(question)

    try:
        report_file, report_contents = handler.export_to_report_file(obj=results, **args.__dict__)
    except Exception as e:
        print e
        sys.exit(99)

    response['report_file'] = report_file
    response['report_contents'] = report_contents

    m = "Report file {!r} written with {} bytes".format
    print(m(report_file, len(report_contents)))
    return response


def process_handler_args(parser, args):
    """Process command line args supplied by user for handler

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    args : args
        * args parsed from `parser`

    Returns
    -------
    h : :class:`pytan.handler.Handler`
        * Handler object
    """
    input_prompts(args)
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = get_grp_opts(parser=parser, grp_names=handler_grp_names)
    handler_args = {k: getattr(args, k) for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
    except Exception:
        traceback.print_exc()
        sys.exit(99)

    print str(h)
    return h


def get_grp_opts(parser, grp_names):
    """Used to get arguments in `parser` that match argument group names in `grp_names`

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object
    grp_names : list of str
        * list of str of argument group names to get arguments for

    Returns
    -------
    grp_opts : list of str
        * list of arguments gathered from argument group names in `grp_names`
    """
    action_grps = [a for a in parser._action_groups if a.title in grp_names]
    grp_opts = [a.dest for b in action_grps for a in b._group_actions]
    return grp_opts


def version_check(reqver):
    """Allows scripts using :mod:`pytan` to validate the version of the script
    aginst the version of :mod:`pytan`

    Parameters
    ----------
    reqver : str
        * string containing version number to check against :exc:`Exception`

    Raises
    ------
    VersionMismatchError : :exc:`Exception`
        * if :data:`pytan.__version__` is not greater or equal to `reqver`
    """
    log_tpl = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        raise pytan.exceptions.VersionMismatchError(log_tpl(s, sys.argv[0], __version__, reqver))

    s = "Script and API Version match"
    mylog.debug(log_tpl(s, sys.argv[0], __version__, reqver))
    return True


def debug_list(debuglist):
    """Utility function to print the variables for a list of objects"""
    for x in debuglist:
        debug_obj(x)


def debug_obj(debugobj):
    """Utility function to print the variables for an object"""
    pprint.pprint(vars(debugobj))


def introspect(obj, depth=0):
    """Utility function to dump all info about an object"""
    import types
    print "%s%s: %s\n" % (depth * "\t", obj, [
        x for x in dir(obj) if x[:2] != "__"])
    depth += 1
    for x in dir(obj):
        if x[:2] == "__":
            continue
        subobj = getattr(obj, x)
        print "%s%s: %s" % (depth * "\t", x, subobj)
        if isinstance(subobj, types.InstanceType) and dir(subobj) != []:
            introspect(subobj, depth=depth + 1)
            print


def input_prompts(args):
    """Utility function to prompt for username, password, and host if empty"""
    if not args.username and not args.session_id:
        username = raw_input('Tanium Username: ')
        args.username = username.strip()

    if not args.password and not args.session_id:
        password = getpass.getpass('Tanium Password: ')
        args.password = password.strip()

    if not args.host:
        host = raw_input('Tanium Host: ')
        args.host = host.strip()
    return args


def print_obj(d, indent=0):
    """Pretty print a dictionary"""
    for k, v in d.iteritems():
        if pytan.utils.is_dict(v):
            print "{}{}: \n".format('  ' * indent, k),
            print_obj(v, indent + 1)
        elif pytan.utils.is_list(v):
            print "{}{}: ".format('  ' * indent, k)
            for a in v:
                print_obj(a, indent + 1)
        else:
            print "{}{}: {}".format('  ' * indent, k, v)


def filter_filename(filename):
    """Utility to filter a string into a valid filename"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename


def remove_file_log(logfile):
    """Utility to remove a log file from python's logging module"""
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
    """Utility to add a log file from python's logging module"""
    remove_file_log(logfile)
    root_logger = logging.getLogger()
    basename = os.path.basename(logfile)
    try:
        file_handler = logging.FileHandler(logfile)
        file_handler.set_name(basename)
        if debug:
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(pytan.constants.DEBUG_FORMAT))
        else:
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(pytan.constants.INFO_FORMAT))
        root_logger.addHandler(file_handler)
        mylog.info(('Added file logging to: {}').format(logfile))
    except Exception as e:
        mylog.error((
            'Problem setting up file logging to {}: {}'
        ).format(logfile, e))


def parse_sensor_platforms(sensor):
    """Utility to create a list of platforms for a given sensor"""
    platforms = [
        q.platform for q in sensor.queries
        if q.script
        and 'THIS IS A STUB' not in q.script
        and 'echo Windows Only' not in q.script
        and 'Not a Windows Sensor' not in q.script
    ]
    return platforms


def filter_sourced_sensors(sensors):
    """Utility to filter out all sensors that have a source_id specified (i.e. they are temp sensors created by the API)"""
    sensors = [x for x in sensors if not x.source_id]
    return sensors


def filter_sensors(sensors, filter_platforms=[], filter_categories=[]):
    """Utility to filter a list of sensors for specific platforms and/or categories"""
    if not filter_platforms and not filter_categories:
        return sorted(sensors, key=lambda x: x.category)

    new_sensors = []
    for x in sorted(sensors, key=lambda x: x.category):
        if filter_categories:
            if str(x.category).lower() not in [y.lower() for y in filter_categories]:
                continue

        platforms = parse_sensor_platforms(x)
        if platforms:
            match = [
                p for p in platforms
                if p.lower() in [y.lower() for y in filter_platforms]
            ]
            if not match:
                continue

        new_sensors.append(x)

    return new_sensors


def get_all_headers(rows_list):
    """Utility to get all the keys for a list of dicts"""
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
