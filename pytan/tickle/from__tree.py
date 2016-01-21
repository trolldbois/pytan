import logging

from pytan import PytanError
from pytan.tanium_ng import BaseType, BASE_TYPES

from pytan.tickle.constants import SUPER_VERBOSE

MYLOG = logging.getLogger(__name__)


class XmlDeserializeError(PytanError):
    pass


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


def from_tree(objtree, **kwargs):
    converter = FromTree(objtree, **kwargs)
    result = converter.RESULT
    return result
