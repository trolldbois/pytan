"""Helper class for the python logging system.

Examples
--------

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import logging.handlers
import os
import sys
import time

DEFAULT_FORMAT = "%(asctime)s [%(name)s] %(levelname)-8s %(message)s"

LOGGER_NAME = "logger"
"""Used to track name of logger."""

LOGGER_LEVEL = "DEBUG"
"""Level to set logger to."""

LOGGER_PATH = ""
"""Path of python logger to fetch, empty fetches the root logger."""

LOG_GMTIME = True
"""Configure pythons logging interface to use gmtime for standardization."""

LOG_CON_OUTPUT = sys.stdout
"""Send console output to stdout."""

LOG_CON_FORMAT = "[%(name)s] %(levelname)-8s %(message)s"
"""Format for the console output."""

LOG_CON_LEVEL = "DEBUG"
"""Set the console handler to DEBUG, let the logger control the actual level."""

LOG_CON_HANDLER_NAME = "console_handler"
"""Name to label console handler with."""

LOG_FILE_DIR = ""
"""Directory to store log files, if not absolute will be joined with cwd."""

LOG_FILE_NAME = ""
"""File name to use for file log, if not supplied the basename of LOGGER_NAME will be used."""

LOG_FILE_MB = 10
"""MB of file log size before rollover."""

LOG_FILE_COUNT = 5
"""Number of rolled over file logs to keep."""

LOG_FILE_FORMAT = "%(asctime)s [%(name)s] %(levelname)-8s %(message)s"
"""Format for the file log output"""

LOG_FILE_LEVEL = "DEBUG"
"""Set the file handler to DEBUG, let the logger control the actual level."""

LOG_FILE_HANDLER_NAME = "log_file_handler"
"""Name to label tanium handler with."""


def _remove_handler(logger, handler):
    """Wrapper method to close file handles properly and remove handler from a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object to remove `handler` from
    handler : python logging handler object
        * python logging handler object to remove from `logger`
    """
    handler_stream_name = "<unknown>"
    if hasattr(handler, "stream"):
        handler_stream_name = getattr(handler.stream, "name", handler_stream_name)

    m = "Stop logging to '{}' ({}) for logger '{}'".format
    m = m(handler.name, handler_stream_name, logger.name)
    logger.debug(m)

    # TODO: support other file handler types
    if isinstance(handler, logging.handlers.RotatingFileHandler):
        try:
            handler.stream.close()
        except:
            pass
        try:
            handler.close()
        except:
            pass
    logger.removeHandler(handler)


def use_gmtime():
    """Configure pythons logging interface to use gmtime."""
    logging.Formatter.converter = time.gmtime


def use_localtime():
    """Configure pythons logging interface to use localtime."""
    logging.Formatter.converter = time.localtime


def set_level(o, l="DEBUG"):
    """Configure a python logging objects logging level.

    Parameters
    ----------
    o : object
        * python logging object (logger or handler)
    l : str, optional
        * str of level to set on `o`
    """
    o.setLevel(getattr(logging, l.upper()))


def set_format(o, **kwargs):
    """Configure a python logging objects logging format.

    Parameters
    ----------
    o : object
        * python logging logger object
    f : str, optional
        * str of logging format to set on `o`
    """
    f = kwargs.get("f", DEFAULT_FORMAT)
    o.setFormatter(logging.Formatter(f))


def remove_handler(logger, handler_name):
    """Remove a handler by name from a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    handler_name : str
        * str of python logging handler name to remove from `logger`
    """
    for h in list(logger.handlers):
        if h.name == handler_name:
            _remove_handler(logger, h)


def remove_all_handlers(logger):
    """Remove all handlers from a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object to remove all handlers from
    """
    for h in list(logger.handlers):
        _remove_handler(logger, h)


def add_handler(logger, handler):
    """Add a handler object to a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    handler : python logging handler object
        * python logging handler object to add to `logger`
    """
    remove_handler(logger, handler.name)
    logger.addHandler(handler)


def get_handler(logger, handler_name):
    """Retrieve a handler object from a logger by name.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    handler_name : str
        * str of python logging handler name to remove from `logger`

    Returns
    -------
    ret : obj or None
        * obj if handler named handler_name is found, None otherwise
    """
    ret = None
    for h in list(logger.handlers):
        if h.name == handler_name:
            ret = h
            break
    return ret


def make_handler_con(logger, **kwargs):
    """Create and add a console output handler object to a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    log_con_format : str, optional
        * python logging formatter str to use for logging
        * default : :data:`Logging.LOG_CON_FORMAT`
    log_con_level : str, optional
        * python logging level to use for logging
        * default : :data:`Logging.LOG_CON_LEVEL`
    log_con_handler_name : str, optional
        * name to use for identifying handler
        * default : :data:`Logging.LOG_CON_HANDLER_NAME`
    log_con_output : stream, optional
        * stream to use for output (sys.stdout, sys.stderr)
        * default : :data:`Logging.LOG_CON_OUTPUT`

    Returns
    -------
    handler : python logging handler object
        * handler created by this method
    """
    log_format = kwargs.get("log_con_format", LOG_CON_FORMAT)
    log_level = kwargs.get("log_con_level", LOG_CON_LEVEL)
    log_handler_name = kwargs.get("log_con_handler_name", LOG_CON_HANDLER_NAME)
    log_output = kwargs.get("log_con_output", LOG_CON_OUTPUT)

    try:
        handler = [h for h in list(logger.handlers) if h.name == log_handler_name][0]
    except:
        handler = None

    if not handler:
        handler = logging.StreamHandler(stream=log_output)
        handler.setFormatter(logging.Formatter(log_format))
        handler.setLevel(getattr(logging, log_level.upper()))
        handler.name = log_handler_name
        logger.addHandler(handler)
    return handler


def make_handler_file(logger, **kwargs):
    """Create and add a file output handler object to a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    log_file_format : str, optional
        * python logging formatter str to use for logging
        * default : :data:`Logging.LOG_FILE_FORMAT`
    log_file_level : str, optional
        * python logging level to use for logging
        * default : :data:`Logging.LOG_FILE_LEVEL`
    log_file_handler_name : str, optional
        * name to use for identifying handler
        * default : :data:`Logging.LOG_FILE_HANDLER_NAME`
    log_file_name : str, optional
        * filename to use for logging
        * uses basename of logger name if not supplied
        * default : :data:`Logging.LOG_FILE_NAME`
    log_file_dir : str, optional
        * dir to use for logging
        * uses absolute path of cwd if empty/not supplied
        * turns all paths into absolute paths from cwd if relative
        * default : :data:`Logging.LOG_FILE_DIR`
    log_file_count : int, optional
        * number of logs to keep when rolling logs over
        * default : :data:`Logging.LOG_FILE_COUNT`
    log_file_mb : int, optional
        * MB of file log size before rollover
        * default : :data:`Logging.LOG_FILE_MB`

    Returns
    -------
    handler : python logging handler object
        * handler created by this method
    """
    log_format = kwargs.get("log_file_format", LOG_FILE_FORMAT)
    log_level = kwargs.get("log_file_level", LOG_FILE_LEVEL)
    log_handler_name = kwargs.get("log_file_handler_name", LOG_FILE_HANDLER_NAME)
    log_name = kwargs.get("log_file_name", LOG_FILE_NAME)
    log_dir = kwargs.get("log_file_dir", LOG_FILE_DIR)
    log_count = kwargs.get("log_file_count", LOG_FILE_COUNT)
    log_mb = kwargs.get("log_file_mb", LOG_FILE_MB)

    log_max_bytes = log_mb * 1024 * 1024

    handler = get_handler(logger, log_handler_name)
    if not handler:
        if not log_name:
            log_name = logger.name
            log_name = os.path.basename(log_name)
            log_name = os.path.splitext(log_name)[0]
            log_name = "{}.log".format(log_name)

        if not os.path.isabs(log_dir):
            log_dir = os.path.abspath(log_dir)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, log_name)

        handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=log_max_bytes,
            backupCount=log_count,
        )
        handler.setFormatter(logging.Formatter(log_format))
        handler.setLevel(getattr(logging, log_level.upper()))
        handler.name = log_handler_name
        logger.addHandler(handler)
    return handler


def make_logger(**kwargs):
    """Create and add a file output handler object to a logger.

    Parameters
    ----------
    logger_name : str, optional
        * name to set for this logger (shown in logging output by default)
        * default : :data:`Logging.LOGGER_NAME`
    logger_level : str, optional
        * python logging level to use for logging
        * default : :data:`Logging.LOGGER_LEVEL`
    logger_path : str, optional
        * dot notation of logger path to make
        * empty str fetches the root logger
        * default : :data:`Logging.LOGGER_PATH`
    log_gmtime : bool, optional
        * True: use gmtime in logging output
        * False: use localtime in logging output
        * default : :data:`Logging.LOG_GMTIME`
    log_isolate : bool, optional
        * True: only this logger gets log messages sent to this logger
        * False: parents of this logger also get log messages sent to this logger
        * default : True

    Returns
    -------
    logger : python logging logger object
        * logger created by this method
    """
    logger_name = kwargs.get("logger_name", LOGGER_NAME)
    logger_level = kwargs.get("logger_level", LOGGER_LEVEL)
    logger_path = kwargs.get("logger_path", LOGGER_PATH)
    log_gmtime = kwargs.get("log_gmtime", LOG_GMTIME)
    log_isolate = kwargs.get("log_isolate", True)

    logger = logging.getLogger(logger_path)
    logger.setLevel(getattr(logging, logger_level.upper()))
    logger.name = logger_name

    if log_gmtime:
        use_gmtime()
    else:
        use_localtime()

    if log_isolate:
        logger.propagate = False
    else:
        logger.propagate = True
    return logger


def config_verbosity(pre, verbosity):
    """Configure verbose loggers depending on verbosity."""
    # pre = "workflow_"
    # verbosity = 1
    for logger_name, logger in logging.Logger.manager.loggerDict.items():
        if not logger_name.startswith(pre):
            continue
        if not hasattr(logger, "verbosity"):
            continue
        if verbosity >= logger.verbosity:
            logger.propagate = True
        else:
            logger.propagate = False
        if not logger.handlers:
            handler = logging.NullHandler()
            handler.name = "NULL__HANDLER"
            logger.addHandler(handler)


def all_loggers():
    logger_dict = logging.Logger.manager.loggerDict
    ret = {k: v for k, v in logger_dict.items() if isinstance(v, logging.Logger)}
    return ret


def match_loggers(m):
    ret = {k: v for k, v in all_loggers().items() if m in k}
    return ret


def match_loggers_set_level(m, level="DEBUG"):
    for k, v in match_loggers(m).items():
        v.setLevel(getattr(logging, level.upper()))


def match_loggers_add_handler(m, handler):
    for k, v in match_loggers(m).items():
        if handler not in v.handlers:
            v.addHandler(handler)


def shutup_requests(loud=True, match="requests"):
    if loud:
        l = "DEBUG"
    else:
        l = "ERROR"

    match_loggers_set_level(match, l)
