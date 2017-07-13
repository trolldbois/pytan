"""Die."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import re


class RegexLogFilter(logging.Filter):
    """Die."""

    search_regex = None
    replace_regex = ""
    filter_mode = "skip"
    description = "No description provided!"
    test_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    valid_test = ""

    _EXC = None
    _MODES = ["skip", "include", "replace"]

    _TMPL_MODES = ", ".join(_MODES)
    _TMPL_NEWEXC = "{}\n!!!! WRAPPED INITIAL {}"
    _TMPL_PREVEXC = "{}\n!!!! WRAPPED PREVIOUS {}"
    _TMPL_EXC = "EXCEPTION {} in {}"

    _TATTRS = ["filter_mode", "search_regex", "replace_regex", "description"]
    _TSTR = ", ".join(["{0}: '{{{0}}}'".format(k) for k in _TATTRS])
    _TMPL_THIS = "Log Filter {}".format(_TSTR)

    def __init__(self, search_regex, **kwargs):
        """Die."""
        err1 = "filter_mode '{}' not one of: {} (in {})"
        err2 = "Search '{}' is not a valid regex, error: {} (in {})"
        err3 = "Regex filter test using string '{}' failed with error: {} (in {})"
        err4 = "Regex filter test using string '{}' failed validation, result '{}' != '{}' (in {})"

        self.search_regex = search_regex
        self.filter_mode = kwargs.get("filter_mode", self.filter_mode).lower()
        self.replace_regex = kwargs.get("replace_regex", self.replace_regex)
        self.description = kwargs.get("description", self.description)
        self.test_str = kwargs.get("test_str", self.test_str)
        self.valid_test = kwargs.get("valid_test", self.valid_test)
        self._EXC = None

        self._TMPL_THIS = self._TMPL_THIS.format(**vars(self))

        if self.filter_mode not in self._MODES:
            raise Exception(err1.format(self.filter_mode, self._TMPL_MODES, self._TMPL_THIS))

        try:
            self.search_regex = self.convert_re(self.search_regex)
        except Exception as e:
            raise Exception(err2.format(self.search_regex, e, self._TMPL_THIS))

        try:
            passed, msg = self.regex_filter(self.test_str)
        except Exception as e:
            raise Exception(err3.format(self.test_str, e, self._TMPL_THIS))

        if self.valid_test and msg != self.valid_test:
            raise Exception(err4.format(self.test_str, msg, self.valid_test, self._TMPL_THIS))

    def convert_re(self, x):
        """Die."""
        return re.compile(x) if not isinstance(x, re._pattern_type) else x

    def filter(self, record):
        """Die."""
        ret, record.msg = self.regex_filter(record.msg)
        return ret

    def regex_filter(self, msg):
        """Die."""
        ret = True
        if self.filter_mode == "replace":
            # replacement regex does not get tested unless it matches search regex
            # we do not want the logging system throwing spurious unexpected exceptions
            # so we wrap them here. if this filter has previously had an exception,
            # we do not even try to re-run the re.sub, we just append the previous exception
            # to the message and return that.
            if self._EXC:
                msg = self._TMPL_PREVEXC.format(msg, self._EXC)
            else:
                try:
                    msg = self.search_regex.sub(self.replace_regex, msg)
                except Exception as e:
                    self._EXC = self._TMPL_EXC.format(e, self._TMPL_THIS)
                    msg = self._TMPL_NEWEXC.format(msg, self._EXC)
        else:
            found = True if self.search_regex.search(msg) else False
            ret = found if self.filter_mode == "include" else not found
        return ret, msg
