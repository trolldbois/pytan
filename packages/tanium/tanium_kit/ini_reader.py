"""IniReader."""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from io import StringIO, open

_VERSION = sys.version_info
IS_PY2 = _VERSION[0] == 2
IS_PY3 = _VERSION[0] == 3

if IS_PY2:
    integer_types = (int, long)  # noqa
    text_type = unicode  # noqa
    import ConfigParser as configparser
elif IS_PY3:
    integer_types = int,
    text_type = str
    import configparser as configparser


class IniReaderError(Exception):
    """Reader exceptions."""


class IniReader(object):
    """IniReader."""

    TEXT_PRE = "__TEXT::"

    BOOL_OPTS = ["true", "false", "yes", "no", "on", "off", 0, "0", 1, "1"]

    BOOL_TRUE = ["true", "yes", "on", 1, "1"]

    _value_cache = {}
    _parser_type = configparser.RawConfigParser

    def read(self, ini_path=None, ini_text=None, ini_handle=None, **kwargs):
        """IniReader."""
        if ini_text:
            fh = StringIO(ini_text)
            path = "<ini_text stream>"
        elif ini_path:
            if os.path.isfile(ini_path):
                fh = open(ini_path, encoding="utf-8")
                path = ini_path
            else:
                m = "Unable to find 'ini_path': '{}'"
                raise IniReaderError(m.format(ini_path))
        elif ini_handle:
            fh = ini_handle
            path = "<ini_handle stream>"
        else:
            m = "Must provide ini_text, ini_path, or ini_handle as an argument"
            raise IniReaderError(m)

        cp = configparser.RawConfigParser()
        try:
            cp.readfp(fh)
        except Exception as e:
            m = "Unable to parse INI file '{}', error: {}"
            raise IniReaderError(m.format(path, e))

        ret = {s: {i[0]: self._tv(i[1]) for i in cp.items(s)} for s in cp.sections()}
        return path, ret

    def _tv(self, value):
        """Cache to avoid transforming value too many times."""
        if value not in self._value_cache:
            new_value = value
            if self.is_txt(value):
                new_value = self.to_txt(value)
            elif self.is_int(value):
                new_value = int(value)
            elif self.is_float(value):
                new_value = float(value)
            elif self.is_bool(value):
                new_value = self.to_bool(value)
            elif self.is_none(value):
                new_value = None
            self._value_cache[value] = new_value
        return self._value_cache[value]

    def is_float(self, value):
        """Check if the value is a float."""
        return self._is_type(value, float)

    def is_int(self, value):
        """Check if the value is an int."""
        return any([self._is_type(value, t) for t in integer_types])

    def is_txt(self, value):
        """Check if the value begins with TEXT_PRE."""
        return text_type(value).startswith(self.TEXT_PRE)

    def is_bool(self, value):
        """Check if the value is a bool."""
        return value.lower() in self.BOOL_OPTS

    def is_none(self, value):
        """Check if the value is a None."""
        return value.lower() == text_type(None).lower()

    def to_txt(self, value):
        """Convert a value to text, removing FORCE_TEXT::."""
        return "".join(text_type(value).split(self.TEXT_PRE, 1)[1:])

    def to_bool(self, value):
        """Convert value to a bool."""
        return value.lower() in self.BOOL_TRUE

    def _is_type(self, value, ptype):
        """Try to set value to python type ptype."""
        try:
            ptype(value)
            ret = True
        except Exception:
            ret = False
        return ret
