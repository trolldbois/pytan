from . import base

EXEC_STR = """
from pytan.utils import *
from pytan.tickle.tools import *
session = handler.SESSION


def dir_print(m):
    return ', '.join([x for x in sorted(dir(m)) if not x.startswith('_')])


def shell_help():
    print("\\n ** 'handler' == pytan.handler.Handler(): {}".format(dir_print(handler)))
    print("\\n ** 'session' == handler.SESSION(): {}".format(dir_print(session)))
    print("\\n ** pytan.utils.*: {}".format(dir_print(pytan.utils)))
    print("\\n ** pytan.tickle.tools.*: {}".format(dir_print(pytan.tickle.tools)))


shell_help()
"""


class Worker(base.Base):
    DESCRIPTION = (
        'Provides an interactive python console with pytan\'s Handler available as handler'
    )
    INTERACTIVE = True

    def get_exec(self):
        return EXEC_STR
