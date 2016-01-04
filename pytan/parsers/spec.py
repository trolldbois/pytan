import logging

from pytan import PytanError, string_types, integer_types, text_type, tanium_ng, tickle
from pytan.parsers.constants import (
    SPEC_FIELD_FALLBACKS, OPERATORS_PYTAN, OPERATORS_TANIUM, TRUE_TYPES, FALSE_TYPES, FIELD_TYPES
)

mylog = logging.getLogger(__name__)


def get_str(spec):
    """pass.

    Computer Name
    v:Computer Name
    val:Computer Name
    value:Computer Name
    Computer Name,f:name
    Computer Name, f:name
    Computer Name, field:name
    v:Computer Name, field:name
    val:Computer Name, field:name
    value:Computer Name, field:name
    value:Computer Name, f:name
    """
    # TODO
    err = "TODO"
    raise PytanError(err)


class Spec(object):
    """pass."""

    def __init__(self, **kwargs):
        self.tanium_ng = tanium_ng
        self.tickle = tickle
        self.post_init(**kwargs)

    def post_init(self, **kwargs):
        pass

    def chk_dict_key(self, k, d, types,):
        """pass."""
        if not isinstance(d[k], types):
            ttxt = ', '.join([x.__name__ for x in types])
            err = "{}: key {!r} must be one of type {!r}; supplied type {!r} value {!r}"
            err = err.format(self.meerr, k, ttxt, type(d[k]).__name__, d[k])
            raise PytanError(err)

    def has_dict_key(self, k, d):
        # check if d has key k
        if k not in d or d.get(k, '') == '':
            err = "{} key {!r} must be supplied and not empty in {!r}!"
            err = err.format(self.meerr, k, d)
            raise PytanError(err)

    def chk_value(self, spec):
        # if spec is a dict with out value defined
        # {"dievalue": "Computer Name"}
        self.has_dict_key('value', spec)

        # check that value is a string or int
        self.chk_dict_key('value', spec, string_types + integer_types)

        # TODO: reminder! value expects str
        # validate value is an appropriate type as defined in single_obj
        # obj_type = self.props[spec['field']]

        # validate value is a string
        if not isinstance(spec['value'], text_type):
            try:
                spec['value'] = text_type(spec['value'])
            except:
                obj_txt = text_type.__name__
                val_type = type(spec['value']).__name__
                err = "{}: key 'value' must be of type {!r}; supplied type {!r} value {!r}"
                err = err.format(self.meerr, obj_txt, val_type, spec['value'])
                raise PytanError(err)
        return spec

    def chk_field(self, spec):
        # if field not specified, and value exists and can be int'd, assume field is id
        # {'value': "1"}
        if 'field' not in spec and 'value' in spec:
            try:
                int(spec['value'])
                spec['field'] = 'id'
            except:
                pass

        # if field not specified, derive it based off fallbacks if they exist in single_obj
        # {"value": "Computer Name"}
        if 'field' not in spec:
            for x in SPEC_FIELD_FALLBACKS:
                if x not in self.props:
                    continue
                spec['field'] = x
                break

        # extra measure in case none of the fallbacks matched (unlikely)
        if not spec.get('field', ''):
            err = "{} key 'field' must be supplied in {!r}, must be one of: {}"
            err = err.format(self.meerr, spec, self.props_txt)
            raise PytanError(err)

        # if field is not a valid property in single_class
        # {"value": "Computer Name", "field": "die"}
        if spec['field'] not in self.props:
            err = "{} key 'field' value {!r} not valid for {!r}, must be one of: {}"
            err = err.format(self.meerr, spec['field'], self.single_name, self.props_txt)
            raise PytanError(err)

        # validate field is a string
        self.chk_dict_key('field', spec, string_types)
        return spec

    def chk_operator(self, spec):
        """pass."""
        # validate operator is a string
        self.chk_dict_key('operator', spec, string_types)

        # if operator is a pytan extended operator, map it back to a Tanium operator
        if spec['operator'].lower() in OPERATORS_PYTAN:
            emap = OPERATORS_PYTAN[spec['operator'].lower()]
            pre_value = emap.get('pre_value', '')
            post_value = emap.get('post_value', '')
            spec['operator'] = emap.get('operator')
            spec['not_flag'] = emap.get('not_flag')
            if pre_value:
                spec['value'] = '{}{}'.format(pre_value, spec['value'])
            if post_value:
                spec['value'] = '{}{}'.format(spec['value'], post_value)

        # validate operator is a valid Tanium Operator
        op_valid = [
            x
            for x in OPERATORS_TANIUM
            if x.lower() == spec['operator'].lower()
        ]

        # see if operator matches a Tanium operator
        if op_valid:
            spec['operator'] == op_valid[0]

        # operator did not match a Tanium operator
        # {"value": "Computer Name", "field": "name", "operator": "die"}
        if not op_valid:
            op_list = ', '.join(OPERATORS_TANIUM + OPERATORS_PYTAN.keys())
            err = "{} key 'operator' value {!r} invalid, must be one of: {}"
            err = err.format(self.meerr, spec['operator'], op_list)
            raise PytanError(err)
        return spec

    def chk_not_flag(self, spec):
        # validate not_flag is a valid true or false type
        if spec['not_flag'] in TRUE_TYPES:
            spec['not_flag'] = 1
        elif spec['not_flag'] in FALSE_TYPES:
            spec['not_flag'] = 0
        else:
            # not_flag did not match a valid type
            # {"value": "Computer Name", "field": "name", "not_flag": "die"}
            types_txt = TRUE_TYPES + FALSE_TYPES
            types_txt = ', '.join([repr(x) for x in types_txt])
            err = "{} key 'not_flag' value {!r} invalid, must be one of: {}"
            err = err.format(self.meerr, spec['not_flag'], types_txt)
            raise PytanError(err)
        return spec

    def chk_field_type(self, spec):
        # validate field_type is a string
        self.chk_dict_key('field_type', spec, string_types)

        # validate field_type is a valid field type
        type_valid = [
            FIELD_TYPES[x]
            for x in FIELD_TYPES
            if x.lower() == spec['field_type'].lower()
        ]

        if type_valid:
            spec['field_type'] == type_valid[0]['t']

        # field_type did not match a valid field type
        # {"value": "Computer Name", "field": "name", "field_type": "die"}
        if not type_valid:
            type_list = ', '.join(FIELD_TYPES)
            err = "{} key 'field_type' value {!r} invalid, must be one of: {}"
            err = err.format(self.meerr, spec['field_type'], type_list)
            raise PytanError(err)
        return spec
