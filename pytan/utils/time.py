#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Time and date module for :mod:`pytan`"""

import time
import datetime
from .. import constants
from . import types


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
        * either a unix epoch or struct_time object to convert to string
    tformat : str, optional
        * format of string to convert time to

    Returns
    -------
    str :
        * `t` converted to str
    """
    if types.is_num(t):
        t = time.localtime(t)
    return time.strftime(tformat, t)


def seconds_from_now(secs=0, tz='utc'):
    """Get time in Tanium SOAP API format `secs` from now

    Parameters
    ----------
    secs : int
        * seconds from now to get time str
    tz : str, optional
        * time zone to return string in, default is 'utc' - supplying anything else will supply local time

    Returns
    -------
    str :
        * time `secs` from now in Tanium SOAP API format
    """
    if secs is None:
        secs = 0

    if tz == 'utc':
        now = datetime.datetime.utcnow()
    else:
        now = datetime.datetime.now()
    from_now = now + datetime.timedelta(seconds=secs)
    # now.strftime('%Y-%m-%dT%H:%M:%S')
    return from_now.strftime('%Y-%m-%dT%H:%M:%S')


def timestr_to_datetime(timestr):
    """Get a datetime.datetime object for `timestr`

    Parameters
    ----------
    timestr : str
        * date & time in taniums format

    Returns
    -------
    datetime.datetime
        * the datetime object for the timestr
    """
    return datetime.datetime.strptime(timestr, constants.TIME_FORMAT)


def datetime_to_timestr(dt):
    """Get a timestr for `dt`

    Parameters
    ----------
    dt : datetime.datetime
        * datetime object

    Returns
    -------
    timestr: str
        * the timestr for `dt` in taniums format
    """
    return dt.strftime(constants.TIME_FORMAT)
