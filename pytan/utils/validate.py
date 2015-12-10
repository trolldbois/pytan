#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Definition Validation module for :mod:`pytan`"""
from .exceptions import ValidationError
from . import constants


def defs_gen(defname, deftypes, strconv=None, empty_ok=True, defs=None, **kwargs):
    """Parses and validates defs into new_defs

    Parameters
    ----------
    defname : str
        * Name of definition
    deftypes : list of str
        * list of valid types that defs can be
    strconv : str
        * if supplied, and defs is a str, turn defs into a dict with key = strconv, value = defs
    empty_ok : bool
        * True: defs is allowed to be empty
        * False: defs is not allowed to be empty

    Returns
    -------
    new_defs : list of dict
        * parsed and validated defs
    """
    if defs is None:
        defs = kwargs.get(defname, eval(deftypes[0]))

    type_msg = "{0!r} requires a non-empty value of type: {1}".format
    type_msg = type_msg(defname, ' or '.join(deftypes))

    if not defs:
        if not empty_ok:
            err = "Argument {0!r} is empty!\n{1}".format
            raise ValidationError(err(defname, type_msg))
        else:
            return defs

    err = (
        "Argument {0!r} has an invalid type {1}\n{2}"
    ).format(defname, type(defs), type_msg)

    if deftypes == ['dict()']:
        if not isinstance(defs, (dict)):
            raise ValidationError(err)
        else:
            return defs

    new_defs = []
    if isinstance(defs, (basestring)):
        if 'str()' in deftypes:
            conv = defs
            if strconv is not None:
                conv = {strconv: defs}
            new_defs.append(conv)
        else:
            raise ValidationError(err)
    elif isinstance(defs, (dict)):
        if 'dict()' in deftypes:
            new_defs.append(defs)
        else:
            raise ValidationError(err)
    elif isinstance(defs, (list, tuple)):
        if 'list()' in deftypes:
            for k in defs:
                new_defs += defs_gen(defname, deftypes, strconv, empty_ok, k, **kwargs)
        else:
            raise ValidationError(err)
    else:
        raise ValidationError(err)

    return new_defs


def defs_sensors(sensor_defs):
    """Validates sensor definitions

    Ensures each sensor definition has a selector, and if a sensor definition has a params, options, or filter key, that each key is valid

    Parameters
    ----------
    sensor_defs : list of dict
        * list of sensor definitions
    """
    s_obj_map = constants.GET_OBJ_MAP['sensor']
    search_keys = s_obj_map['search']

    for d in sensor_defs:
        # value checking for required keys
        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        if len(def_search) == 0:
            err = "Sensor definition {} missing one of {}!".format
            raise ValidationError(err(d, ', '.join(search_keys)))

        elif len(def_search) > 1:
            err = "Sensor definition {} has more than one of {}!".format
            raise ValidationError(err(d, ', '.join(search_keys)))

        # type checking for optional keys
        chk_def_key(d, 'params', [dict])
        chk_def_key(d, 'options', [dict])
        chk_def_key(d, 'filter', [dict])


def def_package(package_def):
    """Validates package definitions

    Ensures package definition has a selector, and if a package definition has a params key, that key is valid

    Parameters
    ----------
    package_def : dict
        * package definition
    """
    s_obj_map = constants.GET_OBJ_MAP['package']
    search_keys = s_obj_map['search']

    # value checking for required keys
    def_search = {
        s: package_def.get(s, '')
        for s in search_keys if package_def.get(s, '')
    }

    if len(def_search) == 0:
        err = "Package definition {} missing one of {}!".format
        raise ValidationError(err(package_def, ', '.join(search_keys)))

    elif len(def_search) > 1:
        err = "Package definition {} has more than one of {}!".format
        raise ValidationError(err(package_def, ', '.join(search_keys)))

    # type checking for optional keys
    chk_def_key(package_def, 'params', [dict])


def defs_filters(filter_defs):
    """Validates question filter definitions

    Ensures each question filter definition has a selector, and if a question filter definition has a filter key, that key is valid

    Parameters
    ----------
    filter_defs : list of dict
        * list of question filter definitions
    """
    s_obj_map = constants.GET_OBJ_MAP['sensor']
    search_keys = s_obj_map['search']

    for d in filter_defs:
        # value checking for required keys
        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        if len(def_search) == 0:
            err = "Question Filter {} missing one of {}!".format
            raise ValidationError(err(d, ', '.join(search_keys)))

        elif len(def_search) > 1:
            err = "Question Filter {} has more than one of {}!".format
            raise ValidationError(err(d, ', '.join(search_keys)))

        # type checking for required filter key
        chk_def_key(d, 'filter', [dict], req=True)


def chk_def_key(def_dict, key, keytypes, keysubtypes=None, req=False):
    """Checks that def_dict has key

    Parameters
    ----------
    def_dict : dict
        * Definition dictionary
    key : str
        * key to check for in def_dict
    keytypes : list of str
        * list of str of valid types for key
    keysubtypes : list of str
        * if key is a dict or list, validate that all values of dict or list are in keysubtypes
    req : bool
        * False: key does not have to be in def_dict
        * True: key must be in def_dict, throw :exc:`ValidationError` if not
    """
    if key not in def_dict:
        if req:
            err = "Definition {} missing 'filter' key!".format
            raise ValidationError(err(def_dict))
        return

    val = def_dict.get(key)
    if type(val) not in keytypes:
        err = (
            "'{}' key in definition dictionary must be a {}, you supplied "
            "a {}!"
        ).format
        raise ValidationError(err(key, keytypes, type(val)))

    if not keysubtypes or not val:
        return

    if isinstance(val, (dict)):
        subtypes = [type(x) for x in val.values()]
    else:
        subtypes = [type(x) for x in val]

    if not all([x in keysubtypes for x in subtypes]):
        err = (
            "'{}' key in definition dictionary must be a {} of {}s, "
            "you supplied {}!"
        ).format
        raise ValidationError(err(key, keytypes, keysubtypes, subtypes))


def get_kwargs_int(key, default=None, **kwargs):
    """Gets key from kwargs and validates it is an int

    Parameters
    ----------
    key : str
        * key to get from kwargs
    default : int, optional
        * default value to use if key not found in kwargs
    kwargs : dict
        * kwargs to get key from

    Returns
    -------
    val : int
        value from key, or default if supplied
    """

    val = kwargs.get(key, default)
    if val is None:
        return val
    try:
        val = int(val)
    except ValueError:
        err = "'{}' must be an int, you supplied: {}"
        raise ValidationError(err(key, val))
    return val


def check_dictkey(d, key, valid_types, valid_list_types):
    """Yet another method to check a dictionary for a key

    Parameters
    ----------
    d : dict
        * dictionary to check for key
    key : str
        * key to check for in d
    valid_types : list of str
        * list of str of valid types for key
    valid_list_types : list of str
        * if key is a list, validate that all values of list are in valid_list_types
    """
    if key in d:
        k_val = d[key]
        k_type = type(k_val)
        if k_type not in valid_types:
            err = "{!r} must be one of {}, you supplied {}!".format
            raise ValidationError(err(key, valid_types, k_type))
        if isinstance(k_val, (list, tuple)) and valid_list_types:
            valid_list_types = [eval(x) for x in valid_list_types]
            list_types = [type(x) for x in k_val]
            list_types_match = [x in valid_list_types for x in list_types]
            if not all(list_types_match):
                err = "{!r} must be a list of {}, you supplied {}!".format
                raise ValidationError(err(key, valid_list_types, list_types))


def clean_kwargs(kwargs, keys=None):
    """Removes each key from kwargs dict if found

    Parameters
    ----------
    kwargs : dict
        * dict of keyword args
    keys : list of str, optional
        * default: ['obj', 'pytan_help', 'objtype']
        * list of strs of keys to remove from kwargs

    Returns
    -------
    clean_kwargs : dict
        * the new dict of kwargs with keys removed
    """
    if keys is None:
        keys = ['obj', 'pytan_help', 'objtype']

    clean_kwargs = dict(kwargs)
    [clean_kwargs.pop(x) for x in keys if x in kwargs]
    return clean_kwargs
