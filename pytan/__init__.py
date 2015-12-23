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


# Set default logging handler to avoid "No handler found" warnings.
root_logger = logging.getLogger()
if not root_logger.handlers:
    root_logger.addHandler(NullHandler())

from .utils.version import __author__  # noqa
from .utils.version import __version__  # noqa
from .utils.version import __email__  # noqa
from .utils.version import __description__  # noqa
from .utils.version import __status__  # noqa
from .utils.version import __license__  # noqa
from .utils.version import __url__  # noqa
from .utils.version import __title__  # noqa

from . import utils
from . import parsers
from .utils import exceptions
from .handler import Handler
from .session import Session
from .pollers import QuestionPoller
from .pollers import ActionPoller
from .pollers import SSEPoller

__all__ = [
    'utils',
    'exceptions',
    'parsers',
    'Handler',
    'Session',
    'QuestionPoller',
    'ActionPoller',
    'SSEPoller',
]
