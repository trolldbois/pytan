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
        result = float(0)
    else:
        result = (100 * (float(base) / float(amount)))

    if text:
        result = textformat.format(result)
    return result


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
    result = int((percent * amount) / 100.0)
    return result


def get_now_dt(gmt=True):
    """pass."""
    if gmt:
        result = datetime.datetime.utcnow()
    else:
        result = datetime.datetime.now()
    return result


def get_now(gmt=True):
    """Get current time in human friendly format """
    now = get_now_dt(gmt)
    result = human_time(now)
    return result


def human_time(dt, dtformat='D%Y-%m-%dT%H-%M-%S', tz=True):
    """Get time in human friendly format"""
    result = dt.strftime(dtformat)
    if tz:
        tz_pre = '-' if time.altzone > 0 else '+'
        add_tz = 'Z{}{:0>2}{:0>2}'
        add_tz = add_tz.format(tz_pre, abs(time.altzone) // 3600, abs(time.altzone // 60) % 60)
        result = result + add_tz
    return result


def seconds_from_now(secs=0, gmt=True, tformat='%Y-%m-%dT%H:%M:%S'):
    """Get time in Tanium SOAP API format `secs` from now

    Parameters
    ----------
    secs : int
        * seconds from now to get time str
    tz : str, optional
        * time zone to return string in, default is 'utc' - supplying anything else will supply
        local time

    Returns
    -------
    str :
        * time `secs` from now in Tanium SOAP API format
    """
    if secs is None:
        secs = 0

    now = get_now_dt(gmt)
    from_now = now + datetime.timedelta(seconds=secs)
    result = from_now.strftime(tformat)
    return result


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
    result = datetime.datetime.strptime(timestr, constants.TIME_FORMAT)
    return result


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
    result = dt.strftime(constants.TIME_FORMAT)
    return result


def question_start_time(q):
    """Caclulates the start time of a question by doing q.expiration - q.expire_seconds

    Parameters
    ----------
    q : :class:`tanium_ng.Question`
        * Question object to calculate start time for

    Returns
    -------
    tuple : str, datetime
        * a tuple containing the start time first in str format for Tanium Server API, second in
        datetime object format
    """
    expire_dt = timestr_to_datetime(q.expiration)
    expire_seconds_delta = datetime.timedelta(seconds=q.expire_seconds)
    start_time_dt = expire_dt - expire_seconds_delta
    start_time = datetime_to_timestr(start_time_dt)
    result = (start_time, start_time_dt)
    return result


def eval_timing(c, thislog=None):
    """Yet another method to time things -- c will be evaluated and timing information will be
    printed out
    """
    if thislog is None:
        thislog = mylog
    t_start = datetime.now()
    r = eval(c)
    t_end = datetime.now()
    t_elapsed = t_end - t_start

    m = "Timing info for {} -- START: {}, END: {}, ELAPSED: {}, RESPONSE LEN: {}".format
    thislog.warn(m(c, t_start, t_end, t_elapsed, len(r)))
    result = (c, r, t_start, t_end, t_elapsed)
    return result


def func_timing(f):
    """Decorator to add timing information around a function """
    def wrap(*args, **kwargs):
        time1 = datetime.datetime.utcnow()
        result = f(*args, **kwargs)
        time2 = datetime.datetime.utcnow()
        elapsed = time2 - time1
        m = '{}() TIMING start: {}, end: {}, elapsed: {}'.format
        mylog.debug(m(f.func_name, time1, time2, elapsed))
        return result
    return wrap
