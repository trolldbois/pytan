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


from pytan.tickle import tools
from pytan.tickle import monkey

__all__ = [
    'ET',
    'tools',
    'monkey',
]
