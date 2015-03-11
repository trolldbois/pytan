#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Collection of exceptions, classes, and methods used throughout :mod:`pytan`"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import socket
import time
import logging
import json
import argparse
import datetime
import re
from argparse import ArgumentDefaultsHelpFormatter as A1 # noqa
from argparse import RawDescriptionHelpFormatter as A2 # noqa
from collections import OrderedDict

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import taniumpy
import xmltodict
from pytan import __version__
from pytan import constants

mylog = logging.getLogger("handler")
humanlog = logging.getLogger("ask_manual_human")
manuallog = logging.getLogger("ask_manual")
progresslog = logging.getLogger("question_progress")
pname = os.path.splitext(os.path.basename(sys.argv[0]))[0]


class HandlerError(Exception):
    """Exception thrown for most errors in :mod:`pytan.handler`"""
    pass


class HumanParserError(Exception):
    """Exception thrown for errors while parsing human strings from :mod:`pytan.handler`"""
    pass


class DefinitionParserError(Exception):
    """Exception thrown for errors while parsing definitions from :mod:`pytan.handler`"""
    pass


class RunFalse(Exception):
    """Exception thrown when run=False from :func:`pytan.handler.Handler.deploy_action`"""
    pass


class PytanHelp(Exception):
    """Exception thrown when printing out help"""
    pass


class SplitStreamHandler(logging.Handler):
    """Custom :class:`logging.Handler` class that sends all messages that are logging.INFO and below to STDOUT, and all messages that are logging.WARNING and above to STDERR
    """

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno < logging.WARNING:
                stream = sys.stdout
            else:
                stream = sys.stderr
            fs = "%s\n"
            try:
                is_unicode = isinstance(msg, unicode)
                if is_unicode and getattr(stream, 'encoding', None):
                    ufs = u'%s\n'
                    try:
                        stream.write(ufs % msg)
                    except UnicodeEncodeError:
                        stream.write((ufs % msg).encode(stream.encoding))
                else:
                    stream.write(fs % msg)
            except UnicodeError:
                stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


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
        * --debugformat (not shown in --help)
    """

    parser = CustomArgParse(
        description=desc,
        add_help=help,
        formatter_class=CustomArgFormat,
    )
    auth_group = parser.add_argument_group('Handler Authentication')
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
        default=False,
        dest='debugformat',
        help=argparse.SUPPRESS,
    )

    return parser


def setup_get_object_argparser(obj, doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to get objects.
    """
    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    get_object_group = parser.add_argument_group(
        'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    )
    get_object_group.add_argument(
        '--all',
        required=False,
        default=False,
        action='store_true',
        dest='all',
        help='Get all {}s'.format(obj),
    )

    obj_map = get_obj_map(obj)
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


def setup_create_json_object_argparser(obj, doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to create objects from json files.
    """

    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group(
        'Create {} from JSON Options'.format(
            obj.replace('_', ' ').capitalize()
        )
    )

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
    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group(
        'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    )

    obj_map = get_obj_map(obj)
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

    obj = 'saved_question'
    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group('Saved Question Selectors')
    group = arggroup.add_mutually_exclusive_group()

    obj_map = get_obj_map(obj)
    search_keys = obj_map['search']
    for k in search_keys:
        group.add_argument(
            '--{}'.format(k),
            required=False,
            action='store',
            dest=k,
            help='{} of {} to ask'.format(k, obj),
        )
    return parser


def setup_stop_action_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to stop actions.
    """

    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group('Stop Action Options')

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

    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group('Deploy Action Options')

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
        default=1,
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
    parser = add_report_file_options(parser)

    return parser


def setup_get_result_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to get results for questions or actions.
    """

    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group('Get Result Options')

    arggroup.add_argument(
        '-o',
        '--object',
        required=True,
        action='store',
        default='',
        choices=['saved_question', 'question', 'action'],
        dest='object_type',
        help='Type of object to get results for',
    )

    arggroup.add_argument(
        '-i',
        '--id',
        required=True,
        action='store',
        default='',
        type=int,
        dest='object_id',
        help='id of object to get results for',
    )
    return parser


def setup_ask_manual_argparser(doc):
    """Method to setup the base :class:`pytan.utils.CustomArgParse` class for command line scripts using :func:`pytan.utils.setup_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask manual questions.
    """
    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    arggroup = parser.add_argument_group('Manual Question Options')

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
    return parser


def add_ask_report_argparser(parser):
    """Method to extend a :class:`pytan.utils.CustomArgParse` class for command line scripts with arguments for scripts that need to supply export format subparsers for asking questions.
    """
    parser = add_report_file_options(parser)

    subparsers = parser.add_subparsers(
        title='Export Formats',
        dest='export_format',
        help='Export Format choices',
    )

    csv_subparser = subparsers.add_parser(
        'csv',
        help='Produce a CSV report, supply "csv -h" to see CSV options',
        description="CSV Export Options"
    )

    group = csv_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='Sort headers by given names'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Sort the headers with a basic alphanumeric sort (default)'
    )

    group = csv_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--add-sensor',
        action='store_true',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='Add the sensor names to each header'
    )
    group.add_argument(
        '--no-add-sensor',
        action='store_false',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not add the sensor names to each header (default)'
    )

    group = csv_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--add-type',
        action='store_true',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='Add the result type to each header'
    )
    group.add_argument(
        '--no-add-type',
        action='store_false',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not add the result type to each header (default)'
    )

    group = csv_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--expand-columns',
        action='store_true',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='Expand multi-line cells into their own rows that have sensor '
        'correlated columns in the new rows'
    )
    group.add_argument(
        '--no-columns',
        action='store_false',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not add expand multi-line cells into their own rows (default)'
    )

    subparsers.add_parser(
        'json',
        help='Produce a JSON report, supply "json -h" to see JSON options',
        description="JSON Export Options"
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

    subparsers = parser.add_subparsers(
        title='Export Formats',
        dest='export_format',
        help='Export Format choices',
    )

    csv_subparser = subparsers.add_parser(
        'csv',
        help='Produce a CSV report, supply "csv -h" to see CSV options',
        description="CSV Export Options"
    )

    group = csv_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='Sort headers by given names'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Sort the headers with a basic alphanumeric sort (default)'
    )

    group = csv_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--no-explode-json',
        action='store_false',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not explode any embedded JSON into their own columns'
    )
    group.add_argument(
        '--explode-json',
        action='store_true',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Explode any embedded JSON into their own columns (default)'
    )

    json_subparser = subparsers.add_parser(
        'json',
        help='Produce a JSON report, supply "json -h" to see JSON options',
        description="CSV Export Options"
    )

    group = json_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--explode-json',
        action='store_true',
        dest='explode_json_string_values',
        required=False,
        default=argparse.SUPPRESS,
        help='Explode any embedded JSON into their own columns'
    )
    group.add_argument(
        '--no-explode-json',
        action='store_false',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not explode any embedded JSON into their own columns '
        '(default)'
    )

    group = json_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--no-include_type',
        action='store_false',
        dest='include_type',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not include SOAP type in JSON output'
    )
    group.add_argument(
        '--include_type',
        action='store_true',
        dest='include_type',
        required=False,
        default=argparse.SUPPRESS,
        help='Include SOAP type in JSON output (default)'
    )

    xml_subparser = subparsers.add_parser(
        'xml',
        help='Produce a XML report, supply "xml -h" to see XML options',
        description="XML Export Options"
    )

    group = xml_subparser.add_mutually_exclusive_group()
    group.add_argument(
        '--no-minimal',
        action='store_false',
        dest='minimal',
        default=argparse.SUPPRESS,
        required=False,
        help='Produce the full XML representation, including empty attributes'
    )
    group.add_argument(
        '--minimal',
        action='store_true',
        dest='minimal',
        default=argparse.SUPPRESS,
        required=False,
        help='Only include attributes that are not empty (default)'
    )

    return parser


def process_create_json_object_args(parser, handler, obj, all_args):
    """Process command line args supplied by user for create json object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        Instance of Handler created from command line args
    obj : str
        Object type for create json object
    all_args : dict
        dict of args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        response from :func:`pytan.handler.Handler.create_from_json`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Create {} from JSON Options'.format(
            obj.replace('_', ' ').capitalize()
        )
    ]
    obj_grp_opts = get_grp_opts(parser, obj_grp_names)
    obj_grp_args = {k: all_args.pop(k) for k in obj_grp_opts}
    try:
        response = handler.create_from_json(obj, **obj_grp_args)
    except Exception as e:
        print e
        sys.exit(100)
    for i in response:
        obj_id = getattr(i, 'id', 'unknown')
        print "Created item: {}, ID: {}".format(i, obj_id)
    return response


def process_delete_object_args(parser, handler, obj, all_args):
    """Process command line args supplied by user for delete object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        Instance of Handler created from command line args
    obj : str
        Object type for delete object
    all_args : dict
        dict of args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        response from :func:`pytan.handler.Handler.delete`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    obj_grp_opts = get_grp_opts(parser, obj_grp_names)
    obj_grp_args = {k: all_args.pop(k) for k in obj_grp_opts}
    try:
        response = handler.delete(obj, **obj_grp_args)
    except Exception as e:
        print e
        sys.exit(100)
    for i in response:
        print "Deleted item: ", i
    return response


def process_get_object_args(parser, handler, obj, all_args):
    """Process command line args supplied by user for get object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        Instance of Handler created from command line args
    obj : str
        Object type for get object
    all_args : dict
        dict of args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        response from :func:`pytan.handler.Handler.get`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    obj_grp_opts = get_grp_opts(parser, obj_grp_names)
    obj_grp_args = {k: all_args.pop(k) for k in obj_grp_opts}
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
    return response


def get_grp_opts(parser, grp_names):
    """Used to get arguments in `parser` that match argument group names in `grp_names`

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        ArgParse object
    grp_names : list of str
        list of str of argument group names to get arguments for

    Returns
    -------
    grp_opts : list of str
        list of arguments gathered from argument group names in `grp_names`
    """
    action_grps = [a for a in parser._action_groups if a.title in grp_names]
    grp_opts = [a.dest for b in action_grps for a in b._group_actions]
    return grp_opts


def is_list(l):
    """returns True if `l` is a list, False if not"""
    return type(l) in [list, tuple]


def is_str(l):
    """returns True if `l` is a string, False if not"""
    return type(l) in [unicode, str]


def is_dict(l):
    """returns True if `l` is a dictionary, False if not"""
    return type(l) in [dict, OrderedDict]


def is_num(l):
    """returns True if `l` is a number, False if not"""
    return type(l) in [float, int, long]


def version_check(reqver):
    """Allows scripts using :mod:`pytan` to validate the version of the script
    aginst the version of :mod:`pytan`

    Parameters
    ----------
    reqver : str
        string containing version number to check against :exc:`Exception`

    Raises
    ------
    Exception : :exc:`Exception`
        if :data:`pytan.__version__` is not greater or equal to `reqver`
    """
    log_tpl = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        raise Exception(log_tpl(s, sys.argv[0], __version__, reqver))

    s = "Script and API Version match"
    logging.debug(log_tpl(s, sys.argv[0], __version__, reqver))
    return True


def jsonify(v, indent=2, sort_keys=True):
    """Turns python object `v` into a pretty printed JSON string

    Parameters
    ----------
    v : object
        python object to convert to JSON

    indent : int, 2
        number of spaces to indent JSON string when pretty printing

    sort_keys : bool, True
        sort keys of JSON string when pretty printing

    Returns
    -------
    str :
        JSON pretty printed string
    """
    return json.dumps(v, indent=indent, sort_keys=sort_keys)


def get_now():
    """Get current time in human friendly format

    Returns
    -------
    str :
        str of current time return from :func:`human_time`
    """
    return human_time(time.localtime())


def human_time(t, tformat='%Y_%m_%d-%H_%M_%S-%Z'):
    """Get time in human friendly format

    Parameters
    ----------
    t : int, float, time
        either a unix epoch or struct_time object to convert to string
    tformat : str, optional
        format of string to convert time to

    Returns
    -------
    str :
        `t` converted to str
    """
    if is_num(t):
        t = time.localtime(t)
    return time.strftime(tformat, t)


def seconds_from_now(secs=0, tz='utc'):
    """Get time in Tanium SOAP API format `secs` from now

    Parameters
    ----------
    secs : int
        seconds from now to get time str
    tz : str, optional
        time zone to return string in, default is 'utc' - supplying anything else will supply local time

    Returns
    -------
    str :
        time `secs` from now in Tanium SOAP API format
    """
    if tz == 'utc':
        now = datetime.datetime.utcnow()
    else:
        now = datetime.datetime.now()
    from_now = now + datetime.timedelta(seconds=secs)
    # now.strftime('%Y-%m-%dT%H:%M:%S')
    return from_now.strftime('%Y-%m-%dT%H:%M:%S')


def port_check(address, port, timeout=5):
    """Check if `address`:`port` can be reached within `timeout`

    Parameters
    ----------
    address : str
        hostname/ip address to check `port` on
    port : int
        port to check on `address`
    timeout : int, optional
        timeout after N seconds of not being able to connect

    Returns
    -------
    :mod:`socket` or False :
        if connection succeeds, the socket object is returned, else False is returned
    """
    try:
        return socket.create_connection((address, port), timeout)
    except socket.error:
        return False


def test_app_port(host, port):
    """Validates that `host`:`port` can be reached using :func:`port_check`

    Parameters
    ----------
    host : str
        hostname/ip address to check `port` on
    port : int
        port to check on `host`

    Raises
    ------
    HandlerError : :exc:`pytan.utils.HandlerError`
        if `host`:`port` can not be reached

    """
    chk_tpl = "Port test to {}:{} {}".format
    if port_check(host, port):
        mylog.debug(chk_tpl(host, port, "SUCCESS"))
    else:
        raise HandlerError(chk_tpl(host, port, "FAILURE"))


def remove_logging_handler(name):
    """Removes a logging handler

    Parameters
    ----------
    name : str
        name of logging handler to remove. if name == 'all' then all logging handlers are removed
    """
    root_logger = logging.getLogger()
    root_handlers = root_logger.handlers
    for h in root_handlers:
        if name == 'all':
            root_logger.removeHandler(h)
        elif h.name == name:
            root_logger.removeHandler(h)


def setup_console_logging():
    """Creates a console logging handler using :class:`SplitStreamHandler`"""
    ch_name = 'console'
    remove_logging_handler('all')
    # add a console handler to the root logger that goes to STDOUT for INFO
    # and below, but STDERR for WARNING and above
    ch = SplitStreamHandler()
    ch.set_name(ch_name)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(constants.INFO_FORMAT))
    root_logger = logging.getLogger()
    root_logger.addHandler(ch)
    root_logger.setLevel(logging.DEBUG)


def change_console_format(debug=False):
    """Changes the logging format for console handler to :data:`pytan.constants.DEBUG_FORMAT` or :data:`pytan.constants.INFO_FORMAT`

    Parameters
    ----------
    debug : bool, optional
        * False : set logging format for console handler to :data:`pytan.constants.INFO_FORMAT`
        * True :  set logging format for console handler to :data:`pytan.constants.DEBUG_FORMAT`
    """
    root_logger = logging.getLogger()
    root_handlers = root_logger.handlers
    for h in root_handlers:
        if h.name == 'console':
            if debug:
                h.setFormatter(logging.Formatter(constants.DEBUG_FORMAT))
            else:
                h.setFormatter(logging.Formatter(constants.INFO_FORMAT))


def set_log_levels(loglevel=0):
    """Enables loggers based on loglevel and :data:`pytan.constants.LOG_LEVEL_MAPS`

    Parameters
    ----------
    loglevel : int, optional
        loglevel to match against each item in :data:`pytan.constants.LOG_LEVEL_MAPS` - each item that is greater than or equal to loglevel will have the according loggers set to their respective levels identified there-in.
    """
    set_all_loglevels('WARN')
    for logmap in constants.LOG_LEVEL_MAPS:
        if loglevel >= logmap[0]:
            for lname, llevel in logmap[1].iteritems():
                # print 'setting %s to %s' % (lname, llevel)
                logging.getLogger(lname).setLevel(getattr(logging, llevel))


def set_all_loglevels(level='DEBUG'):
    """Sets all loggers that the logging system knows about to a given logger level"""
    for k, v in sorted(logging.Logger.manager.loggerDict.iteritems()):
        if not isinstance(v, logging.Logger):
            continue
        v.setLevel(getattr(logging, level))


def dehumanize_sensors(sensors, key='sensors', empty_ok=False):
    """Turns a sensors str or list of str into a sensor definition

    Parameters
    ----------
    sensors : str, list of str
        A str or list of str that describes a sensor(s) and optionally a selector, parameters, filter, and/or options
    key : str, optional
        Name of key that user should have provided `sensors` as
    empty_ok : bool, optional
        False: `sensors` is not allowed to be empty, throw :exc:`HumanParserError` if it is empty
        True: `sensors` is allowed to be empty

    Returns
    -------
    sensor_defs : list of dict
        list of dict parsed from `sensors`
    """
    if not sensors:
        if not empty_ok:
            err = (
                "A string or list of strings must be supplied as '{0}'!"
            ).format(key)
            raise HumanParserError(err)
        else:
            return []

    if not is_list(sensors):
        sensors = [sensors]

    sensor_defs = []
    for sensor in sensors:
        if not is_str(sensor):
            raise HumanParserError("{!r} must be a string".format(sensor))
        s, parsed_selector = extract_selector(sensor)
        s, parsed_params = extract_params(s)
        s, parsed_options = extract_options(s)
        s, parsed_filter = extract_filter(s)
        sensor_def = {}
        sensor_def[parsed_selector] = s
        sensor_def['params'] = parsed_params
        sensor_def['options'] = parsed_options
        sensor_def['filter'] = parsed_filter

        dbg = 'parsed string {!r} into definition:\n {}'.format
        humanlog.debug(dbg(sensor, jsonify(sensor_def)))

        sensor_defs.append(sensor_def)

    return sensor_defs


def dehumanize_package(package):
    """Turns a package str into a package definition

    Parameters
    ----------
    package : str
        A str that describes a package and optionally a selector and/or parameters

    Returns
    -------
    package_def : dict
        dict parsed from `sensors`
    """
    if not is_str(package) or not package:
        err = "{!r} must be a string supplied as 'package'".format
        raise HumanParserError(err(package))
    p, parsed_selector = extract_selector(package)
    p, parsed_params = extract_params(p)
    package_def = {}
    package_def[parsed_selector] = p
    package_def['params'] = parsed_params

    dbg = 'parsed string {!r} into definition:\n {}'.format
    humanlog.debug(dbg(package, jsonify(package_def)))

    return package_def


def dehumanize_question_filters(question_filters):
    """Turns a question_filters str or list of str into a question filter definition

    Parameters
    ----------
    question_filters : str, list of str
        A str or list of str that describes a sensor for a question filter(s) and optionally a selector and/or filter

    Returns
    -------
    question_filter_defs : list of dict
        list of dict parsed from `question_filters`
    """
    if not question_filters:
        return []

    if not is_list(question_filters):
        question_filters = [question_filters]

    question_filter_defs = []
    for question_filter in question_filters:
        s, parsed_selector = extract_selector(question_filter)
        s, parsed_filter = extract_filter(s)
        if not parsed_filter:
            err = "Filter {!r} is not a valid filter!".format
            raise HumanParserError(err(question_filter))

        question_filter_def = {}
        question_filter_def[parsed_selector] = s
        question_filter_def['filter'] = parsed_filter

        dbg = (
            'parsed string {!r} into filter definition:\n {}'
        ).format
        dbg = dbg(question_filter, jsonify(question_filter_def))
        humanlog.debug(dbg)

        question_filter_defs.append(question_filter_def)

    return question_filter_defs


def dehumanize_question_options(question_options):
    """Turns a question_options str or list of str into a question option definition

    Parameters
    ----------
    question_options : str, list of str
        A str or list of str that describes question options

    Returns
    -------
    question_option_defs : list of dict
        list of dict parsed from `question_options`
    """
    if not question_options:
        return {}

    if not is_list(question_options):
        question_options = [question_options]

    dest = ['filter', 'group']
    question_option_defs = map_options(question_options, dest)
    dbg = (
        'parsed string {!r} into option definition:\n {}'
    ).format
    dbg = dbg(question_options, jsonify(question_option_defs))
    humanlog.debug(dbg)

    return question_option_defs


def extract_selector(s):
    """Extracts a selector from str `s`

    Parameters
    ----------
    s : str
        A str that may or may not have a selector in the beginning in the form of id:, name:, or :hash -- if no selector found, name will be assumed as the default selector

    Returns
    -------
    s : str
        str `s` without the parsed_selector included
    parsed_selector : str
        selector extracted from `s`, or 'name' if none found
    """
    parsed_selector = 'name'
    for selector in constants.SELECTORS:
        if s.startswith(selector + ':'):
            parsed_selector = selector
            s = s.replace(selector + ':', '').strip()

    dbg = 'parsed new string to {!r} and selector to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_selector)))

    return s, parsed_selector


def extract_params(s):
    """Extracts parameters from str `s`

    Parameters
    ----------
    s : str
        A str that may or may not have parameters identified by {key=value}

    Returns
    -------
    s : str
        str `s` without the parsed_params included
    parsed_params : list
        parameters extracted from `s` if any found
    """
    # extract params from s

    # given example (note escaped comma in params):
    # 'Folder Name Search with RegEx Match{dirname=Program Files,regex=\,*}' \
    # ', that is .*, opt:max_data_age:3600, opt:ignore_case'

    params = re.findall(constants.PARAM_RE, s)
    # params=['dirname=Program Files,regex=\\,*']

    if len(params) > 1:
        err = "More than one parameter ({{}}) passed in {!r}".format
        raise HumanParserError(err(s))
    elif len(params) == 1:
        param = params[0]
    else:
        param = ''
    # param='dirname=Program Files,regex=\\,*'

    if param:
        split_param = re.split(constants.PARAM_SPLIT_RE, param)
    else:
        split_param = []
    # split_param=['dirname=Program Files', 'regex=\\,*']

    parsed_params = {}
    for sp in split_param:
        # sp = 'dirname=Program Files'
        if constants.PARAM_KEY_SPLIT not in sp:
            err = "Parameter {} missing key/value seperator ({})".format
            raise HumanParserError(err(sp, constants.PARAM_KEY_SPLIT))
        sp_key, sp_value = sp.split(constants.PARAM_KEY_SPLIT, 1)
        # remove any escapes for {}'s
        if '\\}' in sp_value:
            sp_value = sp_value.replace('\\}', '}')
        if '\\{' in sp_value:
            sp_value = sp_value.replace('\\{', '{')

        # sp_key = dirname
        # sp_value = Program Files
        parsed_params[sp_key] = sp_value

    # remove params from the s string
    s = re.sub(constants.PARAM_RE, '', s)
    # s='Folder Name Search with RegEx Match, that is .*, ' \
    # 'opt:max_data_age:3600, opt:ignore_case'

    dbg = 'parsed new string to {!r} and parameters to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_params)))

    return s, parsed_params


def extract_options(s):
    """Extracts options from str `s`

    Parameters
    ----------
    s : str
        A str that may or may not have options identified by ', opt:name[:value]'

    Returns
    -------
    s : str
        str `s` without the parsed_options included
    parsed_options : list
        options extracted from `s` if any found
    """
    # parse options out of s

    split_option = re.split(constants.OPTION_RE, s, 0, re.IGNORECASE)
    # split_option = ['Folder Name Search with RegEx Match, that is .*', \
    # 'max_data_age:3600', 'ignore_case']

    parsed_options = {}

    # if options parsed out from s
    if len(split_option) > 1:

        # get new s from index 0
        s = split_option[0].strip()
        # s='Folder Name Search with RegEx Match, that is .*'

        # get the option strings from index 1 and on
        parsed_options = [x.strip() for x in split_option[1:]]
        # parsed_options=['max_data_age:3600', 'ignore_case']

        parsed_options = map_options(parsed_options, ['filter'])

    dbg = 'parsed new string to {!r} and options to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_options)))

    return s, parsed_options


def map_options(options, dest):
    """Maps a list of options using :func:`map_option`

    Parameters
    ----------
    options : list of str
        list of str that should be validated
    dest : list of str
        list of valid destinations (i.e. `filter` or `group`)

    Returns
    -------
    mapped_options : dict
        dict of all mapped_options
    """
    mapped_options = {}
    for option in options:
        mapped_option = map_option(option, dest)
        if mapped_option:
            mapped_options.update(mapped_option)
        else:
            err = "Option {!r} is not a valid option!".format
            raise HumanParserError(err(option))

    return mapped_options


def map_option(opt, dest):
    """Maps an opt str against :data:`constants.OPTION_MAPS`

    Parameters
    ----------
    opt : str
        option str that should be validated
    dest : list of str
        list of valid destinations (i.e. `filter` or `group`)

    Returns
    -------
    opt_attrs : dict
        dict containing mapped option attributes for SOAP API
    """
    opt_attrs = {}

    for om in constants.OPTION_MAPS:
        if opt_attrs:
            break

        if om['destination'] not in dest:
            continue

        # if what the user supplied for an option doesnt match the
        # string in om['human'], go to next string
        if not opt.lower().startswith(om['human']):
            continue

        dbg = "option {!r} mapped to: {!r}".format
        humanlog.debug(dbg(opt, om))

        opt_attrs = om.get('attrs', {})

        human_type = om.get('human_type', '')
        valid_type = om.get('valid_type', str)
        # if human_type we expect the option string
        # to be name:value
        if human_type:
            opt_split = opt.split(':')

            if len(opt_split) != 2:
                format_str = "Format should be '{}:${}'".format
                format_str = format_str(om['human'], human_type.upper())

                err = "Option {!r} is missing a {} value of {}\n{}".format
                err = err(opt, valid_type, human_type, format_str)
                raise HumanParserError(err)

            opt_name, opt_value = opt_split

            opt_attrs = {om['attr']: opt_value}

    return opt_attrs


def extract_filter(s):
    """Extracts a filter from str `s`

    Parameters
    ----------
    s : str
        A str that may or may not have a filter identified by ', that HUMAN VALUE'

    Returns
    -------
    s : str
        str `s` without the parsed_filter included
    parsed_filter : dict
        filter attributes mapped from filter from `s` if any found
    """
    split_filter = re.split(constants.FILTER_RE, s, re.IGNORECASE)
    # split_filter = ['Folder Name Search with RegEx Match', ' is:.*']

    parsed_filter = {}

    # if filter parsed out from s
    if len(split_filter) > 1:

        # get new s from index 0
        s = split_filter[0].strip()
        # s='Folder Name Search with RegEx Match'

        # get the filter string from index 1
        parsed_filter = split_filter[1].strip()
        # parsed_filter='is:.*'

        parsed_filter = map_filter(parsed_filter)
        if not parsed_filter:
            err = "Filter {!r} is not a valid filter!".format
            raise HumanParserError(err(split_filter[1]))

    dbg = 'parsed new string to {!r} and filters to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_filter)))

    return s, parsed_filter


def map_filter(filter_str):
    """Maps a filter str against :data:`constants.FILTER_MAPS`

    Parameters
    ----------
    filter_str : str
        filter_str str that should be validated

    Returns
    -------
    filter_attrs : dict
        dict containing mapped filter attributes for SOAP API
    """
    filter_attrs = {}

    filter_split = filter_str.split(':')
    if len(filter_split) != 2:
        err = "Invalid filter in {!r}, missing ':' to seperate filter from value?" .format
        raise HumanParserError(err(filter_str))

    filter_name, filter_value = filter_split
    filter_name = filter_name.strip().lower()

    if not filter_value:
        err = "Invalid filter value in {!r}".format
        raise HumanParserError(err(filter_str))

    for fm in constants.FILTER_MAPS:
        for fh in fm['human']:
            if filter_name == fh:
                filter_attrs = fm
                break

    if filter_attrs:

        pre_value = filter_attrs.get('pre_value', '')
        post_value = filter_attrs.get('post_value', '')

        if pre_value:
            filter_value = '{}{}'.format(pre_value, filter_value)

        if post_value:
            filter_value = '{}{}'.format(filter_value, post_value)

        filter_attrs = {
            'operator': filter_attrs['operator'],
            'not_flag': filter_attrs['not_flag'],
            'value': filter_value,
        }
    return filter_attrs


def get_kwargs_int(key, default=None, **kwargs):
    """Gets key from kwargs and validates it is an int

    Parameters
    ----------
    key : str
        key to get from kwargs
    default : int, optional
        default value to use if key not found in kwargs
    **kwargs : dict
        kwargs to get key from

    Returns
    -------
    val : int
        value from key, or default if supplied
    """

    val = kwargs.get(key, default)
    if val is None:
        return val
    try:
        val = int(val)
    except ValueError:
        err = "'{}' must be an int, you supplied: {}"
        raise HandlerError(err(key, val))
    return val


def parse_defs(defname, deftypes, strconv=None, empty_ok=True, defs=None, **kwargs):
    """Parses and validates defs into new_defs

    Parameters
    ----------
    defname : str
        Name of definition
    deftypes : list of str
        list of valid types that defs can be
    strconv : str
        if supplied, and defs is a str, turn defs into a dict with key = strconv, value = defs
    empty_ok : bool
        * True: defs is allowed to be empty
        * False: defs is not allowed to be empty

    Returns
    -------
    new_defs : list of dict
        parsed and validated defs
    """
    if defs is None:
        defs = kwargs.get(defname, eval(deftypes[0]))

    type_msg = "{0!r} requires a non-empty value of type: {1}".format
    type_msg = type_msg(defname, ' or '.join(deftypes))

    if not defs:
        if not empty_ok:
            err = "Argument {0!r} is empty!\n{1}".format
            raise DefinitionParserError(err(defname, type_msg))
        else:
            return defs

    err = (
        "Argument {0!r} has an invalid type {1}\n{2}"
    ).format(defname, type(defs), type_msg)

    if deftypes == ['dict()']:
        if not is_dict(defs):
            raise DefinitionParserError(err)
        else:
            return defs

    new_defs = []
    if is_str(defs):
        if 'str()' in deftypes:
            conv = defs
            if strconv is not None:
                conv = {strconv: defs}
            new_defs.append(conv)
        else:
            raise DefinitionParserError(err)
    elif is_dict(defs):
        if 'dict()' in deftypes:
            new_defs.append(defs)
        else:
            raise DefinitionParserError(err)
    elif is_list(defs):
        if 'list()' in deftypes:
            for k in defs:
                new_defs += parse_defs(
                    defname, deftypes, strconv, empty_ok, k, **kwargs
                )
        else:
            raise DefinitionParserError(err)
    else:
        raise DefinitionParserError(err)

    return new_defs


def val_sensor_defs(sensor_defs):
    """Validates sensor definitions

    Ensures each sensor definition has a selector, and if a sensor definition has a params, options, or filter key, that each key is valid

    Parameters
    ----------
    sensor_defs : list of dict
        list of sensor definitions
    """
    s_obj_map = constants.GET_OBJ_MAP['sensor']
    search_keys = s_obj_map['search']

    for d in sensor_defs:
        # value checking for required keys
        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        if len(def_search) == 0:
            err = "Sensor definition {} missing one of {}!".format
            raise DefinitionParserError(err(d, ', '.join(search_keys)))

        elif len(def_search) > 1:
            err = "Sensor definition {} has more than one of {}!".format
            raise DefinitionParserError(err(d, ', '.join(search_keys)))

        # type checking for optional keys
        chk_def_key(d, 'params', [dict])
        chk_def_key(d, 'options', [dict])
        chk_def_key(d, 'filter', [dict])


def val_package_def(package_def):
    """Validates package definitions

    Ensures package definition has a selector, and if a package definition has a params key, that key is valid

    Parameters
    ----------
    package_def : dict
        package definition
    """
    s_obj_map = constants.GET_OBJ_MAP['package']
    search_keys = s_obj_map['search']

    # value checking for required keys
    def_search = {
        s: package_def.get(s, '')
        for s in search_keys if package_def.get(s, '')
    }

    if len(def_search) == 0:
        err = "Package definition {} missing one of {}!".format
        raise DefinitionParserError(err(package_def, ', '.join(search_keys)))

    elif len(def_search) > 1:
        err = "Package definition {} has more than one of {}!".format
        raise DefinitionParserError(err(package_def, ', '.join(search_keys)))

    # type checking for optional keys
    chk_def_key(package_def, 'params', [dict])


def val_q_filter_defs(q_filter_defs):
    """Validates question filter definitions

    Ensures each question filter definition has a selector, and if a question filter definition has a filter key, that key is valid

    Parameters
    ----------
    q_filter_defs : list of dict
        list of question filter definitions
    """
    s_obj_map = constants.GET_OBJ_MAP['sensor']
    search_keys = s_obj_map['search']

    for d in q_filter_defs:
        # value checking for required keys
        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        if len(def_search) == 0:
            err = "Question Filter {} missing one of {}!".format
            raise DefinitionParserError(err(d, ', '.join(search_keys)))

        elif len(def_search) > 1:
            err = "Question Filter {} has more than one of {}!".format
            raise DefinitionParserError(err(d, ', '.join(search_keys)))

        # type checking for required filter key
        chk_def_key(d, 'filter', [dict], req=True)


def build_selectlist_obj(sensor_defs):
    """Creates a SelectList object from sensor_defs

    Parameters
    ----------
    sensor_defs : list of dict
        List of dict that are sensor definitions

    Returns
    -------
    select_objlist : :class:`taniumpy.object_types.select_list.SelectList`
        SelectList object with list of :class:`taniumpy.object_types.select.Select` built from `sensor_defs`
    """
    select_objlist = taniumpy.SelectList()

    for d in sensor_defs:

        # validate/map sensor params into a ParameterList()
        sensor_obj = d['sensor_obj']
        user_params = d.get('params', {})
        param_objlist = build_param_objlist(
            obj=sensor_obj,
            user_params=user_params,
            delim='||',
            derive_def=True,
            empty_ok=True
        )

        # validate/map sensor filter into a Filter()
        filter_obj = get_filter_obj(d)

        # get the options the user supplied
        options = d.get('options', {})

        # update filter_obj with any options the user supplied
        filter_obj = apply_options_obj(options, filter_obj, 'filter')

        # create a select object for this sensor
        select_obj = taniumpy.Select()
        select_obj.sensor = taniumpy.Sensor()
        select_obj.filter = filter_obj

        # if there are parameters, we need to set the following to
        # sensor_obj.id:
        #  - select_obj.sensor_obj.source_id
        #  - select_obj.filter.sensor.id
        if param_objlist:
            select_obj.sensor.source_id = d['sensor_obj'].id
            select_obj.sensor.parameters = param_objlist
            select_obj.filter.sensor.id = d['sensor_obj'].id
        else:
            select_obj.sensor.hash = d['sensor_obj'].hash

        select_objlist.select.append(select_obj)
    return select_objlist


def build_group_obj(q_filter_defs, q_option_defs):
    """Creates a Group object from q_filter_defs and q_option_defs

    Parameters
    ----------
    q_filter_defs : list of dict
        List of dict that are question filter definitions
    q_option_defs : dict
        dict of question filter options

    Returns
    -------
    group_obj : :class:`taniumpy.object_types.group.Group`
        Group object with list of :class:`taniumpy.object_types.filter.Filter` built from `q_filter_defs` and `q_option_defs`
    """
    filter_objlist = taniumpy.FilterList()

    for d in q_filter_defs:
        # validate/map question filter into a Filter()
        filter_obj = get_filter_obj(d)

        # update filter_obj with any options
        filter_obj = apply_options_obj(q_option_defs, filter_obj, 'filter')
        filter_objlist.filter.append(filter_obj)

    group_obj = taniumpy.Group()
    group_obj.filters = filter_objlist
    group_obj = apply_options_obj(q_option_defs, group_obj, 'group')

    return group_obj


def build_manual_q(selectlist_obj, group_obj):
    """Creates a Question object from selectlist_obj and group_obj

    Parameters
    ----------
    selectlist_obj : :class:`taniumpy.object_types.select_list.SelectList`
        SelectList object to add to Question object
    group_obj : :class:`taniumpy.object_types.group.Group`
        Group object to add to Question object

    Returns
    -------
    add_q_obj : :class:`taniumpy.object_types.question.Question`
        Question object built from selectlist_obj and group_obj
    """
    add_q_obj = taniumpy.Question()
    add_q_obj.selects = selectlist_obj
    add_q_obj.group = group_obj
    return add_q_obj


def get_obj_params(obj):
    """Get the parameters from a TaniumPy object and JSON load them

    obj : :class:`taniumpy.object_types.base.BaseType`
        TaniumPy object to get parameters from

    Returns
    -------
    params : dict
        JSON loaded dict of parameters from `obj`

    """
    # get the parameter definitions
    param_def = getattr(obj, 'parameter_definition', {}) or {}

    # json load the parameter definitions if they exist
    if param_def:
        param_def = json.loads(param_def)

    # get the list of parameters from the parameter definitions
    params = param_def.get('parameters', [])
    return params


def build_param_obj(key, val, delim=''):
    """Creates a Parameter object from key and value, surrounding key with delim

    Parameters
    ----------
    key : str
        key to use for parameter
    value : str
        value to use for parameter
    delim : str
        str to surround key with when adding to parameter object

    Returns
    -------
    param_obj : :class:`taniumpy.object_types.parameter.Parameter`
        Parameter object built from key and val
    """
    # create a parameter object
    param_obj = taniumpy.Parameter()
    param_obj.key = '{0}{1}{0}'.format(delim, key)
    param_obj.value = val
    return param_obj


def derive_param_default(obj_param):
    """Derive a parameter default

    Parameters
    ----------
    obj_param : dict
        parameter dict from TaniumPy object

    Returns
    -------
    def_val : str
        default value derived from obj_param
    """
    # get the default value for this param if it exists
    def_val = obj_param.get('defaultValue', '')

    # get requireSelection for this param if it exists (pulldown menus)
    req_sel = obj_param.get('requireSelection', False)

    # get values for this param if it exists (pulldown menus)
    values = obj_param.get('values', [])

    # if this param requires a selection and it has a list of values
    # and there is no default value, use the first value as the
    # default value
    if req_sel and values and not def_val:
        def_val = values[0]
    return def_val


def build_param_objlist(obj, user_params, delim='', derive_def=False, empty_ok=False):
    """Creates a ParameterList object from user_params

    Parameters
    ----------
    obj : :class:`taniumpy.object_types.base.BaseType`
        TaniumPy object to verify parameters against
    user_params : dict
        dict describing key and value of user supplied params
    delim : str
        str to surround key with when adding to parameter object
    derive_def : bool, optional
        * False: Do not derive default values, and throw a :exc:`HandlerError` if user did not supply a value for a given parameter
        * True: Try to derive a default value for each parameter if user did not supply one
    empty_ok : bool, optional
        * False: If user did not supply a value for a given parameter, throw a :exc:`HandlerError`
        * True: If user did not supply a value for a given parameter, do not add the parameter to the ParameterList object

    Returns
    -------
    param_objlist : :class:`taniumpy.object_types.parameter_list.ParameterList`
        ParameterList object with list of :class:`taniumpy.object_types.parameter.Parameter` built from user_params
    """
    # extract the params from the object
    obj_params = get_obj_params(obj)
    obj_name = str(obj)
    param_objlist = taniumpy.ParameterList()

    processed = []

    for obj_param in obj_params:
        # get the key for this param
        p_key = obj_param["key"]
        processed.append(p_key)
        user_val = user_params.get(p_key, '')

        if not user_val and derive_def:
            user_val = derive_param_default(obj_param)

        if not user_val and not empty_ok:
            err = (
                "{} parameter key '{}' requires a value, "
                "parameter definition:\n{}"
            ).format
            raise HandlerError(err(obj_name, p_key, jsonify(obj_param)))
        param_obj = build_param_obj(p_key, user_val, delim)
        param_objlist.append(param_obj)

        dbg = "Parameter {} for {} mapped to: {}".format
        manuallog.debug(dbg(p_key, obj_name, param_obj))

    # ADD SUPPORT FOR PARAMS THAT ARE NOT IN OBJECT
    for k, v in user_params.iteritems():
        if k in processed:
            continue
        processed.append(k)
        param_obj = build_param_obj(k, v, delim)
        param_objlist.append(param_obj)

        dbg = "Undefined Parameter {} for {} mapped to: {}".format
        manuallog.debug(dbg(k, obj_name, param_obj))

    return param_objlist


def get_filter_obj(sensor_def):
    """Creates a Filter object from sensor_def

    Parameters
    ----------
    sensor_def : dict
        dict containing sensor definition

    Returns
    -------
    filter_obj : :class:`taniumpy.object_types.filter.Filter`
        Filter object created from `sensor_def`
    """
    sensor_obj = sensor_def['sensor_obj']

    # create our basic filter that is needed no matter what
    filter_obj = taniumpy.Filter()
    filter_obj.sensor = taniumpy.Sensor()
    filter_obj.sensor.hash = sensor_obj.hash

    # get the filter the user supplied
    filter_def = sensor_def.get('filter', {})

    # if no user supplied filter, return the basic filter object
    if not filter_def:
        return filter_obj

    # operator required
    def_op = filter_def.get('operator', None)
    if not def_op:
        err = "Filter {!r} requires an 'operator' key!".format
        raise DefinitionParserError(err(filter_def))

    # not_flag optional
    def_not_flag = filter_def.get('not_flag', None)

    # value required
    def_value = filter_def.get('value', None)
    if not def_value:
        err = "Filter {!r} requires a 'value' key!".format
        raise DefinitionParserError(err(filter_def))

    found_match = False
    for fm in constants.FILTER_MAPS:
        # if user supplied operator does not match this operator, next
        if not def_op.lower() == fm['operator'].lower():
            continue

        found_match = True

        filter_obj.value = def_value

        filter_obj.operator = fm['operator']
        if def_not_flag is not None:
            filter_obj.not_flag = def_not_flag

        dbg = "Filter {!r} mapped to: {}".format
        manuallog.debug(dbg(filter_def, str(filter_obj)))
        break

    if not found_match:
        err = "Invalid filter {!r}".format
        raise DefinitionParserError(err(filter_def))

    return filter_obj


def apply_options_obj(options, obj, dest):
    """Updates an object with options

    Parameters
    ----------
    options : dict
        dict containing options definition
    obj : :class:`taniumpy.object_types.base.BaseType`
        TaniumPy object to apply `options` to
    dest : list of str
        list of valid destinations (i.e. `filter` or `group`)

    Returns
    -------
    obj : :class:`taniumpy.object_types.base.BaseType`
        TaniumPy object updated with attributes from `options`
    """
    # if no user supplied options, return the filter object unchanged
    if not options:
        return obj

    for k, v in options.iteritems():
        for om in constants.OPTION_MAPS:

            if om['destination'] != dest:
                continue

            om_attrs = om.get('attrs', {}).keys()
            om_attr = om.get('attr', '')

            if om_attr:
                om_attrs.append(om_attr)

            if k.lower() not in om_attrs:
                continue

            dbg = "option {!r} value {!r} mapped to: {!r}".format
            manuallog.debug(dbg(k, v, om))

            valid_values = om.get('valid_values', [])
            valid_type = om.get('valid_type', str)

            if valid_values:
                valid_values = eval(valid_values)
                valid_values_str = " -- valid values: "
                valid_values_str += ', '.join(valid_values)
            else:
                valid_values = []
                valid_values_str = ""

            if len(str(v)) == 0:
                err = (
                    "Option {!r} requires a {} value{}"
                ).format
                raise DefinitionParserError(err(
                    k, valid_type, valid_values_str)
                )

            if valid_type == int:
                try:
                    v = int(v)
                except:
                    err = (
                        "Option {!r} value {!r} is not an integer"
                    ).format
                    raise DefinitionParserError(err(k, v))

            if valid_type == str:
                if not type(v) in [str, unicode]:
                    err = (
                        "Option {!r} value {!r} is not a string"
                    ).format
                    raise DefinitionParserError(err(k, v))

            value_match = None
            if valid_values:
                for x in valid_values:
                    if v.lower() == x.lower():
                        value_match = x
                        break

                if value_match is None:
                    err = (
                        "Option {!r} value {!r} does not match one of {}"
                    ).format
                    raise DefinitionParserError(err(k, v, valid_values))
                else:
                    v = value_match

            # update obj with k = v
            setattr(obj, k, v)

            break

    dbg = "Options {!r} updated to: {}".format
    manuallog.debug(dbg(options, str(obj)))
    return obj


def chk_def_key(def_dict, key, keytypes, keysubtypes=None, req=False):
    """Checks that def_dict has key

    Parameters
    ----------
    def_dict : dict
        Definition dictionary
    key : str
        key to check for in def_dict
    keytypes : list of str
        list of str of valid types for key
    keysubtypes : list of str
        if key is a dict or list, validate that all values of dict or list are in keysubtypes
    req : bool
        * False: key does not have to be in def_dict
        * True: key must be in def_dict, throw :exc:`DefinitionParserError` if not
    """
    if key not in def_dict:
        if req:
            err = "Definition {} missing 'filter' key!".format
            raise DefinitionParserError(err(def_dict))
        return

    val = def_dict.get(key)
    if type(val) not in keytypes:
        err = (
            "'{}' key in definition dictionary must be a {}, you supplied "
            "a {}!"
        ).format
        raise DefinitionParserError(err(key, keytypes, type(val)))

    if not keysubtypes or not val:
        return

    if type(val) == dict:
        subtypes = [type(x) for x in val.values()]
    else:
        subtypes = [type(x) for x in val]

    if not all([x in keysubtypes for x in subtypes]):
        err = (
            "'{}' key in definition dictionary must be a {} of {}s, "
            "you supplied {}!"
        ).format
        raise DefinitionParserError(err(key, keytypes, keysubtypes, subtypes))


def empty_obj(taniumpy_object):
    """Validate that a given TaniumPy object is not empty

    Parameters
    ----------
    taniumpy_object : :class:`taniumpy.object_types.base.BaseType`
        object to check if empty

    Returns
    -------
    bool
        True if `taniumpy_object` is considered empty, False otherwise
    """
    v = [getattr(taniumpy_object, '_list_properties', {}), is_str(taniumpy_object)]
    if any(v) and not taniumpy_object:
        return True
    else:
        return False


def get_ask_kwargs(**kwargs):
    """Gets QuestionAsker args from kwargs and returns a dict with just those matching args

    Parameters
    ----------
    **kwargs : dict
        kwargs to get keys from

    Returns
    -------
    ask_kwargs : dict
        args from kwargs that are found in :data:`pytan.constants.ASK_KWARGS`
    """

    ask_kwargs = {}
    for i in kwargs:
        if i in constants.ASK_KWARGS:
            ask_kwargs[i] = kwargs[i]
    return ask_kwargs


def get_req_kwargs(**kwargs):
    """Gets SOAP API request args from kwargs and returns a dict with just those matching args

    Parameters
    ----------
    **kwargs : dict
        kwargs to get keys from

    Returns
    -------
    req_kwargs : dict
        args from kwargs that are found in :data:`pytan.constants.REQ_KWARGS`
    """
    req_kwargs = {}
    for i in kwargs:
        if i in constants.REQ_KWARGS:
            req_kwargs[i] = kwargs[i]
    return req_kwargs


def get_q_obj_map(qtype):
    """Gets an object map for `qtype`

    Parameters
    ----------
    qtype : str
        question type to get object map from in :data:`pytan.constants.Q_OBJ_MAP`

    Returns
    -------
    obj_map : dict
        matching object map for `qtype` from :data:`pytan.constants.Q_OBJ_MAP`
    """
    try:
        obj_map = constants.Q_OBJ_MAP[qtype.lower()]
    except KeyError:
        err = "{} not a valid question type, must be one of {!r}".format
        raise HandlerError(err(qtype, constants.Q_OBJ_MAP.keys()))
    return obj_map


def get_obj_map(objtype):
    """Gets an object map for `objtype`

    Parameters
    ----------
    objtype : str
        object type to get object map from in :data:`pytan.constants.GET_OBJ_MAP`

    Returns
    -------
    obj_map : dict
        matching object map for `objtype` from :data:`pytan.constants.GET_OBJ_MAP`
    """
    try:
        obj_map = constants.GET_OBJ_MAP[objtype.lower()]
    except KeyError:
        err = "{} not a valid object to get, must be one of {!r}".format
        raise HandlerError(err(objtype, constants.GET_OBJ_MAP.keys()))
    return obj_map


def question_progress(asker, pct):
    """Call back method for :func:`taniumpy.question_asker.QuestionAsker.run` to report progress while waiting for results from a question

    Parameters
    ----------
    asker : :class:`taniumpy.question_asker.QuestionAsker`
        QuestionAsker instance
    pct : float
        Percentage completion of question
    """
    q_info = asker.question.query_text or asker.question
    progresslog.info("Results {1:.0f}% ({0})".format(q_info, pct))


def check_dictkey(d, key, valid_types, valid_list_types):
    """Yet another method to check a dictionary for a key

    Parameters
    ----------
    d : dict
        dictionary to check for key
    key : str
        key to check for in d
    valid_types : list of str
        list of str of valid types for key
    valid_list_types : list of str
        if key is a list, validate that all values of list are in valid_list_types
    """
    if key in d:
        k_val = d[key]
        k_type = type(k_val)
        if k_type not in valid_types:
            err = "{!r} must be one of {}, you supplied {}!".format
            raise HandlerError(err(key, valid_types, k_type))
        if is_list(k_val) and valid_list_types:
            valid_list_types = [eval(x) for x in valid_list_types]
            list_types = [type(x) for x in k_val]
            list_types_match = [x in valid_list_types for x in list_types]
            if not all(list_types_match):
                err = "{!r} must be a list of {}, you supplied {}!".format
                raise HandlerError(err(key, valid_list_types, list_types))


def xml_pretty(x):
    """Uses :mod:`xmltodict` to pretty print an XML str `x`

    Parameters
    ----------
    x : str
        XML string to pretty print

    Returns
    -------
    str :
        The pretty printed string of `x`
    """

    x_parsed = xmltodict.parse(x)
    x_unparsed = xmltodict.unparse(x_parsed, pretty=True, indent='  ')
    return x_unparsed


def xml_pretty_resultxml(x):
    """Uses :mod:`xmltodict` to pretty print an the ResultXML element in XML str `x`

    Parameters
    ----------
    x : str
        XML string to pretty print

    Returns
    -------
    str :
        The pretty printed string of ResultXML in `x`
    """

    x_parsed = xmltodict.parse(x)
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]["ResultXML"]
    x_unparsed = xml_pretty(x_find)
    return x_unparsed


def xml_pretty_resultobj(x):
    """Uses :mod:`xmltodict` to pretty print an the result-object element in XML str `x`

    Parameters
    ----------
    x : str
        XML string to pretty print

    Returns
    -------
    str :
        The pretty printed string of result-object in `x`
    """

    x_parsed = xmltodict.parse(x)
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]
    x_find = x_parsed["result-object"]
    x_unparsed = xmltodict.unparse(x_find, pretty=True, indent='  ')
    return x_unparsed


def get_dict_list_items(d, i):
    """Gets keys from dict `d` if any item in list `i` is in the list value for each key

    Parameters
    ----------
    d : dict of str : list
        dict to get strs from if list contains any item from `i`
    i : list of str
        list of strs to check if for existence in any lists in `d`

    Returns
    -------
    list : list of str
        list of strings from `d` that have `i` in their values
    """
    return [x for x in d for y in i if y in d[x]]


def get_dict_list_len(d, keys=[], negate=False):
    """Gets the sum of each list in dict `d`

    Parameters
    ----------
    d : dict of str : list
        dict to sums of
    keys : list of str
        list of keys to get sums of, if empty gets a sum of all keys
    negate : bool
        * only used if keys supplied
        * False : get the sums of `d` that do match keys
        * True : get the sums of `d` that do not match keys

    Returns
    -------
    list_len : int
        sum of lists in `d` that match keys
    """
    if keys:
        if negate:
            list_len = sum([len(d[k]) for k in d if k not in keys])
        else:
            list_len = sum([len(d[k]) for k in d if k in keys])
    else:
        list_len = sum([len(d[k]) for k in d])
    return list_len


def build_metadatalist_obj(properties, nameprefix):
    """Creates a MetadataList object from properties

    Parameters
    ----------
    properties : list of list of strs
        list of lists, each list having two strs - str 1: property key, str2: property value
    nameprefix : str
        prefix to insert in front of property key when creating MetadataItem

    Returns
    -------
    metadatalist_obj : :class:`taniumpy.object_types.metadata_list.MetadataList`
        MetadataList object with list of :class:`taniumpy.object_types.metadata_item.MetadataItem` built from `properties`
    """
    metadatalist_obj = taniumpy.MetadataList()
    for prop in properties:
        metadata_obj = taniumpy.MetadataItem()
        metadata_obj.name = "{}.{}".format(nameprefix, prop[0])
        metadata_obj.value = prop[1]
        metadatalist_obj.append(metadata_obj)
    return metadatalist_obj


def passmein(func):
    """Decorator method to pass the function to a function that uses this decorator"""
    def wrapper(*args, **kwargs):
        return func(func, *args, **kwargs)
    return wrapper


@passmein
def help_sensors(me):
    """
Sensors Help
============

Supplying sensors controls what columns will be showed when you ask a
question.

A sensor string is a human string that describes, at a minimum, a sensor.
It can also optionally define a selector for the sensor, parameters for
the sensor, a filter for the sensor, and options for the filter for the
sensor. Sensors can be provided as a string or a list of strings.

Examples for basic sensors
---------------------------------

Supplying a single sensor:

    'Computer Name'

Supplying two sensors in a list of strings:

    ['Computer Name', 'IP Route Details']

Supplying multiple sensors with selectors (name is the default
selector if none is supplied):

    [
        'Computer Name',
        'name:Computer Name',
        'id:1',
        'hash:123456789',
    ]

Sensor Parameters
-----------------

Supplying parameters to a sensor can control the arguments that are
supplied to a sensor, if that sensor takes any arguments.

Sensor parameters must be surrounded with curly braces '{}',
and must have a key and value specified that is separated by
an equals '='. Multiple parameters must be seperated by
a comma ','. The key should match up to a valid parameter key
for the sensor in question.

If a parameter is supplied and the sensor doesn't have a
corresponding key name, it will be ignored. If the sensor has
parameters and a parameter is NOT supplied then one of two
paths will be taken:

    * if the parameter does not require a default value, the
    parameter is left blank and not supplied.
    * if the parameter does require a value (pulldowns, for
    example), a default value is derived (for pulldowns,
    the first value available as a pulldown entry is used).

Examples for sensors with parameters
------------------------------------

Supplying a single sensor with a single parameter 'dirname':

    'Sensor With Params{dirname=Program Files}'

Supplying a single sensor with two parameters, 'param1' and
'param2':

    'Sensor With Params{param1=value1,param2=value2}'

Sensor Filters
--------------

Supplying a filter to a sensor controls what data will be shown in
those columns (sensors) you've provided.

Sensor filters can be supplied by adding ', that FILTER:VALUE',
where FILTER is a valid filter string, and VALUE is the string
that you want FILTER to match on.

See filter help for a list of all possible FILTER strings.

See options help for a list of options that can control how
the filter works.

Examples for sensors with filters
---------------------------------

Supplying a sensor with a filter that limits the results to only
show column data that matches the regular expression
'.*Windows.*' (Tanium does a case insensitive match by default):

    'Computer Name, that contains:Windows'

Supplying a sensor with a filter that limits the results to only
show column data that matches the regular expression
'Microsoft.*':

    'Computer Name, that starts with:Microsoft'

Supply a sensor with a filter that limits the results to only
show column data that has a version greater or equal to
'39.0.0.0'. Since this sensor uses Version as its default result
type, there is no need to change the value type using filter
options.

    'Installed Application Version' \\
    '{Application Name=Google Chrome}, that =>:39.0.0.0'

Sensor Options
--------------

Supplying options to a sensor can change how the filter for
that sensor works.

Sensor options can be supplied by adding ', opt:OPTION' or
', opt:OPTION:VALUE' for those options that require values,
where OPTION is a valid option string, and VALUE is the
appropriate value required by accordant OPTION.

See options help for a list of options that can control how
the filter works.

Examples for sensors with options
---------------------------------

Supplying a sensor with an option that forces tanium to
re-fetch any cached column data that is older than 1 minute:

    'Computer Name, opt:max_data_age:60'

Supplying a sensor with filter and an option that causes
Tanium to match case for the filter value:

    'Computer Name, that contains:Windows, opt:match_case'

Supplying a sensor with a filter and an option that causes
Tanium to match all values supplied:

    'Computer Name, that contains:Windows, opt:match_all_values'

Supplying a sensor with a filter and a set of options that
causes Tanium to recognize the value type as String (which is
the default type for most sensors), re-fetch data older than
10 minutes, match any values, and match case:

    'Computer Name', that contains:Windows, ' \\
    opt:value_type:string, opt:max_data_age:600, ' \\
    'opt:match_any_value, opt:match_case'
"""
    return me.__doc__


@passmein
def help_package(me):
    """
Package Help
============

Supplying package defines what package will be deployed as part of the
action.

A package string is a human string that describes, at a minimum, a
package. It can also optionally define a selector for the package,
and/or parameters for the package. A package must be provided as a string.

Examples for package
---------------------------------

Supplying a package:

    'Distribute Tanium Standard Utilities'

Supplying a package by id:

    'id:1'

Supplying a package by hash:

    'hash:123456789'

Supplying a package by name:

    'name:Distribute Tanium Standard Utilities'

Package Parameters
------------------

Supplying parameters to a package can control the arguments
that are supplied to a package, if that package takes any arguments.

Package parameters must be surrounded with curly braces '{}',
and must have a key and value specified that is separated by
an equals '='. Multiple parameters must be seperated by
a comma ','. The key should match up to a valid parameter key
for the package in question.

If a parameter is supplied and the package doesn't have a
corresponding key name, it will be ignored. If the package has
parameters and a parameter is NOT supplied then an exception
will be raised, printing out the JSON of the missing paramater
for the package in question.

Examples for package with parameters
------------------------------------

Supplying a package with a single parameter '$1':

    'Package With Params{$1=value1}'

Supplying a package with two parameters, '$1' and '$2':

    'Package With Params{$1=value1,$2=value2}'
"""
    return me.__doc__


@passmein
def help_filters(me):
    """
Filters Help
============

Filters are used generously throughout pytan. When used as part of a
sensor string, they control what data is shown for the columns that
the sensor returns. When filters are used for whole question filters,
they control what rows will be returned. They are used by Groups to
define group membership, deploy actions to determine which machines
should have the action deployed to it, and more.

A filter string is a human string that describes, a sensor followed
by ', that FILTER:VALUE', where FILTER is a valid filter string,
and VALUE is the string that you want FILTER to match on.

Valid Filters
-------------

"""
    for x in constants.FILTER_MAPS:
        for y in x['human']:
            me.__doc__ += '    {!r:<25}\n'.format(y)
            me.__doc__ += '        Help: {}\n'.format(x['help'])
            me.__doc__ += '        Example: "Sensor1, that {}:VALUE"\n\n'.format(y)
    return me.__doc__


@passmein
def help_options(me):
    """
Options Help
============

Options are used for controlling how filters act. When options are
used as part of a sensor string, they change how the filters
supplied as part of that sensor operate. When options are used for
whole question options, they change how all of the question filters
operate.

When options are supplied for a sensor string, they must be
supplied as ', opt:OPTION' or ', opt:OPTION:VALUE' for options
that require a value.

When options are supplied for question options, they must be
supplied as 'OPTION' or 'OPTION:VALUE' for options that require
a value.

Options can be used on 'filter' or 'group', where 'group' pertains
to group filters or question filters. All 'filter' options are also
applicable to 'group' for question options.

Valid Options
-------------

"""
    for x in constants.OPTION_MAPS:
        me.__doc__ += '    {!r:<25}\n'.format(x['human'])
        me.__doc__ += '        Help: {}\n'.format(x['help'])

        me.__doc__ += '        Usable on: {}\n'.format(x['destination'])
        if x.get('human_type', ''):
            me.__doc__ += '        VALUE description and type: {}, {}\n'.format(
                x['human_type'], x['valid_type'])
            me.__doc__ += '        Example for sensor: "Sensor1, opt:{}:{}"\n'.format(
                x['human'], x['human_type'])
            me.__doc__ += '        Example for question: "{}:{}"\n'.format(
                x['human'], x['human_type'])
        else:
            me.__doc__ += '        Example for sensor: "Sensor1, opt:{}"\n'.format(x['human'])
            me.__doc__ += '        Example for question: "{}"\n'.format(x['human'])
        me.__doc__ += '\n'
    return me.__doc__
