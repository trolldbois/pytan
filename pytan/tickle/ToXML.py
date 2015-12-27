from pytan import encoding, text_type, tanium_ng
from pytan.tickle import ET
from pytan.tickle.constants import INCLUDE_EMPTY


class ToXML(object):
    """Convert a tanium_ng BaseType object into an ElementTree object and then an XML string.

    x = ToXML(obj)

    Get OBJTREE:
    x.OBJTREE

    Get XML:
    x.XML
    """

    OBJ = None
    """tanium_ng object to convert to ElementTree object OBJTREE"""

    OBJTREE = None
    """ElementTree object created from OBJ"""

    XML = ''
    """XML string created from OBJTREE"""

    _PARENT = True
    """bool to indicate if this is the first spawn of this object"""

    _EMPTY = INCLUDE_EMPTY
    """bool that controls if empty attributes will be included in the Element Tree Object"""

    def __init__(self, obj, **kwargs):
        # print("New ToXML for obj: {}".format(obj))
        self.KWARGS = kwargs
        self._EMPTY = kwargs.get('empty', self._EMPTY)
        self._PARENT = kwargs.get('parent', self._PARENT)
        self.OBJ = obj

        self.OBJTREE = ET.Element(obj._SOAP_TAG)
        self.base_simple()
        self.base_complex()
        self.base_list()

        if self._PARENT:
            self.XML = ET.tostring(self.OBJTREE, encoding=encoding)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self._EMPTY:
                continue
            self.add_simple_el(prop, val)

    def add_simple_el(self, prop, val):
        val = text_type(val) if val is not None else None
        el = ET.Element(prop)
        el.text = val
        self.OBJTREE.append(el)

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self._EMPTY:
                continue

            if isinstance(val, tanium_ng.BaseType):
                tickle_args = {}
                tickle_args.update(self.KWARGS)
                tickle_args.update({'parent': False, 'obj': val})
                val_tickle = ToXML(**tickle_args)
                el = ET.Element(prop)
                [el.append(c) for c in list(val_tickle.OBJTREE)]
                self.OBJTREE.append(el)
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
                    tickle_args = {}
                    tickle_args.update(self.KWARGS)
                    tickle_args.update({'parent': False, 'obj': val})
                    val = ToXML(**tickle_args).OBJTREE
                    self.OBJTREE.append(val)
            else:
                for val in vals:
                    if val is None and not self._EMPTY:
                        continue
                    self.add_simple_el(prop, val)
