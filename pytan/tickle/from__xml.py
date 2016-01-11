import logging

from pytan import PytanError
from pytan.tickle import ET
from pytan.tickle.from__tree import from_tree

from pytan.constants import XMLNS
from pytan.tanium_ng import BASE_TYPES
from pytan.tickle.constants import SSE_WRAP

MYLOG = logging.getLogger(__name__)


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
    rs_xml = SSE_WRAP.format(SSE_DATA=xml)
    result = from_xml(rs_xml, **kwargs)
    return result
