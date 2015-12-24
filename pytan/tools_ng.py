"""Tools for Tanium NG package for :mod:`pytan`"""

import logging
import datetime
from . import utils, tanium_ng

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

mylog = logging.getLogger(__name__)


def shrink_obj(obj, attrs=None):
    """Returns a new class of obj with only id/name/hash defined

    Parameters
    ----------
    obj : :class:`tanium_ng.base.BaseType`
        * Object to shrink
    attrs : list of str
        * default: None
        * list of attribute str's to copy over to new object, will default to
        ['name', 'id', 'hash'] if None

    Returns
    -------
    new_obj : :class:`tanium_ng.base.BaseType`
        * Shrunken object
    """
    if attrs is None:
        attrs = ['name', 'id', 'hash']

    new_obj = obj.__class__()
    [setattr(new_obj, a, getattr(obj, a)) for a in attrs if getattr(obj, a, None) is not None]
    return new_obj


def plugin_zip(p):
    """Maps columns to values for each row in a plugins sql_response and returns a list of dicts

    Parameters
    ----------
    p : :class:`tanium_ng.plugin.Plugin`
        * plugin object

    Returns
    -------
    dict
        * the columns and result_rows of the sql_response in Plugin object zipped up into a
        dictionary
    """
    return [
        dict(zip(p.sql_response.columns, x)) for x in p.sql_response.result_row
    ]


# DEFINITELY NEW

def create_cf_listobj(specs):
    """pass."""
    result = tanium_ng.CacheFilterList()
    if not isinstance(specs, (list, tuple)):
        specs = [specs]
    for spec in specs:
        result.append(create_cf_obj(**spec))
    return result


def create_cf_obj(field, value, operator=None, field_type=None, not_flag=None, **kwargs):
    """pass."""
    result = tanium_ng.CacheFilter()
    result.field = field
    result.value = value
    if operator is not None:
        result.operator = operator
    if field_type is not None:
        result.type = field_type
    if not_flag is not None:
        result.not_flag = not_flag
    return result


def xml_to_result_set_obj(x):
    """Wraps a Result Set XML from a server side export in the appropriate tags and returns a
    ResultSet object

    Parameters
    ----------
    x : str
        * str of XML to convert to a ResultSet object

    Returns
    -------
    rs : :class:`utils.tanium_ng.result_set.ResultSet`
        * x converted into a ResultSet object
    """
    rs_xml = '<result_sets><result_set>{}</result_set></result_sets>'.format
    rs_xml = rs_xml(x)
    rs_tree = ET.fromstring(rs_xml)
    rs = tanium_ng.ResultSet.fromSOAPElement(rs_tree)
    rs._RAW_XML = rs_xml
    return rs


def create_selectlist_obj(specs):
    """pass."""
    result = tanium_ng.SelectList()
    for spec in specs:
        result.append(create_select_obj(spec))
    return result


def create_select_obj(spec):
    """pass."""
    result = tanium_ng.Select()
    result.sensor = tanium_ng.Sensor()

    if 'parameters' in spec:
        result.sensor.source_id = spec['sensor_object'].id
        result.sensor.parameters = create_parameter_objlist(spec['parameters'])
    else:
        result.sensor.id = spec['sensor_object'].id

    if 'filter' in spec:
        result.filter = create_filter_obj(spec)
    return result


def create_filter_obj(spec):
    """pass."""
    filter_spec = spec['filter']
    result = tanium_ng.Filter()
    result.sensor = tanium_ng.Sensor()
    result.sensor.hash = spec['sensor_object'].hash  # needs to be hash, id no work!
    result.value = filter_spec['value']
    result.operator = filter_spec.get('operator', 'Equal')  # tanium default operator is Less!
    return result


def create_parameter_objlist(parameters, **kwargs):
    """pass."""
    result = tanium_ng.ParameterList()
    for k, v in parameters.items():
        result.append(create_parameter_obj(key=k, val=v, **kwargs))
    return result


def create_parameter_obj(key, val, delim='||'):
    """pass."""
    result = tanium_ng.Parameter()
    result.key = '{0}{1}{0}'.format(delim, key)
    result.value = val
    return result


def create_filterlist_obj(spec):
    """pass."""
    result = tanium_ng.FilterList()
    result.append(create_filter_obj(spec))
    return result


def create_group_with_filter_obj(spec):
    """pass."""
    result = tanium_ng.Group()
    result.filters = create_filterlist_obj(spec)
    return result


def create_parent_group_obj(specs):
    """pass."""
    result = tanium_ng.Group()
    result.sub_groups = tanium_ng.GroupList()
    parent_sub = tanium_ng.Group()
    parent_sub.sub_groups = tanium_ng.GroupList()
    result.sub_groups.append(parent_sub)

    for idx, spec in enumerate(specs):
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


def create_question_obj(left=[], right=[]):
    """pass."""
    result = tanium_ng.Question()
    result.selects = create_selectlist_obj(left)
    if right:
        result.group = create_parent_group_obj(right)
    return result


def check_limits(objects, **kwargs):
    """pass."""
    specs = kwargs.get('specs', [])

    if not isinstance(objects, tanium_ng.BaseType):
        err = "{} must be a tanium_ng object, type: {}"
        err = err.format(objects, type(objects))
        raise utils.exceptions.PytanError(err)

    # coerce single items into a list
    objects_class = objects.__class__.__name__
    if not objects_class.endswith('List'):
        new_class = objects_class + 'List'
        new_objects = getattr(tanium_ng, new_class)()
        new_objects.append(objects)
        objects = new_objects

    limit_map = [
        {'k': 'limit_min', 'm': "{} items or more", 'e': '>='},
        {'k': 'limit_max', 'm': "{} items or less", 'e': '<='},
        {'k': 'limit_exact', 'm': "{} items exactly", 'e': '=='},
    ]

    for l in limit_map:
        limit_val = kwargs.get(l['k'], None)

        if limit_val is None:
            m = "check_limits(): found {}, skipped {} (not supplied)"
            m = m.format(objects, l['k'], )
            mylog.debug(m)
            continue

        limit_val = int(limit_val)
        e = "len(objects) {} limit_val".format(l['e'])
        limit_pass = eval(e)

        p = "check_limits(): found {}, {} {} (must be {})"
        limit_msg = l['m'].format(limit_val)

        if limit_pass:
            m = p.format(objects, 'PASSED', l['k'], limit_msg)
            mylog.debug(m)
        else:
            # get the str of each objects for printing in exception
            objtxt = '\n\t'.join([str(x) for x in objects])

            # get the specs txt if any specs
            specstxt = "\n"
            if specs:
                specstxt = "\nspecs:\n\t" + "\n\t".join([str(x) for x in specs]) + "\n"

            err_pre = p.format(objects, 'FAILED', l['k'], limit_msg)
            err = "{}{}returned items:\n\t{}"
            err = err.format(err_pre, specstxt, objtxt)
            mylog.critical(err)
            raise utils.exceptions.PytanError(err)


def question_start_time(q):
    """Caclulates the start time of a question by doing q.expiration - q.expire_seconds

    Parameters
    ----------
    q : :class:`tanium_ng.Question`
        * Question object to calculate start time for

    Returns
    -------
    tuple : str, datetime
        * a tuple containing the start time first in str format for Tanium Server API, second in
        datetime object format
    """
    expire_dt = utils.tools.timestr_to_datetime(q.expiration)
    expire_seconds_delta = datetime.timedelta(seconds=q.expire_seconds)
    start_time_dt = expire_dt - expire_seconds_delta
    start_time = utils.tools.datetime_to_timestr(start_time_dt)
    result = (start_time, start_time_dt)
    return result
