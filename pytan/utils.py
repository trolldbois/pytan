#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Generic Utility Functions"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import socket
import time
import logging
import json
import argparse
from argparse import ArgumentDefaultsHelpFormatter as A1
from argparse import RawDescriptionHelpFormatter as A2
from collections import OrderedDict

from . import __version__
from . import constants
from . import api
from . import xmltodict

mylog = logging.getLogger("handler")
humanlog = logging.getLogger("ask_manual_human")
manuallog = logging.getLogger("ask_manual")
progresslog = logging.getLogger("question_progress")
pname = os.path.splitext(os.path.basename(sys.argv[0]))[0]


class HandlerError(Exception):
    pass


class HumanParserError(Exception):
    pass


class DefinitionParserError(Exception):
    pass


class SplitStreamHandler(logging.Handler):
    '''sends info and below to stdout, warning and above to stderr'''

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
    pass


class CustomArgParse(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomArgFormat
        #print kwargs
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
    parser = CustomArgParse(
        description=desc,
        add_help=help,
        formatter_class=CustomArgFormat,
    )
    auth_group = parser.add_argument_group('Handler Authentication')
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


def setup_ask_saved_argparser(doc):
    obj = 'saved_question'
    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    ask_arggroup = parser.add_argument_group('Saved Question Selectors')
    group = ask_arggroup.add_mutually_exclusive_group()

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


def setup_ask_manual_argparser(doc):
    parent_parser = setup_parser(doc)
    parser = CustomArgParse(
        description=doc,
        parents=[parent_parser],
    )
    ask_arggroup = parser.add_argument_group('Manual Question Options')

    ask_arggroup.add_argument(
        '-s',
        '--sensor',
        required=True,
        action='append',
        default=[],
        dest='sensors',
        help='Sensor, optionally describe parameters, options, and a filter'
        '; pass --sensor-help to get a full description',
    )

    ask_arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='question_filters',
        help='Whole question filter; pass --filter-help'
        'to get a full description',
    )

    ask_arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='question_options',
        help='Whole question option; pass --option-help to get a full '
        'description',
    )

    return parser


def add_ask_report_argparser(parser):
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


def process_get_object_args(parser, handler, obj, all_args):
    # put our query args into their own dict and remove them from all_args
    getobj_grp_names = [
        'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    getobj_grp_opts = get_grp_opts(parser, getobj_grp_names)
    getobj_grp_args = {k: all_args.pop(k) for k in getobj_grp_opts}
    get_all = getobj_grp_args.pop('all')
    if get_all:
        try:
            response = handler.get_all(obj)
        except Exception as e:
            print e
            sys.exit(100)
    else:
        try:
            response = handler.get(obj, **getobj_grp_args)
        except Exception as e:
            print e
            sys.exit(100)

    print "Found items: ", response
    return response


def get_grp_opts(parser, grp_names):
    action_grps = [a for a in parser._action_groups if a.title in grp_names]
    grp_opts = [a.dest for b in action_grps for a in b._group_actions]
    return grp_opts


def is_list(l):
    return type(l) in [list, tuple]


def is_str(l):
    return type(l) in [unicode, str]


def is_dict(l):
    return type(l) in [dict, OrderedDict]


def is_num(l):
    return type(l) in [float, int, long]


def version_check(reqver):
    """for scripts using this API to validate the version of the API

    :param reqver: string containing version number to check against
    """
    log_tpl = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        raise Exception(log_tpl(s, __file__, __version__, reqver))

    s = "Script and API Version match"
    logging.debug(log_tpl(s, __file__, __version__, reqver))
    return True


def jsonify(v, indent=2, sort_keys=True):
    '''json pretty printer'''
    return json.dumps(v, indent=indent, sort_keys=sort_keys)


def get_now():
    """return current time in human friendly format

    :return: :class:`str`
    """
    return human_time(time.localtime())


def human_time(t, tformat='%Y_%m_%d-%H_%M_%S-%Z'):
    """return time in human friendly format

    :param t: either a epoch or struct_time time object
    :param tformat: strftime format string
    :return: :class:`str`
    """
    if is_num(t):
        t = time.localtime(t)
    return time.strftime(tformat, t)


def port_check(address, port, timeout=5):
    """Check if address:port can be reached within timeout

    :param address: string of host to connect to
    :param port: string of port to connect to
    :param timeout: int of seconds to wait until connection fails

    :return: :class:`bool`
    """
    try:
        return socket.create_connection((address, port), timeout)
    except socket.error:
        return False


def test_app_port(host, port):
    """validates that the SOAP port on the SOAP host can be reached"""
    chk_tpl = "Port test to {}:{} {}".format
    if port_check(host, port):
        mylog.debug(chk_tpl(host, port, "SUCCESS"))
    else:
        raise HandlerError(chk_tpl(host, port, "FAILURE"))


def remove_logging_handler(name):
    '''used to remove a handler (or all handlers if name == all)'''
    root_logger = logging.getLogger()
    root_handlers = root_logger.handlers
    for h in root_handlers:
        if name == 'all':
            root_logger.removeHandler(h)
        elif h.name == name:
            root_logger.removeHandler(h)


def setup_console_logging():
    ch_name = 'console'
    remove_logging_handler('all')
    # add a console handler to the root logger that goes to STDOUT for INFO
    # and below, but STDERR for WARNING and above
    ch = SplitStreamHandler()
    ch.set_name(ch_name)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(constants.INFO_FORMAT)
    root_logger = logging.getLogger()
    root_logger.addHandler(ch)
    root_logger.setLevel(logging.DEBUG)


def change_console_format(debug=False):
    '''changes the logging format to DEBUG_FORMAT or INFO_FORMAT'''
    root_logger = logging.getLogger()
    root_handlers = root_logger.handlers
    for h in root_handlers:
        if h.name == 'console':
            if debug:
                h.setFormatter(constants.DEBUG_FORMAT)
            else:
                h.setFormatter(constants.INFO_FORMAT)


def set_log_levels(loglevel=0):
    '''used to set the loggers in constants.LOG_LEVEL_MAP to their
    respective level depending on loglevel'''
    set_all_loglevels('WARN')
    for logmap in constants.LOG_LEVEL_MAPS:
        if loglevel >= logmap[0]:
            for lname, llevel in logmap[1].iteritems():
                # print 'setting %s to %s' % (lname, llevel)
                logging.getLogger(lname).setLevel(getattr(logging, llevel))


def set_all_loglevels(level='DEBUG'):
    '''sets all loggers that the logging system knows about to a given level'''
    for k, v in sorted(logging.Logger.manager.loggerDict.iteritems()):
        if not isinstance(v, logging.Logger):
            continue
        v.setLevel(getattr(logging, level))


def dehumanize_sensors(sensors):
    if not sensors:
        err = (
            "A sensor string or list of strings must be supplied as 'sensors'!"
        )
        raise HumanParserError(err)

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

        dbg = 'parsed sensor string {!r} into sensor definition:\n {}'.format
        humanlog.debug(dbg(sensor, jsonify(sensor_def)))

        sensor_defs.append(sensor_def)

    return sensor_defs


def dehumanize_question_filters(question_filters):
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
            'parsed question filter string {!r} into question filter '
            'definition:\n {}'
        ).format
        dbg = dbg(question_filter, jsonify(question_filter_def))
        humanlog.debug(dbg)

        question_filter_defs.append(question_filter_def)

    return question_filter_defs


def dehumanize_question_options(question_options):
    if not question_options:
        return {}

    if not is_list(question_options):
        question_options = [question_options]

    dest = ['filter', 'group']
    question_option_defs = map_options(question_options, dest)
    dbg = (
        'parsed question options {!r} into question option '
        'definition:\n {}'
    ).format
    dbg = dbg(question_options, jsonify(question_option_defs))
    humanlog.debug(dbg)

    return question_option_defs


def extract_selector(s):
    parsed_selector = 'name'
    for selector in constants.SELECTORS:
        if s.startswith(selector + ':'):
            parsed_selector = selector
            s = s.replace(selector + ':', '').strip()

    dbg = 'parsed new string to {!r} and selector to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_selector)))

    return s, parsed_selector


def extract_params(s):
    # extract params from s

    # given example (note escaped comma in params):
    # 'Folder Name Search with RegEx Match{dirname=Program Files,regex=\,*}' \
    # ', that is .*, opt:max_data_age:3600, opt:ignore_case'

    params = constants.PARAM_RE.findall(s)
    ## params=['dirname=Program Files,regex=\\,*']

    if len(params) > 1:
        err = "More than one parameter ({{}}) passed in {!r}".format
        raise HumanParserError(err(s))
    elif len(params) == 1:
        param = params[0]
    else:
        param = ''
    ## param='dirname=Program Files,regex=\\,*'

    if param:
        split_param = constants.PARAM_SPLIT_RE.split(param)
    else:
        split_param = []
    ## split_param=['dirname=Program Files', 'regex=\\,*']

    parsed_params = {}
    for sp in split_param:
        # sp = 'dirname=Program Files'
        if constants.PARAM_KEY_SPLIT not in sp:
            err = "Parameter {} missing key/value seperator ({})".format
            raise HumanParserError(err(sp, constants.PARAM_KEY_SPLIT))
        sp_key, sp_value = sp.split(constants.PARAM_KEY_SPLIT, 1)
        ## sp_key = dirname
        ## sp_value = Program Files
        parsed_params[sp_key] = sp_value

    # remove params from the s string
    s = constants.PARAM_RE.sub('', s)
    ## s='Folder Name Search with RegEx Match, that is .*, ' \
    ## 'opt:max_data_age:3600, opt:ignore_case'

    dbg = 'parsed new string to {!r} and parameters to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_params)))

    return s, parsed_params


def extract_options(s):
    # parse options out of s

    split_option = constants.OPTION_RE.split(s)
    ## split_option = ['Folder Name Search with RegEx Match, that is .*', \
    ## 'max_data_age:3600', 'ignore_case']

    parsed_options = {}

    # if options parsed out from s
    if len(split_option) > 1:

        # get new s from index 0
        s = split_option[0].strip()
        ## s='Folder Name Search with RegEx Match, that is .*'

        # get the option strings from index 1 and on
        parsed_options = [x.strip() for x in split_option[1:]]
        ## parsed_options=['max_data_age:3600', 'ignore_case']

        parsed_options = map_options(parsed_options, ['filter'])

    dbg = 'parsed new string to {!r} and options to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_options)))

    return s, parsed_options


def map_options(options, dest):
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

    split_filter = constants.FILTER_RE.split(s)
    ## split_filter = ['Folder Name Search with RegEx Match', ' is .*']

    parsed_filter = {}

    # if filter parsed out from s
    if len(split_filter) > 1:

        # get new s from index 0
        s = split_filter[0].strip()
        ## s='Folder Name Search with RegEx Match'

        # get the filter string from index 1
        parsed_filter = split_filter[1].strip()
        ## parsed_filter='is .*'

        parsed_filter = map_filter(parsed_filter)
        if not parsed_filter:
            err = "Filter {!r} is not a valid filter!".format
            raise HumanParserError(err(split_filter[1]))

    dbg = 'parsed new string to {!r} and filters to:\n{}'.format
    humanlog.debug(dbg(s, jsonify(parsed_filter)))

    return s, parsed_filter


def map_filter(filter_str):
    filter_attrs = {}

    for fm in constants.FILTER_MAPS:
        for fh in fm['human']:
            if filter_str.lower().startswith(fh + " "):
                filter_str = filter_str[len(fh + " "):]
                filter_attrs = fm
                break

    if filter_attrs:

        if not filter_str:
            err = "Invalid filter value in {!r}".format
            raise HumanParserError(err(filter_str))

        pre_value = filter_attrs.get('pre_value', '')
        post_value = filter_attrs.get('post_value', '')

        if pre_value:
            filter_str = '{}{}'.format(pre_value, filter_str)

        if post_value:
            filter_str = '{}{}'.format(filter_str, post_value)

        filter_attrs = {
            'operator': filter_attrs['operator'],
            'not_flag': filter_attrs['not_flag'],
            'value': filter_str,
        }
    return filter_attrs


def parse_sensor_defs(**kwargs):
    sensor_defs = parse_defs(
        defname='sensor_defs',
        deftypes=['list()', 'str()', 'dict()'],
        strconv='name',
        empty_ok=False,
        **kwargs
    )
    return sensor_defs


def parse_question_filter_defs(**kwargs):
    question_filter_defs = parse_defs(
        defname='question_filter_defs',
        deftypes=['list()', 'dict()'],
        empty_ok=True,
        **kwargs
    )
    return question_filter_defs


def parse_question_option_defs(**kwargs):
    question_option_defs = parse_defs(
        defname='question_option_defs',
        deftypes=['dict()'],
        empty_ok=True,
        **kwargs
    )
    return question_option_defs


def parse_defs(defname, deftypes, strconv=None, empty_ok=True, defs=None,
               **kwargs):

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
    return sensor_defs


def val_q_filter_defs(q_filter_defs):
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

    return q_filter_defs


def build_selectlist_obj(sensor_defs):
    select_objlist = api.SelectList()

    for d in sensor_defs:
        # validate/map sensor params into a ParameterList()
        param_objlist = get_param_objlist(d)

        # validate/map sensor filter into a Filter()
        filter_obj = get_filter_obj(d)

        # get the options the user supplied
        options = d.get('options', {})

        # update filter_obj with any options the user supplied
        filter_obj = apply_options_obj(options, filter_obj, 'filter')

        # create a select object for this sensor
        select_obj = api.Select()
        select_obj.sensor = api.Sensor()
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
    filter_objlist = api.FilterList()

    for d in q_filter_defs:
        # validate/map question filter into a Filter()
        filter_obj = get_filter_obj(d)

        # update filter_obj with any options
        filter_obj = apply_options_obj(q_option_defs, filter_obj, 'filter')
        filter_objlist.filter.append(filter_obj)

    group_obj = api.Group()
    group_obj.filters = filter_objlist
    group_obj = apply_options_obj(q_option_defs, group_obj, 'group')

    return group_obj


def build_manual_q(selectlist_obj, group_obj):
    add_q_obj = api.Question()
    add_q_obj.selects = selectlist_obj
    add_q_obj.group = group_obj
    return add_q_obj


def get_param_objlist(sensor_def):
    sensor_obj = sensor_def['sensor_obj']
    param_objlist = api.ParameterList()

    # get the user supplied params dict
    d_params = sensor_def.get('params', {})

    # get the sensor name
    s_name = str(sensor_obj)

    # get the sensor parameter definitions
    s_param_def = sensor_obj.parameter_definition or {}

    # json load the parameter definitions if they exist
    if s_param_def:
        s_param_def = json.loads(s_param_def)

    # get the list of parameters from the parameter definitions
    s_params = s_param_def.get('parameters', [])

    # if user defined params and this sensor doesn't take params,
    # we will just ignore them

    for s_param in s_params:
        # get the key for this param
        sp_key = s_param["key"]

        # get the default value for this param if it exists
        sp_def_val = s_param.get('defaultValue', '')

        # get requireSelection for this param if it exists (pulldown menus)
        sp_req_sel = s_param.get('requireSelection', False)

        # get values for this param if it exists (pulldown menus)
        sp_values = s_param.get('values', [])

        # if this param requires a selection and it has a list of values
        # and there is no default value, use the first value as the
        # default value
        if sp_req_sel and sp_values and not sp_def_val:
            sp_def_val = sp_values[0]

        # get the user defined value if it exists
        user_val = d_params.get(sp_key, '')

        # if no user defined value, set the user value to the default
        # value
        if not user_val:
            user_val = sp_def_val

        # if still no user defined value, and param requires selection,
        # throw an exception
        if not user_val and sp_req_sel:
            err = (
                "{} parameter key {!r} requires a value, "
                "parameter definition:\n{}"
            ).format
            raise DefinitionParserError(err(s_name, sp_key, jsonify(s_param)))

        # create a parameter object
        param_obj = api.Parameter()
        param_obj.key = '{0}{1}{0}'.format(constants.PARAM_DELIM, sp_key)
        param_obj.value = user_val
        param_objlist.append(param_obj)

        dbg = "Parameter {} for {} mapped to: {}".format
        manuallog.debug(dbg(sp_key, s_name, param_obj))

    return param_objlist


def get_filter_obj(sensor_def):
    sensor_obj = sensor_def['sensor_obj']

    # create our basic filter that is needed no matter what
    filter_obj = api.Filter()
    filter_obj.sensor = api.Sensor()
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


def empty_obj(api_object):
    v = [getattr(api_object, '_list_properties', {}), is_str(api_object)]
    if any(v) and not api_object:
        return True
    else:
        return False


def get_ask_kwargs(**kwargs):
    ask_kwargs = {}
    if 'timeout' in kwargs:
        ask_kwargs['timeout'] = kwargs.pop('timeout')
    return ask_kwargs


def get_req_kwargs(**kwargs):
    REQ_KWARGS = constants.REQ_KWARGS
    req_kwargs = {}
    for i in kwargs:
        if i in REQ_KWARGS:
            req_kwargs[i] = kwargs[i]
    return req_kwargs


def get_q_obj_map(qtype):
    Q_OBJ_MAP = constants.Q_OBJ_MAP
    try:
        obj_map = Q_OBJ_MAP[qtype.lower()]
    except KeyError:
        err = "{} not a valid question type, must be one of {!r}".format
        raise HandlerError(err(qtype, Q_OBJ_MAP.keys()))
    return obj_map


def get_obj_map(obj):
    GET_OBJ_MAP = constants.GET_OBJ_MAP
    try:
        obj_map = GET_OBJ_MAP[obj.lower()]
    except KeyError:
        err = "{} not a valid object to get, must be one of {!r}".format
        raise HandlerError(err(obj, GET_OBJ_MAP.keys()))
    return obj_map


def progressChanged(asker, pct):
    progresslog.info("Results {1:.0f}% ({0})".format(asker, pct))


def check_dictkey(d, key, valid_types, valid_list_types):
    if key in d:
        k_val = d[key]
        k_type = type(k_val)
        if k_type not in valid_types:
            err = "{!r} must be one of {}, you supplied {}!".format
            raise HandlerError(err(key, valid_types, k_type))
        if is_list(k_val) and valid_list_types:
            list_types = [type(x) for x in k_val]
            list_types_match = [x in valid_list_types for x in list_types]
            if not all(list_types_match):
                err = "{!r} must be a list of {}, you supplied {}!".format
                raise HandlerError(err(key, valid_list_types, list_types))


def xml_pretty(x):
    x_parsed = xmltodict.parse(x)
    x_unparsed = xmltodict.unparse(x_parsed, pretty=True, indent='  ')
    return x_unparsed


def xml_pretty_resultxml(x):
    x_parsed = xmltodict.parse(x)
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]["ResultXML"]
    x_unparsed = xml_pretty(x_find)
    return x_unparsed


def xml_pretty_resultobj(x):
    x_parsed = xmltodict.parse(x)
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]
    x_find = x_parsed["result-object"]
    x_unparsed = xmltodict.unparse(x_find, pretty=True, indent='  ')
    return x_unparsed
