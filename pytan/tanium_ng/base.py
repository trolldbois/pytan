"""The BaseType used by (almost) all tanium_ng objects.

Handles the serialization and deserialization of objects to / from XML and Python

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
# TODO: fix str for un'init'd

import sys
from collections import OrderedDict

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
    encoding = "unicode"
else:
    text_type = unicode  # noqa
    encoding = "us-ascii"


class TaniumNextGenException(Exception):
    pass


class IncorrectTypeException(TaniumNextGenException):
    """Raised when a property is not of the expected type"""
    def __init__(self, name, value, expected):
        self.name = name
        self.expected = expected
        self.value = value
        err = "Attribute '{}' expected type '{}', got '{}' (value: '{}')"
        err = err.format(name, expected.__name__, type(value).__name__, value)
        TaniumNextGenException.__init__(self, err)


class BaseType(object):

    _soap_tag = None

    def __init__(self, simple_properties, complex_properties, list_properties, **kwargs):
        self._initialized = False
        self._simple_properties = simple_properties
        self._complex_properties = complex_properties
        self._list_properties = list_properties
        self._initialized = True

    def __getitem__(self, idx):
        """Allow automatic indexing into lists."""
        if not self._is_list():
            err = 'Not a list type, __getitem__ not supported'
            raise TaniumNextGenException(err)
        result = getattr(self, self._get_list_attr())[idx]
        return result

    def __len__(self):
        """Allow len() for lists and str"""
        result = 0
        if self._is_list():
            result = len(getattr(self, self._get_list_attr()))
        elif getattr(self, 'name', ''):
            result = len(str(self.name))
        elif getattr(self, 'id', ''):
            result = len(str(self.id))
        return result

    def __str__(self):
        class_name = self.__class__.__name__
        vals = OrderedDict()
        if self._is_list():
            vals['length'] = len(self)
        else:
            for k in ['id', 'name']:
                if not hasattr(self, k):
                    continue
                vals[k] = getattr(self, k, None)

            for k in ['query_text', 'hidden_flag', 'package_spec', 'url_regex']:
                if not getattr(self, k, None):
                    continue
                vals[k] = getattr(self, k, None)

        if not vals:
            for k in sorted(self._simple_properties):
                val = getattr(self, k, None)
                if val is not None:
                    vals[k] = val

        if vals:
            vals = ', '.join(["'{}'='{}'".format(*p) for p in vals.items()])
        else:
            vals = "No attributes assigned yet!"

        result = '{}: {}'.format(class_name, vals)
        return result

    def __setattr__(self, name, value):
        """Enforce type of attribute assignments"""
        val_not_none = value is not None
        name_not_init = name != '_initialized'
        self_is_init = getattr(self, '_initialized', False)
        check_type = all([val_not_none, name_not_init, self_is_init])

        if check_type:
            if name in getattr(self, '_complex_properties', {}):
                value = self._check_complex(name, value)
            elif name in getattr(self, '_simple_properties', {}):
                value = self._check_simple(name, value)
            elif name in getattr(self, '_list_properties', {}):
                value = self._check_list(name, value)
        super(BaseType, self).__setattr__(name, value)

    def _set_values(self, values):
        for k, v in values.items():
            setattr(self, k, v)

    def _is_list(self):
        result = len(self._list_properties) == 1
        return result

    def _get_list_attr(self):
        result = None
        if self._is_list:
            result = list(self._list_properties.keys())[0]
        return result

    def _check_complex(self, name, value):
        if not isinstance(value, self._complex_properties[name]):
            raise IncorrectTypeException(name, value, self._complex_properties[name])
        return value

    def _check_simple(self, name, value):
        if not isinstance(value, self._simple_properties[name]):
            try:
                value = self._simple_properties[name](value)
            except:
                raise IncorrectTypeException(name, value, self._simple_properties[name])
        return value

    def _check_list(self, name, value):
        if value != [] and not isinstance(value, self._list_properties[name]):
            raise IncorrectTypeException(name, value, self._list_properties[name])
        return value

    def append(self, n):
        """Allow adding to list."""
        if not self._is_list():
            err = 'Not a list type, append not supported'
            raise TaniumNextGenException(err)
        getattr(self, self._get_list_attr()).append(n)

    def to_soap_element(self, minimal=False):  # noqa
        # print(minimal)
        root = ET.Element(self._soap_tag)
        for p in self._simple_properties:
            el = ET.Element(p)
            val = getattr(self, p)
            # print(p, val)
            if val is not None:
                el.text = str(val)
            if val is not None or not minimal:
                root.append(el)
        for p, t in self._complex_properties.items():
            val = getattr(self, p)
            # print(p, t, val)
            if val is not None or not minimal:
                if val is not None and not isinstance(val, t):
                    raise IncorrectTypeException(p, t, type(val))
                if isinstance(val, BaseType):
                    child = val.to_soap_element(minimal=minimal)
                    # the tag name is the property name,
                    # not the property type's soap tag
                    el = ET.Element(p)
                    if child.getchildren() is not None:
                        for child_prop in child.getchildren():
                            el.append(child_prop)
                    root.append(el)
                else:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.append(str(val))
        for p, t in self._list_properties.items():
            vals = getattr(self, p)
            # print(p, t, vals)
            if not vals:
                continue
            # fix for str types in list props
            if issubclass(t, BaseType):
                for val in vals:
                    # print(val, type(val))
                    root.append(val.to_soap_element(minimal=minimal))
            else:
                for val in vals:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.text = str(val)
                    if vals is not None or not minimal:
                        root.append(el)
        return root

    def to_soap_body(self, minimal=False):
        """Deserialize self into an XML body"""
        el = self.to_soap_element(minimal=minimal)
        result = ET.tostring(el, encoding=encoding)
        # print(result)
        return result

    @classmethod
    def from_soap_element(cls, el):
        result = cls()
        for p, t in result._simple_properties.items():
            pel = el.find("./{}".format(p))
            if pel is not None and pel.text:
                setattr(result, p, t(pel.text))
            else:
                setattr(result, p, None)
        for p, t in result._complex_properties.items():
            elems = el.findall('./{}'.format(p))
            if len(elems) > 1:
                raise TaniumNextGenException(
                    'Unexpected: {} elements for property'.format(p)
                )
            elif len(elems) == 1:
                setattr(
                    result,
                    p,
                    result._complex_properties[p].from_soap_element(elems[0]),
                )
            else:
                setattr(result, p, None)
        for p, t in result._list_properties.items():
            setattr(result, p, [])
            elems = el.findall('./{}'.format(p))
            for elem in elems:
                if issubclass(t, BaseType):
                    getattr(result, p).append(t.from_soap_element(elem))
                else:
                    getattr(result, p).append(elem.text)

        return result

    @classmethod
    def _get_obj_type(cls, el):
        """Based on the tag of ``el``, find the appropriate tanium_type."""
        from . import OBJECT_TYPES
        if el.tag not in OBJECT_TYPES:
            err = 'Unknown type {}'
            err = err.format(el.tag)
            raise TaniumNextGenException(err)
        result = OBJECT_TYPES[el.tag]
        return result

    @classmethod
    def from_soap_body(cls, body):
        """Parse text ``body`` as XML and produce Python tanium objects.

        This method assumes a single <result_object>, which may be a list or a single object.
        """
        tree = ET.fromstring(body)
        el = tree.find(".//result_object/*")
        if el is None:
            result = el
        if el is not None:
            obj = cls._get_obj_type(el)
            result = obj.from_soap_element(el)
            result._ORIGINAL_OBJECT = el
        return result
