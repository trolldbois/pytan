"""Dict-like object class."""
from __future__ import absolute_import, division, print_function, unicode_literals

import re
import sys

_VERSION = sys.version_info
IS_PY2 = _VERSION[0] == 2
IS_PY3 = _VERSION[0] == 3

if IS_PY2:
    text_type = unicode  # noqa
elif IS_PY3:
    text_type = str


class Store(dict):
    """Dict-like object class."""

    __HIDDEN = ["password", "secret", "crypt_key"]

    def __init__(self, *args, **kwargs):
        """Dict-like object class."""
        super(Store, self).__init__(*args, **kwargs)
        for name, value in kwargs.items():
            try:
                super(Store, self).__setattr__(name, value)
            except:
                pass

    def __str__(self):
        ret = super(Store, self).__str__()
        for x in self.__HIDDEN:
            s = "'{}': .*?', ".format(x)
            r = "'{}': '**HIDDEN**', ".format(x)
            ret = re.sub(s, r, ret, re.IGNORECASE)
        return ret

    def items_clean(self):
        ret = super(Store, self).items()
        ret = {k: "**HIDDEN**" if text_type(k).lower() in self.__HIDDEN else v for k, v in ret}
        return ret

    def __getattr__(self, name):
        """For self.name."""
        ret = None
        try:
            ret = super(Store, self).__getitem__(name)
        except:
            pass
        return ret

    def __setattr__(self, name, value):
        """For ``self.name = value``, will also do ``self[name] = value``."""
        super(Store, self).__setitem__(name, value)
        try:
            super(Store, self).__setattr__(name, value)
        except:
            pass

    def __delattr__(self, name):
        """For del(self.name)."""
        if name in self.keys():
            super(Store, self).__delitem__(name)
            super(Store, self).__delattr__(name)

    def __getitem__(self, name):
        """For ``self[name]``, will also do ``self.name = value``."""
        ret = None
        try:
            ret = super(Store, self).__getitem__(name)
        except:
            pass
        return ret

    def __setitem__(self, name, value):
        """For self[name] = value."""
        super(Store, self).__setitem__(name, value)
        try:
            super(Store, self).__setattr__(name, value)
        except:
            pass

    def __delitem__(self, name):
        """For del(self[name])."""
        if name in self.keys():
            super(Store, self).__delitem__(name)
            super(Store, self).__delattr__(name)

    def gets(self, name, default=None):
        """Get value of name, set to default if not exists."""
        if name in self.keys():
            ret = self.get(name)
        else:
            ret = default
            setattr(self, name, ret)
        return ret
