'''A python package that makes using the Tanium Server SOAP API easy.'''

import sys
import logging

try:
    from logging import NullHandler
except ImportError:  # NullHandler not present in Python < 2.7
    from logging import Handler

    class NullHandler(Handler):
        def emit(self, record):
            pass

# Set default logging handler to avoid "No handler found" warnings.
root_logger = logging.getLogger()
if not root_logger.handlers:
    root_logger.addHandler(NullHandler())

pytan_logger = logging.getLogger(__name__)

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
    string_types = str,  # noqa
    integer_types = int,  # noqa
    encoding = "unicode"
    range = range  # noqa
    input = input

    def b(s):  # noqa
        return s.encode("latin-1")

    def u(s):  # noqa
        return s
else:
    text_type = unicode  # noqa
    string_types = basestring,  # noqa
    encoding = "us-ascii"
    integer_types = (int, long)  # noqa
    range = xrange  # noqa
    input = raw_input  # noqa

    def b(s):  # noqa
        return s

    # Workaround for standalone backslash
    def u(s):
        return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")  # noqa


class PytanError(Exception):
    """Base exception thrown for all exceptions in pytan"""
    pass


from pytan import version

__version__ = version.__version__
__codename__ = version.__codename__
__title__ = version.__title__
__url__ = version.__url__
__author__ = version.__author__
__email__ = version.__email__
__description__ = version.__description__
__license__ = version.__license__
__copyright__ = version.__copyright__
__status__ = version.__status__

from pytan import utils
from pytan import parsers
from pytan import pollers
from pytan import tanium_ng
from pytan import tickle
from pytan import session
from pytan import handler
from pytan import store
from pytan import shellparser
from pytan import handler_args
from pytan import handler_logs
from pytan.handler import Handler

__all__ = [
    'PytanError',
    'version',
    'utils',
    'parsers',
    'pollers',
    'tanium_ng',
    'tickle',
    'session',
    'handler',
    'store',
    'handler_args',
    'handler_logs',
    'shellparser',
    'Handler',
]
