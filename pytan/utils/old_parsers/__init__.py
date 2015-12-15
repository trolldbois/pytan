# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Parsers package for :mod:`pytan` - responsible for parsing human strings into python dictionaries that can be used by
"""
# TODO: DOC FIX
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

from .parsers import parse_sensors
from .parsers import parse_options
from .parsers import parse_filters
from .parsers import parse_package

__all__ = [
    'parse_sensors',
    'parse_options',
    'parse_filters',
    'parse_package',
]
