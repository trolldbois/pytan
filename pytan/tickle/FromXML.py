from pytan import tanium_ng
from pytan.tickle import ET, DeserializeError
from pytan.tickle.constants import OBJECT_XPATH, RESULT_XPATH


class FromXML(object):
    """Convert an XML String or an ElementTree object into a tanium_ng BaseType object.

    x = FromXML(xml=xml_text)
        ..or..
    x = FromXML(objclass=tanium_ng.Sensor, objtree=ElementTreeObject)

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

    _OBJECT_XPATH = OBJECT_XPATH
    _RESULT_XPATH = RESULT_XPATH

    def __init__(self, **kwargs):
        # print("New FromXML kwargs: {}".format(kwargs))
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
            raise DeserializeError(err)

    def check_object_in_tree(self):
        """Try to find a result object in self.XMLTREE"""
        objtree = self.XMLTREE.find(self._OBJECT_XPATH)

        # m = "check_object_in_tree(): xpath: {} objtree: {}"
        # m = m.format(self.OBJECT_XPATH, objtree)
        # print(m)

        if objtree is not None:
            # print("setting self.OBJTREE to object found")
            self.OBJTREE = objtree

    def check_result_in_tree(self):
        objtree = self.XMLTREE.find(self._RESULT_XPATH)
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
                raise DeserializeError(err)
            elif len(prop_elems) == 1:
                val_pickle = FromXML(objclass=prop_type, objtree=prop_elems[0])
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
                    val_pickle = FromXML(objclass=prop_type, objtree=prop_elem)
                    prop_list.append(val_pickle.OBJ)
                else:
                    prop_list.append(prop_elem.text)
            setattr(self.OBJ, prop, prop_list)
