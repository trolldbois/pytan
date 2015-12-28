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


from pytan.tickle.FromJSON import FromJSON
from pytan.tickle.FromXML import FromXML
from pytan.tickle.ToJSON import ToJSON
from pytan.tickle.ToXML import ToXML
from pytan.tickle.constants import LIST_NAME, TAG_NAME, EXPLODE_NAME, FLAT_WARN, SSE_WRAP
from pytan.tickle import tools


# CONVENIENCE WRAPPERS AROUND TICKLE CLASSES::

def to_xml(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into an XML body using ObjectToXML"""
    tickle_val = ToXML(obj, **kwargs)
    result = tickle_val.XML
    return result


def to_dict(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a dict using ToJSON"""
    tickle_val = ToJSON(obj, **kwargs)
    result = tickle_val.DICT
    return result


def to_json(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a JSON string using ToJSON"""
    tickle_val = ToJSON(obj, **kwargs)
    result = tickle_val.JSON
    return result


def to_csv(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a CSV string using ToJSON"""
    # TODO FIGURE OUT ResultSet
    kwargs['skips'] = kwargs.get('skips', [])
    kwargs['sort'] = kwargs.get('sort', [])

    kwargs['flat'] = True

    tickle_val = ToJSON(obj, **kwargs)
    flat_obj = tickle_val.DICT

    if LIST_NAME in flat_obj:
        kwargs['rows'] = flat_obj[LIST_NAME]
    else:
        kwargs['rows'] = [flat_obj]

    default_sort = ['id', 'name', 'description']
    default_skip = [TAG_NAME, LIST_NAME, EXPLODE_NAME]
    default_skip += list(FLAT_WARN.keys())

    kwargs['sort'] += default_sort
    kwargs['skips'] += default_skip

    result = tools.csvdictwriter(**kwargs)
    return result


def from_json(jsonstr, **kwargs):
    """Deserialize a JSON string into a tanium_ng object sing FromJSON"""
    tickle_val = FromJSON(jsonstr=jsonstr, **kwargs)
    result = tickle_val.OBJ
    return result


def from_dict(pyobj, **kwargs):
    """Deserialize a dict or list of dicts into a tanium_ng object using FromJSON"""
    tickle_val = FromJSON(pyobj=pyobj, **kwargs)
    result = tickle_val.OBJ
    return result


def from_xml(xml, **kwargs):
    """Deserialize ``xml`` from XML into a tanium_ng object using FromXML."""
    tickle_val = FromXML(xml=xml, **kwargs)
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
    rs_xml = SSE_WRAP.format(SSE_DATA=xml)
    result = from_xml(rs_xml, **kwargs)
    return result
