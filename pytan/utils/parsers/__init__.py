# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Parsers package for :mod:`pytan` - responsible for parsing human strings into python dictionaries that can be used by
"""
# TODO: DOC FIX

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
