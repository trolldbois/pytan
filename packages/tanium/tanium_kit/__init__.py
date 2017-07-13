"""Tanium Kit - Collection of python utility modules."""
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

_VERSION = sys.version_info
IS_PY2 = _VERSION[0] == 2
IS_PY3 = _VERSION[0] == 3

if IS_PY3:
    text_type = str  # noqa
    string_types = str,  # noqa
    integer_types = int,  # noqa
    encoding = "unicode"
    uni_chr = chr
    range = range  # noqa
    input = input

    def b(s):  # noqa
        return s.encode("latin-1")
else:
    text_type = unicode  # noqa
    string_types = basestring,  # noqa
    encoding = "us-ascii"
    integer_types = (int, long)  # noqa
    uni_chr = unichr  # noqa
    range = xrange  # noqa
    input = raw_input  # noqa

    def b(s):  # noqa
        return s

try:
    from . import ask
    from . import excel_writer
    from . import history_console
    from . import ini_reader
    from . import log_filters
    from . import log_tanium
    from . import log_tools
    from . import options_parser
    from . import pretty
    from . import pytanx
    from . import shell_parser
    from . import store
    from . import tools
    from . import version
    from . import wequests
    from . import xml_cleaner
    from . import zipper
except:
    raise

__all__ = [
    "ask",
    "excel_writer",
    "history_console",
    "ini_reader",
    "integer_types",
    "log_filters",
    "log_tanium",
    "log_tools",
    "options_parser",
    "pretty",
    "pytanx",
    "shell_parser",
    "store",
    "string_types",
    "text_type",
    "tools",
    "version",
    "wequests",
    "xml_cleaner",
    "zipper",
    "IS_PY2",
    "IS_PY3",
]
