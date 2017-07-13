"""A python package that makes using the Tanium Server SOAP API easy."""

import logging
import os
import sys

THIS_FILE = __file__
"""This file, ala ``/github/pytan/lib/pytan/__init__.py``"""

THIS_PATH = os.path.abspath(os.path.dirname(THIS_FILE))
"""The absolute path from this file, ala ``/github/pytan/lib/pytan``"""

TOOL_PATH = os.path.dirname(THIS_PATH)
"""The path of this tool, ala ``/github/pytan/lib/``"""

if TOOL_PATH not in sys.path:
    sys.path.insert(0, TOOL_PATH)
    # insert ``/github/pytan/lib/`` at front of sys.path / PYTHONPATH

try:
    import taniumpy
    from . import exceptions
    from . import constants
    from . import version
    from . import utils
    from . import pollers
    from . import sessions
    from . import help
    from . import handler
except:
    raise

Handler = handler.Handler

__author__ = version.__author__
__codename__ = version.__codename__
__copyright__ = version.__copyright__
__description__ = version.__description__
__email__ = version.__email__
__license__ = version.__license__
__status__ = version.__status__
__title__ = version.__title__
__url__ = version.__url__
__version__ = version.__version__

__all__ = [
    "taniumpy",
    "exceptions",
    "constants",
    "utils",
    "pollers",
    "sessions",
    "help",
    "handler",
    "Handler",
]

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
