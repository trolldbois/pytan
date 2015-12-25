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

from . import utils
from . import parsers
from . import tanium_ng
from . import tools_ng
from . import tickle
from .utils import exceptions
from .handler import Handler
from .session import Session
from .pollers import QuestionPoller
from .pollers import ActionPoller
from .pollers import SSEPoller

__version__ = utils.__version__
__codename__ = utils.__codename__
__title__ = utils.__title__
__url__ = utils.__url__
__author__ = utils.__author__
__email__ = utils.__email__
__description__ = utils.__description__
__license__ = utils.__license__
__copyright__ = utils.__copyright__
__status__ = utils.__status__

__all__ = [
    'utils',
    'exceptions',
    'parsers',
    'Handler',
    'Session',
    'QuestionPoller',
    'ActionPoller',
    'SSEPoller',
    'tanium_ng',
    'tools_ng',
    'tickle',
]
