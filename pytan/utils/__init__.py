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
logging.getLogger().addHandler(NullHandler())

from . import constants
from . import exceptions
from . import crypt
from . import helpers
from . import log
from . import math
from . import network
from . import pretty
from . import tanium_obj
from . import time
from . import parsers
from .external import taniumpy
from .external import xmltodict
from .external import requests
from .xml_clean import xml_cleaner

__all__ = [
    'constants',
    'exceptions',
    'crypt',
    'helpers',
    'log',
    'math',
    'network',
    'pretty',
    'tanium_obj',
    'time',
    'xml_cleaner',
    'parsers',
    'taniumpy',
    'xmltodict',
    'requests',
]
