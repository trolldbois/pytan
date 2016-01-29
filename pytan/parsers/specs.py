import copy
import logging

from pytan import PytanError, string_types, integer_types, text_type
from pytan.tickle.tools import secs_from_now

from pytan.parsers.constants import (
    SPEC_FIELD_FALLBACKS, OPERATORS_PYTAN, OPERATORS_TANIUM, TRUE_TYPES, FALSE_TYPES, CF_TYPES,
    FILTER_VALUE_TYPES, KIND_VALUES
)

MYLOG = logging.getLogger(__name__)


class SpecInvalidError(PytanError):
    pass


class Specify(object):
    """pass."""

    VALUE_KEY = 'value'
    OPERATOR_KEY = 'operator'
    FIELD_KEY = 'field'
    TYPE_KEY = 'type'
    NOT_KEY = 'not_flag'
    KIND_KEY = 'kind'
    VALID_TYPES = CF_TYPES
    OBJ = None
    ME_ADD = ''

    def __init__(self, spec, **kwargs):
        if not isinstance(spec, dict):
            err = "spec must be a dict; supplied type {!r} spec {!r}"
            err = err.format(type(spec).__name__, spec)
            MYLOG.error(err)
            raise SpecInvalidError(err)

        self.SPEC = spec
        self.KWARGS = kwargs
        self.RESULT = copy.deepcopy(self.SPEC)
        self.determine_obj()
        self.post_init()
        self.log_change()

    def determine_obj(self):
        class_list = self.KWARGS.get('class_list', None)
        obj = self.KWARGS.get('obj', None)
        if class_list:
            obj_list = class_list()
            class_single = obj_list._LIST_TYPE
            objtype = class_single.__name__
            obj_single = class_single()
            self.OBJ = obj_single
            self.ME_ADD = ' for object type {!r}'.format(objtype)
        elif obj:
            self.OBJ = obj
            self.ME_ADD = ' for object type {!r}'.format(type(obj).__name__)

    def post_init(self):
        pass

    @property
    def me(self):
        me = self.__class__.__name__
        meadd = getattr(self, 'ME_ADD', '')
        result = "{}(){}:"
        result = result.format(me, meadd)
        return result

    def log_change(self):
        # if changed, log the change
        if self.SPEC != self.RESULT:
            m = "{} original spec: {!r} parsed into new spec: {!r}"
            m = m.format(self.me, self.SPEC, self.RESULT)
            MYLOG.debug(m)
        else:
            m = "{} parsed without change: {!r}"
            m = m.format(self.me, self.RESULT)
            MYLOG.debug(m)

    def invalid_key(self, key, valid_types, valid_text):
        valid_types_text = ', '.join(valid_types)
        err1 = "{}: key {!r} is an invalid {}, must be one of: {!r}"
        err2 = "\t* supplied type {!r} for key {!r} value {!r}"
        err3 = "\t* original spec: {!r}"
        err1 = err1.format(self.me, key, valid_text, valid_types_text)
        err2 = err2.format(type(self.RESULT[key]).__name__, key, self.RESULT[key])
        err3 = err3.format(self.SPEC)
        err = '\n'.join([err1, err2, err3])
        MYLOG.error(err)
        raise SpecInvalidError(err)

    def check_key_type(self, key, types):
        """pass."""
        if not isinstance(self.RESULT[key], types):
            valid_types = [x.__name__ for x in types]
            self.invalid_key(key, valid_types, 'object type')

    def check_key_exists(self, key):
        if key not in self.RESULT:
            err = "{}: key {!r} must be supplied in spec {!r}!"
            err = err.format(self.me, key, self.RESULT)
            MYLOG.error(err)
            raise SpecInvalidError(err)

    def check_key_bool(self, key):
        # validate key is a valid true or false type
        value = self.RESULT[key]
        if isinstance(value, string_types):
            value = value.lower()
        if value in TRUE_TYPES:
            value = 1
        elif value in FALSE_TYPES:
            value = 0
        else:
            # value did not match a valid type
            valid_types = [repr(x) for x in [TRUE_TYPES + FALSE_TYPES]]
            self.invalid_key(key, valid_types, key)
        self.RESULT[key] = value

    def check_req_subparser(self, key, subparser, **kwargs):
        self.check_key_exists(key)
        self.check_subparser(key, subparser, **kwargs)

    def check_opt_subparser(self, key, subparser, **kwargs):
        if key in self.RESULT:
            self.check_subparser(key, subparser, **kwargs)

    def check_subparser(self, key, subparser, **kwargs):
        sargs = {}
        sargs.update(self.KWARGS)
        sargs.update(kwargs)
        sargs.update({key: self.RESULT[key]})
        self.RESULT[key] = subparser(**sargs)

    def force_str_value(self, key, value, valid_text):
        types = string_types + integer_types
        valid_types = [x.__name__ for x in types]

        if not isinstance(value, types):
            self.invalid_key(key, valid_types, valid_text)

        if not isinstance(value, string_types):
            try:
                value = text_type(value)
            except:
                self.invalid_key(key, valid_types, valid_text)
        return value

    def check_key_opt_list(self, key):
        if key in self.RESULT:
            self.check_key_type(key, (list, tuple))
            for idx, i in enumerate(self.RESULT[key]):
                valid_text = 'list type at index {}'.format(idx + 1)
                self.RESULT[key][idx] = self.force_str_value(key, i, valid_text)

    def validate_opt_bool(self, key):
        if key in self.RESULT:
            self.check_key_bool(key)

    def validate_value(self):
        # check that value key in self.RESULT exists
        self.check_key_exists(self.VALUE_KEY)

        # check that value key in self.RESULT is a string or int
        self.check_key_type(self.VALUE_KEY, string_types + integer_types)

        # force value key in self.RESULT into a string
        if not isinstance(self.RESULT[self.VALUE_KEY], string_types):
            self.RESULT[self.VALUE_KEY] = text_type(self.RESULT[self.VALUE_KEY])

    def validate_field(self):
        # if field key in self.RESULT does not exist and is an int, assume field is id
        if self.FIELD_KEY not in self.RESULT:
            try:
                int(self.RESULT.get(self.VALUE_KEY, ''))
                self.RESULT[self.FIELD_KEY] = 'id'
            except:
                pass

        # if field key in self.RESULT does not exist, derive from fallbacks
        if self.FIELD_KEY not in self.RESULT and self.OBJ is not None:
            for x in SPEC_FIELD_FALLBACKS:
                if x in dir(self.OBJ):
                    self.RESULT[self.FIELD_KEY] = x
                    break

        # check that field key in self.RESULT exists
        self.check_key_exists(self.FIELD_KEY)

        # check that field key in self.RESULT is a string
        self.check_key_type(self.FIELD_KEY, string_types)

    def seconds_to_date(self, value):
        try:
            value = int(value)
        except:
            err = "Unable to convert value {!r} to integer!"
            err = err.format(value)
            MYLOG.error(err)
            raise SpecInvalidError(err)

        result = secs_from_now(secs=value)
        return result

    def emap_value_helper(self, emap):
        if 'value_helper' in emap:
            helper_method = getattr(self, emap['value_helper'])
            self.RESULT[self.VALUE_KEY] = helper_method(self.RESULT[self.VALUE_KEY])

    def emap_not_flag(self, emap):
        if self.NOT_KEY not in self.RESULT and self.NOT_KEY in emap:
            self.RESULT[self.NOT_KEY] = emap[self.NOT_KEY]

    def emap_type_fallbacks(self, emap):
        if 'type_fallbacks' in emap and not self.RESULT.get(self.TYPE_KEY):
            for k, v in emap['type_fallbacks'].items():
                if self.TYPE_KEY == k:
                    self.RESULT[self.TYPE_KEY] = v
                    break

    def emap_pre_value(self, emap):
        if 'pre_value' in emap and 'value' in self.RESULT:
            value = '{}{}'.format(emap['pre_value'], self.RESULT[self.VALUE_KEY])
            self.RESULT[self.VALUE_KEY] = value

    def emap_post_value(self, emap):
        if 'post_value' in emap and 'value' in self.RESULT:
            value = '{}{}'.format(self.RESULT[self.VALUE_KEY], emap['post_value'])
            self.RESULT[self.VALUE_KEY] = value

    def emap_field_fallbacks(self, emap):
        if self.FIELD_KEY:
            field = self.RESULT.get(self.FIELD_KEY)
            if 'field_fallbacks' in emap and not field and self.OBJ is not None:
                for x in emap['field_fallbacks']:
                    if x in dir(self.OBJ):
                        self.RESULT[self.FIELD_KEY] = x
                        break

    def check_pytan_operator(self):
        operator = self.RESULT[self.OPERATOR_KEY].lower()
        if operator in OPERATORS_PYTAN:
            emap = OPERATORS_PYTAN[operator]
            self.RESULT[self.OPERATOR_KEY] = emap['operator']
            self.emap_value_helper(emap)
            self.emap_pre_value(emap)
            self.emap_post_value(emap)
            self.emap_not_flag(emap)
            self.emap_type_fallbacks(emap)
            self.emap_field_fallbacks(emap)

    def check_tanium_operator(self):
        operator = self.RESULT[self.OPERATOR_KEY].lower()

        # validate operator is a valid Tanium Operator
        op_valid = [x for x in OPERATORS_TANIUM if x.lower() == operator.lower()]

        if op_valid:
            # operator matches a Tanium operator
            self.RESULT[self.OPERATOR_KEY] = op_valid[0]
        else:
            # operator did not match a Tanium operator
            valid_types = OPERATORS_TANIUM + OPERATORS_PYTAN.keys()
            self.invalid_key(self.OPERATOR_KEY, valid_types, self.OPERATOR_KEY)

    def validate_operator(self):
        """pass."""
        if self.OPERATOR_KEY in self.RESULT:
            # check that operator key in self.RESULT is a string
            self.check_key_type(self.OPERATOR_KEY, string_types)
            self.check_pytan_operator()
            self.check_tanium_operator()

    def validate_type(self):
        # valid_types = FILTER_VALUE_TYPES

        if self.TYPE_KEY in self.RESULT:
            # validate type is a string
            self.check_key_type(self.TYPE_KEY, string_types)
            value = self.RESULT[self.TYPE_KEY].lower()

            # validate type is a valid field type
            value_valid = [self.VALID_TYPES[x] for x in self.VALID_TYPES if x.lower() == value]

            if value_valid:
                self.RESULT[self.TYPE_KEY] = value_valid[0]['t']
            else:
                # type did not match a valid field type
                self.invalid_key(self.TYPE_KEY, self.VALID_TYPES, self.TYPE_KEY)

    def validate_kind(self):
        if self.KIND_KEY in self.RESULT:
            # validate type is a string
            self.check_key_type(self.KIND_KEY, string_types)
            value = self.RESULT[self.KIND_KEY].lower()

            # validate type is a valid field type
            value_valid = value in KIND_VALUES

            if value_valid:
                self.RESULT[self.KIND_KEY] = value
            else:
                # type did not match a valid field type
                valid_types = KIND_VALUES
                self.invalid_key(self.KIND_KEY, valid_types, self.KIND_KEY)


class SearchSpecify(Specify):

    def post_init(self):
        """search spec must be a dict with keys:

        value: required
        field: required (but will try to auto determine)
        operator: optional
        type: optional
        not_flag: optional
        """
        self.validate_value()
        self.validate_operator()
        self.validate_field()
        self.validate_type()
        self.validate_opt_bool('not_flag')


class LeftSpecify(Specify):

    def post_init(self):
        """left spec must be a dict with keys:

        search_spec: required
        filter_spec: optional
        named_param_spec: optional
        unnamed_param_spec: optional
        """
        self.check_key_exists('search_spec')
        self.check_opt_subparser(key='filter_spec', subparser=filter_specify)
        self.check_opt_subparser(key='named_param_spec', subparser=named_param_specify)
        self.check_opt_subparser(key='unnamed_param_spec', subparser=unnamed_param_specify)


class RightSpecify(Specify):

    def post_init(self):
        """right spec must be a dict with keys:

        search_spec: required
        filter_spec: required
        named_param_spec: optional
        unnamed_param_spec: optional
        """
        self.check_key_exists('search_spec')
        self.check_key_exists('filter_spec')
        self.check_opt_subparser(key='group_spec', subparser=group_specify)
        self.check_opt_subparser(key='filter_spec', subparser=filter_specify)
        self.check_opt_subparser(key='named_param_spec', subparser=named_param_specify)
        self.check_opt_subparser(key='unnamed_param_spec', subparser=unnamed_param_specify)


class FilterSpecify(Specify):

    TYPE_KEY = 'value_type'
    VALID_TYPES = FILTER_VALUE_TYPES
    FIELD_KEY = None

    def post_init(self):
        """filter spec can be empty. if not empty, must be a dict with keys:

        value: required
        operator: optional
        not_flag: optional
        ignore_case_flag: optional
        all_values_flag: optional
        value_type: optional
        max_age_seconds: optional
        """
        if self.RESULT:
            self.validate_value()
            self.validate_operator()
            self.validate_opt_bool('not_flag')
            self.validate_opt_bool('ignore_case_flag')
            self.validate_opt_bool('all_values_flag')
            self.validate_type()

            key = 'max_age_seconds'
            if key in self.RESULT:
                self.check_key_type(key, integer_types)


class LotSpecify(Specify):

    def post_init(self):
        """lot spec can be empty. if not empty, must be a dict with keys:

        lot: required
        not_flag: optional
        and_flag: optional
        """
        if self.RESULT:
            self.check_key_exists('lot')
            self.check_key_type('lot', string_types + integer_types)
            self.validate_opt_bool('not_flag')
            self.validate_opt_bool('and_flag')


class GroupSpecify(Specify):

    def post_init(self):
        """group spec can be empty. if not empty, must be a dict with keys:

        kind: optional
        lot: optional
        """
        if self.RESULT:
            self.validate_kind()
            if 'lot' in self.RESULT:
                self.check_key_type('lot', string_types + integer_types)


class NamedParamSpecify(Specify):

    def post_init(self):
        """named param spec must be a dict with key/value pairs as string types"""
        if self.RESULT:
            for key, value in self.RESULT.items():
                key = self.force_str_value(key, key, key)
                value = self.force_str_value(key, value, key)


class UnNamedParamSpecify(Specify):

    def post_init(self):
        """named param spec must be a dict with the following keys:

        values: optional (list of parameter values)
        """
        if self.RESULT:
            self.check_key_opt_list('values')


def search_specify(search_specs, **kwargs):
    parser = SearchSpecify(search_specs, **kwargs)
    result = parser.RESULT
    return result


def left_specify(left_spec, **kwargs):
    parser = LeftSpecify(left_spec, **kwargs)
    result = parser.RESULT
    return result


def right_specify(right_spec, **kwargs):
    parser = RightSpecify(right_spec, **kwargs)
    result = parser.RESULT
    return result


def group_specify(group_spec, **kwargs):
    parser = GroupSpecify(group_spec, **kwargs)
    result = parser.RESULT
    return result


def filter_specify(filter_spec, **kwargs):
    parser = FilterSpecify(filter_spec, **kwargs)
    result = parser.RESULT
    return result


def named_param_specify(named_param_spec, **kwargs):
    parser = NamedParamSpecify(named_param_spec, **kwargs)
    result = parser.RESULT
    return result


def unnamed_param_specify(unnamed_param_spec, **kwargs):
    parser = UnNamedParamSpecify(unnamed_param_spec, **kwargs)
    result = parser.RESULT
    return result


def lot_specify(lot_spec, **kwargs):
    parser = LotSpecify(lot_spec, **kwargs)
    result = parser.RESULT
    return result
