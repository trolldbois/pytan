#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""String Parsers for :mod:`string_parsers`"""

import logging
import pprint
from . import exceptions
from . import extractors
from . import mappers

mylog = logging.getLogger(__name__)


def sensors(sensors, key='sensors', empty_ok=True):
    """Turns a sensors str or list of str into a sensor definition

    Parameters
    ----------
    sensors : str, list of str
        * A str or list of str that describes a sensor(s) and optionally a selector, parameters, filter, and/or options
    key : str, optional
        * Name of key that user should have provided `sensors` as
    empty_ok : bool, optional
        * False: `sensors` is not allowed to be empty, throw :exc:`exceptions.ParserError` if it is empty
        * True: `sensors` is allowed to be empty

    Returns
    -------
    sensor_defs : list of dict
        * list of dict parsed from `sensors`
    """
    if not isinstance(sensors, (list, tuple, basestring)):
        err = "A string or list of strings must be supplied as '{0}'!".format(key)
        raise exceptions.ParserError(err)

    if not sensors:
        if not empty_ok:
            err = "A string or list of strings must be supplied as '{0}'!".format(key)
            raise exceptions.ParserError(err)
        else:
            return []

    if not isinstance(sensors, (list, tuple)):
        sensors = [sensors]

    sensor_defs = []
    for sensor in sensors:
        if not isinstance(sensor, (basestring)):
            raise exceptions.ParserError("{!r} must be a string".format(sensor))
        s, parsed_selector = extractors.selector(sensor)
        s, parsed_params = extractors.parameters(s)
        s, parsed_options = extractors.options(s)
        s, parsed_filter = extractors.filters(s)
        sensor_def = {}
        sensor_def[parsed_selector] = s
        sensor_def['params'] = parsed_params
        sensor_def['options'] = parsed_options
        sensor_def['filter'] = parsed_filter

        dbg = 'parsed string {!r} into definition:\n{}'.format
        mylog.debug(dbg(sensor, pprint.pformat(sensor_def)))

        sensor_defs.append(sensor_def)

    return sensor_defs


def options(options):
    """Turns a options str or list of str into a question option definition

    Parameters
    ----------
    options : str, list of str
        * A str or list of str that describes question options

    Returns
    -------
    option_defs : list of dict
        * list of dict parsed from `options`
    """
    if not options:
        return {}

    if not isinstance(options, (basestring)):
        options = [options]

    dest = ['filter', 'group']
    option_defs = mappers.options(options, dest)
    dbg = 'parsed string {!r} into option definition:\n{}'.format
    dbg = dbg(options, pprint.pformat(option_defs))
    mylog.debug(dbg)
    return option_defs


def filters(filters):
    """Turns a filters str or list of str into a question filter definition

    Parameters
    ----------
    filters : str, list of str
        * A str or list of str that describes a sensor for a question filter(s) and optionally a selector and/or filter

    Returns
    -------
    filter_defs : list of dict
        * list of dict parsed from `filters`
    """
    if not filters:
        return []

    if not isinstance(filters, (list, tuple)):
        filters = [filters]

    filter_defs = []
    for f in filters:
        s, parsed_selector = extractors.selector(f)
        s, parsed_filter = extractors.filters(s)
        if not parsed_filter:
            err = "Filter {!r} is not a valid filter!".format
            raise exceptions.ParserError(err(f))

        f_def = {}
        f_def[parsed_selector] = s
        f_def['filter'] = parsed_filter

        dbg = 'parsed string {!r} into filter definition:\n{}'.format
        dbg = dbg(f, pprint.pformat(f_def))
        mylog.debug(dbg)

        filter_defs.append(f_def)

    return filter_defs


def package(package):
    """Turns a package str into a package definition

    Parameters
    ----------
    package : str
        * A str that describes a package and optionally a selector and/or parameters

    Returns
    -------
    package_def : dict
        * dict parsed from `sensors`
    """
    if not isinstance(package, (basestring)) or not package:
        err = "{!r} must be a string supplied as 'package'".format
        raise exceptions.ParserError(err(package))
    p, parsed_selector = extractors.selector(package)
    p, parsed_params = extractors.params(p)
    package_def = {}
    package_def[parsed_selector] = p
    package_def['params'] = parsed_params

    dbg = 'parsed string {!r} into definition:\n {}'.format
    mylog.debug(dbg(package, pprint.pformat(package_def)))

    return package_def
