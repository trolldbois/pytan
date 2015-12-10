# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Calculations module for for :mod:`pytan`"""

import time
import datetime
import logging
from . import constants

mylog = logging.getLogger(__name__)


def get_percent(base, amount, text=None, textformat="{0:.2f}%"):
    """Utility method for getting percentage of base out of amount

    Parameters
    ----------
    base: int, float
    amount: int, float
    text: bool

    Returns
    -------
    percent : the percentage of base out of amount
    """
    if 0 in [base, amount]:
        percent = float(0)
    else:
        percent = (100 * (float(base) / float(amount)))

    if text:
        percent = textformat.format(percent)
    return percent


def get_base(percent, amount):
    """Utility method for getting base for percentage of amount

    Parameters
    ----------
    percent: int, float
    amount: int, float

    Returns
    -------
    base : the base from percentage of amount
    """
    base = int((percent * amount) / 100.0)
    return base


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
    if isinstance(t, (int, float)):
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


def calculate_question_start_time(q):
    """Caclulates the start time of a question by doing q.expiration - q.expire_seconds

    Parameters
    ----------
    q : :class:`taniumpy.object_types.question.Question`
        * Question object to calculate start time for

    Returns
    -------
    tuple : str, datetime
        * a tuple containing the start time first in str format for Tanium Server API, second in datetime object format
    """
    expire_dt = timestr_to_datetime(q.expiration)
    expire_seconds_delta = datetime.timedelta(seconds=q.expire_seconds)
    start_time_dt = expire_dt - expire_seconds_delta
    start_time = datetime_to_timestr(start_time_dt)
    return start_time, start_time_dt


def eval_timing(c):
    """Yet another method to time things -- c will be evaluated and timing information will be printed out
    """
    t_start = datetime.now()
    r = eval(c)
    t_end = datetime.now()
    t_elapsed = t_end - t_start

    m = "Timing info for {} -- START: {}, END: {}, ELAPSED: {}, RESPONSE LEN: {}".format
    mylog.warn(m(c, t_start, t_end, t_elapsed, len(r)))
    return (c, r, t_start, t_end, t_elapsed)


def func_timing(f):
    """Decorator to add timing information around a function """
    def wrap(*args, **kwargs):
        time1 = datetime.datetime.utcnow()
        ret = f(*args, **kwargs)
        time2 = datetime.datetime.utcnow()
        elapsed = time2 - time1
        m = '{}() TIMING start: {}, end: {}, elapsed: {}'.format
        mylog.debug(m(f.func_name, time1, time2, elapsed))
        return ret
    return wrap
