import logging
import json

from pytan import PytanError
from pytan.tanium_ng import BaseType, BASE_TYPES
from pytan.constants import XMLNS, SUPER_VERBOSE

from pytan.tickle import ET
from pytan.tickle.constants import TAG_NAME, LIST_NAME, EXPLODE_NAME, FLAT_WARN, SSE_WRAP

MYLOG = logging.getLogger(__name__)


class XmlDeserializeError(PytanError):
    pass


class DictDeserializeError(PytanError):
    pass


class XmlParseError(PytanError):
    pass


class FromXML(object):

    ORIGINAL_XML = ''
    ORIGINAL_TREE = None
    RESULT = None

    TARGET_TREE = None
    TARGET_SOURCE = ''
    TARGET_CLASS = None

    def __init__(self, xml, **kwargs):
        self.ORIGINAL_XML = xml
        self.ORIGINAL_TREE = ET.fromstring(xml)
        self.find_target_tree()
        self.get_result_from_target_tree(**kwargs)

    def get_result_from_target_tree(self, **kwargs):
        self.RESULT = from_tree(self.TARGET_TREE, **kwargs)

        m = "Converted tree {!r} from source {!r} into tanium_ng object:: {}"
        m = m.format(self.TARGET_TREE.tag, self.TARGET_SOURCE, self.RESULT)
        MYLOG.info(m)

        attrs = ['ORIGINAL_XML', 'ORIGINAL_TREE', 'TARGET_TREE', 'TARGET_SOURCE']
        for a in attrs:
            setattr(self.RESULT, '_' + a, getattr(self, a))

    def find_target_tree(self):
        # do we have a SOAP envelope?
        if self.ORIGINAL_TREE.tag.endswith('Envelope'):
            pre_xpath = './soap:Envelope/soap:Body/t:return/'

            # get the return tree that should be in under the Envelope
            return_tree = self.xpath_find(self.ORIGINAL_TREE, './soap:Body/t:return')

            # get the text of the command element that should be under the return_tree
            cmd = self.xpath_find(return_tree, './command', True).text

            # if the text of the command element is GetResultData or GetResultInfo,
            # there should be a non empty ResultXML element with CDATA text
            # that must be parsed into it's own element
            if cmd in ['GetResultData', 'GetResultInfo']:
                resultxml_return = self.xpath_find(return_tree, './ResultXML', True)
                resultxml_tree = ET.fromstring(resultxml_return.text)
                self.TARGET_TREE = resultxml_tree
                self.TARGET_SOURCE = '{}ResultXML for command {!r}'.format(pre_xpath, cmd)
            # for other commands, there should be a result_object with one child element
            # i.e. "questions", "sensors", "actions", ...
            else:
                result_object_tree = self.xpath_find(return_tree, './result_object/*')
                self.TARGET_TREE = result_object_tree
                self.TARGET_SOURCE = '{}result_object/* for command {!r}'.format(pre_xpath, cmd)
        # is the XML just a straight representation of a tanium_ng object?
        elif self.ORIGINAL_TREE.tag in BASE_TYPES:
            self.TARGET_TREE = self.ORIGINAL_TREE
            self.TARGET_SOURCE = 'straight tanium_ng tag {!r}'.format(self.ORIGINAL_TREE.tag)
        # XML tag is unknown, throw exception
        else:
            err = "Unkwown tag {!r} found, unable to process XML:\n{}"
            err = err.format(self.ORIGINAL_TREE.tag, self.ORIGINAL_XML)
            MYLOG.error(err)
            raise XmlParseError(err)

    def xpath_find(self, tree, xpath, fail_empty=False):
        result = tree.find(xpath, XMLNS)

        if tree == self.ORIGINAL_TREE:
            parent_tree = ''
        else:
            parent_tree = ' child tree of {!r}'.format(self.ORIGINAL_TREE.tag)

        if result is None:
            err = "No element found using xpath {!r} in tree {!r}{}"
            err = err.format(xpath, tree.tag, parent_tree)
            MYLOG.error(err)
            raise XmlParseError(err)

        if fail_empty and not result.text:
            err = "Element {!r} with no text returned using xpath {!r} in tree {!r}{}"
            err = err.format(result.tag, xpath, tree.tag, parent_tree)
            MYLOG.error(err)
            raise XmlParseError(err)

        m = "Found element {!r} using xpath {!r} in tree {!r}{}"
        m = m.format(result.tag, xpath, tree.tag, parent_tree)
        MYLOG.debug(m)

        return result


class FromTree(object):
    """Convert an XML String or an ElementTree object into a tanium_ng BaseType object.

    x = FromTree(objtree=ElementTreeObject, objclass=tanium_ng.Sensor)

    Get RESULT:
    x.RESULT
    """

    RESULT = None
    """tanium_ng object that gets created from OBJTREE as a OBJCLASS"""

    OBJTREE = None
    """ElementTree object to convert into a tanium_ng object"""

    OBJCLASS = None
    """Taniumg NG object class to create RESULT as"""

    def __init__(self, objtree, **kwargs):
        self.OBJTREE = objtree
        self.get_objclass(**kwargs)
        self.get_result()

    def get_result(self):
        self.RESULT = self.OBJCLASS()
        self.RESULT._OBJTREE = self.OBJTREE
        self.base_simple()
        self.base_complex()
        self.base_list()

        if hasattr(self.RESULT, '_post_xml_hook'):
            self.RESULT._post_xml_hook()

        if SUPER_VERBOSE:
            m = "Converted tree {!r} into tanium_ng object:: {}"
            m = m.format(self.OBJTREE.tag, type(self.RESULT))
            MYLOG.debug(m)

    def get_objclass(self, **kwargs):
        objclass = kwargs.get('objclass', '')
        if objclass:
            self.OBJCLASS = objclass
        else:
            if self.OBJTREE.tag in BASE_TYPES:
                self.OBJCLASS = BASE_TYPES[self.OBJTREE.tag]
            else:
                err = "Tag {!r} matches no known tanium_ng object"
                err = err.format(self.OBJTREE.tag)
                MYLOG.error(err)
                raise XmlDeserializeError(err)

    def get_xpath(self, prop):
        """pass."""
        xpath = "./{}".format(prop)
        overrides = getattr(self.RESULT, '_OVERRIDE_XPATH', {})
        if prop in overrides:
            xpath = overrides[prop]
        return xpath

    def base_simple(self):
        """Process the simple properties for the tanium_ng object"""
        for prop, prop_type in self.RESULT._SIMPLE_PROPS.items():
            xpath = self.get_xpath(prop)
            prop_el = self.OBJTREE.find(xpath)
            if prop_el is not None and prop_el.text:
                setattr(self.RESULT, prop, prop_type(prop_el.text))
            else:
                setattr(self.RESULT, prop, None)

    def base_complex(self):
        """Process the complex properties for the tanium_ng object"""
        for prop, prop_type in self.RESULT._COMPLEX_PROPS.items():
            xpath = self.get_xpath(prop)
            prop_elems = self.OBJTREE.findall(xpath)
            if len(prop_elems) > 1:
                err = 'Found {} elements for property {}, should only be 1 (xpath: {})'
                err = err.format(len(prop_elems), prop, xpath)
                MYLOG.error(err)
                raise XmlDeserializeError(err)
            elif len(prop_elems) == 1:
                setattr(self.RESULT, prop, from_tree(prop_elems[0], objclass=prop_type))
            else:
                setattr(self.RESULT, prop, None)

    def base_list(self):
        """Process the list properties for the tanium_ng object"""
        for prop, prop_type in self.RESULT._LIST_PROPS.items():
            xpath = self.get_xpath(prop)
            prop_elems = self.OBJTREE.findall(xpath)
            prop_list = []
            for prop_elem in prop_elems:
                if issubclass(prop_type, BaseType):
                    prop_list.append(from_tree(prop_elem, objclass=prop_type))
                else:
                    prop_list.append(prop_elem.text)
            setattr(self.RESULT, prop, prop_list)


class FromDict(object):
    """Convert a single or list of dict into a tanium_ng BaseType object

    x = FromDict(obj=python_dict)
        .. or ..
    x = FromDict(obj=[python_dict])

    Get RESULT:
    x.RESULT
    """

    RESULT = None
    """single or list of tanium_ng objects created from OBJ"""

    OBJ = None
    """python object to create RESULT from"""

    def __init__(self, obj, **kwargs):
        self.OBJ = obj
        self.RESULT = None

        if not self.OBJ:
            err = "Must supply a non-empty obj!"
            MYLOG.error(err)
            raise DictDeserializeError(err)

        if isinstance(self.OBJ, list):
            self.handle_list()
        elif isinstance(self.OBJ, dict):
            self.handle_dict()
        else:
            err = "obj is {}, must be a list or dict, unable to deserialize!"
            err = err.format(type(self.OBJ))
            MYLOG.error(err)
            raise DictDeserializeError(err)

    def handle_list(self):
        self.RESULT = [from_dict(v) for v in self.OBJ]
        m = "Converted list of dict with {} items into {} Tanium NG objects"
        m = m.format(len(self.OBJ, len(self.RESULT)))
        MYLOG.debug(m)

    def handle_dict(self, **kwargs):
        if list(FLAT_WARN.keys())[0] in self.OBJ:
            err = "Unable to deserialize flattened objects!"
            MYLOG.error(err)
            raise DictDeserializeError(err)

        if LIST_NAME in self.OBJ:
            self.handle_dict_list()
        elif TAG_NAME in self.OBJ:
            self.handle_dict_item()
        else:
            err = "Dictionary missing attribute {!r} or {!r}, unable to deserialize!"
            err = err.format(TAG_NAME, LIST_NAME)
            MYLOG.error(err)
            raise DictDeserializeError(err)

    def handle_dict_list(self):
        self.RESULT = [from_dict(v) for v in self.OBJ[LIST_NAME]]
        m = "Converted list of dict with {} items into:: {} Tanium NG objects"
        m = m.format(len(self.OBJ), len(self.RESULT))
        MYLOG.debug(m)

    def handle_dict_item(self):
        soap_tag = self.OBJ[TAG_NAME]

        if soap_tag in BASE_TYPES:
            target_class = BASE_TYPES[soap_tag]
        else:
            err = "Dictionary attribute {!r}: {!r} matches no known tanium_ng object"
            err = err.format(TAG_NAME, soap_tag)
            MYLOG.error(err)
            raise DictDeserializeError(err)

        self.RESULT = target_class()
        self.base_simple()
        self.base_complex()
        self.base_list()

        if SUPER_VERBOSE:
            m = "Converted dict with keys '{}' into tanium_ng object:: {}"
            m = m.format(', '.join(self.OBJ.keys()), type(self.RESULT))
            MYLOG.debug(m)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop, prop_type in self.RESULT._SIMPLE_PROPS.items():
            val = self.OBJ.get(prop, None)
            if val is None:
                continue
            if isinstance(val, dict) and EXPLODE_NAME in val:
                val = json.dumps(val[EXPLODE_NAME])
            setattr(self.RESULT, prop, prop_type(val))

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.RESULT._COMPLEX_PROPS:
            val = self.OBJ.get(prop, None)
            if val is None:
                continue
            setattr(self.RESULT, prop, from_dict(val))

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.RESULT._LIST_PROPS.items():
            vals = self.OBJ.get(prop, None)
            if vals is None:
                continue

            new_vals = []
            for val in vals:
                if issubclass(prop_type, BaseType):
                    new_vals.append(from_dict(val))
                else:
                    new_vals.append(val)
            setattr(self.RESULT, prop, new_vals)


def from_dict(obj, **kwargs):
    converter = FromDict(obj, **kwargs)
    result = converter.RESULT
    return result


def from_json(jsonstr, **kwargs):
    obj = json.loads(jsonstr)
    result = from_dict(obj, **kwargs)
    return result


def from_tree(objtree, **kwargs):
    converter = FromTree(objtree, **kwargs)
    result = converter.RESULT
    return result


def from_xml(xml, **kwargs):
    converter = FromXML(xml, **kwargs)
    result = converter.RESULT
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
    info_overlay = kwargs.get('info_overlay', None)
    rs_xml = SSE_WRAP.format(SSE_DATA=xml)
    result = from_xml(rs_xml, **kwargs)
    if info_overlay:
        result.now = info_overlay.now
        for k in info_overlay.result_info._SIMPLE_PROPS:
            setattr(result.result_set, k, getattr(info_overlay.result_info, k))
    return result
