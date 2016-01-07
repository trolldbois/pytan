from . import base

EXEC_STR = """
from pytan.utils import *
from pytan.tickle.tools import *
session = handler.SESSION


def shell_help():
    def dirp(m):
        return ', '.join([x for x in sorted(dir(m)) if not x.startswith('_')])

    def linep(d, o):
        print(" ** {}: {}".format(d, dirp(o)))

    print('''
 ************************************************
 PyTan Shell Help:

## Classes and functions available ##
''')
    linep("'pytan' package", pytan)
    print("")
    linep("'pytan.utils' module", pytan.utils)
    print("")
    linep("'pytan.tickle.tools' module", pytan.tickle.tools)
    print("")
    print('## Objects available ##')
    print("")
    print(" ** 'handler' object is the pytan.handler.Handler class instantiated with the parameters passed in via the command line.")
    print(" ** 'handler' object: {}".format(handler))
    linep("'handler' object methods", handler)
    print("")
    print(" ** 'session' object is the pytan.session.Session class instantiated as handler.SESSION")
    print(" ** 'session' object: {}".format(session))
    linep("'session' object methods", session)
    print('''
 ** Type 'shell_help()' to see this again

************************************************
 ''')


shell_help()
"""  # noqa


class Worker(base.Base):
    DESCRIPTION = (
        'Provides an interactive python console with pytan\'s Handler available as handler'
    )
    INTERACTIVE = True

    def get_exec(self):
        return EXEC_STR
