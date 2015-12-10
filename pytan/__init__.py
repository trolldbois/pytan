# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''A python package that makes using the Tanium Server SOAP API easy.'''

from .version import __author__  # noqa
from .version import __version__  # noqa
from .version import __email__  # noqa
from .version import __description__  # noqa
from .version import __status__  # noqa
from .version import __license__  # noqa
from .version import __url__  # noqa
from .version import __title__  # noqa

from . import utils
from .pollers import QuestionPoller
from .pollers import ActionPoller
from .pollers import SSEPoller
from .handler import Handler
from .session import Session

__all__ = [
    utils,
    Handler,
    Session,
    QuestionPoller,
    ActionPoller,
    SSEPoller,
]
