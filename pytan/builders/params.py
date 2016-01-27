import re
import logging

from pytan.builders import ObjectBuildError, log_result
from pytan.tanium_ng import Sensor, Parameter, ParameterList, PackageSpec
from pytan.builders.constants import PARAMETER_DEFAULTS

MYLOG = logging.getLogger(__name__)


class ParameterValidationError(ObjectBuildError):
    pass


class BuildParams(object):

    def __init__(self, obj, **kwargs):
        if not isinstance(obj, (PackageSpec, Sensor)):
            err = 'obj must be an PackageSpec or Sensor, you supplied type {}: {}'
            err = err.format(type(obj).__name__, obj)
            MYLOG.error(err)
            raise ObjectBuildError(err)

        kwargs.update({k: kwargs.get(k, v) for k, v in PARAMETER_DEFAULTS.items()})
        self.EXTRAS_ALLOWED = kwargs.get('extras_allowed', True)
        self.AUTO_DEFAULT = kwargs.get('auto_default', True)
        self.NAMED_PARAM_SPEC = kwargs.get('named_param_spec', {})
        self.UNNAMED_PARAM_SPEC = kwargs.get('unnamed_param_spec', [])

        if 'delimiter' in kwargs:
            self.DELIMITER = kwargs['delimiter']
        elif isinstance(obj, PackageSpec):
            self.DELIMITER = kwargs['action_delimiter']
        elif isinstance(obj, Sensor):
            self.DELIMITER = kwargs['sensor_delimiter']

        self.OBJ = obj
        self.OBJ_PARAMS = self.OBJ.get_parsed_params()
        self.EXTRA_PARAMS = {}

        if self.NAMED_PARAM_SPEC:
            if isinstance(self.NAMED_PARAM_SPEC, dict):
                self.handle_named_params()
            else:
                err = 'named_param_spec must be a dict, you supplied type {}: {}'
                err = err.format(type(self.NAMED_PARAM_SPEC).__name__, self.NAMED_PARAM_SPEC)
                MYLOG.error(err)
                raise ObjectBuildError(err)

        if self.UNNAMED_PARAM_SPEC:
            if isinstance(self.UNNAMED_PARAM_SPEC, dict):
                self.handle_unnamed_params()
            else:
                err = 'unnamed_param_spec must be a dict, you supplied type {}: {}'
                err = err.format(type(self.UNNAMED_PARAM_SPEC).__name__, self.UNNAMED_PARAM_SPEC)
                MYLOG.error(err)
                raise ObjectBuildError(err)

        self.check_param_values()
        self.RESULT = self.build_parameter_list()

    def build_parameter_list(self):
        params = []
        for op in self.OBJ_PARAMS:
            pobj = self.build_parameter(op['key'], op['VALUE'])
            pobj.value_source = op['VALUE_SOURCE']
            pobj.parsed_param = op
            params.append(pobj)

        for k, v in self.EXTRA_PARAMS.items():
            pobj = self.build_parameter(k, v)
            pobj.value_source = 'user supplied extra named parameter'
            params.append(pobj)

        if params:
            result = ParameterList(parameter=params)
        else:
            m = "No user supplied parameters and no object parameters for obj {}!"
            m = m.format(self.OBJ)
            MYLOG.debug(m)
            result = None
        log_result('BuildParams.build_parameter_list', result, locals())
        return result

    def check_value_exists(self, op):
        if 'VALUE' not in op:
            auto_default_value = op.get('auto_default_value', '')
            if self.AUTO_DEFAULT:
                op['VALUE'] = auto_default_value
                op['VALUE_SOURCE'] = 'no user supplied value and auto_default = True'
            else:
                err = "No parameter value supplied and 'auto_default'={} for parameter: {}"
                err = err.format(self.AUTO_DEFAULT, op['desc'])
                MYLOG.error(err)
                raise ParameterValidationError(err)
        return op

    def check_value_valid(self, op):
        orig_def = op['orig']
        validations = orig_def.get('validationExpressions', [])
        for v in validations:
            ve = v.get('expression', '')
            vh = v.get('helpString', '')
            if not ve:
                continue
            if re.match(ve, op['VALUE']):
                m = "Parameter value '{}' passed validation '{}' ({}) for parameter: {}"
                m = m.format(op['VALUE'], ve, vh, op['desc'])
                MYLOG.debug(m)
            else:
                err = "Parameter value '{}' failed validation '{}' ({}) for parameter: {}"
                err = err.format(op['VALUE'], ve, vh, op['desc'])
                MYLOG.error(err)
                raise ParameterValidationError(err)
        return op

    def check_value_max_char(self, op):
        max_characters = int(op.get('max_characters', 0))
        if max_characters:
            value_len = len(op['VALUE'])
            if not value_len > max_characters:
                m = "Parameter value '{}' length '{}' passed max_characters '{}' for parameter: {}"
                m = m.format(op['VALUE'], value_len, max_characters, op['desc'])
                MYLOG.debug(m)
            else:
                err = (
                    "Parameter value '{}' length '{}' failed max_characters '{}' for parameter: {}"
                )
                err = err.format(op['VALUE'], value_len, max_characters, op['desc'])
                MYLOG.error(err)
                raise ParameterValidationError(err)
        return op

    def check_value_max_value(self, op):
        max_value = int(op.get('max_value', 0))
        if max_value:
            value = int(op['VALUE'])
            if value > max_value:
                m = "Parameter value '{}' passed max_value '{}' for parameter: {}"
                m = m.format(op['VALUE'], max_value, op['desc'])
                MYLOG.debug(m)
            else:
                err = (
                    "Parameter value '{}' failed max_value '{}' for parameter: {}"
                )
                err = err.format(op['VALUE'], max_value, op['desc'])
                MYLOG.error(err)
                raise ParameterValidationError(err)
        return op

    def check_value_min_value(self, op):
        min_value = int(op.get('min_value', 0))
        if min_value:
            value = int(op['VALUE'])
            if value > min_value:
                m = "Parameter value '{}' passed min_value '{}' for parameter: {}"
                m = m.format(op['VALUE'], min_value, op['desc'])
                MYLOG.debug(m)
            else:
                err = (
                    "Parameter value '{}' failed min_value '{}' for parameter: {}"
                )
                err = err.format(op['VALUE'], min_value, op['desc'])
                MYLOG.error(err)
                raise ParameterValidationError(err)
        return op

    def check_value_in_values(self, op):
        valid_values = op.get('valid_values', [])
        valid_values_txt = op.get('valid_values_txt', '')
        value = op['VALUE']
        if valid_values:
            if value in valid_values:
                m = "Parameter value '{}' is one of '{}' valid values for parameter: {}"
                m = m.format(op['VALUE'], valid_values_txt, op['desc'])
                MYLOG.debug(m)
            else:
                err = "Parameter value '{}' is not one of '{}' valid values for parameter: {}"
                err = err.format(op['VALUE'], valid_values_txt, op['desc'])
                MYLOG.error(err)
                raise ParameterValidationError(err)
        return op

    def check_param_values(self):
        for op in self.OBJ_PARAMS:
            self.check_value_exists(op)
            self.check_value_valid(op)
            self.check_value_max_char(op)
            self.check_value_max_value(op)
            self.check_value_min_value(op)
            self.check_value_in_values(op)

    def valid_op_strings(self, j='\n  *'):
        result = [x['desc'] for x in self.OBJ_PARAMS]
        result = j.join(result)
        return result

    def find_named_op(self, key, value):
        result = None
        for op in self.OBJ_PARAMS:
            if op['key'] != key:
                continue
            op['VALUE'] = value
            op['VALUE_SOURCE'] = 'user supplied named parameter'
            result = op
            break
        return result

    def find_unnamed_op(self, idx, value):
        result = None
        try:
            result = self.OBJ_PARAMS[idx]
            result['VALUE'] = value
            result['VALUE_SOURCE'] = 'user supplied unnamed parameter at idx {}'.format(idx)
        except:
            pass
        return result

    def handle_named_params(self):
        for key, value in self.NAMED_PARAM_SPEC.items():
            found = self.find_named_op(key, value)
            if found:
                m = "Found a matching object parameter for named param key {!r} / value {!r}: {}"
                m = m.format(key, value, found['desc'])
                MYLOG.debug(m)
            else:
                m = "No matching object parameter for key {!r} / value {!r} (extras_allowed: {})"
                m = m.format(key, value, self.EXTRAS_ALLOWED)
                if self.EXTRAS_ALLOWED:
                    MYLOG.warn(m)
                    self.EXTRA_PARAMS[key] = value
                else:
                    err = "{} -- Valid Parameters in object:\n  *{}"
                    err = err.format(m, self.valid_op_strings())
                    MYLOG.error(err)
                    raise ParameterValidationError(err)

    def handle_unnamed_params(self):
        values = self.UNNAMED_PARAM_SPEC.get('values', [])

        if not isinstance(values, (list, tuple)):
            err = 'unnamed_param_spec "values" key must be a list, you supplied type {}: {}'
            err = err.format(type(values).__name__, values)
            MYLOG.error(err)
            raise ObjectBuildError(err)

        for idx, value in enumerate(values):
            found = self.find_unnamed_op(idx, value)
            if found:
                m = "Found a matching object parameter for unnamed param #{} value {!r}: {}"
                m = m.format(idx + 1, value, found['desc'])
                MYLOG.debug(m)
            else:
                m = "No matching object parameter for unnamed param #{} value {!r}"
                m = m.format(idx + 1, value)
                err = "{} -- Valid Parameters in object:\n  *{}"
                err = err.format(m, self.valid_op_strings())
                MYLOG.error(err)
                raise ParameterValidationError(err)

    def build_parameter(self, key, value):
        """pass."""
        result = Parameter()
        delimited_key = '{0}{1}{0}'.format(self.DELIMITER, key)
        result.key = delimited_key
        result.value = value
        log_result('BuildParams.build_paramete', result, locals())
        return result


def build_params(obj, **kwargs):
    builder = BuildParams(obj, **kwargs)
    result = builder.RESULT
    return result
