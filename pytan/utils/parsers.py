#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Logging module for :mod:`pytan`."""

import logging
from . import constants
from . import exceptions
from . import tanium_obj

mylog = logging.getLogger(__name__)


def chk_type(v, types, src, k=''):
    """pass."""
    if k:
        k = "key '{}' ".format(k)

    if not isinstance(v, types):
        txt = ', '.join([x.__name__ for x in types])
        err = "{}: {}must be one of type {!r}; supplied type {!r} value {!r}"
        err = err.format(src, k, txt, type(v).__name__, v)
        raise exceptions.PytanError(err)


def search_spec(**kwargs):
    """pass."""
    me = __name__ + "search_spec()"
    search_spec = kwargs.get('search_spec')
    chk_type(v=search_spec, types=(basestring, dict,), src=me)

    all_class = kwargs.get('all_class')
    single_class = tanium_obj.get_single_class(all_class)
    single_props = single_class()._simple_properties.keys()
    props_txt = ', '.join(single_props)

    # if search_spec is a string, assume it is a value
    # "Computer Name"
    if isinstance(search_spec, (basestring,)):
        result = {'value': search_spec}
    else:
        result = dict(search_spec)

    # if search_spec is a dict with out value defined
    # {"dievalue": "Computer Name"}
    if not result.get('value', ''):
        err = "{} key 'value' must be supplied and not empty in {!r}!"
        err = err.format(me, search_spec)
        raise exceptions.PytanError(err)

    chk_type(k='value', v=result['value'], types=(basestring,), src=me)

    if 'field' not in result:
        # if field not specified, and it can be int'd, assume field is id
        try:
            int(result['value'])
            result['field'] = 'id'
        except:
            # if field not specified, derive it based off single_class
            # {"value": "Computer Name"}
            for x in constants.SPEC_FIELD_FALLBACKS:
                if x not in single_props:
                    continue
                result['field'] = x
                break

    # extra measure in case none of the fallbacks matched (unlikely)
    if not result.get('field', ''):
        err = "{} key 'field' must be supplied in {!r}, must be one of: {}"
        err = err.format(me, search_spec, props_txt)
        raise exceptions.PytanError(err)

    # if field is not a valid property in single_class
    # {"value": "Computer Name", "field": "die"}
    if result['field'] not in single_props:
        err = "{} key 'field' value {!r} not valid for {!r}, must be one of: {}"
        err = err.format(me, result['field'], single_class.__name__, props_txt)
        raise exceptions.PytanError(err)

    chk_type(k='field', v=result['field'], types=(basestring,), src=me)

    if 'operator' in result:
        chk_type(k='operator', v=result['operator'], types=(basestring,), src=me)
        # if operator is a pytan extended operator, map it back to a Tanium operator
        if result['operator'].lower() in constants.OPERATORS_EXTENDED:
            emap = constants.OPERATORS_EXTENDED[result['operator'].lower()]
            pre_value = emap.get('pre_value', '')
            post_value = emap.get('post_value', '')
            result['operator'] = emap.get('operator')
            result['not_flag'] = emap.get('not_flag')
            if pre_value:
                result['value'] = '{}{}'.format(pre_value, result['value'])
            if post_value:
                result['value'] = '{}{}'.format(result['value'], post_value)

        op_valid = [x for x in constants.OPERATORS if x.lower() == result['operator'].lower()]

        # see if operator matches a Tanium operator
        if op_valid:
            result['operator'] == op_valid[0]

        # operator did not match a Tanium operator
        # {"value": "Computer Name", "field": "name", "operator": "die"}
        if not op_valid:
            op_list = ', '.join(constants.OPERATORS + constants.OPERATORS_EXTENDED.keys())
            err = "{} key 'operator' value {!r} invalid, must be one of: {}"
            err = err.format(me, result['operator'], op_list)
            raise exceptions.PytanError(err)

    if 'not_flag' in result:
        chk_type(k='not_flag', v=result['not_flag'], types=(basestring, int, float,), src=me)
        if result['not_flag'] in constants.TRUE_TYPES:
            result['not_flag'] = 1
        elif result['not_flag'] in constants.FALSE_TYPES:
            result['not_flag'] = 0
        else:
            # not_flag did not match a valid type
            # {"value": "Computer Name", "field": "name", "not_flag": "die"}
            types_txt = constants.TRUE_TYPES + constants.FALSE_TYPES
            types_txt = ', '.join([repr(x) for x in types_txt])
            err = "{} key 'not_flag' value {!r} invalid, must be one of: {}"
            err = err.format(me, result['not_flag'], types_txt)
            raise exceptions.PytanError(err)

    if 'field_type' in result:
        chk_type(k='field_type', v=result['field_type'], types=(basestring,), src=me)
        type_valid = [x for x in constants.FIELD_TYPES if x.lower() == result['field_type']]
        if type_valid:
            result['field_type'] == type_valid[0]['t']

        # field_type did not match a valid field type
        # {"value": "Computer Name", "field": "name", "field_type": "die"}
        if not type_valid:
            type_list = ', '.join(constants.FIELD_TYPES)
            err = "{} key 'field_type' value {!r} invalid, must be one of: {}"
            err = err.format(me, result['field_type'], type_list)
            raise exceptions.PytanError(err)

    if search_spec != result:
        m = "{} parsed from {!r} into {!r}"
        m = m.format(me, search_spec, result)
        mylog.debug(m)
    return result
