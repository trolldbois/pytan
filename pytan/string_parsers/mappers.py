#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Mappers for :mod:`string_parsers`"""

import logging
from . import exceptions
from . import constants

mylog = logging.getLogger(__name__)


def options(options, dest):
    """Maps a list of options using :func:`option`

    Parameters
    ----------
    options : list of str
        * list of str that should be validated
    dest : list of str
        * list of valid destinations (i.e. `filter` or `group`)

    Returns
    -------
    mapped_options : dict
        * dict of all mapped_options
    """
    mapped_options = {}
    for option in options:
        mapped_option = option(option, dest)
        if mapped_option:
            mapped_options.update(mapped_option)
        else:
            err = "Option {!r} is not a valid option!".format
            raise exceptions.ParserError(err(option))

    return mapped_options


def option(opt, dest):
    """Maps an opt str against :data:`constants.OPTION_MAPS`

    Parameters
    ----------
    opt : str
        * option str that should be validated
    dest : list of str
        * list of valid destinations (i.e. `filter` or `group`)

    Returns
    -------
    opt_attrs : dict
        * dict containing mapped option attributes for SOAP API
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
        mylog.debug(dbg(opt, om))

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
                raise exceptions.ParserError(err)

            opt_name, opt_value = opt_split

            opt_attrs = {om['attr']: opt_value}

    return opt_attrs


def filters(filter_str):
    """Maps a filter str against :data:`constants.FILTER_MAPS`

    Parameters
    ----------
    filter_str : str
        * filter_str str that should be validated

    Returns
    -------
    filter_attrs : dict
        * dict containing mapped filter attributes for SOAP API
    """
    filter_attrs = {}

    filter_split = filter_str.split(':')
    if len(filter_split) != 2:
        err = "Invalid filter in {!r}, missing ':' to seperate filter from value?" .format
        raise exceptions.ParserError(err(filter_str))

    filter_name, filter_value = filter_split
    filter_name = filter_name.strip().lower()

    if not filter_value:
        err = "Invalid filter value in {!r}".format
        raise exceptions.ParserError(err(filter_str))

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
