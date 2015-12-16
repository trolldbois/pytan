# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""TaniumPy object module for for :mod:`pytan`"""

import logging
from .external import taniumpy

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

mylog = logging.getLogger(__name__)


def shrink_obj(obj, attrs=None):
    """Returns a new class of obj with only id/name/hash defined

    Parameters
    ----------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * Object to shrink
    attrs : list of str
        * default: None
        * list of attribute str's to copy over to new object, will default to ['name', 'id', 'hash'] if None

    Returns
    -------
    new_obj : :class:`taniumpy.object_types.base.BaseType`
        * Shrunken object
    """
    if attrs is None:
        attrs = ['name', 'id', 'hash']

    new_obj = obj.__class__()
    [setattr(new_obj, a, getattr(obj, a)) for a in attrs if getattr(obj, a, '')]
    return new_obj


def plugin_zip(p):
    """Maps columns to values for each row in a plugins sql_response and returns a list of dicts

    Parameters
    ----------
    p : :class:`taniumpy.object_types.plugin.Plugin`
        * plugin object

    Returns
    -------
    dict
        * the columns and result_rows of the sql_response in Plugin object zipped up into a dictionary
    """
    return [
        dict(zip(p.sql_response.columns, x)) for x in p.sql_response.result_row
    ]


# DEFINITELY NEW

def create_cf_listobj(specs):
    """pass."""
    result = taniumpy.CacheFilterList()
    if not isinstance(specs, (list, tuple)):
        specs = [specs]
    for spec in specs:
        result.append(create_cf_obj(**spec))
    return result


def create_cf_obj(field, value, operator=None, field_type=None, not_flag=None, **kwargs):
    """pass."""
    result = taniumpy.CacheFilter()
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
    """Wraps a Result Set XML from a server side export in the appropriate tags and returns a ResultSet object

    Parameters
    ----------
    x : str
        * str of XML to convert to a ResultSet object

    Returns
    -------
    rs : :class:`utils.taniumpy.object_types.result_set.ResultSet`
        * x converted into a ResultSet object
    """
    rs_xml = '<result_sets><result_set>{}</result_set></result_sets>'.format
    rs_xml = rs_xml(x)
    rs_tree = ET.fromstring(rs_xml)
    rs = taniumpy.ResultSet.fromSOAPElement(rs_tree)
    rs._RAW_XML = rs_xml
    return rs


def create_selectlist_obj(specs):
    """pass."""
    result = taniumpy.SelectList()
    for spec in specs:
        result.append(create_select_obj(spec))
    return result


def create_select_obj(spec):
    """pass."""
    result = taniumpy.Select()
    result.sensor = taniumpy.Sensor()

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
    result = taniumpy.Filter()
    result.sensor = taniumpy.Sensor()
    result.sensor.hash = spec['sensor_object'].hash  # needs to be hash, id no work!
    result.value = filter_spec['value']
    result.operator = filter_spec.get('operator', 'Equal')  # tanium default operator is Less!
    return result


def create_parameter_objlist(parameters, **kwargs):
    """pass."""
    result = taniumpy.ParameterList()
    for k, v in parameters.iteritems():
        result.append(create_parameter_obj(key=k, val=v, **kwargs))
    return result


def create_parameter_obj(key, val, delim='||'):
    """pass."""
    result = taniumpy.Parameter()
    result.key = '{0}{1}{0}'.format(delim, key)
    result.value = val
    return result


def create_filterlist_obj(spec):
    """pass."""
    result = taniumpy.FilterList()
    result.append(create_filter_obj(spec))
    return result


def create_group_with_filter_obj(spec):
    """pass."""
    result = taniumpy.Group()
    result.filters = create_filterlist_obj(spec)
    return result


def create_parent_group_obj(specs):
    """pass."""
    result = taniumpy.Group()
    result.sub_groups = taniumpy.GroupList()
    parent_sub = taniumpy.Group()
    parent_sub.sub_groups = taniumpy.GroupList()
    result.sub_groups.append(parent_sub)

    for idx, spec in enumerate(specs):
        # if they supplied a group object, use that instead of creating one
        if 'group_object' in spec:
            parent_sub.sub_groups.append(spec['group_object'])
            continue

        first = idx == 0
        this_and = spec['filter'].get('and_flag', None)

        # if this is the first spec
        # add a group with a filter from this spec to the current parent_sub
        if first:
            parent_sub.sub_groups.append(create_group_with_filter_obj(spec))
            if this_and is not None:
                parent_sub.and_flag = this_and
            continue

        # if this spec does not have and_flag
        # add a group with a filter from this spec to the current parent_sub
        if this_and is None:
            parent_sub.sub_groups.append(create_group_with_filter_obj(spec))
            continue

        # if this spec does have an and_flag and it doesn't match the current
        # parent_sub's and, create a new parent_sub
        # add a group with a filter from this spec to the new parent_sub
        if parent_sub.and_flag != this_and:
            parent_sub = taniumpy.Group()
            parent_sub.and_flag = this_and
            parent_sub.sub_groups = taniumpy.GroupList()
            parent_sub.sub_groups.append(create_group_with_filter_obj(spec))
            result.sub_groups.append(parent_sub)
            continue

        # add a group with a filter from this spec to the current parent_sub
        parent_sub.sub_groups.append(create_group_with_filter_obj(spec))
        continue

    return result


def create_question_obj(left=[], right=[]):
    """pass."""
    result = taniumpy.Question()
    result.selects = create_selectlist_obj(left)
    if right:
        result.group = create_parent_group_obj(right)
    return result
