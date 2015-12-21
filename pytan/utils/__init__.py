# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Utilities package for :mod:`pytan`"""

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

from . import constants
from . import exceptions
from . import helpers
from . import helpstr
from . import log
from . import calc
from . import network
from . import pretty
from . import tanium_obj
from . import parsers
from . import tools
from . import store
from .xml_clean import xml_cleaner

__all__ = [
    'constants',
    'exceptions',
    'helpers',
    'helpstr',
    'log',
    'calc',
    'network',
    'pretty',
    'tanium_obj',
    'xml_cleaner',
    'parsers',
    'tools',
    'store',
]
