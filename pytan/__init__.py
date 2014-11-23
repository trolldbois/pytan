# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
__title__ = 'pytan'
__version__ = '0.7.0'
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__license__ = 'TBD'
__copyright__ = 'Copyright 2014 Tanium'

import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

from .handler import Handler
from . import utils
from . import constants
from . import api


# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
