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

# disable python from creating .pyc files everywhere
import sys
sys.dont_write_bytecode = True

from . import taniumpy  # noqa
# from . import xml_clean  # noqa
# from . import utils  # noqa
# from . import handler  # noqa
# from . import sessions  # noqa
# from . import constants  # noqa
# from . import help_utils  # noqa
# from .handler import Handler  # noqa

# Set default logging handler to avoid "No handler found" warnings.
import logging

if hasattr(logging, 'NullHandler'):
    NullHandler = logging.NullHandler
else:
    # Python 2.6 and older
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
