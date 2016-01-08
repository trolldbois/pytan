import logging

from pytan import PytanError
from pytan.utils import (
    get_all_logs, set_all_logs, create_log_handler, add_log_handler, remove_log_handler
)

from pytan.constants import HANDLER_DEFAULTS, OVERRIDE_LEVEL, LOGMAP, DEFAULT_LEVEL, DEBUG_BUMP

MYLOG = logging.getLogger(__name__)


def add_override_log(**kwargs):
    myargs = get_myargs(**kwargs)
    if myargs['loglevel'] >= OVERRIDE_LEVEL:
        all_loggers = get_all_logs()
        MYLOG.setLevel(logging.DEBUG)
        handler = create_log_handler(name='override_console')
        [add_log_handler(v, handler) for k, v in all_loggers.items()]
        set_all_logs(propagate=False)
        MYLOG.debug("added override log and set all python loggers to debug")


def del_override_log(**kwargs):
    myargs = get_myargs(**kwargs)
    if myargs['loglevel'] >= OVERRIDE_LEVEL:
        all_loggers = get_all_logs()
        MYLOG.debug("removed override log")
        [remove_log_handler(v, name='override_console') for k, v in all_loggers.items()]


def get_myargs(**kwargs):
    myargs = {}
    myargs.update(HANDLER_DEFAULTS)
    myargs.update(kwargs)
    myargs['loglevel'] = int(myargs.get('loglevel', HANDLER_DEFAULTS['loglevel']))
    return myargs


def setup_log(**kwargs):
    """Setup logging for PyTan."""
    check_logging_setup()
    del_override_log(**kwargs)

    myargs = get_myargs(**kwargs)

    msgs = []
    msgs += config_log_handler(argpre='logconsole', **myargs)
    msgs += config_log_handler(argpre='logfile', **myargs)

    if myargs['loglevel'] >= OVERRIDE_LEVEL:
        msgs += set_all_logs(propagate=False)
        m = 'loglevel is over {}, setting all loggers to DEBUG'
    else:
        msgs += set_log_levels(**kwargs)
        m = 'loglevel is not over {}, set all loggers according to constants'

    m = m.format(OVERRIDE_LEVEL)
    msgs.append(m)

    for i in msgs:
        MYLOG.debug(i)
    return msgs


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

    msgs = []

    all_loggers = get_all_logs()

    modded = []
    not_modded = []

    handler = create_log_handler(**myargs)

    for l in sorted(LOGMAP):
        if myargs['enable']:
            mod = add_log_handler(all_loggers[l], handler)
        else:
            mod = remove_log_handler(all_loggers[l], myargs['name'])

        if mod:
            modded.append(l)
        else:
            not_modded.append(l)

    myargs['action'] = 'added' if myargs['enable'] else 'removed'
    myargs['modded'] = ', '.join(modded)
    myargs['not_modded'] = ', '.join(modded)

    m = "{action} handler: '{name}' for loggers {modded!r}, but not for loggers {not_modded!r}"
    m = m.format(**myargs)
    msgs.append(m)
    return msgs


def set_log_levels(loglevel=0, **kwargs):
    """Enable loggers based on loglevel and :data:`LOGMAP`.

    Parameters
    ----------
    loglevel : int, optional
        * loglevel to match against each item in :data:`LOGMAP` -
          each item that is greater than or equal to loglevel will have the
          according loggers set to their respective levels identified there-in.
    """
    msgs = []
    loggers = get_all_logs()
    loggers_done = []
    for pytanlog, pytanlvl in sorted(LOGMAP.items()):
        if pytanlog in loggers_done:
            err = "pytan logger {} already processed!!"
            err = err.format(pytanlog)
            raise PytanError(err)

        oldlvl = loggers[pytanlog].level
        dbglvl = pytanlvl + DEBUG_BUMP
        if pytanlvl == 0 or loglevel >= dbglvl:
            m = "{} set from {} to {} (DEBUG)"
            newlvl = logging.DEBUG
        elif loglevel >= pytanlvl:
            m = "{} set from {} to {} (INFO)"
            newlvl = logging.INFO
        else:
            m = "{} set from {} to {} ({})"
            newlvl = getattr(logging, DEFAULT_LEVEL)

        loggers[pytanlog].setLevel(newlvl)
        loggers[pytanlog].propagate = False
        loggers_done.append(pytanlog)
        m = m.format(pytanlog, oldlvl, newlvl, DEFAULT_LEVEL)
        msgs.append(m)

    loggers_not_done = [x for x in loggers if x not in loggers_done]
    if loggers_not_done:
        m = 'loggers not set: {}'
        m = m.format(', '.join(loggers_not_done))
        msgs.append(m)
    return msgs


def print_levels(**kwargs):
    """Utility to print info about each logger."""
    loggers = get_all_logs()
    loggers_done = []

    m = "{} logger {!r} {} and above messages shown at pytan loglevel {} and above"
    t = "pytan"
    for pytanlog, pytanlvl in sorted(LOGMAP.items()):
        loggers_done.append(pytanlog)
        dbglvl = pytanlvl + DEBUG_BUMP
        if pytanlvl == 0:
            print(m.format(t, pytanlog, 'DEBUG', 0))
        else:
            print(m.format(t, pytanlog, DEFAULT_LEVEL, 0))
            print(m.format(t, pytanlog, 'INFO', pytanlvl))
            print(m.format(t, pytanlog, 'DEBUG', dbglvl))

    loggers_not_done = [x for x in loggers if x not in loggers_done]
    t = "NON-pytan"
    for logger in loggers_not_done:
        print(m.format(t, logger, 'DEBUG', OVERRIDE_LEVEL))
