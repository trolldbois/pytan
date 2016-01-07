from pytan import text_type, encoding, tanium_ng
from pytan.tickle import ET
from pytan.tickle.constants import INCLUDE_EMPTY


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

        self.RESULT = ET.Element(obj._SOAP_TAG)
        self.base_simple()
        self.base_complex()
        self.base_list()

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

            if isinstance(val, tanium_ng.BaseType):
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

            if issubclass(prop_type, tanium_ng.BaseType):
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
