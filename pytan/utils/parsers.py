#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Logging module for :mod:`pytan`."""

import copy
import logging
from . import constants
from . import exceptions
from .external import taniumpy

mylog = logging.getLogger(__name__)


def get_str(spec):
    """pass.

    Computer Name
    v:Computer Name
    val:Computer Name
    value:Computer Name
    Computer Name,f:name
    Computer Name, f:name
    Computer Name, field:name
    v:Computer Name, field:name
    val:Computer Name, field:name
    value:Computer Name, field:name
    value:Computer Name, f:name
    """
    # TODO
    err = "TODO"
    raise exceptions.PytanError(err)


class Spec(object):
    """pass."""

    def get_single_class(self, all_class):
        """pass."""
        single_class = all_class()._list_properties.values()[0]
        return single_class

    def chk_dict_key(self, k, d, types,):
        """pass."""
        if not isinstance(d[k], types):
            ttxt = ', '.join([x.__name__ for x in types])
            err = "{}: key {!r} must be one of type {!r}; supplied type {!r} value {!r}"
            err = err.format(self.meerr, k, ttxt, type(d[k]).__name__, d[k])
            raise exceptions.PytanError(err)

    def has_dict_key(self, k, d):
        # check if d has key k
        if k not in d or d.get(k, '') == '':
            err = "{} key {!r} must be supplied and not empty in {!r}!"
            err = err.format(self.meerr, k, d)
            raise exceptions.PytanError(err)

    def chk_value(self, spec):
        # if spec is a dict with out value defined
        # {"dievalue": "Computer Name"}
        self.has_dict_key('value', spec)

        # check that value is a string or int
        self.chk_dict_key('value', spec, (basestring, int,))

        # validate value is an appropriate type as defined in single_obj
        obj_type = self.props[spec['field']]
        if not isinstance(spec['value'], obj_type):
            try:
                spec['value'] = obj_type(spec['value'])
            except:
                obj_txt = obj_type.__name__
                val_type = type(spec['value']).__name__
                err = "{}: key 'value' must be of type {!r}; supplied type {!r} value {!r}"
                err = err.format(self.meerr, obj_txt, val_type, spec['value'])
                raise exceptions.PytanError(err)
        return spec

    def chk_field(self, spec):
        # if field not specified, and value exists and can be int'd, assume field is id
        # {'value': "1"}
        if 'field' not in spec and 'value' in spec:
            try:
                int(spec['value'])
                spec['field'] = 'id'
            except:
                pass

        # if field not specified, derive it based off fallbacks if they exist in single_obj
        # {"value": "Computer Name"}
        if 'field' not in spec:
            for x in constants.SPEC_FIELD_FALLBACKS:
                if x not in self.props:
                    continue
                spec['field'] = x
                break

        # extra measure in case none of the fallbacks matched (unlikely)
        if not spec.get('field', ''):
            err = "{} key 'field' must be supplied in {!r}, must be one of: {}"
            err = err.format(self.meerr, spec, self.props_txt)
            raise exceptions.PytanError(err)

        # if field is not a valid property in single_class
        # {"value": "Computer Name", "field": "die"}
        if spec['field'] not in self.props:
            err = "{} key 'field' value {!r} not valid for {!r}, must be one of: {}"
            err = err.format(self.meerr, spec['field'], self.single_name, self.props_txt)
            raise exceptions.PytanError(err)

        # validate field is a string
        self.chk_dict_key('field', spec, (basestring,))
        return spec

    def chk_operator(self, spec):
        """pass."""
        # validate operator is a string
        self.chk_dict_key('operator', spec, (basestring,))

        # if operator is a pytan extended operator, map it back to a Tanium operator
        if spec['operator'].lower() in constants.OPERATORS_PYTAN:
            emap = constants.OPERATORS_PYTAN[spec['operator'].lower()]
            pre_value = emap.get('pre_value', '')
            post_value = emap.get('post_value', '')
            spec['operator'] = emap.get('operator')
            spec['not_flag'] = emap.get('not_flag')
            if pre_value:
                spec['value'] = '{}{}'.format(pre_value, spec['value'])
            if post_value:
                spec['value'] = '{}{}'.format(spec['value'], post_value)

        # validate operator is a valid Tanium Operator
        op_valid = [
            x
            for x in constants.OPERATORS_TANIUM
            if x.lower() == spec['operator'].lower()
        ]

        # see if operator matches a Tanium operator
        if op_valid:
            spec['operator'] == op_valid[0]

        # operator did not match a Tanium operator
        # {"value": "Computer Name", "field": "name", "operator": "die"}
        if not op_valid:
            op_list = ', '.join(constants.OPERATORS_TANIUM + constants.OPERATORS_PYTAN.keys())
            err = "{} key 'operator' value {!r} invalid, must be one of: {}"
            err = err.format(self.meerr, spec['operator'], op_list)
            raise exceptions.PytanError(err)
        return spec

    def chk_not_flag(self, spec):
        # validate not_flag is a valid true or false type
        if spec['not_flag'] in constants.TRUE_TYPES:
            spec['not_flag'] = 1
        elif spec['not_flag'] in constants.FALSE_TYPES:
            spec['not_flag'] = 0
        else:
            # not_flag did not match a valid type
            # {"value": "Computer Name", "field": "name", "not_flag": "die"}
            types_txt = constants.TRUE_TYPES + constants.FALSE_TYPES
            types_txt = ', '.join([repr(x) for x in types_txt])
            err = "{} key 'not_flag' value {!r} invalid, must be one of: {}"
            err = err.format(self.meerr, spec['not_flag'], types_txt)
            raise exceptions.PytanError(err)
        return spec

    def chk_field_type(self, spec):
        # validate field_type is a string
        self.chk_dict_key('field_type', spec, (basestring,))

        # validate field_type is a valid field type
        type_valid = [
            constants.FIELD_TYPES[x]
            for x in constants.FIELD_TYPES
            if x.lower() == spec['field_type'].lower()
        ]

        if type_valid:
            spec['field_type'] == type_valid[0]['t']

        # field_type did not match a valid field type
        # {"value": "Computer Name", "field": "name", "field_type": "die"}
        if not type_valid:
            type_list = ', '.join(constants.FIELD_TYPES)
            err = "{} key 'field_type' value {!r} invalid, must be one of: {}"
            err = err.format(self.meerr, spec['field_type'], type_list)
            raise exceptions.PytanError(err)
        return spec


class GetObject(Spec):
    """pass."""

    def __init__(self, all_class, spec):
        """pass."""
        self.single_class = self.get_single_class(all_class)
        self.single_name = self.single_class.__name__
        self.single_obj = self.single_class()
        self.props = self.single_obj._simple_properties
        self.props_txt = ', '.join(self.props)
        self.me = "{}() for object {!r}"
        self.me = self.me.format(self.__class__.__name__, self.single_class.__name__)
        self.meerr = "{}.{}".format(__name__, self.me)

        # check that spec is a dict
        self.chk_dict_key('spec', {'spec': spec}, (dict,))

        # make a copy of spec into result
        self.original_spec = spec
        self.parsed_spec = copy.deepcopy(self.original_spec)

        # check that field key exists and is valid
        self.parsed_spec = self.chk_field(self.parsed_spec)

        # check that value key exists and is valid
        self.parsed_spec = self.chk_value(self.parsed_spec)

        # if operator key exists, parse & validate
        if 'operator' in self.parsed_spec:
            self.parsed_spec = self.chk_operator(self.parsed_spec)

        if 'not_flag' in self.parsed_spec:
            self.parsed_spec = self.chk_not_flag(self.parsed_spec)

        if 'field_type' in self.parsed_spec:
            self.parsed_spec = self.chk_field_type(self.parsed_spec)

        # if changed, log the change
        if self.original_spec != self.parsed_spec:
            m = "{} parsed from {!r} into {!r}"
            m = m.format(self.me, self.original_spec, self.parsed_spec)
            mylog.info(m)
        else:
            m = "{} parsed without change {!r}"
            m = m.format(self.me, self.parsed_spec)
            mylog.info(m)


class FilterObject(Spec):

    def __init__(self, spec):
        """pass."""
        self.single_class = taniumpy.Filter()
        self.single_name = self.single_class.__name__
        self.single_obj = self.single_class()
        self.props = self.single_obj._simple_properties
        self.props_txt = ', '.join(self.props)
        self.me = "{}() for object {!r}"
        self.me = self.me.format(self.__class__.__name__, self.single_class.__name__)
        self.meerr = "{}.{}".format(__name__, self.me)

        # check that spec is a dict
        self.chk_dict_key('spec', {'spec': spec}, (dict,))

        # make a copy of spec into result
        self.original_spec = spec
        self.parsed_spec = copy.deepcopy(self.original_spec)

        # check that field key exists and is valid
        self.parsed_spec = self.chk_field(self.parsed_spec)

        # check that value key exists and is valid
        self.parsed_spec = self.chk_value(self.parsed_spec)

        # if operator key exists, parse & validate
        if 'operator' in self.parsed_spec:
            self.parsed_spec = self.chk_operator(self.parsed_spec)

        if 'not_flag' in self.parsed_spec:
            self.parsed_spec = self.chk_not_flag(self.parsed_spec)

        if 'field_type' in self.parsed_spec:
            self.parsed_spec = self.chk_field_type(self.parsed_spec)

        # if changed, log the change
        if self.original_spec != self.parsed_spec:
            m = "{} parsed from {!r} into {!r}"
            m = m.format(self.me, self.original_spec, self.parsed_spec)
            mylog.info(m)
        else:
            m = "{} parsed without change {!r}"
            m = m.format(self.me, self.parsed_spec)
            mylog.info(m)


class LeftSide(Spec):

    def __init__(self, specs):
        """pass."""
        self.me = "{}()".format(self.__class__.__name__)
        self.meerr = "{}.{}".format(__name__, self.me)

        self.chk_dict_key('specs', {'specs': specs}, (dict, list, tuple,))

        self.original_specs = specs

        if not isinstance(self.original_specs, (list, tuple)):
            self.original_specs = [self.original_specs]

        self.parsed_specs = [self.parse_spec(s) for s in self.original_specs]

    def parse_spec(self, spec):
        parsed_spec = copy.deepcopy(spec)
        # check that spec is a dict
        self.chk_dict_key('spec', {'spec': spec}, (dict,))

        # check that sensor key exists and is a dict
        self.has_dict_key('sensor', spec)
        self.chk_dict_key('sensor', spec, (dict,))

        # parse the sensor dict
        sensor_parser = GetObject(taniumpy.SensorList, spec['sensor'])
        parsed_spec['sensor'] = sensor_parser.parsed_spec
        return parsed_spec
