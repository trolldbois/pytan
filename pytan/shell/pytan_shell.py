from . import base

EXEC_STR = """
from pytan.utils import *
from pytan.tickle.tools import *
from pytan.parsers.tokens import *
from pytan.parsers.specs import *
from pytan.parsers.coerce import *

session = handler.SESSION


def shell_help():
    def dirp(m):
        return ', '.join([x for x in sorted(dir(m)) if not x.startswith('_')])

    def linep(d, o):
        print(" ** {}: {}".format(d, dirp(o)))

    print('''
************************************************
PyTan Shell Help

## Classes and functions available ##
''')
    linep("'pytan' package", pytan)
    print("")

    mods = [
        "pytan.utils",
        "pytan.tickle.tools",
        "pytan.parsers.tokens",
        "pytan.parsers.specs",
        "pytan.parsers.coerce",
    ]

    for m in mods:
        imp_str = "from {} import *".format(m)
        m_str = "'{}' module".format(m)
        exec(imp_str) in globals(), locals()
        linep(m_str, eval(m))
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

print("\\n ** Type 'shell_help()' to see methods and functions available")
"""  # noqa


class Worker(base.Base):
    DESCRIPTION = (
        'Provides an interactive python console with pytan\'s Handler '
        'available as handler'
    )
    INTERACTIVE = True

    def get_exec(self):
        return EXEC_STR
