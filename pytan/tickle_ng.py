
from . import encoding
from . import tanium_ng

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


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


def to_soap_element(cls, minimal=False):  # noqa
    # print(minimal)
    root = ET.Element(cls._soap_tag)
    for p in cls._simple_properties:
        el = ET.Element(p)
        val = getattr(cls, p)
        # print(p, val)
        if val is not None:
            el.text = str(val)
        if val is not None or not minimal:
            root.append(el)
    for p, t in cls._complex_properties.items():
        val = getattr(cls, p)
        # print(p, t, val)
        if val is not None or not minimal:
            if val is not None and not isinstance(val, t):
                raise IncorrectTypeException(p, t, type(val))
            if isinstance(val, tanium_ng.BaseType):
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
    for p, t in cls._list_properties.items():
        vals = getattr(cls, p)
        # print(p, t, vals)
        if not vals:
            continue
        # fix for str types in list props
        if issubclass(t, tanium_ng.BaseType):
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


def to_soap_body(cls, minimal=False):
    """Deserialize cls into an XML body"""
    el = to_soap_element(cls, minimal=minimal)
    result = ET.tostring(el, encoding=encoding)
    return result


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
            if issubclass(t, tanium_ng.BaseType):
                getattr(result, p).append(t.from_soap_element(elem))
            else:
                getattr(result, p).append(elem.text)
    return result


def from_soap_body(body):
    """Parse text ``body`` as XML and produce Python tanium objects.

    This method assumes a single <result_object>, which may be a list or a single object.
    """
    tree = ET.fromstring(body)
    el = tree.find(".//result_object/*")
    if el is None:
        result = el
    if el is not None:
        obj = tanium_ng.get_obj_type(el.tag)
        result = obj.from_soap_element(el)
        result._ORIGINAL_OBJECT = el
    return result
