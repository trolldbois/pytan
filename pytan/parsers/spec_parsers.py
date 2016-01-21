import copy
import logging

from pytan import PytanError, string_types, integer_types, text_type
from pytan.utils import coerce_list
from pytan.parsers.token_parsers import find_token_parser

from pytan.parsers.constants import (
    SPEC_FIELD_FALLBACKS, OPERATORS_PYTAN, OPERATORS_TANIUM, TRUE_TYPES, FALSE_TYPES, FIELD_TYPES
)

MYLOG = logging.getLogger(__name__)


class SpecInvalidError(PytanError):
    pass


class SpecParser(object):
    """pass."""

    def __init__(self, spec, **kwargs):
        if not isinstance(spec, dict):
            err = "spec must be a dict; supplied type {!r} spec {!r}"
            err = err.format(type(spec).__name__, spec)
            MYLOG.error(err)
            raise SpecInvalidError(err)

        self.SPEC = spec
        self.OBJ_SINGLE = kwargs.get('obj_single', None)
        self.RESULT = copy.deepcopy(self.SPEC)
        self.post_init()
        self.log_change()

    def post_init(self):
        pass

    @property
    def me(self):
        me = self.__class__.__name__
        if self.OBJ_SINGLE is not None:
            objtype = type(self.OBJ_SINGLE).__name__
        else:
            objtype = 'unknown!'
        result = "{}() for object type: {!r}"
        result = result.format(me, objtype)
        return result

    def log_change(self):
        # if changed, log the change
        if self.SPEC != self.RESULT:
            m = "{} original spec: {!r}"
            m = m.format(self.me, self.SPEC)
            MYLOG.info(m)

            m = "{} parsed into new spec: {!r}"
            m = m.format(self.me, self.RESULT)
            MYLOG.info(m)
        else:
            m = "{} parsed without change: {!r}"
            m = m.format(self.me, self.RESULT)
            MYLOG.info(m)

    def invalid_key(self, k, valid_types, valid_text):
        valid_types_text = ', '.join(valid_types)
        err1 = "{}: key {!r} is an invalid {}, must be one of: {!r}"
        err2 = "\t* supplied type {!r} for key {!r} value {!r}"
        err3 = "\t* original spec: {!r}"
        err1 = err1.format(self.me, k, valid_text, valid_types_text)
        err2 = err2.format(type(self.RESULT[k]).__name__, k, self.RESULT[k])
        err3 = err3.format(self.SPEC)
        err = '\n'.join([err1, err2, err3])
        MYLOG.error(err)
        raise SpecInvalidError(err)

    def check_key_type(self, k, types):
        """pass."""
        if not isinstance(self.RESULT[k], types):
            valid_types = [x.__name__ for x in types]
            self.invalid_key(k, valid_types, 'object type')

    def check_key_exists(self, k):
        if k not in self.RESULT:
            err = "{}: key {!r} must be supplied in spec {!r}!"
            err = err.format(self.me, k, self.RESULT)
            MYLOG.error(err)
            raise SpecInvalidError(err)

    def validate_key_value(self):
        # check that value key in self.RESULT exists
        self.check_key_exists('value')

        # check that value key in self.RESULT is a string or int
        self.check_key_type('value', string_types + integer_types)

        # force value key in self.RESULT into a string
        if not isinstance(self.RESULT['value'], string_types):
            self.RESULT['value'] = text_type(self.RESULT['value'])

    def validate_key_field(self):
        # if field key in self.RESULT does not exist and is an int, assume field is id
        if 'field' not in self.RESULT:
            try:
                int(self.RESULT.get('value', ''))
                self.RESULT['field'] = 'id'
            except:
                pass

        # if field key in self.RESULT does not exist, derive from fallbacks
        if 'field' not in self.RESULT and self.OBJ_SINGLE is not None:
            for x in SPEC_FIELD_FALLBACKS:
                if x not in dir(self.OBJ_SINGLE):
                    continue
                self.RESULT['field'] = x
                break

        # check that field key in self.RESULT exists
        self.check_key_exists('field')

        # check that field key in self.RESULT is a string
        self.check_key_type('field', string_types)

    def validate_key_operator(self):
        """pass."""
        if 'operator' in self.RESULT:
            # check that operator key in self.RESULT is a string
            self.check_key_type('operator', string_types)
            operator = self.RESULT['operator'].lower()

            # if operator is a pytan extended operator, map it back to a Tanium operator
            if operator in OPERATORS_PYTAN:
                emap = OPERATORS_PYTAN[operator]
                pre_value = emap.get('pre_value', '')
                post_value = emap.get('post_value', '')
                operator = emap.get('operator')
                if 'not_flag' not in self.RESULT and 'not_flag' in emap:
                    self.RESULT['not_flag'] = emap.get('not_flag')
                if pre_value:
                    self.RESULT['value'] = '{}{}'.format(pre_value, self.RESULT['value'])
                if post_value:
                    self.RESULT['value'] = '{}{}'.format(self.RESULT['value'], post_value)

            # validate operator is a valid Tanium Operator
            op_valid = [x for x in OPERATORS_TANIUM if x.lower() == operator.lower()]

            if op_valid:
                # operator matches a Tanium operator
                operator == op_valid[0]
            else:
                # operator did not match a Tanium operator
                valid_types = OPERATORS_TANIUM + OPERATORS_PYTAN.keys()
                self.invalid_key('operator', valid_types, 'operator')

            self.RESULT['operator'] = operator

    def validate_key_not_flag(self):
        if 'not_flag' in self.RESULT:
            # validate not_flag is a valid true or false type
            not_flag = self.RESULT['not_flag']
            if isinstance(not_flag, string_types):
                not_flag = not_flag.lower()
            if not_flag in TRUE_TYPES:
                not_flag = 1
            elif not_flag in FALSE_TYPES:
                not_flag = 0
            else:
                # not_flag did not match a valid type
                valid_types = [repr(x) for x in [TRUE_TYPES + FALSE_TYPES]]
                self.invalid_key('not_flag', valid_types, 'not_flag')

            self.RESULT['not_flag'] = not_flag

    def validate_key_type(self):
        if 'type' in self.RESULT:
            # validate type is a string
            self.check_key_type('type', string_types)
            type_key = self.RESULT['type'].lower()

            # validate type is a valid field type
            type_valid = [FIELD_TYPES[x] for x in FIELD_TYPES if x.lower() == type_key]

            if type_valid:
                type_key == type_valid[0]['t']
            else:
                # type did not match a valid field type
                valid_types = FIELD_TYPES
                self.invalid_key('type', valid_types, 'type')

            self.RESULT['type'] = type_key


class FindSpecParser(SpecParser):

    def post_init(self):
        # check that value key exists and is valid
        self.validate_key_value()

        # check that field key exists and is valid
        self.validate_key_field()

        # if operator key exists, parse & validate
        self.validate_key_operator()

        # if not_flag key exists, parse & validate
        self.validate_key_not_flag()

        # if type key exists, parse & validate
        self.validate_key_type()


def find_spec_parser(spec, **kwargs):
    parser = FindSpecParser(spec, **kwargs)
    result = parser.RESULT
    return result


def coerce_find_subspec(subspec, **kwargs):
    if isinstance(subspec, dict):
        result = find_spec_parser(subspec, **kwargs)
    else:
        err = "sub spec {} must be a dict!"
        err = err.format(subspec)
        raise Exception(err)
    return result


def coerce_find_subspecs(spec, **kwargs):
    add_specs = kwargs.get('add_specs', [])

    if isinstance(spec, string_types):
        spec = find_token_parser(spec, **kwargs)

    spec = coerce_list(spec)

    if add_specs:
        [spec.append(s) for s in add_specs if s not in spec]

    result = [coerce_find_subspec(s, **kwargs) for s in spec]
    return result


def coerce_find_specs(**kwargs):
    specs = kwargs.get('specs', ())
    if 'add_specs' in kwargs:
        kwargs['add_specs'] = coerce_find_subspecs(spec=kwargs.get('add_specs', []))
    specs = coerce_list(specs)

    if not specs and kwargs.get('add_specs'):
        specs = kwargs['add_specs']

    result = [coerce_find_subspecs(s, **kwargs) for s in specs]
    return result
