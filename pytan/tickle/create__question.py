import logging

from pytan import PytanError, tanium_ng

MYLOG = logging.getLogger(__name__)


class ObjectCreateError(PytanError):
    pass


def printable_spec(spec):
    result = {k: v for k, v in spec.items() if not k.endswith('_object')}
    return result


def create_selectlist(specs):
    """pass."""
    result = tanium_ng.SelectList()
    for spec in specs:
        result.append(create_select(spec))
    log_result('create_selectlist', result, specs)
    return result


def create_select(spec):
    """pass."""
    result = tanium_ng.Select()
    result.sensor = tanium_ng.Sensor()
    if 'parameters' in spec:
        result.sensor.source_id = spec['sensor_object'].id
        result.sensor.parameters = create_parameterlist(spec['parameters'])
    else:
        result.sensor.id = spec['sensor_object'].id
    if 'filter' in spec:
        result.filter = create_filter(spec)
    log_result('create_select', result, spec)
    return result


def create_filter(spec):
    """pass."""
    filter_spec = spec['filter']
    result = tanium_ng.Filter()
    result.sensor = tanium_ng.Sensor()
    result.sensor.hash = spec['sensor_object'].hash  # needs to be hash, id no work!
    result.value = filter_spec['value']
    result.operator = filter_spec.get('operator', 'Equal')  # tanium default operator is Less!
    log_result('create_filter', result, spec)
    return result


def create_parameterlist(parameters, **kwargs):
    """pass."""
    result = tanium_ng.ParameterList()
    for k, v in parameters.items():
        result.append(create_parameter(key=k, val=v, **kwargs))
    log_result('create_parameterlist', result, locals())
    return result


def create_parameter(key, val, delim='||'):
    """pass."""
    result = tanium_ng.Parameter()
    result.key = '{0}{1}{0}'.format(delim, key)
    result.value = val
    log_result('create_parameter', result, locals())
    return result


def create_filterlist(spec):
    """pass."""
    result = tanium_ng.FilterList()
    result.append(create_filter(spec))
    log_result('create_filterlist', result, locals())
    return result


def create_group_with_filter_obj(spec):
    """pass."""
    result = tanium_ng.Group()
    result.filters = create_filterlist(spec)
    log_result('create_group_with_filter_obj', result, locals())
    return result


def create_parent_group(specs):
    """pass."""
    result = tanium_ng.Group()
    result.sub_groups = tanium_ng.GroupList()
    parent_sub = tanium_ng.Group()
    parent_sub.sub_groups = tanium_ng.GroupList()
    result.sub_groups.append(parent_sub)

    for idx, spec in enumerate(specs):
        if 'filter' not in spec:
            err = "Must specify 'filter' to apply to right spec: {}"
            err = err.format(printable_spec(spec))
            MYLOG.error(err)
            raise ObjectCreateError(err)

        # if they supplied a group object, use that instead of creating one
        if 'group_object' in spec:
            print("using group object instead of filter")
            parent_sub.sub_groups.append(spec['group_object'])
            continue

        first = idx == 0
        this_and = spec['filter'].get('and_flag', None)

        # if this is the first spec
        # add a group with a filter from this spec to the current parent_sub
        if first:
            new_group = create_group_with_filter_obj(spec)
            print('first: creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)

            if this_and is not None:
                print('applying and_flag {} to parent_sub'.format(this_and))
                parent_sub.and_flag = this_and
            continue

        # if this spec does not have and_flag
        # add a group with a filter from this spec to the current parent_sub
        if this_and is None:
            new_group = create_group_with_filter_obj(spec)
            print('not first: and is None, creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)
            continue

        # if this spec does have an and_flag and it doesn't match the current
        # parent_sub's and, create a new parent_sub
        # add a group with a filter from this spec to the new parent_sub
        if parent_sub.and_flag != this_and:
            print('not first:, and is {} creating a new parent_sub'.format(this_and))
            parent_sub = tanium_ng.Group()
            parent_sub.and_flag = this_and
            parent_sub.sub_groups = tanium_ng.GroupList()
            result.sub_groups.append(parent_sub)

            new_group = create_group_with_filter_obj(spec)
            print('not first: creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)
            continue

        new_group = create_group_with_filter_obj(spec)
        print('catch all: creating a new group and adding to parent_sub')
        print(spec['filter'])
        parent_sub.sub_groups.append(new_group)
        continue

    recurse_group(result)
    log_result('create_parent_group', result, locals())
    return result


def recurse_group(g, level=1):
    """pass"""
    sglen = len(g.sub_groups or [])
    flen = len(g.filters or [])

    a = "level: {}, and_flag: {}, filters: {}, sub_groups: {}"
    a = a.format(level, g.and_flag, flen, sglen)
    print(a)

    if g.filters:
        for i in g.filters:
            f = "operator: {0.operator} value: {0.value}".format(i)
            m = "level: {}, and_flag: {}, filter: {}"
            m = m.format(level, g.and_flag, f)
            print(m)

    if g.sub_groups:
        for i in g.sub_groups:
            recurse_group(i, level + 1)


def create_question(**kwargs):
    """pass."""
    left = kwargs.get('left', [])
    right = kwargs.get('right', [])
    max_age_seconds = kwargs.get('max_age_seconds', 0)
    result = tanium_ng.Question()
    result.selects = create_selectlist(left)
    if right:
        result.group = create_parent_group(right)
    if max_age_seconds:
        result.max_age_seconds = int(max_age_seconds)
    log_result('create_question', result, locals())
    return result


def log_result(caller, result, caller_locals):
    m = "{}() result:: {}".format(caller, result)
    MYLOG.info(m)
    # m = "caller_locals for {}():: {}".format(caller, caller_locals)
    # MYLOG.debug(m)
