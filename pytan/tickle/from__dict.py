import logging
import json

from pytan import PytanError
from pytan.tanium_ng import BaseType, BASE_TYPES

from pytan.tickle.constants import TAG_NAME, LIST_NAME, EXPLODE_NAME, FLAT_WARN, SUPER_VERBOSE

MYLOG = logging.getLogger(__name__)


class DictDeserializeError(PytanError):
    pass


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
