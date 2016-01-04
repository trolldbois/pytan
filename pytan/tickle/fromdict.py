import json

from pytan import PytanError, tanium_ng
from pytan.tickle.constants import TAG_NAME, LIST_NAME, EXPLODE_NAME


class FromDict(object):
    """Convert a single or list of dict into a tanium_ng BaseType object

    x = FromDict(obj_dict=python_dict)
        .. or ..
    x = FromDict(obj_dict=[python_dict])

    Get RESULT:
    x.RESULT
    """

    RESULT = None
    """single or list of tanium_ng objects created from OBJ_DICT"""

    OBJ_DICT = None
    """python obj_dict to create OBJ from"""

    def __init__(self, obj_dict, **kwargs):
        # print("New FromDict for obj: {}".format(obj))
        self.OBJ_DICT = obj_dict
        self.RESULT = None

        if not self.OBJ_DICT:
            err = "Must supply a non-empty obj_dict!"
            raise DictDeserializeError(err)

        # TODO: this wont work, need to check for _tickled_list ??
        if isinstance(self.OBJ_DICT, list):
            self.RESULT = [FromDict(pyobj=v).RESULT for v in self.OBJ_DICT]
        elif isinstance(self.OBJ_DICT, dict):
            if LIST_NAME in self.OBJ_DICT:
                self.RESULT = [FromDict(pyobj=v).RESULT for v in self.OBJ_DICT[LIST_NAME]]
            else:
                if TAG_NAME not in self.OBJ_DICT:
                    err = "Dictionary missing attribute {!r}, unable to deserialize!"
                    err = err.format(TAG_NAME)
                    raise DictDeserializeError(err)
                soap_tag = self.OBJ_DICT[TAG_NAME]
                self.RESULT = tanium_ng.get_obj_type(soap_tag)()
                self.base_simple()
                self.base_complex()
                self.base_list()
        else:
            err = "obj_dict is {}, must be a list or dict, unable to deserialize!"
            err = err.format(type(self.OBJ_DICT))
            raise DictDeserializeError(err)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop, prop_type in self.RESULT._SIMPLE_PROPS.items():
            val = self.OBJ_DICT.get(prop, None)
            if val is None:
                continue
            if isinstance(val, dict) and EXPLODE_NAME in val:
                val = json.dumps(val[EXPLODE_NAME])
            setattr(self.RESULT, prop, prop_type(val))

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.RESULT._COMPLEX_PROPS:
            val = self.OBJ_DICT.get(prop, None)
            if val is None:
                continue
            converter = FromDict(obj_dict=val)
            setattr(self.RESULT, prop, converter.RESULT)

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.RESULT._LIST_PROPS.items():
            vals = self.OBJ_DICT.get(prop, None)
            if vals is None:
                continue

            new_vals = []
            for val in vals:
                if issubclass(prop_type, tanium_ng.BaseType):
                    converter = FromDict(obj_dict=val)
                    new_vals.append(converter.RESULT)
                else:
                    new_vals.append(val)
            setattr(self.RESULT, prop, new_vals)


class DictDeserializeError(PytanError):
    pass
