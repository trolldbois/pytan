# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''A python package that makes using the Tanium Server SOAP API easy.'''

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

from .version import __author__  # noqa
from .version import __version__  # noqa
from .version import __email__  # noqa
from .version import __description__  # noqa
from .version import __status__  # noqa
from .version import __license__  # noqa
from .version import __url__  # noqa
from .version import __title__  # noqa

from . import utils
from .utils import exceptions
from .utils import taniumpy
from .handler import Handler
from .session import Session
from .pollers import QuestionPoller
from .pollers import ActionPoller
from .pollers import SSEPoller


__all__ = [
    'utils',
    'exceptions',
    'taniumpy',
    'Handler',
    'Session',
    'QuestionPoller',
    'ActionPoller',
    'SSEPoller',
]
