#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Logging module for :mod:`pytan`."""

import re
import os
import logging
import time
from . import constants

mylog = logging.getLogger(__name__)
mylog.setLevel(logging.WARN)


def setup(**kwargs):
    """Setup logging for PyTan."""
    loglevel = int(kwargs.get('loglevel', 0))

    mylog_debug = any([
        loglevel >= constants.OVERRIDE_PYTAN_LEVEL,
        loglevel >= constants.LOG_LEVEL_MAPS[mylog.name] + 10,
    ])

    if mylog_debug:
        mylog.setLevel(logging.DEBUG)

    install_console(**kwargs)

    argmap = ['loggmt']
    args = get_args("", kwargs, argmap)

    if args['loggmt']:
        logging.Formatter.converter = time.gmtime
        m = "Using GMT time zone for logging"
    else:
        logging.Formatter.converter = time.localtime
        m = "Using local time zone for logging"

    mylog.debug(m.format())

    if loglevel >= constants.OVERRIDE_PYTAN_LEVEL:
        m = 'loglevel is over {}, setting all loggers to DEBUG'
        mylog.debug(m.format(constants.OVERRIDE_PYTAN_LEVEL))
        set_all_levels()
    else:
        set_levels(**kwargs)

    install_file(**kwargs)


def install_file(**kwargs):
    """Utility to add a file log to python's logging module."""
    argmap = ['enable', 'formatter', 'output', 'handler', 'level']
    create_args = get_args("logfile_", kwargs, argmap)
    create_args['output'] = os.path.expanduser(create_args['output'])
    create_args['name'] = os.path.basename(create_args['output'])

    if not create_args['enable']:
        mylog.debug("logfile_enable = False, disabling file log")
        uninstall_file(**create_args)
        return

    # mylog.debug("install_file create_handler args: {}".format(create_args))
    loghandler = create_handler(**create_args)
    add_handler(loghandler=loghandler, **kwargs)
    mylog.debug("added file log name: '{name}', output: '{output}'".format(**create_args))


def install_console(**kwargs):
    """Utility to add a console log to python's logging module."""
    argmap = ['enable', 'formatter', 'output', 'handler', 'level', 'name']
    create_args = get_args("logconsole_", kwargs, argmap)

    if not create_args['enable']:
        mylog.debug("logconsole_enable = False, disabling console log")
        uninstall_console(**create_args)
        return

    # mylog.debug("install_console create_handler args: {}".format(create_args))
    loghandler = create_handler(**create_args)
    add_handler(loghandler=loghandler, **kwargs)
    mylog.debug("added console log name: '{name}', output: '{output}'".format(**create_args))


def get_args(prefix, kwargs, argmap):
    """Get arguments from kwargs using argmap."""
    args = {}
    for k in argmap:
        nk = "{}{}".format(prefix, k)
        args[k] = constants.DEFAULTS[nk]
        if nk in kwargs:
            args[k] = kwargs.get(nk)
    return args


def uninstall_file(**kwargs):
    """Utility to remove a log file from python's logging module."""
    argmap = ["output"]
    remove_args = get_args("logfile_", kwargs, argmap)
    loghandler_name = os.path.basename(remove_args['output'])
    remove_handler(loghandler_name=loghandler_name)


def uninstall_console(**kwargs):
    """Utility to remove a console log from python's logging module."""
    argmap = ["name"]
    remove_args = get_args("logconsole_", kwargs, argmap)
    remove_handler(loghandler_name=remove_args['output'])


def create_handler(handler, output, name, level, formatter, **kwargs):
    """Utility to create a logging handler."""
    loghandler = getattr(logging, handler)(output)
    loghandler.set_name(name)
    loghandler.setLevel(getattr(logging, level))
    loghandler.setFormatter(logging.Formatter(formatter))
    return loghandler


def add_handler(loghandler, **kwargs):
    """Utility to add a logging handler to all loggers."""
    loggers = get_loggers(**kwargs)
    for pytanlog in sorted(constants.LOG_LEVEL_MAPS):
        if loghandler.name not in [h.name for h in loggers[pytanlog].handlers]:
            # mylog.debug("add_handler: {0.name} to logger {1}".format(loghandler, pytanlog))
            loggers[pytanlog].addHandler(loghandler)


def remove_handler(**kwargs):
    """Utility to remove a logging handler from all loggers."""
    loggers = get_loggers(**kwargs)
    loghandler_name = kwargs.get('loghandler_name', None)
    for pytanlog in sorted(constants.LOG_LEVEL_MAPS):
        if pytanlog not in loggers:
            m = "pytan logger {} does not exist in logging system!!"
            raise Exception(m.format(pytanlog))

        for handler in loggers[pytanlog].handlers:
            if loghandler_name is None:
                # m = "remove_handler: {} from {} due to None"
                # mylog.debug(m.format(handler.name, pytanlog))
                loggers[pytanlog].removeHandler(handler)
            elif handler.name == loghandler_name:
                # m = "remove_handler: {} from {} due to match"
                # mylog.debug(m.format(handler.name, pytanlog))
                loggers[pytanlog].removeHandler(handler)


def get_loggers(**kwargs):
    """Get all loggers currently known to pythons logging system`."""
    logger_dict = logging.Logger.manager.loggerDict
    all_loggers = {k: v for k, v in logger_dict.iteritems() if isinstance(v, logging.Logger)}
    all_loggers['root'] = logging.getLogger()
    return all_loggers


def set_levels(**kwargs):
    """Enable loggers based on loglevel and :data:`constants.LOG_LEVEL_MAPS`.

    Parameters
    ----------
    loglevel : int, optional
        * loglevel to match against each item in :data:`constants.LOG_LEVEL_MAPS` -
          each item that is greater than or equal to loglevel will have the
          according loggers set to their respective levels identified there-in.
    """
    loglevel = int(kwargs.get('loglevel', 0))
    loggers = get_loggers()
    loggers_done = []
    for pytanlog, infolvl in sorted(constants.LOG_LEVEL_MAPS.iteritems()):
        if pytanlog not in loggers:
            m = "pytan logger {} does not exist in logging system!!"
            raise Exception(m.format(pytanlog))

        if pytanlog in loggers_done:
            m = "pytan logger {} already processed!!"
            raise Exception(m.format(pytanlog))

        dbglvl = infolvl + 10
        if infolvl == 0 or loglevel >= dbglvl:
            m = "{} set from {} to {} (DEBUG)"
            newlvl = logging.DEBUG
        elif loglevel >= infolvl:
            m = "{} set from {} to {} (INFO)"
            newlvl = logging.INFO
        else:
            m = "{} set from {} to {} ({})"
            newlvl = getattr(logging, constants.DEFAULT_LOGGER_LEVEL)

        oldlvl = loggers[pytanlog].level
        loggers[pytanlog].setLevel(newlvl)
        loggers[pytanlog].propagate = False
        loggers_done.append(pytanlog)
        mylog.debug(m.format(pytanlog, oldlvl, newlvl, constants.DEFAULT_LOGGER_LEVEL))

    loggers_not_done = [x for x in loggers if x not in loggers_done]
    if loggers_not_done:
        mylog.debug('non pytan loggers: {}'.format(', '.join(loggers_not_done)))


def set_all_levels(**kwargs):
    """Set all loggers that the logging system knows about to a given logger level."""
    logger_level = kwargs.get('logger_level', 'DEBUG')
    loggers = get_loggers()
    mylog.setLevel(getattr(logging, logger_level))
    for lname, llogger in sorted(loggers.iteritems()):
        # mylog.debug("setting logger '{}' to {}".format(lname, logger_level))
        llogger.setLevel(getattr(logging, logger_level))
        if lname in constants.LOG_LEVEL_MAPS:
            llogger.propagate = False


def print_levels(**kwargs):
    """Utility to print info about each logger."""
    loggers = get_loggers()
    loggers_done = []
    deflvl = constants.DEFAULT_LOGGER_LEVEL

    m = "{} logger {!r} {} and above messages shown at pytan loglevel {} and above"
    t = "pytan"
    for pytanlog, infolvl in sorted(constants.LOG_LEVEL_MAPS.iteritems()):
        loggers_done.append(pytanlog)
        dbglvl = infolvl + 10
        if infolvl == 0:
            print m.format(t, pytanlog, 'DEBUG', 0)
        else:
            print m.format(t, pytanlog, deflvl, 0)
            print m.format(t, pytanlog, 'INFO', infolvl)
            print m.format(t, pytanlog, 'DEBUG', dbglvl)

    loggers_not_done = [x for x in loggers if x not in loggers_done]
    t = "NON-pytan"
    for logger in loggers_not_done:
        print m.format(t, logger, 'DEBUG', constants.OVERRIDE_PYTAN_LEVEL)


def enable_logs(regex, level='DEBUG'):
    """Utility to enable loggers based on regex."""
    regex = re.compile(regex)
    loggers = get_loggers()
    for lname, llogger in sorted(loggers.iteritems()):
        if not regex.search(lname):
            continue
        llogger.setLevel(getattr(logging, level))


def disable_logs(regex, level='WARN'):
    """Utility to disable loggers based on regex."""
    regex = re.compile(regex)
    loggers = get_loggers()
    for lname, llogger in sorted(loggers.iteritems()):
        if not regex.search(lname):
            continue
        llogger.setLevel(getattr(logging, level))
