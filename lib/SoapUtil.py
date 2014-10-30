#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Generic Utility Functions"""
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

import sys
import traceback
import socket
import time
import getpass
import logging
# from datetime import datetime

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

# debug log format
DEBUG_FORMAT = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(name)s %(message)s'
)

# info log format
INFO_FORMAT = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s %(message)s'
)

LOG_LEVEL_MAPS = [
    (0, {
        'SoapWrap': 'INFO',
        'SoapWrap.auth': 'WARN',
        'SoapWrap.transform': 'WARN',
        'SoapWrap.result_infos': 'WARN',
        'SoapWrap.xmlcreate': 'WARN',
        'SoapWrap.xmlparse': 'WARN',
        'SoapWrap.http': 'WARN',
        'requests': 'WARN',
        'requests.packages': 'WARN',
        'requests.packages.urllib3': 'WARN',
        'requests.packages.urllib3.connectionpool': 'WARN',
        'requests.packages.urllib3.poolmanager': 'WARN',
        'requests.packages.urllib3.util': 'WARN',
        'requests.packages.urllib3.util.retry': 'WARN',
    }),
    (1, {
        'SoapWrap': 'DEBUG',
    }),
    (2, {
        'SoapWrap.auth': 'DEBUG',
        'SoapWrap.result_infos': 'DEBUG',
        'SoapWrap.transform': 'DEBUG',
    }),
    (3, {
        'SoapWrap.xmlcreate': 'DEBUG',
    }),
    (4, {
        'SoapWrap.xmlparse': 'DEBUG',
    }),
    (5, {
        'SoapWrap.http': 'DEBUG',
    }),
    (10, {
        'requests': 'DEBUG',
        'requests.packages': 'DEBUG',
        'requests.packages.urllib3': 'DEBUG',
        'requests.packages.urllib3.connectionpool': 'DEBUG',
        'requests.packages.urllib3.poolmanager': 'DEBUG',
        'requests.packages.urllib3.util': 'DEBUG',
        'requests.packages.urllib3.util.retry': 'DEBUG',
    }),

]


def version_check(reqver):
    """for scripts using this API to validate the version of the API

    :param reqver: string containing version number to check against
    """
    LOG_TPL = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        logging.error(LOG_TPL(s, __file__, __version__, reqver))
        sys.exit(100)
    s = "Script and API Version match"
    logging.debug(LOG_TPL(s, __file__, __version__, reqver))


def utf_clean(v, e='utf-8'):
    if is_str(v):
        v = v.replace(u"\xa0", u" ")
        v = v.encode(e)
    return v


def is_list(l):
    return type(l) in [list, tuple]


def is_str(l):
    return type(l) in [unicode, str]


def is_dict(l):
    return type(l) in [dict]


def is_num(l):
    return type(l) in [float, int]


def get_caller_method():
    stack = traceback.extract_stack()
    # for x, y in enumerate(stack):
        # print x, y
    caller_stack = stack[-3]
    caller_method = caller_stack[2]
    return caller_method


def prompt_username():
    """for scripts using this API to prompt the user for a username

    :return: :class:`str`
    """
    print('Username: '),
    username = sys.stdin.readline()
    return username.strip()


def prompt_password():
    """for scripts using this API to prompt the user for a password

    :return: :class:`str`
    """
    password = getpass.getpass(('Password: '))
    return password.strip()


def get_now():
    """return current time in human friendly format

    :return: :class:`str`
    """
    return human_time(time.localtime())


def fn_gen(ext, pname):
    fn = "{}_{}.{}".format(get_now(), pname, ext)
    return fn


def human_time(t, format='%Y_%m_%d-%H_%M_%S-%Z'):
    """return time in human friendly format

    :param t: either a epoch or struct_time time object
    :param format: strftime format string
    :return: :class:`str`
    """
    if is_num(t):
        t = time.localtime(t)
    return time.strftime(format, t)


# not in use
# def datetime_diff(t=False):
#     """Get the dtdiff of now - time

#     :param t: either a epoch or datatime object
#     :return: :class:`datatime.timedelta`
#     """
#     now = datetime.now()

#     if is_num(t):
#         dtdiff = now - datetime.fromtimestamp(t)
#     elif isinstance(t, datetime):
#         dtdiff = now - t
#     else:
#         dtdiff = now - now

#     # dtdiff = SoapUtil.datetime_diff(timestamp)
#     # minutes_dtdiff = dtdiff.seconds / 60

#     #second_dtdiff = dtdiff.seconds
#     #minute_dtdiff = dtdiff.seconds / 60
#     #hour_dtdiff = minute_dtdiff / 60
#     #day_dtdiff = dtdiff.days
#     return dtdiff


def port_check(address, port, timeout=5):
    """Check if address:port can be reached within timeout

    :param address: string of host to connect to
    :param port: string of port to connect to
    :param timeout: int of seconds to wait until connection fails

    :return: :class:`bool`
    """
    try:
        return socket.create_connection((address, port), timeout)
    except:
        return False


class SplitStreamHandler(logging.Handler):
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
                if (is_unicode and getattr(stream, 'encoding', None)):
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


def remove_logging_handler(name):
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
    ch.setFormatter(INFO_FORMAT)
    root_logger = logging.getLogger()
    root_logger.addHandler(ch)
    root_logger.setLevel(logging.DEBUG)


def change_console_format(debug=False):
    root_logger = logging.getLogger()
    root_handlers = root_logger.handlers
    for h in root_handlers:
        if h.name == 'console':
            if debug:
                h.setFormatter(DEBUG_FORMAT)
            else:
                h.setFormatter(INFO_FORMAT)


def set_log_levels(loglevel=0):
    # print loglevel
    for logmap in LOG_LEVEL_MAPS:
        if loglevel >= logmap[0]:
            for lname, llevel in logmap[1].iteritems():
                # print 'setting %s to %s' % (lname, llevel)
                logging.getLogger(lname).setLevel(getattr(logging, llevel))
