"""Object serialization and deserialization module for tanium_ng"""
import json
import logging
import datetime

from pytan import encoding, text_type
from pytan import tanium_ng
from pytan.utils import constants, exceptions, tools

mylog = logging.getLogger(__name__)
serlog = logging.getLogger(__name__ + '.serialize')
deslog = logging.getLogger(__name__ + '.deserialize')

FALLBACK = False
if constants.DEFAULT_XML_ENGINE == "lxml":
    try:
        import lxml.etree as ET
        mylog.debug("Using lxml.etree for XML engine")
    except ImportError:
        FALLBACK = True
elif constants.DEFAULT_XML_ENGINE == "cet":
    try:
        import xml.etree.cElementTree as ET
        mylog.debug("Using xml.etree.cElementTree for XML engine")
    except ImportError:
        FALLBACK = True
elif constants.DEFAULT_XML_ENGINE == "et":
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
    """Deserialize a JSON string into a tanium_ng object sing JsonToObject"""
    tickle_val = JsonToObject(jsonstr=jsonstr, **kwargs)
    result = tickle_val.OBJ
    return result


def from_dict(pyobj, **kwargs):
    """Deserialize a dict or list of dicts into a tanium_ng object using JsonToObject"""
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
    rs : :class:`tanium_ng.result_set.ResultSet`
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
        # only explode non str/int types
        if not isinstance(result, (list, tuple, dict)):
            result = None
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


# OBJECT HANDLING METHODS


def shrink_obj(obj, attrs=None):
    """Returns a new class of obj with only id/name/hash defined

    Parameters
    ----------
    obj : :class:`tanium_ng.base.BaseType`
        * Object to shrink
    attrs : list of str
        * default: None
        * list of attribute str's to copy over to new object, will default to
        ['name', 'id', 'hash'] if None

    Returns
    -------
    new_obj : :class:`tanium_ng.base.BaseType`
        * Shrunken object
    """
    if attrs is None:
        attrs = ['name', 'id', 'hash']

    new_obj = obj.__class__()
    [setattr(new_obj, a, getattr(obj, a)) for a in attrs if getattr(obj, a, None) is not None]
    return new_obj


def plugin_zip(p):
    """Maps columns to values for each row in a plugins sql_response and returns a list of dicts

    Parameters
    ----------
    p : :class:`tanium_ng.plugin.Plugin`
        * plugin object

    Returns
    -------
    dict
        * the columns and result_rows of the sql_response in Plugin object zipped up into a
        dictionary
    """
    return [
        dict(zip(p.sql_response.columns, x)) for x in p.sql_response.result_row
    ]


# DEFINITELY NEW

def create_cf_listobj(specs):
    """pass."""
    result = tanium_ng.CacheFilterList()
    if not isinstance(specs, (list, tuple)):
        specs = [specs]
    for spec in specs:
        result.append(create_cf_obj(**spec))
    return result


def create_cf_obj(field, value, operator=None, field_type=None, not_flag=None, **kwargs):
    """pass."""
    result = tanium_ng.CacheFilter()
    result.field = field
    result.value = value
    if operator is not None:
        result.operator = operator
    if field_type is not None:
        result.type = field_type
    if not_flag is not None:
        result.not_flag = not_flag
    return result


def create_selectlist_obj(specs):
    """pass."""
    result = tanium_ng.SelectList()
    for spec in specs:
        result.append(create_select_obj(spec))
    return result


def create_select_obj(spec):
    """pass."""
    result = tanium_ng.Select()
    result.sensor = tanium_ng.Sensor()

    if 'parameters' in spec:
        result.sensor.source_id = spec['sensor_object'].id
        result.sensor.parameters = create_parameter_objlist(spec['parameters'])
    else:
        result.sensor.id = spec['sensor_object'].id

    if 'filter' in spec:
        result.filter = create_filter_obj(spec)
    return result


def create_filter_obj(spec):
    """pass."""
    filter_spec = spec['filter']
    result = tanium_ng.Filter()
    result.sensor = tanium_ng.Sensor()
    result.sensor.hash = spec['sensor_object'].hash  # needs to be hash, id no work!
    result.value = filter_spec['value']
    result.operator = filter_spec.get('operator', 'Equal')  # tanium default operator is Less!
    return result


def create_parameter_objlist(parameters, **kwargs):
    """pass."""
    result = tanium_ng.ParameterList()
    for k, v in parameters.items():
        result.append(create_parameter_obj(key=k, val=v, **kwargs))
    return result


def create_parameter_obj(key, val, delim='||'):
    """pass."""
    result = tanium_ng.Parameter()
    result.key = '{0}{1}{0}'.format(delim, key)
    result.value = val
    return result


def create_filterlist_obj(spec):
    """pass."""
    result = tanium_ng.FilterList()
    result.append(create_filter_obj(spec))
    return result


def create_group_with_filter_obj(spec):
    """pass."""
    result = tanium_ng.Group()
    result.filters = create_filterlist_obj(spec)
    return result


def create_parent_group_obj(specs):
    """pass."""
    result = tanium_ng.Group()
    result.sub_groups = tanium_ng.GroupList()
    parent_sub = tanium_ng.Group()
    parent_sub.sub_groups = tanium_ng.GroupList()
    result.sub_groups.append(parent_sub)

    for idx, spec in enumerate(specs):
        # if they supplied a group object, use that instead of creating one
        if 'group_object' in spec:
            print("using group object instead of filter")
            parent_sub.sub_groups.append(spec['group_object'])
            continue

        first = idx == 0
        this_and = spec['filter'].get('and_flag', None)

        # if this is the first spec
        # add a group with a filter from this spec to the current parent_sub
        if first:
            new_group = create_group_with_filter_obj(spec)
            print('first: creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)

            if this_and is not None:
                print('applying and_flag {} to parent_sub'.format(this_and))
                parent_sub.and_flag = this_and
            continue

        # if this spec does not have and_flag
        # add a group with a filter from this spec to the current parent_sub
        if this_and is None:
            new_group = create_group_with_filter_obj(spec)
            print('not first: and is None, creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)
            continue

        # if this spec does have an and_flag and it doesn't match the current
        # parent_sub's and, create a new parent_sub
        # add a group with a filter from this spec to the new parent_sub
        if parent_sub.and_flag != this_and:
            print('not first:, and is {} creating a new parent_sub'.format(this_and))
            parent_sub = tanium_ng.Group()
            parent_sub.and_flag = this_and
            parent_sub.sub_groups = tanium_ng.GroupList()
            result.sub_groups.append(parent_sub)

            new_group = create_group_with_filter_obj(spec)
            print('not first: creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)
            continue

        new_group = create_group_with_filter_obj(spec)
        print('catch all: creating a new group and adding to parent_sub')
        print(spec['filter'])
        parent_sub.sub_groups.append(new_group)
        continue

    recurse_group(result)
    return result


def recurse_group(g, level=1):
    """pass"""
    sglen = len(g.sub_groups or [])
    flen = len(g.filters or [])

    a = "level: {}, and_flag: {}, filters: {}, sub_groups: {}"
    a = a.format(level, g.and_flag, flen, sglen)
    print(a)

    if g.filters:
        for i in g.filters:
            f = "operator: {0.operator} value: {0.value}".format(i)
            m = "level: {}, and_flag: {}, filter: {}"
            m = m.format(level, g.and_flag, f)
            print(m)

    if g.sub_groups:
        for i in g.sub_groups:
            recurse_group(i, level + 1)


def create_question_obj(left=[], right=[]):
    """pass."""
    result = tanium_ng.Question()
    result.selects = create_selectlist_obj(left)
    if right:
        result.group = create_parent_group_obj(right)
    return result


def check_limits(objects, **kwargs):
    """pass."""
    specs = kwargs.get('specs', [])

    if not isinstance(objects, tanium_ng.BaseType):
        err = "{} must be a tanium_ng object, type: {}"
        err = err.format(objects, type(objects))
        raise exceptions.PytanError(err)

    # coerce single items into a list
    objects_class = objects.__class__.__name__
    if not objects_class.endswith('List'):
        new_class = objects_class + 'List'
        new_objects = getattr(tanium_ng, new_class)()
        new_objects.append(objects)
        objects = new_objects

    limit_map = [
        {'k': 'limit_min', 'm': "{} items or more", 'e': '>='},
        {'k': 'limit_max', 'm': "{} items or less", 'e': '<='},
        {'k': 'limit_exact', 'm': "{} items exactly", 'e': '=='},
    ]

    for l in limit_map:
        limit_val = kwargs.get(l['k'], None)

        if limit_val is None:
            m = "check_limits(): found {}, skipped {} (not supplied)"
            m = m.format(objects, l['k'], )
            mylog.debug(m)
            continue

        limit_val = int(limit_val)
        e = "len(objects) {} limit_val".format(l['e'])
        limit_pass = eval(e)

        p = "check_limits(): found {}, {} {} (must be {})"
        limit_msg = l['m'].format(limit_val)

        if limit_pass:
            m = p.format(objects, 'PASSED', l['k'], limit_msg)
            mylog.debug(m)
        else:
            # get the str of each objects for printing in exception
            objtxt = '\n\t'.join([str(x) for x in objects])

            # get the specs txt if any specs
            specstxt = "\n"
            if specs:
                specstxt = "\nspecs:\n\t" + "\n\t".join([str(x) for x in specs]) + "\n"

            err_pre = p.format(objects, 'FAILED', l['k'], limit_msg)
            err = "{}{}returned items:\n\t{}"
            err = err.format(err_pre, specstxt, objtxt)
            mylog.critical(err)
            raise exceptions.PytanError(err)


def question_start_time(q):
    """Caclulates the start time of a question by doing q.expiration - q.expire_seconds

    Parameters
    ----------
    q : :class:`tanium_ng.Question`
        * Question object to calculate start time for

    Returns
    -------
    tuple : str, datetime
        * a tuple containing the start time first in str format for Tanium Server API, second in
        datetime object format
    """
    expire_dt = tools.timestr_to_datetime(q.expiration)
    expire_seconds_delta = datetime.timedelta(seconds=q.expire_seconds)
    start_time_dt = expire_dt - expire_seconds_delta
    start_time = tools.datetime_to_timestr(start_time_dt)
    result = (start_time, start_time_dt)
    return result


def create_options_obj(**kwargs):
    result = tanium_ng.Options()

    for k, v in kwargs.items():
        if hasattr(result, k):
            m = "Setting Options attribute {!r} to value '{}'".format
            mylog.debug(m(k, v))
            setattr(result, k, v)
    return result
