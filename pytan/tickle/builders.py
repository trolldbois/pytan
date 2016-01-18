import re
import logging

from pytan import PytanError
from pytan.tanium_ng import (
    Sensor, SelectList, Select, Parameter, Question, Filter, PackageSpec, ParameterList,
    FilterList, Group, GroupList, CacheFilter, CacheFilterList
)

from pytan.tickle.constants import (
    PARAMETER_DEFAULTS, FILTER_DEFAULTS, QUESTION_DEFAULTS, GROUP_DEFAULTS
)


MYLOG = logging.getLogger(__name__)


class ObjectCreateError(PytanError):
    pass


class ParameterValidationError(PytanError):
    pass


class CreateParams(object):

    def __init__(self, obj, **kwargs):
        if not isinstance(obj, (PackageSpec, Sensor)):
            err = 'obj must be an PackageSpec or Sensor, you supplied type {}: {}'
            err = err.format(type(obj).__name__, obj)
            MYLOG.error(err)
            raise ObjectCreateError(err)

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
                raise ObjectCreateError(err)

        if self.UNNAMED_PARAM_SPEC:
            if isinstance(self.UNNAMED_PARAM_SPEC, (list, tuple)):
                self.handle_unnamed_params()
            else:
                err = 'unnamed_param_spec must be a list, you supplied type {}: {}'
                err = err.format(type(self.UNNAMED_PARAM_SPEC).__name__, self.UNNAMED_PARAM_SPEC)
                MYLOG.error(err)
                raise ObjectCreateError(err)

        self.check_param_values()
        self.RESULT = self.create_parameter_list()

    def create_parameter_list(self):
        params = []
        for op in self.OBJ_PARAMS:
            pobj = self.create_parameter(op['key'], op['VALUE'])
            pobj.value_source = op['VALUE_SOURCE']
            pobj.parsed_param = op
            params.append(pobj)

        for k, v in self.EXTRA_PARAMS.items():
            pobj = self.create_parameter(k, v)
            pobj.value_source = 'user supplied extra named parameter'
            params.append(pobj)

        if params:
            result = ParameterList(parameter=params)
        else:
            m = "No user supplied parameters and no object parameters for obj {}!"
            m = m.format(self.OBJ)
            MYLOG.debug(m)
            result = None
        log_result('create_parameter_list', result, locals())
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
        for idx, value in enumerate(self.UNNAMED_PARAM_SPEC):
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

    def create_parameter(self, key, value):
        """pass."""
        result = Parameter()
        delimited_key = '{0}{1}{0}'.format(self.DELIMITER, key)
        result.key = delimited_key
        result.value = value
        log_result('create_parameter', result, locals())
        return result


class CreateSelect(object):

    def __init__(self, handler, spec, **kwargs):
        self.SPEC = spec
        self.HANDLER = handler
        self.KWARGS = kwargs

        if not isinstance(spec, dict):
            err = 'spec must be a dict, you supplied type {}: {}'
            err = err.format(type(spec).__name__, spec)
            raise ObjectCreateError(err)

        if 'sensor_spec' not in spec:
            err = 'spec dict must have a "sensor_spec" key, you supplied: {}'
            err = err.format(spec)
            raise ObjectCreateError(err)

        self.build_select()

    def build_select(self):
        self.SENSOR_OBJ = self.get_sensor_obj()
        self.SENSOR_PARAMS = self.create_sensor_params()
        self.SELECT_SENSOR = self.create_select_sensor()
        self.SELECT_FILTER = self.create_select_filter()
        self.RESULT = self.create_select()

    def create_sensor_params(self):
        pargs = {}
        pargs.update(self.KWARGS)
        pargs['named_param_spec'] = self.SPEC.get('named_param_spec', {})
        pargs['unnamed_param_spec'] = self.SPEC.get('unnamed_param_spec', [])
        pargs['obj'] = self.SENSOR_OBJ
        result = create_params(**pargs)
        return result

    def create_select(self):
        result = Select()
        result.sensor = self.SELECT_SENSOR
        result.filter = self.SELECT_FILTER
        log_result('create_select', result, locals())
        return result

    def get_sensor_obj(self):
        result = self.HANDLER.get_sensors(limit_exact=1, specs=self.SPEC['sensor_spec'])
        return result

    def create_select_sensor(self):
        result = Sensor()
        if self.SENSOR_PARAMS:
            result.source_hash = self.SENSOR_OBJ.hash
            result.parameters = self.SENSOR_PARAMS
        else:
            result.hash = self.SENSOR_OBJ.hash
        log_result('create_select_sensor', result, locals())
        return result

    def create_select_filter(self):
        filter_spec = self.SPEC.get('filter_spec', {})
        sensor = Sensor(hash=self.SENSOR_OBJ.hash)
        result = create_filter(sensor, filter_spec)
        return result


class CreateFilterGroup(object):

    def __init__(self, handler, spec, **kwargs):
        self.SPEC = spec
        self.HANDLER = handler
        self.KWARGS = kwargs

        if not isinstance(spec, dict):
            err = 'spec must be a dict, you supplied type {}: {}'
            err = err.format(type(spec).__name__, spec)
            raise ObjectCreateError(err)

        if 'group_spec' in spec:
            self.get_group_obj()
        elif 'sensor_spec' in spec:
            if 'filter_spec' not in spec:
                err = 'spec dict must have a "filter_spec" key, you supplied: {}'
                err = err.format(spec)
                raise ObjectCreateError(err)
            self.build_group_obj()
        else:
            err = 'spec dict must have a "sensor_spec" or "group_spec" key, you supplied: {}'
            err = err.format(spec)
            raise ObjectCreateError(err)

    def get_group_obj(self):
        self.RESULT = self.HANDLER.get_groups(limit_exact=1, specs=self.SPEC['group_spec'])
        self.RESULT.grouping = self.SPEC.get('grouping', 1)

    def build_group_obj(self):
        self.SENSOR_OBJ = self.get_sensor_obj()
        self.SENSOR_PARAMS = self.create_sensor_params()
        self.FILTER_SENSOR = self.create_filter_sensor()
        self.FILTER = self.create_filter()
        self.FILTERLIST = self.create_filterlist()
        self.RESULT = self.create_filtergroup()
        self.RESULT.grouping = self.SPEC.get('grouping', 1)

    def create_sensor_params(self):
        pargs = {}
        pargs.update(self.KWARGS)
        pargs['named_param_spec'] = self.SPEC.get('named_param_spec', {})
        pargs['unnamed_param_spec'] = self.SPEC.get('unnamed_param_spec', [])
        pargs['obj'] = self.SENSOR_OBJ
        result = create_params(**pargs)
        return result

    def get_sensor_obj(self):
        result = self.HANDLER.get_sensors(limit_exact=1, specs=self.SPEC['sensor_spec'])
        return result

    def create_filter_sensor(self):
        result = Sensor()
        if self.SENSOR_PARAMS:
            result.source_hash = self.SENSOR_OBJ.hash
            result.parameters = self.SENSOR_PARAMS
        else:
            result.hash = self.SENSOR_OBJ.hash
        log_result('create_filter_sensor', result, locals())
        return result

    def create_filter(self):
        result = create_filter(self.FILTER_SENSOR, self.SPEC['filter_spec'])
        return result

    def create_filterlist(self):
        result = FilterList(filter=[self.FILTER])
        log_result('create_filterlist', result, locals())
        return result

    def create_filtergroup(self):
        result = Group(filters=self.FILTERLIST)
        log_result('create_filtergroup', result, locals())
        return result


def log_result(caller, result, caller_locals):
    m = "{}() result:: {}".format(caller, result)
    MYLOG.debug(m)
    # m = "caller_locals for {}():: {}".format(caller, caller_locals)
    # MYLOG.debug(m)


def get_group_hierarchy(g, level=1):
    def get_map(t, m):
        return m[t] if t in m else m['*']

    def mn(not_flag):
        m = {None: ' ---- ', 1: ' isnt ', 0: ' is   ', '*': ' ???? '}
        return get_map(not_flag, m)

    def ma(and_flag):
        m = {None: ' --- ', 1: ' and ', 0: ' or  ', '*': ' ??? '}
        return get_map(and_flag, m)

    grp_m = (
        "{}lvl {}\tgrouping:{}\tsubgroups={}\tfilters={}\tname:{}\tand_flag:{}\tnot_flag:{}"
    ).format
    filt_m = (
        "{0}\t[filter] hash:'{1.sensor.hash}' source_hash:'{1.sensor.source_hash}' "
        "operator:'{1.operator}' value_type:'{1.value_type}'  value:'{1.value}' not_flag:'{2}'"
    ).format
    result = []
    grouping = getattr(g, 'grouping', None)
    sglen = len(g.sub_groups or [])
    flen = len(g.filters or [])
    pre = '\t' * level
    result.append(grp_m(pre, level, grouping, sglen, flen, g.name, ma(g.and_flag), mn(g.not_flag)))
    if g.filters:
        result += [filt_m(pre, f, mn(f.not_flag)) for f in g.filters]
    if g.sub_groups:
        for i in g.sub_groups:
            result += get_group_hierarchy(i, level + 1)
    return result


def create_filter(sensor, filter_spec, **kwargs):
    result = None
    if filter_spec:
        if not isinstance(filter_spec, dict):
            err = 'filter_spec must be a dict, you supplied type {}: {}'
            err = err.format(type(filter_spec).__name__, filter_spec)
            raise ObjectCreateError(err)

        if 'value' not in filter_spec:
            err = 'filter_spec dict must have a "value" key, you supplied: {}'
            err = err.format(filter_spec)
            raise ObjectCreateError(err)

        oargs = {k: filter_spec.get(k, v) for k, v in FILTER_DEFAULTS.items()}
        oargs['sensor'] = sensor
        result = Filter(**oargs)
    log_result('create_filter', result, locals())
    return result


def create_group(group_spec, sub_groups):
    oargs = {k: group_spec.get(k, v) for k, v in GROUP_DEFAULTS.items()}
    oargs['sub_groups'] = GroupList(group=sub_groups)
    result = Group(**oargs)
    return result


def create_question(handler, **kwargs):
    selectlist = create_question_selectlist(handler, **kwargs)
    group = create_question_group(handler, **kwargs)
    oargs = {k: kwargs.get(k, v) for k, v in QUESTION_DEFAULTS.items()}
    result = Question(selects=selectlist, group=group, **oargs)
    log_result('create_question', result, locals())
    return result


def create_params(obj, **kwargs):
    creator = CreateParams(obj, **kwargs)
    result = creator.RESULT
    return result


def create_select(handler, spec, **kwargs):
    creator = CreateSelect(handler, spec, **kwargs)
    result = creator.RESULT
    return result


def create_filter_group(handler, spec, **kwargs):
    creator = CreateFilterGroup(handler, spec, **kwargs)
    result = creator.RESULT
    return result


def create_right_group(right_items, right_groups, grouping):
    sub_groups = [x for x in right_items if getattr(x, 'grouping', 1) == grouping]
    group_spec = right_groups.get(grouping, {})
    result = create_group(group_spec, sub_groups)
    log_result('create_right_group {}'.format(grouping), result, locals())
    return result


def create_parent_group(right_items, **kwargs):
    if 'right_groups' in kwargs:
        right_groups = kwargs.pop('right_groups')
    else:
        right_groups = {}

    all_groupings = [x.grouping for x in right_items if x.grouping != 0]
    parent_sub_groups = [create_right_group(right_items, right_groups, g) for g in all_groupings]
    parent_sub_groups += [x for x in right_items if x.grouping == 0]
    parent_group_spec = right_groups.get(0, {})
    result = create_group(parent_group_spec, parent_sub_groups)
    log_result('create_parent_group', result, locals())
    return result


def create_question_group(handler, **kwargs):
    right_items = []
    result = None

    if 'right' in kwargs:
        right = kwargs.pop('right')
        right_items = [create_filter_group(handler, s, **kwargs) for s in right]
        result = create_parent_group(right_items, **kwargs)
        hierarchy = get_group_hierarchy(result)
        m = 'create_question_group hierarchy:\n{}'
        m = m.format('\n'.join(hierarchy))
        MYLOG.debug(m)

    else:
        m = "No right side supplied for create_question, question will be '... from all machines'"
        MYLOG.info(m)
    log_result('create_question_group', result, locals())
    return result


def create_question_selectlist(handler, **kwargs):
    left_items = []
    if 'left' in kwargs:
        left = kwargs.pop('left')
        left_items = [create_select(handler, s, **kwargs) for s in left]

    if not left_items:
        m = "No left side supplied for create_question, question will be 'Get Online from...'"
        MYLOG.info(m)

    result = SelectList(select=left_items)
    log_result('create_question_selectlist', result, locals())
    return result


def create_cachefilterlist(specs):
    """pass."""
    result = CacheFilterList()
    if not isinstance(specs, (list, tuple)):
        specs = [specs]
    for spec in specs:
        result.append(create_cachefilter(**spec))
    log_result('create_cachefilterlist', result, locals())
    return result


def create_cachefilter(field, value, operator=None, field_type=None, not_flag=None, **kwargs):
    """pass."""
    result = CacheFilter()
    result.field = field
    result.value = value
    if operator is not None:
        result.operator = operator
    if field_type is not None:
        result.type = field_type
    if not_flag is not None:
        result.not_flag = not_flag
    log_result('create_cachefilter', result, locals())
    return result
