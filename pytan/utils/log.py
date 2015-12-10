#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Logging module for :mod:`pytan`"""

DEBUG_OUTPUT = False

import sys
import logging
import itertools
import time
from . import constants


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


def spew(t):
    """Prints a string based on DEBUG_OUTPUT bool

    Parameters
    ----------
    t : str
        * string to debug print
    """
    if DEBUG_OUTPUT:
        print "DEBUG::{}".format(t)


def set_log_levels(loglevel=0):
    """Enables loggers based on loglevel and :data:`constants.LOG_LEVEL_MAPS`

    Parameters
    ----------
    loglevel : int, optional
        * loglevel to match against each item in :data:`constants.LOG_LEVEL_MAPS` - each item that is greater than or equal to loglevel will have the according loggers set to their respective levels identified there-in.
    """
    if loglevel >= 20:
        set_all_loglevels('DEBUG')
        return

    set_all_loglevels('WARN')

    for logmap in constants.LOG_LEVEL_MAPS:
        if loglevel >= logmap[0]:
            for lname, llevel in logmap[1].iteritems():
                spew('set_log_levels(): setting %s to %s' % (lname, llevel))
                logging.getLogger(lname).setLevel(getattr(logging, llevel))


def print_log_levels():
    """Prints info about each loglevel from :data:`constants.LOG_LEVEL_MAPS`"""
    for logmap in constants.LOG_LEVEL_MAPS:
        print "Logging level: {} - Description: {}".format(logmap[0], logmap[2])
        if logmap[0] == 0:
            for k, v in sorted(get_all_pytan_loggers().iteritems()):
                print "\tLogger {!r} will only show WARNING and above".format(k)
            continue
        for lname, llevel in logmap[1].iteritems():
            print "\tLogger {!r} will show {} and above".format(lname, llevel)


def set_all_loglevels(level='DEBUG'):
    """Sets all loggers that the logging system knows about to a given logger level"""

    for k, v in sorted(get_all_pytan_loggers().iteritems()):
        spew("set_all_loglevels(): setting pytan logger '{}' to {}".format(k, level))
        v.setLevel(getattr(logging, level))
        v.propagate = False


def get_all_pytan_loggers():
    """Gets all loggers currently known to pythons logging system that exist in :data:`constants.LOG_LEVEL_MAPS`

    Creates loggers for any pytan loggers that do not exist yet
    """
    pytan_log_strings = [x[1].keys() for x in constants.LOG_LEVEL_MAPS if x[1].keys()]
    pytan_log_strings = sorted(list(set(list(itertools.chain(*pytan_log_strings)))))

    pytan_loggers = {x: logging.getLogger(x) for x in pytan_log_strings}
    return pytan_loggers


def get_all_loggers():
    """Gets all loggers currently known to pythons logging system`"""
    logger_dict = logging.Logger.manager.loggerDict
    all_loggers = {k: v for k, v in logger_dict.iteritems() if isinstance(v, logging.Logger)}
    all_loggers['root'] = logging.getLogger()
    return all_loggers


def remove_logging_handler(name='all'):
    """Removes a logging handler

    Parameters
    ----------
    name : str
        * name of logging handler to remove. if name == 'all' then all logging handlers are removed
    """
    for k, v in sorted(get_all_pytan_loggers().iteritems()):
        for handler in v.handlers:
            if name == 'all':
                spew("Removing logging handler: {0}/{0.name} due to 'all'".format(handler))
                v.removeHandler(handler)
            elif handler.name == name:
                spew("Removing logging handler: {0}/{0.name} due to match".format(handler))
                v.removeHandler(handler)


def setup_console_logging(gmt_tz=True):
    """Creates a console logging handler using logging.StreamHandler(sys.stdout)"""

    ch_name = 'console'
    remove_logging_handler('console')

    if gmt_tz:
        # change the default time zone to GM time
        logging.Formatter.converter = time.gmtime
    else:
        logging.Formatter.converter = time.localtime

    # add a console handler to all loggers that goes to STDOUT for INFO
    # and below, but STDERR for WARNING and above (old method)
    # ch = SplitStreamHandler()

    ch = logging.StreamHandler(sys.stdout)
    ch.set_name(ch_name)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(constants.INFO_FORMAT))

    for k, v in sorted(get_all_pytan_loggers().iteritems()):
        spew("setup_console_logging(): add handler: {0}/{0.name} to logger {1}".format(ch, k))
        v.addHandler(ch)


def change_console_format(debug=False):
    """Changes the logging format for console handler to :data:`constants.DEBUG_FORMAT` or :data:`constants.INFO_FORMAT`

    Parameters
    ----------
    debug : bool, optional
        * False : set logging format for console handler to :data:`constants.INFO_FORMAT`
        * True :  set logging format for console handler to :data:`constants.DEBUG_FORMAT`
    """
    for k, v in sorted(get_all_pytan_loggers().iteritems()):
        for handler in v.handlers:
            if handler.name == 'console':
                if debug:
                    handler.setFormatter(logging.Formatter(constants.DEBUG_FORMAT))
                else:
                    handler.setFormatter(logging.Formatter(constants.INFO_FORMAT))
