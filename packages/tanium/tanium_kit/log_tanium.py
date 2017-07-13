"""Die.

Notes
-----
The tanium log will show LEVEL at the appropriate tanium log levels according to
TaniumHandler.LOG_TAN_LVL_MAP.

When running from Taniums embedded python interpreter, stdout is not captured!
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys

LOG_TAN_FORMAT = "[%(name)s] %(levelname)-8s %(message)s"
"""Format for the tanium log output."""

LOG_TAN_LEVEL = "DEBUG"
"""Set the tanium handler to DEBUG, let the logger control the actual level."""

LOG_TAN_HANDLER_NAME = "tanium_handler"
"""Name to label tanium handler with."""


class TaniumStream(object):
    """Fake stream object for TaniumHandler."""

    pass


class TaniumHandler(logging.Handler):
    """Python logging handler for tanium logging that can be added to a python logger."""

    LOG_TAN_LVL_MAP = {
        logging.DEBUG: 40,
        # show python logging level DEBUG (10) in tanium log at level 40
        logging.INFO: 20,
        # show python logging level INFO (20) in tanium log at level 20
        logging.WARNING: 0,
        # show python logging level WARNING (30) in tanium log at level 0
        logging.ERROR: 0,
        # show python logging level ERROR (40) in tanium log at level 0
        logging.CRITICAL: 0,
        # show python logging level CRITICAL (50) in tanium log at level 0
    }
    """Map of python logging levels to tanium logging levels."""

    LOG_TAN_DEFAULT_LVL = 0
    """Show python logging levels that do not match in LOG_TAN_LVL_MAP in tanium log at level 0."""

    def __init__(self, **kwargs):
        """Python logging handler for tanium logging that can be added to a python logger.

        Parameters
        ----------
        tanium_module : object
            * The tanium module as exposed from within the internal python environment of the Tanium Platform
        levels : dict, optional
            * a dictionary that maps python logging levels to tanium log levels
        """
        self.stream = TaniumStream()
        self.stream.name = "<Tanium Platform Logging System>"

        log_tan_lvl_map = kwargs.get("log_tan_lvl_map", self.LOG_TAN_LVL_MAP)
        self.LOG_TAN_LVL_MAP.update(log_tan_lvl_map)
        self.LOG_TAN_DEFAULT_LVL = kwargs.get("log_tan_default", self.LOG_TAN_DEFAULT_LVL)
        logging.Handler.__init__(self)

    def send_it(self, lvl, msg):
        """Die."""
        if "_tanium" in sys.modules:
            sys.modules["_tanium"].log({"level": lvl, "message": msg})

    def update_level_map(self, log_tan_lvl_map):
        """Utility to update `self.LOG_TAN_LVL_MAP`."""
        self.LOG_TAN_LVL_MAP.update(log_tan_lvl_map)

    def emit(self, record):
        """Used by a python logging handler to log messages."""
        try:
            msg = self.format(record)

            done = False
            for loglevel, taniumlvl in sorted(self.LOG_TAN_LVL_MAP.items()):
                if record.levelno <= loglevel:
                    # currently, tanium module does not support unicode strings
                    # str() in py2.x will convert a string object from unicode to str
                    self.send_it(taniumlvl, str(msg))
                    done = True
                    break

            if not done:
                self.send_it(self.LOG_TAN_DEFAULT_LVL, str(msg))
        except:
            self.handleError(record)


def make_handler_tan(logger, **kwargs):
    """Create and add a tanium output handler object to a logger.

    Parameters
    ----------
    logger : python logging logger object
        * python logging logger object
    log_tan_format : str, optional
        * python logging formatter str to use for logging
        * default : :data:`Logging.LOG_TAN_FORMAT`
    log_tan_level : str, optional
        * python logging level to use for logging
        * default : :data:`Logging.LOG_TAN_LEVEL`
    log_tan_handler_name : str, optional
        * name to use for identifying handler
        * default : :data:`Logging.LOG_TAN_HANDLER_NAME`
    log_tan_lvl_map : dict, optional
        * passthru to :class:`TaniumHandler`
    log_tan_default_lvl : int, optional
        * passthru to :class:`TaniumHandler`

    Returns
    -------
    handler : python logging handler object
        * handler created by this method
    """
    log_format = kwargs.get("log_tan_format", LOG_TAN_FORMAT)
    log_level = kwargs.get("log_tan_level", LOG_TAN_LEVEL)
    log_handler_name = kwargs.get("log_tan_handler_name", LOG_TAN_HANDLER_NAME)

    try:
        handler = [h for h in list(logger.handlers) if h.name == log_handler_name][0]
    except:
        handler = None

    if not handler:
        handler = TaniumHandler(**kwargs)
        handler.setFormatter(logging.Formatter(log_format))
        handler.setLevel(getattr(logging, log_level.upper()))
        handler.name = log_handler_name
        logger.addHandler(handler)
    return handler
