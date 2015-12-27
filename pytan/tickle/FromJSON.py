import json

from pytan import tanium_ng
from pytan.tickle import DeserializeError
from pytan.tickle.constants import TAG_NAME, LIST_NAME, EXPLODE_NAME


class FromJSON(object):
    """Convert a JSON string or a single or list of dict into a tanium_ng BaseType object

    x = FromJSON(jsonstr=json_str)
        .. or ..
    x = FromJSON(pyobj=python_dict)
        .. or ..
    x = FromJSON(pyobj=[python_dict])

    Get PYOBJ:
    x.PYOBJ

    Get OBJ:
    x.OBJ
    """

    _TAG_NAME = TAG_NAME
    """attribute to hold OBJ._SOAP_TAG so tickle can deserialize into an OBJ"""

    _LIST_NAME = LIST_NAME
    """attribute to hold list of serialized OBJs"""

    _EXPLODE_PROP = EXPLODE_NAME
    """attribute to identify JSON exploded property value"""

    OBJ = None
    """single or list of tanium_ng objects created from PYOBJ"""

    PYOBJ = None
    """python object created from JSON"""

    JSONSTR = ''
    """json string to create PYOBJ from"""

    def __init__(self, **kwargs):
        # print("New FromJSON for obj: {}".format(obj))
        self.KWARGS = kwargs
        self.JSONSTR = kwargs.get('jsonstr', self.JSONSTR)
        self.PYOBJ = kwargs.get('pyobj', self.PYOBJ)
        self.OBJ = None

        if self.JSONSTR and not self.PYOBJ:
            self.PYOBJ = json.loads(self.JSONSTR)

        if not self.PYOBJ:
            err = "Must supply a non-empty jsonstr or non-empty pyobj!"
            raise DeserializeError(err)

        # TODO: this wont work, need to check for _tickled_list ??
        if isinstance(self.PYOBJ, list):
            self.OBJ = [FromJSON(pyobj=v).OBJ for v in self.PYOBJ]
        elif isinstance(self.PYOBJ, dict):
            if self._LIST_NAME in self.PYOBJ:
                self.OBJ = [FromJSON(pyobj=v).OBJ for v in self.PYOBJ[self._LIST_NAME]]
            else:
                if self._TAG_NAME not in self.PYOBJ:
                    err = "JSON missing attribute {!r}, unable to deserialize!"
                    err = err.format(self._TAG_NAME)
                    raise DeserializeError(err)
                soap_tag = self.PYOBJ[self._TAG_NAME]
                self.OBJ = tanium_ng.get_obj_type(soap_tag)()
                self.base_simple()
                self.base_complex()
                self.base_list()
        else:
            err = "JSON contained {}, must contain either a list or dict, unable to deserialize!"
            err = err.format(type(self.PYOBJ))
            raise DeserializeError(err)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._SIMPLE_PROPS.items():
            val = self.PYOBJ.get(prop, None)
            if val is None:
                continue
            if isinstance(val, dict) and self._EXPLODE_PROP in val:
                val = json.dumps(val[self._EXPLODE_PROP])
            setattr(self.OBJ, prop, prop_type(val))

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = self.PYOBJ.get(prop, None)
            if val is None:
                continue
            setattr(self.OBJ, prop, FromJSON(pyobj=val).OBJ)

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = self.PYOBJ.get(prop, None)
            if vals is None:
                continue

            new_vals = []

            for val in vals:
                if issubclass(prop_type, tanium_ng.BaseType):
                    new_vals.append(FromJSON(pyobj=val).OBJ)
                else:
                    new_vals.append(val)
            setattr(self.OBJ, prop, new_vals)
