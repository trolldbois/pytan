from pytan import PytanError, tanium_ng
from pytan.tickle import ET
from pytan.tickle.from_tree import from_tree
from pytan.tickle.constants import SSE_WRAP


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
            self.RESULT = from_tree(self.TARGET_TREE, self.TARGET_CLASS, **kwargs)
        else:
            self.RESULT = self.TARGET_CLASS()

        self.RESULT._XML = xml
        self.RESULT._FULL_TREE = self.FULL_TREE
        self.RESULT._TARGET_TREE = self.TARGET_TREE


def from_xml(xml, **kwargs):
    converter = FromXML(xml=xml, **kwargs)
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
    rs_xml = SSE_WRAP.format(SSE_DATA=xml)
    result = from_xml(rs_xml, **kwargs)
    return result
