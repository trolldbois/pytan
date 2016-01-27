import logging

from pytan import PytanError

MYLOG = logging.getLogger(__name__)


class ObjectBuildError(PytanError):
    pass


def log_result(caller, result, caller_locals):
    m = "{}() result:: {}".format(caller, result)
    MYLOG.debug(m)
