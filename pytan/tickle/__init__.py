import sys
import logging

from pytan import PytanError

from pytan.tickle.constants import XML_ENGINE, XML_ENGINES

MYLOG = logging.getLogger(__name__)


class XMLEngineError(PytanError):
    pass


ET = None

if XML_ENGINE in XML_ENGINES:
    try:
        __import__(XML_ENGINES[XML_ENGINE])
        ET = sys.modules[XML_ENGINES[XML_ENGINE]]
        m = "Using {} for XML engine"
        m = m.format(XML_ENGINES[XML_ENGINE])
        MYLOG.debug(m)
        fallback = False
    except ImportError as e:
        m = "XML engine {} failed to import: {}"
        m = m.format(XML_ENGINES[XML_ENGINE], e)
        MYLOG.warning(m)
        fallback = True
else:
    fallback = True

if fallback:
    for k, v in XML_ENGINES.items():
        try:
            __import__(v)
            ET = sys.modules[v]
            m = "Using {} for XML engine"
            m = m.format(v)
            MYLOG.debug(m)
        except ImportError as e:
            m = "XML engine {} failed to import: {}"
            m = m.format(XML_ENGINES[XML_ENGINE], e)
            MYLOG.warning(m)

if ET is None:
    err = "Failed to import any XML Engine!"
    MYLOG.critical(err)
    raise XMLEngineError(err)


ElementType = type(ET.Element(None))
"""Established for type checking since cElementTree does not have an ElementType class"""

from pytan.constants import XMLNS

# register our XML namespaces so ET can properly parse/unparse our XML documents
for k, v in XMLNS.items():
    ET.register_namespace(k, v)


from pytan.tickle.serialize import (
    to_xml, to_tree, to_dict, to_json, to_csv, to_dict_resultset, to_json_resultset,
    to_csv_resultset
)

from pytan.tickle.deserialize import from_xml, from_sse_xml, from_tree, from_dict, from_json

from pytan.tanium_ng import BaseType, ResultSetList, ResultSet
from pytan.tickle import tools


__all__ = [
    'ET',
    'tools',
    'to_xml',
    'to_tree',
    'to_dict',
    'to_json',
    'to_csv',
    'to_dict_resultset',
    'to_json_resultset',
    'to_csv_resultset',
    'from_xml',
    'from_sse_xml',
    'from_tree',
    'from_dict',
    'from_json',
]


def monkey_to_xml(self, **kwargs):
    """Serialize self into an XML body, relies on tickle"""
    result = to_xml(self, **kwargs)
    return result


def monkey_to_dict(self, **kwargs):
    """Serialize self into a dict, relies on tickle"""
    result = to_dict(self, **kwargs)
    return result


def monkey_to_json(self, **kwargs):
    """Serialize self into a JSON string, relies on tickle"""
    result = to_json(self, **kwargs)
    return result


def monkey_to_csv(self, **kwargs):
    """Serialize self into a CSV string, relies on tickle"""
    result = to_csv(self, **kwargs)
    return result


def monkey_to_csv_resultset(self, **kwargs):
    """Serialize self into a CSV string, relies on tickle"""
    result = to_csv_resultset(self, **kwargs)
    return result


def monkey_to_json_resultset(self, **kwargs):
    """Serialize self into a JSON string, relies on tickle"""
    result = to_json_resultset(self, **kwargs)
    return result


def monkey_to_dict_resultset(self, **kwargs):
    """Serialize self into a list of dicts, relies on tickle"""
    result = to_dict_resultset(self, **kwargs)
    return result


# add the wrappers to pytan.tanium_ng.BaseType for ease of access
BaseType.to_xml = monkey_to_xml
BaseType.to_dict = monkey_to_dict
BaseType.to_json = monkey_to_json
BaseType.to_csv = monkey_to_csv
# add the wrappers to pytan.tanium_ng.ResultSetList for ease of access
ResultSetList.to_csv_resultset = monkey_to_csv_resultset
ResultSetList.to_json_resultset = monkey_to_json_resultset
ResultSetList.to_dict_resultset = monkey_to_dict_resultset
# add the wrappers to pytan.tanium_ng.ResultSet for ease of access
ResultSet.to_csv_resultset = monkey_to_csv_resultset
ResultSet.to_json_resultset = monkey_to_json_resultset
ResultSet.to_dict_resultset = monkey_to_dict_resultset

# add the wrappers to pytan.tickle.tools for ease of access
tools.to_xml = to_xml
tools.to_tree = to_tree
tools.to_dict = to_dict
tools.to_json = to_json
tools.to_csv = to_csv
tools.to_dict_resultset = to_dict_resultset
tools.to_json_resultset = to_json_resultset
tools.to_csv_resultset = to_csv_resultset
tools.from_xml = from_xml
tools.from_sse_xml = from_sse_xml
tools.from_tree = from_tree
tools.from_dict = from_dict
tools.from_json = from_json
tools.ET = ET
