# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""TaniumPy object module for for :mod:`pytan`"""

import logging
import pprint
import json
from .external import taniumpy
from .exceptions import ValidationError
from .exceptions import PytanError
from . import constants

mylog = logging.getLogger(__name__)


def build_selectlist_obj(sensor_defs):
    """Creates a SelectList object from sensor_defs

    Parameters
    ----------
    sensor_defs : list of dict
        * List of dict that are sensor definitions

    Returns
    -------
    select_objlist : :class:`taniumpy.object_types.select_list.SelectList`
        * SelectList object with list of :class:`taniumpy.object_types.select.Select` built from `sensor_defs`
    """
    select_objlist = taniumpy.SelectList()

    for d in sensor_defs:

        # validate/map sensor params into a ParameterList()
        sensor_obj = d['sensor_obj']
        user_params = d.get('params', {})
        param_objlist = build_param_objlist(
            obj=sensor_obj,
            user_params=user_params,
            delim='||',
            derive_def=True,
            empty_ok=True
        )

        # validate/map sensor filter into a Filter()
        filter_obj = get_filter_obj(d)

        # get the options the user supplied
        options = d.get('options', {})

        # update filter_obj with any options the user supplied
        filter_obj = apply_options_obj(options, filter_obj, 'filter')

        # create a select object for this sensor
        select_obj = taniumpy.Select()
        select_obj.sensor = taniumpy.Sensor()
        select_obj.filter = filter_obj

        # if there are parameters, we need to set the following to
        # sensor_obj.id:
        #  - select_obj.sensor_obj.source_id
        #  - select_obj.filter.sensor.id
        if param_objlist:
            select_obj.sensor.source_id = d['sensor_obj'].id
            select_obj.sensor.parameters = param_objlist
            select_obj.filter.sensor.id = d['sensor_obj'].id
        else:
            select_obj.sensor.hash = d['sensor_obj'].hash

        select_objlist.select.append(select_obj)
    return select_objlist


def build_group_obj(filter_defs, option_defs):
    """Creates a Group object from filter_defs and option_defs

    Parameters
    ----------
    filter_defs : list of dict
        * List of dict that are question filter definitions
    option_defs : dict
        * dict of question filter options

    Returns
    -------
    group_obj : :class:`taniumpy.object_types.group.Group`
        * Group object with list of :class:`taniumpy.object_types.filter.Filter` built from `filter_defs` and `option_defs`
    """
    filter_objlist = taniumpy.FilterList()

    for d in filter_defs:
        # validate/map question filter into a Filter()
        filter_obj = get_filter_obj(d)

        # update filter_obj with any options
        filter_obj = apply_options_obj(option_defs, filter_obj, 'filter')
        filter_objlist.filter.append(filter_obj)

    group_obj = taniumpy.Group()
    group_obj.filters = filter_objlist
    group_obj = apply_options_obj(option_defs, group_obj, 'group')

    return group_obj


def build_manual_q(selectlist_obj, group_obj):
    """Creates a Question object from selectlist_obj and group_obj

    Parameters
    ----------
    selectlist_obj : :class:`taniumpy.object_types.select_list.SelectList`
        * SelectList object to add to Question object
    group_obj : :class:`taniumpy.object_types.group.Group`
        * Group object to add to Question object

    Returns
    -------
    add_q_obj : :class:`taniumpy.object_types.question.Question`
        * Question object built from selectlist_obj and group_obj
    """
    add_q_obj = taniumpy.Question()
    add_q_obj.selects = selectlist_obj
    add_q_obj.group = group_obj
    return add_q_obj


def get_obj_params(obj):
    """Get the parameters from a TaniumPy object and JSON load them

    obj : :class:`taniumpy.object_types.base.BaseType`
        * TaniumPy object to get parameters from

    Returns
    -------
    params : dict
        * JSON loaded dict of parameters from `obj`

    """
    # get the parameter definitions
    param_def = getattr(obj, 'parameter_definition', {}) or {}

    # json load the parameter definitions if they exist
    if param_def:
        param_def = json.loads(param_def)

    # get the list of parameters from the parameter definitions
    params = param_def.get('parameters', [])
    return params


def build_param_obj(key, val, delim=''):
    """Creates a Parameter object from key and value, surrounding key with delim

    Parameters
    ----------
    key : str
        * key to use for parameter
    value : str
        * value to use for parameter
    delim : str
        * str to surround key with when adding to parameter object

    Returns
    -------
    param_obj : :class:`taniumpy.object_types.parameter.Parameter`
        * Parameter object built from key and val
    """
    # create a parameter object
    param_obj = taniumpy.Parameter()
    param_obj.key = '{0}{1}{0}'.format(delim, key)
    param_obj.value = val
    return param_obj


def derive_param_default(obj_param):
    """Derive a parameter default

    Parameters
    ----------
    obj_param : dict
        * parameter dict from TaniumPy object

    Returns
    -------
    def_val : str
        * default value derived from obj_param
    """
    # get the default value for this param if it exists
    def_val = obj_param.get('defaultValue', '')

    # get requireSelection for this param if it exists (pulldown menus)
    req_sel = obj_param.get('requireSelection', False)

    # get values for this param if it exists (pulldown menus)
    values = obj_param.get('values', [])

    # if this param requires a selection and it has a list of values
    # and there is no default value, use the first value as the
    # default value
    if req_sel and values and not def_val:
        def_val = values[0]
    return def_val


def build_param_objlist(obj, user_params, delim='', derive_def=False, empty_ok=False):
    """Creates a ParameterList object from user_params

    Parameters
    ----------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * TaniumPy object to verify parameters against
    user_params : dict
        * dict describing key and value of user supplied params
    delim : str
        * str to surround key with when adding to parameter object
    derive_def : bool, optional
        * False: Do not derive default values, and throw a :exc:`ValidationError` if user did not supply a value for a given parameter
        * True: Try to derive a default value for each parameter if user did not supply one
    empty_ok : bool, optional
        * False: If user did not supply a value for a given parameter, throw a :exc:`ValidationError`
        * True: If user did not supply a value for a given parameter, do not add the parameter to the ParameterList object

    Returns
    -------
    param_objlist : :class:`taniumpy.object_types.parameter_list.ParameterList`
        ParameterList object with list of :class:`taniumpy.object_types.parameter.Parameter` built from user_params
    """
    # extract the params from the object
    obj_params = get_obj_params(obj)
    obj_name = str(obj)
    param_objlist = taniumpy.ParameterList()

    processed = []

    for obj_param in obj_params:
        # get the key for this param
        p_key = obj_param["key"]
        processed.append(p_key)
        user_val = user_params.get(p_key, '')

        if not user_val and derive_def:
            user_val = derive_param_default(obj_param)

        if not user_val and not empty_ok:
            err = (
                "{} parameter key '{}' requires a value, "
                "parameter definition:\n{}"
            ).format
            raise ValidationError(err(obj_name, p_key, pprint.pformat(obj_param)))
        param_obj = build_param_obj(p_key, user_val, delim)
        param_objlist.append(param_obj)

        dbg = "Parameter {} for {} mapped to: {}".format
        mylog.debug(dbg(p_key, obj_name, param_obj))

    # ADD SUPPORT FOR PARAMS THAT ARE NOT IN OBJECT
    for k, v in user_params.iteritems():
        if k in processed:
            continue
        processed.append(k)
        param_obj = build_param_obj(k, v, delim)
        param_objlist.append(param_obj)

        dbg = "Undefined Parameter {} for {} mapped to: {}".format
        mylog.debug(dbg(k, obj_name, param_obj))

    return param_objlist


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


def copy_obj(obj, skip_attrs=None):
    """Returns a new class of obj with with out any attributes in skip_attrs specified

    Parameters
    ----------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * Object to copy
    skip_attrs : list of str
        * default: None
        * list of attribute str's to skip copying over to new object, will default to [] if None

    Returns
    -------
    new_obj : :class:`taniumpy.object_types.base.BaseType`
        * Copied object with attributes in skip_attrs skipped
    """
    if not skip_attrs:
        skip_attrs = []

    new_obj = obj.__class__()
    [
        setattr(new_obj, a, getattr(obj, a))
        for a in vars(obj)
        if getattr(obj, a, None) is not None
        and a not in skip_attrs
    ]
    return new_obj


def copy_package_obj_for_action(obj, skip_attrs=None):
    """Returns a new class of package obj with with out any attributes in skip_attrs specified

    Parameters
    ----------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * Object to copy
    skip_attrs : list of str
        * default: None
        * list of attribute str's to skip copying over to new object, default if None: ['id', 'deleted_flag', 'available_time', 'creation_time', 'modification_time', 'source_id']

    Returns
    -------
    new_obj : :class:`taniumpy.object_types.base.BaseType`
        * Copied object with attributes in skip_attrs skipped
    """
    if skip_attrs is None:
        # names of attributes to skip copying over from source package
        skip_attrs = [
            'id',
            'deleted_flag',
            'available_time',
            'creation_time',
            'modification_time',
            'source_id',
            'files',
        ]

    new_obj = copy_obj(obj, skip_attrs)
    return new_obj


def get_filter_obj(sensor_def):
    """Creates a Filter object from sensor_def

    Parameters
    ----------
    sensor_def : dict
        * dict containing sensor definition

    Returns
    -------
    filter_obj : :class:`taniumpy.object_types.filter.Filter`
        * Filter object created from `sensor_def`
    """
    sensor_obj = sensor_def['sensor_obj']

    # create our basic filter that is needed no matter what
    filter_obj = taniumpy.Filter()
    filter_obj.sensor = taniumpy.Sensor()
    filter_obj.sensor.hash = sensor_obj.hash

    # get the filter the user supplied
    filter_def = sensor_def.get('filter', {})

    # if no user supplied filter, return the basic filter object
    if not filter_def:
        return filter_obj

    # operator required
    def_op = filter_def.get('operator', None)
    if not def_op:
        err = "Filter {!r} requires an 'operator' key!".format
        raise ValidationError(err(filter_def))

    # not_flag optional
    def_not_flag = filter_def.get('not_flag', None)

    # value required
    def_value = filter_def.get('value', None)
    if not def_value:
        err = "Filter {!r} requires a 'value' key!".format
        raise ValidationError(err(filter_def))

    found_match = False
    for fm in constants.FILTER_MAPS:
        # if user supplied operator does not match this operator, next
        if not def_op.lower() == fm['operator'].lower():
            continue

        found_match = True

        filter_obj.value = def_value

        filter_obj.operator = fm['operator']
        if def_not_flag is not None:
            filter_obj.not_flag = def_not_flag

        dbg = "Filter {!r} mapped to: {}".format
        mylog.debug(dbg(filter_def, str(filter_obj)))
        break

    if not found_match:
        err = "Invalid filter {!r}".format
        raise ValidationError(err(filter_def))

    return filter_obj


def apply_options_obj(options, obj, dest):
    """Updates an object with options

    Parameters
    ----------
    options : dict
        * dict containing options definition
    obj : :class:`taniumpy.object_types.base.BaseType`
        * TaniumPy object to apply `options` to
    dest : list of str
        * list of valid destinations (i.e. `filter` or `group`)

    Returns
    -------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * TaniumPy object updated with attributes from `options`
    """
    # if no user supplied options, return the filter object unchanged
    if not options:
        return obj

    for k, v in options.iteritems():
        for om in constants.OPTION_MAPS:

            if om['destination'] != dest:
                continue

            om_attrs = om.get('attrs', {}).keys()
            om_attr = om.get('attr', '')

            if om_attr:
                om_attrs.append(om_attr)

            if k.lower() not in om_attrs:
                continue

            dbg = "option {!r} value {!r} mapped to: {!r}".format
            mylog.debug(dbg(k, v, om))

            valid_values = om.get('valid_values', [])
            valid_type = om.get('valid_type', str)

            if valid_values:
                valid_values = eval(valid_values)
                valid_values_str = " -- valid values: "
                valid_values_str += ', '.join(valid_values)
            else:
                valid_values = []
                valid_values_str = ""

            if len(str(v)) == 0:
                err = (
                    "Option {!r} requires a {} value{}"
                ).format
                raise ValidationError(err(k, valid_type, valid_values_str))

            if valid_type == int:
                try:
                    v = int(v)
                except:
                    err = (
                        "Option {!r} value {!r} is not an integer"
                    ).format
                    raise ValidationError(err(k, v))

            if valid_type == str:
                if not isinstance(v, (basestring)):
                    err = (
                        "Option {!r} value {!r} is not a string"
                    ).format
                    raise ValidationError(err(k, v))

            value_match = None
            if valid_values:
                for x in valid_values:
                    if v.lower() == x.lower():
                        value_match = x
                        break

                if value_match is None:
                    err = (
                        "Option {!r} value {!r} does not match one of {}"
                    ).format
                    raise ValidationError(err(k, v, valid_values))
                else:
                    v = value_match

            # update obj with k = v
            setattr(obj, k, v)

            break

    dbg = "Options {!r} updated to: {}".format
    mylog.debug(dbg(options, str(obj)))
    return obj


def empty_obj(taniumpy_object):
    """Validate that a given TaniumPy object is not empty

    Parameters
    ----------
    taniumpy_object : :class:`taniumpy.object_types.base.BaseType`
        * object to check if empty

    Returns
    -------
    bool
        * True if `taniumpy_object` is considered empty, False otherwise
    """
    v = [getattr(taniumpy_object, '_list_properties', {}), isinstance(taniumpy_object, (basestring))]
    if any(v) and not taniumpy_object:
        return True
    else:
        return False


def get_q_obj_map(qtype):
    """Gets an object map for `qtype`

    Parameters
    ----------
    qtype : str
        * question type to get object map from in :data:`constants.Q_OBJ_MAP`

    Returns
    -------
    obj_map : dict
        * matching object map for `qtype` from :data:`constants.Q_OBJ_MAP`
    """
    try:
        obj_map = constants.Q_OBJ_MAP[qtype.lower()]
    except KeyError:
        err = "{} not a valid question type, must be one of {!r}".format
        raise ValidationError(err(qtype, constants.Q_OBJ_MAP.keys()))
    return obj_map


def get_obj_map(objtype):
    """Gets an object map for `objtype`

    Parameters
    ----------
    objtype : str
        * object type to get object map from in :data:`constants.GET_OBJ_MAP`

    Returns
    -------
    obj_map : dict
        * matching object map for `objtype` from :data:`constants.GET_OBJ_MAP`
    """
    try:
        obj_map = constants.GET_OBJ_MAP[objtype.lower()]
    except KeyError:
        err = "{} not a valid object to get, must be one of {!r}".format
        raise ValidationError(err(objtype, constants.GET_OBJ_MAP.keys()))
    return obj_map


def get_taniumpy_obj(obj_map):
    """Gets a taniumpy object from `obj_map`

    Parameters
    ----------
    obj_map : str
        * str of taniumpy object to fetch

    Returns
    -------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * matching taniumpy object for `obj_map`
    """
    try:
        obj = getattr(taniumpy, obj_map)
    except Exception as e:
        err = "Could not find taniumpy object {}: {}".format
        raise ValidationError(err(obj_map, e))

    return obj


def build_metadatalist_obj(properties, nameprefix=""):
    """Creates a MetadataList object from properties

    Parameters
    ----------
    properties : list of list of strs
        * list of lists, each list having two strs - str 1: property key, str2: property value
    nameprefix : str
        * prefix to insert in front of property key when creating MetadataItem

    Returns
    -------
    metadatalist_obj : :class:`taniumpy.object_types.metadata_list.MetadataList`
        * MetadataList object with list of :class:`taniumpy.object_types.metadata_item.MetadataItem` built from `properties`
    """
    metadatalist_obj = taniumpy.MetadataList()
    for prop in properties:
        name = prop[0]
        value = prop[1]

        if nameprefix:
            name = "{}.{}".format(nameprefix, name)

        metadata_obj = taniumpy.MetadataItem()
        metadata_obj.name = name
        metadata_obj.value = value
        metadatalist_obj.append(metadata_obj)
    return metadatalist_obj


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


def load_taniumpy_from_json(json_file):
    """Opens a json file and parses it into an taniumpy object

    Parameters
    ----------
    json_file : str
        * path to JSON file that describes an API object

    Returns
    -------
    obj : :class:`taniumpy.object_types.base.BaseType`
        * TaniumPy object converted from json file
    """
    try:
        fh = open(json_file)
    except Exception as e:
        m = "Unable to open json_file {!r}, {}".format
        raise PytanError(m(json_file, e))

    howto_m = (
        "Use get_${OBJECT_TYPE}.py with --include-type and "
        "--no-explode-json to export a valid JSON file that can be used "
        "for importing"
    )

    try:
        json_dict = json.load(fh)
    except Exception as e:
        m = "Unable to parse json_file {!r}, {}\n{}".format
        raise PytanError(m(json_file, e, howto_m))

    try:
        fh.close()
    except:
        pass

    if '_type' not in json_dict:
        m = "Missing '_type' key in JSON loaded dictionary!\n{}".format
        raise PytanError(m(howto_m))

    try:
        obj = taniumpy.BaseType.from_jsonable(json_dict)
    except Exception as e:
        m = (
            "Unable to parse json_file {!r} into an API {} object\n"
            "Exception from API.from_jsonable(): {}\n{}"
        ).format
        raise PytanError(m(json_file, json_dict['_type'], e, howto_m))
    return obj


def load_param_json_file(parameters_json_file):
    """Opens a json file and sanity checks it for use as a parameters element for a taniumpy object

    Parameters
    ----------
    parameters_json_file : str
        * path to JSON file that describes an API object

    Returns
    -------
    obj
        * contents of parameters_json_file de-serialized
    """
    try:
        pf = open(parameters_json_file)
    except Exception as e:
        m = (
            "Failed to load JSON parameter file {!r}, error {!r}!!\n"
            "Refer to doc/example_of_all_package_parameters.json "
            "file for examples of each parameter type"
        ).format
        raise PytanError(m(parameters_json_file, e))

    try:
        pd = json.load(pf)
    except Exception as e:
        m = (
            "Failed to load JSON parameter file {!r}, error {!r}!!\n"
            "Refer to doc/example_of_all_package_parameters.json "
            "file for examples of each parameter type"
        ).format
        raise PytanError(m(parameters_json_file, e))

    try:
        pf.close()
    except:
        pass

    try:
        pd_params = pd['parameters']
    except:
        m = (
            "JSON parameter file {!r} is missing a 'parameters' "
            "list!!\n"
            "Refer to doc/example_of_all_package_parameters.json "
            "file for examples of each parameter type"
        ).format
        raise PytanError(m(parameters_json_file))

    for pd_param in pd_params:
        if 'key' not in pd_param:
            m = (
                "JSON parameter file {!r} is missing a 'key' "
                "in the parameter {!r}!!\n"
                "Refer to doc/example_of_all_package_parameters.json "
                "file for examples of each parameter type"
            ).format
            raise PytanError(m(parameters_json_file, pd_param))

    return json.dumps(pd)


def parse_sensor_platforms(sensor):
    """Utility to create a list of platforms for a given sensor"""
    platforms = [
        q.platform for q in sensor.queries
        if q.script
        and 'THIS IS A STUB' not in q.script
        and 'echo Windows Only' not in q.script
        and 'Not a Windows Sensor' not in q.script
    ]
    return platforms


def filter_sourced_sensors(sensors):
    """Utility to filter out all sensors that have a source_id specified (i.e. they are temp sensors created by the API)"""
    sensors = [x for x in sensors if not x.source_id]
    return sensors


def filter_sensors(sensors, filter_platforms=[], filter_categories=[]):
    """Utility to filter a list of sensors for specific platforms and/or categories"""
    if not filter_platforms and not filter_categories:
        return sorted(sensors, key=lambda x: x.category)

    new_sensors = []
    for x in sorted(sensors, key=lambda x: x.category):
        if filter_categories:
            # print "Filter cats: ", [y.lower() for y in filter_categories]
            # print "Sensor cat: ", str(x.category).lower()
            if str(x.category).lower() not in [y.lower() for y in filter_categories]:
                # print "no cat match!"
                continue

        platforms = parse_sensor_platforms(x)
        if filter_platforms:
            match = [
                p for p in platforms
                if p.lower() in [y.lower() for y in filter_platforms]
            ]
            if not match:
                # print "no platform match!"
                continue

        new_sensors.append(x)

    return new_sensors


def get_single_class(all_class):
    """pass."""
    single_class = all_class()._list_properties.values()[0]
    return single_class


def create_cf_listobj(search):
    """pass."""
    result = taniumpy.CacheFilterList()
    if not isinstance(search, (list, tuple)):
        search = [search]
    for spec in search:
        result.append(create_cf_obj(**spec))
    return result


def create_cf_obj(field, value, operator='Equal', field_type='String', not_flag=False, **kwargs):
    """pass."""
    result = taniumpy.CacheFilter()
    result.field = field
    result.value = value
    result.operator = operator
    result.type = field_type
    result.not_flag = not_flag
    return result
