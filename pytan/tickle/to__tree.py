import logging

from pytan import PytanError, text_type, encoding
from pytan.tickle import ET
from pytan.tanium_ng import BaseType
from pytan.tickle.constants import INCLUDE_EMPTY

MYLOG = logging.getLogger(__name__)


class XmlSerializeError(PytanError):
    pass


class ToTree(object):
    """Convert a tanium_ng BaseType object into an ElementTree object.

    x = ToTree(obj)

    Get RESULT:
    x.RESULT
    """

    OBJ = None
    """tanium_ng object to convert to ElementTree object RESULT"""

    RESULT = None
    """ElementTree object created from OBJ"""

    def __init__(self, obj, **kwargs):
        self.KWARGS = kwargs
        self.INCLUDE_EMPTY = kwargs.get('include_empty', INCLUDE_EMPTY)
        self.OBJ = obj

        if not isinstance(obj, BaseType):
            err = "obj is type {!r}, must be a tanium_ng.BaseType object"
            err = err.format(type(obj).__name__)
            raise XmlSerializeError(err)

        self.RESULT = ET.Element(obj._SOAP_TAG)
        self.base_simple()
        self.base_complex()
        self.base_list()

        m = "Converted tanium_ng object {!r} into tree:: {}"
        m = m.format(type(self.OBJ), self.RESULT)
        MYLOG.debug(m)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.INCLUDE_EMPTY:
                continue
            self.add_simple_el(prop, val)

    def add_simple_el(self, prop, val):
        val = text_type(val) if val is not None else None
        el = ET.Element(prop)
        el.text = val
        self.RESULT.append(el)

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.INCLUDE_EMPTY:
                continue

            if isinstance(val, BaseType):
                el = ET.Element(prop)
                child_val = to_tree(val, **self.KWARGS)
                [el.append(c) for c in list(child_val)]
                self.RESULT.append(el)
            else:
                self.add_simple_el(prop, val)

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = getattr(self.OBJ, prop)
            if not vals:
                continue

            if issubclass(prop_type, BaseType):
                for val in vals:
                    child_val = to_tree(val, **self.KWARGS)
                    self.RESULT.append(child_val)
            else:
                for val in vals:
                    if val is None and not self.INCLUDE_EMPTY:
                        continue
                    self.add_simple_el(prop, val)


def to_tree(obj, **kwargs):
    converter = ToTree(obj, **kwargs)
    result = converter.RESULT
    return result


def to_xml(obj, **kwargs):
    tree = to_tree(obj, **kwargs)
    result = ET.tostring(tree, encoding=encoding)
    return result
