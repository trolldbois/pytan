#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Type functions for :mod:`pytan`"""

from collections import OrderedDict


def is_list(l):
    """returns True if `l` is a list, False if not"""
    return type(l) in [list, tuple]


def is_str(l):
    """returns True if `l` is a string, False if not"""
    return type(l) in [unicode, str]


def is_dict(l):
    """returns True if `l` is a dictionary, False if not"""
    return type(l) in [dict, OrderedDict]


def is_num(l):
    """returns True if `l` is a number, False if not"""
    return type(l) in [float, int, long]
