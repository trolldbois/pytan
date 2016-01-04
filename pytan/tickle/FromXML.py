from pytan import PytanError, tanium_ng
from pytan.tickle import ET
from pytan.tickle.fromet import FromET


# TODO LOGGING
class FromXML(object):
    """Convert an XML String into a tanium_ng BaseType object.

    x = FromXML(xml=xml_text)

    Get RESULT:
    x.RESULT
    """

    RESULT = None
    """tanium_ng object that gets created from OBJTREE"""

    XML = ''
    """XML string to convert into a tanium_ng object"""

    OBJECT_XPATH = ".//result_object/*"
    """str of xpath to find objects in Tanium SOAP API XML"""
    DATA_XPATH = ".//ResultXML"
    """str of xpath to find result data/result info in Tanium SOAP API XML"""

    def __init__(self, xml, **kwargs):
        self.FULL_TREE = ET.fromstring(xml)
        self.OBJECT_TREE = self.FULL_TREE.find(self.OBJECT_XPATH)
        self.TARGET_TREE = self.OBJECT_TREE

        self.DATA_TREE = self.FULL_TREE.find(self.DATA_XPATH)
        self.CDATA_TREE = None
        if self.DATA_TREE is not None:
            if self.DATA_TREE.text:
                self.CDATA_TREE = ET.fromstring(self.DATA_TREE.text)
                if self.CDATA_TREE is not None:
                    self.TARGET_TREE = self.CDATA_TREE

        if self.OBJECT_TREE is not None and self.CDATA_TREE is not None:
            err = "Found data {} in tree, but object {} already found in tree: {}"
            err = err.format(self.CDATA_TREE, self.OBJECT_TREE, self.FULL_TREE)
            raise PytanError(err)  # TODO MAKE OWN EXCEPTION

        if self.TARGET_TREE is not None:
            self.TARGET_CLASS = tanium_ng.get_obj_type(self.TARGET_TREE.tag)

            converter = FromET(self.TARGET_TREE, self.TARGET_CLASS, **kwargs)
            self.RESULT = converter.RESULT
        else:
            self.RESULT = self.TARGET_CLASS()

        self.RESULT._XML = xml
        self.RESULT._FULL_TREE = self.FULL_TREE
        self.RESULT._TARGET_TREE = self.TARGET_TREE
