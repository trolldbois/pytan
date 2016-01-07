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
            MYLOG.debug(m)

if ET is None:
    err = "Failed to import any XML Engine!"
    MYLOG.critical(err)
    raise XMLEngineError(err)


from pytan.tickle.to_tree import to_xml, to_tree
from pytan.tickle.to_dict import to_dict, to_json, to_csv
from pytan.tickle.from_xml import from_xml, from_sse_xml
from pytan.tickle.from_tree import from_tree
from pytan.tickle.from_dict import from_dict, from_json
from pytan.tickle.to_dict_report import to_dict_report, to_json_report, to_csv_report
from pytan import tanium_ng
from pytan.tickle import tools

__all__ = [
    'ET',
    'tools',
    'to_xml',
    'to_tree',
    'to_dict',
    'to_json',
    'to_csv',
    'to_dict_report',
    'to_json_report',
    'to_csv_report',
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


def monkey_to_csv_report(self, **kwargs):
    """Serialize self into a CSV string, relies on tickle"""
    result = to_csv_report(self, **kwargs)
    return result


def monkey_to_json_report(self, **kwargs):
    """Serialize self into a JSON string, relies on tickle"""
    result = to_json_report(self, **kwargs)
    return result


def monkey_to_dict_report(self, **kwargs):
    """Serialize self into a list of dicts, relies on tickle"""
    result = to_dict_report(self, **kwargs)
    return result


tanium_ng.BaseType.to_xml = monkey_to_xml
tanium_ng.BaseType.to_dict = monkey_to_dict
tanium_ng.BaseType.to_json = monkey_to_json
tanium_ng.BaseType.to_csv = monkey_to_csv
tanium_ng.ResultSetList.to_csv_report = monkey_to_csv_report
tanium_ng.ResultSetList.to_json_report = monkey_to_json_report
tanium_ng.ResultSetList.to_dict_report = monkey_to_dict_report
