import json

from pytan import tanium_ng
from pytan.tickle.constants import (
    TAG_NAME, LIST_NAME, EXPLODE_NAME, FLAT_WARN, JSON_INDENT, FLAT_SEP, JSON_SORT_KEYS,
    INCLUDE_EMPTY
)


class ToJSON(object):
    """Convert either a single or list of tanium_ng BaseType objects into a python
    dict object and then into a JSON string

    x = ToJSON(obj)
     ..or..
    x = ToJSON([obj])

    Get DICT:
    x.DICT

    Get JSON:
    x.JSON
    """

    _TAG_NAME = TAG_NAME
    """attribute to store OBJ._SOAP_TAG so tickle can deserialize into an OBJ later"""

    _LIST_NAME = LIST_NAME
    """attribute to hold list of serialized OBJs"""

    _EXPLODE_PROP = EXPLODE_NAME
    """attribute to identify JSON exploded property value"""

    _FLAT_WARNING = FLAT_WARN
    """dict to update DICT with if FLAT=True"""

    _PROP_PRE = ''
    """str that holds FLAT_PRE + _FLAT_SEP IF FLAT=True"""

    _PARENT = True
    """bool to indicate if this is the first spawn of this object"""

    _INDENT = JSON_INDENT
    """int that controls how many spaces will be used to pretty print the JSON, None to disable"""

    _EMPTY = INCLUDE_EMPTY

    _PARENT = True

    FLAT = False
    """bool that controls if all nested objects of OBJ will be flattened out when creating DICT"""

    _SORT_KEYS = JSON_SORT_KEYS

    _FLAT_PRE = ''
    """str to prefix property names if FLAT=True"""

    _FLAT_SEP = FLAT_SEP
    """str to seperate FLAT_PRE and property name with if FLAT=True"""

    OBJ = None
    """tanium_ng object to convert to DICT"""

    DICT = {}
    """dict created from OBJ"""

    JSON = ''
    """json string created from DICT"""

    def __init__(self, obj, **kwargs):
        # print("New ToJSON for obj: {}".format(obj))
        self.KWARGS = kwargs
        self._PARENT = kwargs.get('parent', self._PARENT)
        self._EMPTY = kwargs.get('empty', self._EMPTY)
        self._INDENT = kwargs.get('indent', self._INDENT)
        self._SORT_KEYS = kwargs.get('sort_keys', self._SORT_KEYS)

        self.FLAT = kwargs.get('flat', self.FLAT)
        self._FLAT_PRE = kwargs.get('flat_pre', self._FLAT_PRE)
        self._FLAT_SEP = kwargs.get('_flat_sep', self._FLAT_SEP)

        if self.FLAT and self._FLAT_PRE and not self._PARENT:
            self._PROP_PRE = '{}{}'.format(self._FLAT_PRE, self._FLAT_SEP)
        else:
            self._PROP_PRE = ''

        self.OBJ = obj
        self.DICT = {}
        self.JSON = ''

        if isinstance(self.OBJ, list):
            self.do_list()
        else:
            if self.OBJ._IS_LIST and self.FLAT and self._PARENT:
                self.do_list()
            else:
                self.do_obj()

        if self._PARENT:
            self.JSON = json.dumps(self.DICT, indent=self._INDENT, sort_keys=self._SORT_KEYS)

    def do_obj(self):
        if self.FLAT:
            self.DICT.update(self._FLAT_WARNING)
        self.DICT[self._TAG_NAME] = self.OBJ._SOAP_TAG
        self.base_simple()
        self.base_complex()
        self.base_list()
        self.DICT[self._TAG_NAME] = self.OBJ._SOAP_TAG

    def do_list(self):
        if self.FLAT:
            self.DICT.update(self._FLAT_WARNING)

        try:
            self.DICT[self._TAG_NAME] = self.OBJ._SOAP_TAG
        except:
            pass

        self.DICT[self._LIST_NAME] = []
        for val in self.OBJ:
            tickle_args = {}
            tickle_args.update(self.KWARGS)
            tickle_args.update({'parent': False, 'obj': val})
            val = ToJSON(**tickle_args).DICT
            self.DICT[self._LIST_NAME].append(val)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self._EMPTY:
                continue

            prop_name = '{}{}'.format(self._PROP_PRE, prop)

            val_json = explode_json(val)

            if val_json:
                if self.FLAT:
                    val = flatten_pyobj(val_json, prefix=prop_name, sep=self._FLAT_SEP)
                    self.DICT.update(val)
                else:
                    self.DICT[self._EXPLODE_PROP] = val_json
            else:
                self.DICT[prop_name] = val

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self._EMPTY:
                continue

            prop_name = '{}{}'.format(self._PROP_PRE, prop)

            if val is not None:
                tickle_args = {}
                tickle_args.update(self.KWARGS)
                tickle_args.update({'parent': False, 'obj': val, 'flat_pre': prop_name})
                val = ToJSON(**tickle_args).DICT
                if self.FLAT:
                    self.DICT.update(val)
                else:
                    self.DICT[prop_name] = val
            else:
                self.DICT[prop_name] = val

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = getattr(self.OBJ, prop)
            if not vals and not self._EMPTY:
                continue

            new_vals = []
            for idx, val in enumerate(vals):
                # if self.FLAT:
                prop_name = '{}{}{}{}'.format(self._PROP_PRE, prop, self._FLAT_SEP, idx)
                # else:
                # prop_name = prop

                if issubclass(prop_type, tanium_ng.BaseType):
                    tickle_args = {}
                    tickle_args.update(self.KWARGS)
                    tickle_args.update({'parent': False, 'obj': val, 'flat_pre': prop_name})
                    val = ToJSON(**tickle_args).DICT
                    new_vals.append(val)
                else:
                    if self.FLAT:
                        new_vals.append({prop_name: val})
                    else:
                        new_vals.append(val)

            if self.FLAT and not self._PARENT:
                [self.DICT.update(v) for v in new_vals]
            else:
                self.DICT[prop] = new_vals


def explode_json(val):
    """pass."""
    try:
        result = json.loads(val)
        # only explode non str/int types
        if not isinstance(result, (list, tuple, dict)):
            result = None
    except:
        result = None
    return result


def flatten_pyobj(pyobj, prefix='', sep='_'):
    """pass."""
    result = {}
    if isinstance(pyobj, (list, tuple)):
        for idx, val in enumerate(pyobj):
            mypre = '{}{}{}'.format(prefix, sep, idx)
            result.update(flatten_pyobj(val, mypre, sep))
    elif isinstance(pyobj, dict):
        for k, v in pyobj.items():
            mypre = '{}{}{}'.format(prefix, sep, k)
            result.update(flatten_pyobj(v, mypre, sep))
    else:
        if not prefix:
            prefix = type(pyobj).__name__
        result[prefix] = pyobj
    return result
