import logging

from pytan import PytanError
from pytan.utils import (
    get_all_logs, set_all_logs, create_log_handler, add_log_handler, remove_log_handler
)

from pytan.constants import HANDLER_DEFAULTS, OVERRIDE_LEVEL, LOGMAP, LOGGER_LEVELS

MYLOG = logging.getLogger(__name__)


def get_myargs(**kwargs):
    myargs = {}
    myargs.update(HANDLER_DEFAULTS)
    myargs.update(kwargs)
    myargs['loglevel'] = int(myargs.get('loglevel', HANDLER_DEFAULTS['loglevel']))
    return myargs


def setup_log(**kwargs):
    """Setup logging for PyTan."""
    check_logging_setup()
    myargs = get_myargs(**kwargs)

    config_log_handler(argpre='logconsole', **myargs)
    config_log_handler(argpre='logfile', **myargs)

    if myargs['loglevel'] >= OVERRIDE_LEVEL:
        set_all_logs(propagate=False)
        m = 'loglevel is over {}, setting all loggers to DEBUG'
    else:
        set_log_levels(**kwargs)
        m = 'loglevel is not over {}, set all loggers according to LOGMAP in pytan.constants'

    m = m.format(OVERRIDE_LEVEL)
    MYLOG.info(m)


def check_logging_setup():
    all_loggers = get_all_logs()

    errs = []
    for pytanlog in sorted(LOGMAP):

        if pytanlog not in all_loggers:
            err = "pytan logger {!r} does not exist in logging system!!"
            err = err.format(pytanlog)
            errs.append(err)

    for name, logger in sorted(all_loggers.items()):
        if name.startswith('pytan') and name not in LOGMAP:
            err = "pytan logger {!r} is not defined in constants!"
            err = err.format(name)
            errs.append(err)

    if errs:
        err = '\n'.join(errs)
        MYLOG.critical(err)
        raise PytanError(err)


def config_log_handler(argpre, **kwargs):
    args = ['enable', 'formatter', 'output', 'handler', 'level', 'name']

    myargs = {}
    myargs.update(kwargs)
    myargs = {k: kwargs.get(argpre + '_' + k) for k in args}

    all_loggers = get_all_logs()
    log_handler = create_log_handler(**myargs)

    for l in sorted(LOGMAP):
        if myargs['enable']:
            remove_log_handler(all_loggers[l], myargs['name'])
            add_log_handler(all_loggers[l], log_handler)
        else:
            remove_log_handler(all_loggers[l], myargs['name'])

    m = "logging handler: '{name}' enabled: {enable}"
    m = m.format(**myargs)
    MYLOG.info(m)


def get_new_level(loglevel, pytan_levels):
    result = 'NOTSET'
    for pytan_lvl, logger_lvl in sorted(pytan_levels.items()):
        if not loglevel >= pytan_lvl:
            continue
        result = logger_lvl
    return result


def set_log_levels(loglevel=0, **kwargs):
    """Enable loggers based on loglevel and :data:`LOGMAP`.

    Parameters
    ----------
    loglevel : int, optional
        * loglevel to match against each item in :data:`LOGMAP` -
          each item that is greater than or equal to loglevel will have the
          according loggers set to their respective levels identified there-in.
    """
    loggers = get_all_logs()
    loggers_done = []

    for pytan_logger, pytan_levels in sorted(LOGMAP.items()):
        if pytan_logger in loggers_done:
            err = "pytan logger {} already processed!!"
            err = err.format(pytan_logger)
            raise PytanError(err)

        oldlvl_int = loggers[pytan_logger].level
        oldlvl_txt = logging.getLevelName(oldlvl_int)

        newlvl_txt = get_new_level(loglevel, pytan_levels)
        newlvl_int = getattr(logging, newlvl_txt)

        if oldlvl_int != newlvl_int:
            loggers[pytan_logger].setLevel(newlvl_int)
            loggers[pytan_logger].propagate = False
            loggers_done.append(pytan_logger)
            m = "pytan loglevel=={}, set logger {} from {!r} to {!r}"
            m = m.format(loglevel, pytan_logger, oldlvl_txt, newlvl_txt)
            MYLOG.debug(m)

    loggers_not_done = [x for x in loggers if x not in loggers_done]
    if loggers_not_done:
        m = 'No actions performed against loggers: {}'
        m = m.format(', '.join(loggers_not_done))
        MYLOG.debug(m)


def get_enabled_levels(level):
    result = LOGGER_LEVELS[LOGGER_LEVELS.index(level):]
    return result


def print_pytan_loglevels(**kwargs):
    """Utility to print info about each logger."""
    loggers = get_all_logs()
    m = "{} logger {!r} at pytan loglevel {} and up will show levels: {}"
    for logger_name, logger_obj in sorted(loggers.items()):
        if logger_name in LOGMAP:
            for pytan_lvl, logger_lvl in sorted(LOGMAP[logger_name].items()):
                levels = ', '.join(get_enabled_levels(logger_lvl))
                print(m.format("pytan", logger_name, pytan_lvl, levels))
        else:
            levels = ', '.join(get_enabled_levels('DEBUG'))
            print(m.format("non-pytan", logger_name, OVERRIDE_LEVEL, levels))
