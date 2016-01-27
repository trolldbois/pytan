import copy
import logging

from pytan import PytanError, string_types, integer_types, text_type

from pytan.parsers.constants import (
    SPEC_FIELD_FALLBACKS, OPERATORS_PYTAN, OPERATORS_TANIUM, TRUE_TYPES, FALSE_TYPES, FIELD_TYPES
)

MYLOG = logging.getLogger(__name__)


class SpecInvalidError(PytanError):
    pass


class Specify(object):
    """pass."""

    def __init__(self, spec, **kwargs):
        if not isinstance(spec, dict):
            err = "spec must be a dict; supplied type {!r} spec {!r}"
            err = err.format(type(spec).__name__, spec)
            MYLOG.error(err)
            raise SpecInvalidError(err)

        self.SPEC = spec
        self.KWARGS = kwargs
        self.RESULT = copy.deepcopy(self.SPEC)
        self.post_init()
        self.log_change()

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

    def validate_value(self, key='value'):
        # check that value key in self.RESULT exists
        self.check_key_exists(key)

        # check that value key in self.RESULT is a string or int
        self.check_key_type(key, string_types + integer_types)

        # force value key in self.RESULT into a string
        if not isinstance(self.RESULT[key], string_types):
            self.RESULT[key] = text_type(self.RESULT[key])

    def validate_field(self, key='field', value_key='value'):
        # if field key in self.RESULT does not exist and is an int, assume field is id
        if key not in self.RESULT:
            try:
                int(self.RESULT.get(value_key, ''))
                self.RESULT[key] = 'id'
            except:
                pass

        # if field key in self.RESULT does not exist, derive from fallbacks
        if key not in self.RESULT and self.OBJ_SINGLE is not None:
            for x in SPEC_FIELD_FALLBACKS:
                if x not in dir(self.OBJ_SINGLE):
                    continue
                self.RESULT[key] = x
                break

        # check that field key in self.RESULT exists
        self.check_key_exists(key)

        # check that field key in self.RESULT is a string
        self.check_key_type(key, string_types)

    def validate_operator(self, key='operator', value_key='value', not_key='not_flag'):
        """pass."""
        if key in self.RESULT:
            # check that operator key in self.RESULT is a string
            self.check_key_type(key, string_types)
            operator = self.RESULT[key].lower()

            # if operator is a pytan extended operator, map it back to a Tanium operator
            if operator in OPERATORS_PYTAN:
                emap = OPERATORS_PYTAN[operator]
                pre_value = emap.get('pre_value', '')
                post_value = emap.get('post_value', '')
                operator = emap.get('operator')
                if not_key not in self.RESULT and not_key in emap:
                    self.RESULT[not_key] = emap.get(not_key)
                if pre_value:
                    self.RESULT[value_key] = '{}{}'.format(pre_value, self.RESULT[value_key])
                if post_value:
                    self.RESULT[value_key] = '{}{}'.format(self.RESULT[value_key], post_value)

            # validate operator is a valid Tanium Operator
            op_valid = [x for x in OPERATORS_TANIUM if x.lower() == operator.lower()]

            if op_valid:
                # operator matches a Tanium operator
                operator == op_valid[0]
            else:
                # operator did not match a Tanium operator
                valid_types = OPERATORS_TANIUM + OPERATORS_PYTAN.keys()
                self.invalid_key(key, valid_types, key)

            self.RESULT[key] = operator

    def validate_type(self, key='type'):
        if key in self.RESULT:
            # validate type is a string
            self.check_key_type(key, string_types)
            type_key = self.RESULT[key].lower()

            # validate type is a valid field type
            type_valid = [FIELD_TYPES[x] for x in FIELD_TYPES if x.lower() == type_key]

            if type_valid:
                type_key == type_valid[0]['t']
            else:
                # type did not match a valid field type
                valid_types = FIELD_TYPES
                self.invalid_key(key, valid_types, key)

            self.RESULT[key] = type_key


class SearchSpecify(Specify):

    def post_init(self):
        """search spec must be a dict with keys:

        value: required
        field: required (but will try to auto determine)
        operator: optional
        type: optional
        not_flag: optional
        """

        class_list = self.KWARGS.get('class_list', None)
        objtype = 'unknown'
        if class_list:
            obj_list = class_list()
            class_single = obj_list._LIST_TYPE
            objtype = class_single.__name__
            obj_single = class_single()
            self.OBJ_SINGLE = obj_single

        self.ME_ADD = ' for object type {!r}'.format(objtype)

        self.validate_value('value')
        self.validate_field('field')
        self.validate_operator('operator')
        self.validate_type('type')
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
        self.check_opt_subparser(key='filter_spec', subparser=filter_specify)
        self.check_opt_subparser(key='named_param_spec', subparser=named_param_specify)
        self.check_opt_subparser(key='unnamed_param_spec', subparser=unnamed_param_specify)


class FilterSpecify(Specify):

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
            self.validate_value('value')
            self.validate_operator('operator')
            self.validate_opt_bool('not_flag')
            self.validate_opt_bool('ignore_case_flag')
            self.validate_opt_bool('all_values_flag')
            self.validate_type('value_type')

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
