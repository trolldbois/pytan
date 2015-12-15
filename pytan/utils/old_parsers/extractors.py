#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Extractors for :mod:`string_parsers`"""

import logging
import pprint
import re
from . import exceptions
from . import mappers
from . import constants

mylog = logging.getLogger(__name__)


def selector(s):
    """Extracts a selector from str `s`

    Parameters
    ----------
    s : str
        * A str that may or may not have a selector in the beginning in the form of id:, name:, or :hash -- if no selector found, name will be assumed as the default selector

    Returns
    -------
    s : str
        * str `s` without the parsed_selector included
    parsed_selector : str
        * selector extracted from `s`, or 'name' if none found
    """
    parsed_selector = 'name'
    for selector in constants.SELECTORS:
        if s.startswith(selector + ':'):
            parsed_selector = selector
            s = s.replace(selector + ':', '').strip()

    dbg = 'parsed new string to {!r} and selector to:\n{}'.format
    mylog.debug(dbg(s, pprint.pformat(parsed_selector)))

    return s, parsed_selector


def parameters(s):
    """Extracts parameters from str `s`

    Parameters
    ----------
    s : str
        * A str that may or may not have parameters identified by {key=value}

    Returns
    -------
    s : str
        * str `s` without the parsed_params included
    parsed_params : list
        * parameters extracted from `s` if any found
    """
    # extract params from s

    # given example (note escaped comma in params):
    # 'Folder Name Search with RegEx Match{dirname=Program Files,regex=\,*}' \
    # ', that is .*, opt:max_data_age:3600, opt:ignore_case'

    params = re.findall(constants.PARAM_RE, s)
    # params=['dirname=Program Files,regex=\\,*']

    if len(params) > 1:
        err = "More than one parameter ({{}}) passed in {!r}".format
        raise exceptions.ParserError(err(s))
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
            raise exceptions.ParserError(err(sp, constants.PARAM_KEY_SPLIT))
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
    mylog.debug(dbg(s, pprint.pformat(parsed_params)))

    return s, parsed_params


def options(s):
    """Extracts options from str `s`

    Parameters
    ----------
    s : str
        * A str that may or may not have options identified by ', opt:name[:value]'

    Returns
    -------
    s : str
        * str `s` without the parsed_options included
    parsed_options : list
        * options extracted from `s` if any found
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

        parsed_options = mappers.options(parsed_options, ['filter'])

    dbg = 'parsed new string to {!r} and options to:\n{}'.format
    mylog.debug(dbg(s, pprint.pformat(parsed_options)))

    return s, parsed_options


def filters(s):
    """Extracts a filter from str `s`

    Parameters
    ----------
    s : str
        * A str that may or may not have a filter identified by ', that HUMAN VALUE'

    Returns
    -------
    s : str
        * str `s` without the parsed_filter included
    parsed_filter : dict
        * filter attributes mapped from filter from `s` if any found
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

        parsed_filter = mappers.filters(parsed_filter)
        if not parsed_filter:
            err = "Filter {!r} is not a valid filter!".format
            raise exceptions.ParserError(err(split_filter[1]))

    dbg = 'parsed new string to {!r} and filters to:\n{}'.format
    mylog.debug(dbg(s, pprint.pformat(parsed_filter)))

    return s, parsed_filter
