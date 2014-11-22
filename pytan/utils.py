#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Generic Utility Functions"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import socket
import time
import logging
import json
from collections import OrderedDict

from . import __version__
from . import constants
from .exceptions import ManualParserError

humanlog = logging.getLogger("ask_manual_human")


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
        # TODO
        raise ManualParserError("help me")

    if not is_list(sensors):
        sensors = [sensors]

    sensor_defs = []
    for sensor in sensors:
        if not is_str(sensor):
            raise ManualParserError("{!r} must be a string".format(sensor))
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
        raise ManualParserError(err(s))
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
            raise ManualParserError(err(sp, constants.PARAM_KEY_SPLIT))
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


def extract_options(s,):
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
            raise ManualParserError(err(option))

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
                raise ManualParserError(err)

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
            raise ManualParserError(err(split_filter[1]))

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
            raise ManualParserError(err(filter_str))

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
