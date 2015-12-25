"""Object serialization and deserialization module for tanium_ng"""
import json
import logging

mylog = logging.getLogger(__name__)

from . import encoding, text_type
from . import tanium_ng
from . import utils

FALLBACK = False
if utils.constants.DEFAULT_XML_ENGINE == "lxml":
    try:
        import lxml.etree as ET
        mylog.debug("Using lxml.etree for XML engine")
    except ImportError:
        FALLBACK = True
elif utils.constants.DEFAULT_XML_ENGINE == "cet":
    try:
        import xml.etree.cElementTree as ET
        mylog.debug("Using xml.etree.cElementTree for XML engine")
    except ImportError:
        FALLBACK = True
elif utils.constants.DEFAULT_XML_ENGINE == "et":
    try:
        import xml.etree.ElementTree as ET
        mylog.debug("Using xml.etree.ElementTree for XML engine")
    except ImportError:
        FALLBACK = True
else:
    FALLBACK = True

# currently, cElementTree is showing the fastest times. more testing needed
if FALLBACK:
    try:
        import xml.etree.cElementTree as ET  # noqa
        mylog.debug("Using xml.etree.cElementTree for XML engine")
    except ImportError:
        try:
            import lxml.etree as ET  # noqa
            mylog.debug("Using lxml.etree for XML engine")
        except ImportError:
            import xml.etree.ElementTree as ET  # noqa
            mylog.debug("Using xml.etree.ElementTree for XML engine")


# CONVENIENCE FUNCTIONS:

def to_xml(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into an XML body using ObjectToXML"""
    tickle_val = ObjectToXML(obj, **kwargs)
    result = tickle_val.XML
    return result


def to_dict(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a dict using ObjectToJson"""
    tickle_val = ObjectToJson(obj, **kwargs)
    result = tickle_val.DICT
    return result


def to_json(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a JSON string using ObjectToJson"""
    tickle_val = ObjectToJson(obj, **kwargs)
    result = tickle_val.JSON
    return result


def from_json(jsonstr, **kwargs):
    """Deserialize a JSON string into tanium_ng object ``obj`` using JsonToObject"""
    tickle_val = JsonToObject(jsonstr=jsonstr, **kwargs)
    result = tickle_val.OBJ
    return result


def from_dict(pyobj, **kwargs):
    """Deserialize a dict into tanium_ng object ``obj`` using JsonToObject"""
    tickle_val = JsonToObject(pyobj=pyobj, **kwargs)
    result = tickle_val.OBJ
    return result


def from_xml(xml, **kwargs):
    """Deserialize ``xml`` from XML into a tanium_ng object using XMLToObject."""
    tickle_val = XMLToObject(xml=xml, **kwargs)
    result = tickle_val.OBJ
    return result


def from_sse_xml(xml, **kwargs):
    """Wraps a Result Set XML from a server side export in the appropriate tags and returns a
    ResultSet object

    Parameters
    ----------
    x : str
        * str of XML to convert to a ResultSet object

    Returns
    -------
    rs : :class:`utils.tanium_ng.result_set.ResultSet`
        * x converted into a ResultSet object
    """
    rs_xml = (
        '<return><ResultXML>\n'
        '<![CDATA[<result_sets><result_set>\n'
        '{}\n'
        '</result_set></result_sets>\n'
        ']]>\n'
        '</ResultXML>\n'
        '</return>\n'
    )
    rs_xml = rs_xml.format(xml)
    result = from_xml(rs_xml, **kwargs)
    return result


def _explode_json(val):
    """pass."""
    try:
        result = json.loads(val)
    except:
        result = None
    return result


def _implode_json(val):
    """pass."""
    result = json.dumps(val)
    return result


class JsonToObject(object):
    """Convert a JSON string or a single or list of dict into a tanium_ng BaseType object

    x = JsonToObject(jsonstr=json_str)
        .. or ..
    x = JsonToObject(pyobj=python_dict)
        .. or ..
    x = JsonToObject(pyobj=[python_dict])

    Get PYOBJ:
    x.PYOBJ

    Get OBJ:
    x.OBJ
    """

    TAG_NAME = '_tickled_tag'
    """attribute to hold OBJ._SOAP_TAG so tickle can deserialize into an OBJ"""

    LIST_NAME = '_tickled_list'
    """attribute to hold list of serialized OBJs"""

    EXPLODE_PROP_VALUE = '_tickled_explode'
    """attribute to identify JSON exploded property value"""

    OBJ = None
    """single or list of tanium_ng objects created from PYOBJ"""

    PYOBJ = None
    """python object created from JSON"""

    JSONSTR = ''
    """json string to create PYOBJ from"""

    def __init__(self, **kwargs):
        # print("New JsonToObject for obj: {}".format(obj))
        self.KWARGS = kwargs
        # self.PARENT = kwargs.get('parent', True)
        self.JSONSTR = kwargs.get('jsonstr', self.JSONSTR)
        self.PYOBJ = kwargs.get('pyobj', self.PYOBJ)
        self.OBJ = None

        if self.JSONSTR and not self.PYOBJ:
            self.PYOBJ = json.loads(self.JSONSTR)

        if not self.PYOBJ:
            err = "Must supply a non-empty jsonstr or non-empty pyobj!"
            raise tanium_ng.TaniumNextGenException(err)

        if isinstance(self.PYOBJ, list):
            self.OBJ = [JsonToObject(pyobj=v).OBJ for v in self.PYOBJ]
        elif isinstance(self.PYOBJ, dict):
            if self.LIST_NAME in self.PYOBJ:
                self.OBJ = [JsonToObject(pyobj=v).OBJ for v in self.PYOBJ[self.LIST_NAME]]
            else:
                if self.TAG_NAME not in self.PYOBJ:
                    err = "JSON missing attribute {!r}, unable to deserialize!"
                    err = err.format(self.TAG_NAME)
                    raise tanium_ng.TaniumNextGenException(err)
                soap_tag = self.PYOBJ[self.TAG_NAME]
                self.OBJ = tanium_ng.get_obj_type(soap_tag)()
                self.base_simple()
                self.base_complex()
                self.base_list()
        else:
            err = "JSON contained {}, must contain either a list or dict, unable to deserialize!"
            err = err.format(type(self.PYOBJ))
            raise tanium_ng.TaniumNextGenException(err)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._SIMPLE_PROPS.items():
            val = self.PYOBJ.get(prop, None)
            if val is None:
                continue
            if isinstance(val, dict) and self.EXPLODE_PROP_VALUE in val:
                val = _implode_json(val[self.EXPLODE_PROP_VALUE])
            setattr(self.OBJ, prop, prop_type(val))

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = self.PYOBJ.get(prop, None)
            if val is None:
                continue
            setattr(self.OBJ, prop, JsonToObject(pyobj=val).OBJ)

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = self.PYOBJ.get(prop, None)
            if vals is None:
                continue

            new_vals = []

            for val in vals:
                if issubclass(prop_type, tanium_ng.BaseType):
                    new_vals.append(JsonToObject(pyobj=val).OBJ)
                else:
                    new_vals.append(val)
            setattr(self.OBJ, prop, new_vals)


class ObjectToJson(object):
    """Convert either a single or list of tanium_ng BaseType objects into a python
    dict object and then into a JSON string

    x = ObjectToJson(obj)
     ..or..
    x = ObjectToJson([obj])

    Get DICT:
    x.DICT

    Get JSON:
    x.JSON
    """

    EMPTY_ATTRS = False
    """bool that controls if empty attributes will be included in DICT"""

    SORT_KEYS = True
    """bool that controls if the JSON string will be written with its keys sorted"""

    INDENT = 2
    """int that controls how many spaces will be used to pretty print the JSON, None to disable"""

    TAG_NAME = '_tickled_tag'
    """attribute to store OBJ._SOAP_TAG so tickle can deserialize into an OBJ later"""

    LIST_NAME = '_tickled_list'
    """attribute to hold list of serialized OBJs"""

    EXPLODE_PROP_VALUE = '_tickled_explode'
    """attribute to identify JSON exploded property value"""

    OBJ = None
    """tanium_ng object to convert to DICT"""

    DICT = {}
    """dict created from OBJ"""

    JSON = ''
    """json string created from DICT"""

    def __init__(self, obj, **kwargs):
        # print("New ObjectToJson for obj: {}".format(obj))
        self.KWARGS = kwargs
        self.EMPTY_ATTRS = kwargs.get('empty_attrs', self.EMPTY_ATTRS)
        self.INDENT = kwargs.get('indent', self.INDENT)
        self.SORT_KEYS = kwargs.get('sort_keys', self.SORT_KEYS)
        self.PARENT = kwargs.get('parent', True)

        self.OBJ = obj
        self.DICT = {}
        self.JSON = ''

        if isinstance(self.OBJ, list):
            self.DICT[self.LIST_NAME] = []
            for val in self.OBJ:
                tickle_args = {}
                tickle_args.update(self.KWARGS)
                tickle_args.update({'parent': False, 'obj': val})
                val_tickle = ObjectToJson(**tickle_args)
                self.DICT[self.LIST_NAME].append(val_tickle.DICT)
        else:
            self.DICT[self.TAG_NAME] = self.OBJ._SOAP_TAG
            self.base_simple()
            self.base_complex()
            self.base_list()

        if self.PARENT:
            self.JSON = json.dumps(self.DICT, indent=self.INDENT, sort_keys=self.SORT_KEYS)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.EMPTY_ATTRS:
                continue

            val_json = _explode_json(val)

            if val_json:
                val = {self.EXPLODE_PROP_VALUE: val_json}

            self.DICT[prop] = val

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.EMPTY_ATTRS:
                continue

            if val is not None:
                tickle_args = {}
                tickle_args.update(self.KWARGS)
                tickle_args.update({'parent': False, 'obj': val})
                val_tickle = ObjectToJson(**tickle_args)
                self.DICT[prop] = val_tickle.DICT
            else:
                self.DICT[prop] = val

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = getattr(self.OBJ, prop)
            if not vals and not self.EMPTY_ATTRS:
                continue

            self.DICT[prop] = []

            for val in vals:
                if issubclass(prop_type, tanium_ng.BaseType):
                    tickle_args = {}
                    tickle_args.update(self.KWARGS)
                    tickle_args.update({'parent': False, 'obj': val})
                    val_tickle = ObjectToJson(**tickle_args)
                    self.DICT[prop].append(val_tickle.DICT)
                else:
                    self.DICT[prop].append(val)


class ObjectToXML(object):
    """Convert a tanium_ng BaseType object into an ElementTree object and then an XML string.

    x = ObjectToXML(obj)

    Get OBJTREE:
    x.OBJTREE

    Get XML:
    x.XML
    """

    EMPTY_ATTRS = False
    """bool that controls if empty attributes will be included in the Element Tree Object"""

    OBJ = None
    """tanium_ng object to convert to ElementTree object OBJTREE"""

    OBJTREE = None
    """ElementTree object created from OBJ"""

    XML = ''
    """XML string created from OBJTREE"""

    def __init__(self, obj, **kwargs):
        # print("New ObjectToXML for obj: {}".format(obj))
        self.KWARGS = kwargs
        self.EMPTY_ATTRS = kwargs.get('empty_attrs', self.EMPTY_ATTRS)
        self.PARENT = kwargs.get('parent', True)
        self.OBJ = obj

        self.OBJTREE = ET.Element(obj._SOAP_TAG)
        self.base_simple()
        self.base_complex()
        self.base_list()

        if self.PARENT:
            self.XML = ET.tostring(self.OBJTREE, encoding=encoding)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.EMPTY_ATTRS:
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
            if val is None and not self.EMPTY_ATTRS:
                continue

            if isinstance(val, tanium_ng.BaseType):
                tickle_args = {}
                tickle_args.update(self.KWARGS)
                tickle_args.update({'parent': False, 'obj': val})
                val_tickle = ObjectToXML(**tickle_args)
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
                    val_tickle = ObjectToXML(**tickle_args)
                    self.OBJTREE.append(val_tickle.OBJTREE)
            else:
                for val in vals:
                    if val is None and not self.EMPTY_ATTRS:
                        continue
                    self.add_simple_el(prop, val)


class XMLToObject(object):
    """Convert an XML String or an ElementTree object into a tanium_ng BaseType object.

    x = XMLToObject(xml=xml_text)
        ..or..
    x = XMLToObject(objclass=tanium_ng.Sensor, objtree=ElementTreeObject)

    Get OBJ:
    x.OBJ
    """

    OBJ = None
    """tanium_ng object that gets created from OBJTREE"""

    OBJTREE = None
    """ElementTree object to convert into a tanium_ng object"""

    XML = ''
    """XML string to convert into a tanium_ng object"""

    XMLTREE = None
    """If XML string supplied, full elementtree used to search for OBJTREE"""

    OBJECT_XPATH = ".//result_object/*"
    RESULT_XPATH = ".//ResultXML"

    def __init__(self, **kwargs):
        # print("New XMLToObject kwargs: {}".format(kwargs))
        self.KWARGS = kwargs
        self.XML = kwargs.get('xml', '')
        self.OBJTREE = kwargs.get('objtree', None)
        self.OBJCLASS = kwargs.get('objclass', None)
        self.create_obj()
        self.populate_obj()

    def populate_obj(self):
        # if self.OBJ has been created by create_obj, then populate it with the values from XML
        if self.OBJ is not None:
            self.base_simple()
            self.base_complex()
            self.base_list()

            if hasattr(self.OBJ, '_post_xml_hook'):
                self.OBJ._post_xml_hook()

            self.OBJ._XMLTREE = self.XMLTREE
            self.OBJ._XML = self.XML
            self.OBJ._OBJTREE = self.OBJTREE

    def create_obj(self):
        # create self.OBJ from self.OBJCLASS if objclass and objtree supplied
        if self.OBJCLASS and self.OBJTREE is not None:
            self.OBJ = self.OBJCLASS()
        elif self.XML:
            # convert text self.XML into ElementTree object self.XMLTREE
            self.XMLTREE = ET.fromstring(self.XML)
            # check for an object in self.XMLTREE and store it in self.OBJTREE if found
            self.check_object_in_tree()
            # check for a result in self.XMLTREE and store it in self.OBJTREE if found
            self.check_result_in_tree()
            # if self.OBJTREE found
            if self.OBJTREE is not None:
                # print("Looking for tanium_ng class for tag: {}".format(self.OBJTREE.tag))
                # get the tanium_ng class for tag self.OBJTREE.tag
                self.OBJCLASS = tanium_ng.get_obj_type(self.OBJTREE.tag)
                # print("Found tanium_ng class: {}".format(self.OBJCLASS))
                # create self.OBJ from self.OBJCLASS
                self.OBJ = self.OBJCLASS()
                # print("Created tanium_ng object: {!r}".format(self.OBJ))
        else:
            err = "Must supply either xml or both objclass and objtree!"
            raise tanium_ng.TaniumNextGenException(err)

    def check_object_in_tree(self):
        """Try to find a result object in self.XMLTREE"""
        objtree = self.XMLTREE.find(self.OBJECT_XPATH)

        # m = "check_object_in_tree(): xpath: {} objtree: {}"
        # m = m.format(self.OBJECT_XPATH, objtree)
        # print(m)

        if objtree is not None:
            # print("setting self.OBJTREE to object found")
            self.OBJTREE = objtree

    def check_result_in_tree(self):
        objtree = self.XMLTREE.find(self.RESULT_XPATH)
        # m = "check_result_in_tree(): xpath: {} objtree: {}"
        # m = m.format(self.RESULT_XPATH, objtree)

        cdatatree = None
        if objtree is not None:
            if objtree.text:
                cdatatree = ET.fromstring(objtree.text)

        # m = "check_result_in_tree(): cdata fromstring: {}"
        # m = m.format(cdatatree)
        # print(m)

        if self.OBJTREE is not None and cdatatree is not None:
            err = "Found result {} in tree, but object already found in tree: {}"
            err = err.format(objtree, self.OBJTREE)
            raise tanium_ng.TaniumNextGenException(err)

        if cdatatree is not None:
            # print("setting self.OBJTREE to result found")
            self.OBJTREE = cdatatree

    def get_xpath(self, prop):
        """pass."""
        xpath = "./{}".format(prop)
        overrides = getattr(self.OBJ, '_OVERRIDE_XPATH', {})
        if prop in overrides:
            xpath = overrides[prop]
        return xpath

    def base_simple(self):
        """Process the simple properties for the tanium_ng object"""
        for prop, prop_type in self.OBJ._SIMPLE_PROPS.items():
            xpath = self.get_xpath(prop)
            prop_el = self.OBJTREE.find(xpath)
            if prop_el is not None and prop_el.text:
                setattr(self.OBJ, prop, prop_type(prop_el.text))
            else:
                setattr(self.OBJ, prop, None)

    def base_complex(self):
        """Process the complex properties for the tanium_ng object"""
        for prop, prop_type in self.OBJ._COMPLEX_PROPS.items():
            xpath = self.get_xpath(prop)
            prop_elems = self.OBJTREE.findall(xpath)
            if len(prop_elems) > 1:
                err = 'Found {} elements for property {}, should only be 1 (xpath: {})'
                err = err.format(len(prop_elems), prop, xpath)
                raise tanium_ng.TaniumNextGenException(err)
            elif len(prop_elems) == 1:
                val_pickle = XMLToObject(objclass=prop_type, objtree=prop_elems[0])
                setattr(self.OBJ, prop, val_pickle.OBJ)
            else:
                setattr(self.OBJ, prop, None)

    def base_list(self):
        """Process the list properties for the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            xpath = self.get_xpath(prop)
            prop_elems = self.OBJTREE.findall(xpath)
            prop_list = []
            for prop_elem in prop_elems:
                if issubclass(prop_type, tanium_ng.BaseType):
                    val_pickle = XMLToObject(objclass=prop_type, objtree=prop_elem)
                    prop_list.append(val_pickle.OBJ)
                else:
                    prop_list.append(prop_elem.text)
            setattr(self.OBJ, prop, prop_list)
