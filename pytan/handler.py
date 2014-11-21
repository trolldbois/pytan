# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""PyTan: A wrapper around Tanium's SOAP API in Python

Like saran wrap. But not.

This requires Python 2.7
"""
import sys
import json

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging
from . import utils
from . import constants
from . import api
from .ask_manual_human_parser import dehumanize_sensors
from .ask_manual_human_parser import dehumanize_question_filters
from .ask_manual_human_parser import dehumanize_question_options
from .exceptions import HandlerError

mylog = logging.getLogger("handler")
manuallog = logging.getLogger("ask_manual")


def progressChanged(asker, pct):
    mylog.info("Results {1:.0f}% ({0})".format(asker, pct))


class Handler(object):

    def __init__(self, username, password, host, port="444", loglevel=0,
                 debugformat=False, **kwargs):
        super(Handler, self).__init__()

        # use port 444 if you have direct access to it,
        # port 444 is direct access to API
        # port 443 uses apache forwarder which then goes to port 444

        # setup the console logging handler
        utils.setup_console_logging()
        # create all the loggers and set their levels based on loglevel
        utils.set_log_levels(loglevel)
        # change the format of console logging handler if need be
        utils.change_console_format(debugformat)

        if not username:
            raise HandlerError("Must supply username!")
        if not password:
            raise HandlerError("Must supply password!")
        if not host:
            raise HandlerError("Must supply host!")
        if not port:
            raise HandlerError("Must supply port!")
        try:
            int(port)
        except ValueError:
            raise HandlerError("port must be an integer!")

        self.test_app_port(host, port)
        self.session = api.Session(host, port)
        self.session.authenticate(username, password)

    def __str__(self):
        str_tpl = "Handler for {}".format
        ret = str_tpl(self.session)
        return ret

    def test_app_port(self, host, port):
        """validates that the SOAP port on the SOAP host can be reached"""
        chk_tpl = "Port test to {}:{} {}".format
        if utils.port_check(host, port):
            mylog.debug(chk_tpl(host, port, "SUCCESS"))
        else:
            raise HandlerError(chk_tpl(host, port, "FAILURE"))

    def ask_manual_human(self, q_obj_map, sensors=None, **kwargs):
        '''Parses a set of "human" strings into python objects usable
        by ask_manual()
        '''
        if not sensors:
            err = "Must provide a sensor string or list of sensor strings!"
            raise HandlerError(err)

        if 'question_filters' in kwargs:
            q_filters = kwargs.pop('question_filters')
        else:
            q_filters = []

        if 'question_options' in kwargs:
            q_options = kwargs.pop('question_options')
        else:
            q_options = []

        sensor_defs = dehumanize_sensors(sensors)
        q_filter_defs = dehumanize_question_filters(q_filters)
        q_option_defs = dehumanize_question_options(q_options)

        result = self.ask_manual(
            q_obj_map=q_obj_map,
            sensor_defs=sensor_defs,
            question_filter_defs=q_filter_defs,
            question_option_defs=q_option_defs,
            **kwargs
        )
        return result

    def ask_manual(self, q_obj_map, sensor_defs=None, **kwargs):
        q_filter_defs = kwargs.get('question_filter_defs', None)
        q_option_defs = kwargs.get('question_option_defs', None)

        sensor_defs = self._parse_sensor_defs(sensor_defs)
        q_filter_defs = self._parse_q_filter_defs(q_filter_defs)
        q_option_defs = self._parse_q_option_defs(q_option_defs)

        sensor_defs = self._validate_sensor_defs(sensor_defs)
        q_filter_defs = self._validate_q_filter_defs(
            q_filter_defs, q_option_defs,
        )

        add_q_obj = self._build_manual_q(
            q_obj_map, sensor_defs, q_filter_defs, q_option_defs,
        )

        q_obj = self.session.add(add_q_obj)

        ask_kwargs = self._get_ask_kwargs(**kwargs)
        asker = api.QuestionAsker(self.session, q_obj, **ask_kwargs)
        asker.run({'ProgressChanged': progressChanged})

        req_kwargs = self._get_req_kwargs(**kwargs)
        result = self.session.getResultData(q_obj, **req_kwargs)

        result.sensors = [x['sensor_obj'] for x in sensor_defs]
        result.asker = asker
        return result

    def ask_saved(self, q_obj_map, **kwargs):
        q_objs = self.get('saved_question', **kwargs)
        if len(q_objs) != 1:
            err = (
                "Multiple saved questions returned, can only ask one "
                "saved question!\nArgs: {}\nReturned saved questions:\n\t{}"
            ).format
            q_obj_str = '\n\t'.join([str(x) for x in q_objs])
            raise HandlerError(err(kwargs, q_obj_str))

        q_obj = q_objs[0]

        ask_kwargs = self._get_ask_kwargs(**kwargs)
        asker = api.QuestionAsker(self.session, q_obj, **ask_kwargs)
        asker.run({'ProgressChanged': progressChanged})

        req_kwargs = self._get_req_kwargs(**kwargs)
        result = self.session.getResultData(q_obj, **req_kwargs)

        result.sensors = [x.sensor for x in q_obj.question.selects]
        result.asker = asker
        return result

    def ask(self, **kwargs):
        qtype = kwargs.get('qtype', '')
        if not qtype:
            err = (
                "Must supply question type as 'qtype'! Valid choices: {}"
            ).format
            raise HandlerError(err(', '.join(constants.Q_OBJ_MAP)))
        q_obj_map = self._get_q_obj_map(qtype)
        result = getattr(self, q_obj_map['handler'])(q_obj_map, **kwargs)
        return result

    def get_all(self, obj, **kwargs):
        obj_map = self._get_obj_map(obj)
        api_obj_all = getattr(api, obj_map['all'])()
        found = self._find(api_obj_all, **kwargs)
        return found

    def get(self, obj, **kwargs):
        obj_map = self._get_obj_map(obj)
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]

        # if the api doesn't support filtering for this object,
        # return all objects of this type
        if not api_attrs:
            return self.get_all(obj, **kwargs)

        # if api supports filtering for this object,
        # but no filters supplied in kwargs, raise
        if not any(api_kwattrs):
            err = "Getting a {} requires at least one filter: {}".format
            raise HandlerError(err(obj, api_attrs))

        # if there is a multi in obj_map, that means we can pass a list
        # type to the api. the list will an entry for each api_kw
        if obj_map['multi']:
            return self._get_multi(obj_map, **kwargs)

        # if there is a single in obj_map but not multi, that means
        # we have to find each object individually
        if obj_map['single']:
            return self._get_single(obj_map, **kwargs)

        err = "No single or multi search defined for {}".format
        raise HandlerError(err(obj))

    # begin private methods
    @staticmethod
    def _api_obj(objname, **kwargs):
        obj = getattr(api, objname)()
        for k, v in kwargs.iteritems():
            setattr(obj, k, v)
        return obj

    def _build_manual_q(self, q_obj_map, sensor_defs, q_filter_defs,
                        q_option_defs):

        select_objlist = api.SelectList()
        select_objlist.select = [d['select_obj'] for d in sensor_defs]

        filter_objlist = api.FilterList()
        filter_objlist.filter = [d['filter_obj'] for d in q_filter_defs]

        group_obj = api.Group()
        group_obj.filters = filter_objlist
        group_obj = self._apply_options_obj(q_option_defs, group_obj, 'group')

        add_q_obj = getattr(api, q_obj_map['api'])()
        add_q_obj.selects = select_objlist
        add_q_obj.group = group_obj
        return add_q_obj

    def _parse_q_option_defs(self, q_option_defs):

        if q_option_defs is None:
            return {}

        # type checking for required keys
        if not utils.is_dict(q_option_defs):
            err = (
                "Unexpected Question Option type {}: {}! -- "
                "Must be a dictionary!"
            ).format
            raise HandlerError(err(type(q_option_defs), q_option_defs))
        return q_option_defs

    def _parse_q_filter_defs(self, q_filter_defs):
        new_defs = []

        if q_filter_defs is None:
            return new_defs

        # type checking for required keys
        if utils.is_dict(q_filter_defs):
            new_defs.append(q_filter_defs)
        elif utils.is_list(q_filter_defs):
            for k in q_filter_defs:
                new_defs += self._parse_sensor_defs(k)
        else:
            err = (
                "Unexpected Question Filter type {}: {}! -- "
                "Must be a list or dictionary!"
            ).format
            raise HandlerError(err(type(q_filter_defs), q_filter_defs))
        return new_defs

    def _parse_sensor_defs(self, sensor_defs):
        if sensor_defs is None:
            # TODO
            raise HandlerError("help me")

        # type checking for required keys
        new_defs = []
        if utils.is_str(sensor_defs):
            new_defs.append({'name': sensor_defs})
        elif utils.is_dict(sensor_defs):
            new_defs.append(sensor_defs)
        elif utils.is_list(sensor_defs):
            for k in sensor_defs:
                new_defs += self._parse_sensor_defs(k)
        else:
            err = (
                "Unexpected Sensor definition type {}: {}! -- "
                "Must be one of string, list, or dictionary!"
            ).format
            raise HandlerError(err(type(sensor_defs), sensor_defs))
        return new_defs

    def _validate_q_filter_defs(self, q_filter_defs, q_option_defs):
        s_obj_map = constants.GET_OBJ_MAP['sensor']
        search_keys = s_obj_map['search']

        for d in q_filter_defs:
            # value checking for required keys
            def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

            if len(def_search) == 0:
                err = "Question Filter {} missing one of {}!".format
                raise HandlerError(err(d, ', '.join(search_keys)))

            elif len(def_search) > 1:
                err = "Question Filter {} has more than one of {}!".format
                raise HandlerError(err(d, ', '.join(search_keys)))

            # type checking for required filter key
            self._chk_def_key(d, 'filter', [dict], req=True)

            # get the sensor object for this question filter
            sensor_obj = self.get('sensor', **def_search)[0]

            # validate/map question filter into a Filter()
            filter_obj = self._get_filter_obj(d, sensor_obj)

            # update filter_obj with any options
            filter_obj = self._apply_options_obj(
                q_option_defs, filter_obj, 'filter',
            )

            d['sensor_obj'] = sensor_obj
            d['filter_obj'] = filter_obj

            # TODO: if 'help' in options/filter/type: print help
        return q_filter_defs

    def _validate_sensor_defs(self, sensor_defs):
        s_obj_map = constants.GET_OBJ_MAP['sensor']
        search_keys = s_obj_map['search']

        for d in sensor_defs:
            # value checking for required keys
            def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

            if len(def_search) == 0:
                err = "Sensor definition {} missing one of {}!".format
                raise HandlerError(err(d, ', '.join(search_keys)))

            elif len(def_search) > 1:
                err = "Sensor definition {} has more than one of {}!".format
                raise HandlerError(err(d, ', '.join(search_keys)))

            # type checking for optional keys
            self._chk_def_key(d, 'params', [dict])
            self._chk_def_key(d, 'options', [dict])
            self._chk_def_key(d, 'filter', [dict])

            # get the sensor object
            sensor_obj = self.get('sensor', **def_search)[0]

            # validate/map sensor params into a ParameterList()
            param_objlist = self._get_param_objlist(d, sensor_obj)

            # validate/map sensor filter into a Filter()
            filter_obj = self._get_filter_obj(d, sensor_obj)

            # get the options the user supplied
            options = d.get('options', {})

            # update filter_obj with any options the user supplied
            filter_obj = self._apply_options_obj(
                options, filter_obj, 'filter',
            )

            # create a select object for this sensor
            select_obj = api.Select()
            select_obj.sensor = api.Sensor()
            select_obj.filter = filter_obj

            # if there are parameters, we need to set the following to
            # sensor_obj.id:
            #  - select_obj.sensor_obj.source_id
            #  - select_obj.filter.sensor.id
            if param_objlist:
                select_obj.sensor.source_id = sensor_obj.id
                select_obj.sensor.parameters = param_objlist
                select_obj.filter.sensor.id = sensor_obj.id
            else:
                select_obj.sensor.hash = sensor_obj.hash

            d['sensor_obj'] = sensor_obj
            d['filter_obj'] = filter_obj
            d['select_obj'] = select_obj

        return sensor_defs

    @staticmethod
    def _get_param_objlist(sensor_def, sensor_obj):
        param_objlist = api.ParameterList()

        # get the user supplied params dict
        d_params = sensor_def.get('params', {})

        # get the sensor name
        s_name = str(sensor_obj)

        # get the sensor parameter definitions
        s_param_def = sensor_obj.parameter_definition or {}

        # json load the parameter definitions if they exist
        if s_param_def:
            s_param_def = json.loads(s_param_def)

        # get the list of parameters from the parameter definitions
        s_params = s_param_def.get('parameters', [])

        # if user defined params and this sensor doesn't take params,
        # we will just ignore them

        for s_param in s_params:
            # get the key for this param
            sp_key = s_param["key"]

            # get the default value for this param if it exists
            sp_def_val = s_param.get('defaultValue', '')

            # get requireSelection for this param if it exists (pulldown menus)
            sp_req_sel = s_param.get('requireSelection', False)

            # get values for this param if it exists (pulldown menus)
            sp_values = s_param.get('values', [])

            # if this param requires a selection and it has a list of values
            # and there is no default value, use the first value as the
            # default value
            if sp_req_sel and sp_values and not sp_def_val:
                sp_def_val = sp_values[0]

            # get the user defined value if it exists
            user_val = d_params.get(sp_key, '')

            # if no user defined value, set the user value to the default
            # value
            if not user_val:
                user_val = sp_def_val

            # if still no user defined value, and param requires selection,
            # throw an exception
            if not user_val and sp_req_sel:
                err = (
                    "{} parameter key {!r} requires a value, "
                    "parameter definition:\n{}"
                ).format
                raise HandlerError(err(s_name, sp_key, utils.jsonify(s_param)))

            # create a parameter object
            param_obj = api.Parameter()
            param_obj.key = '{0}{1}{0}'.format(constants.PARAM_DELIM, sp_key)
            param_obj.value = user_val
            param_objlist.append(param_obj)

            dbg = "Parameter {} for {} mapped to: {}".format
            manuallog.debug(dbg(sp_key, s_name, param_obj))

            param_objlist.append(param_obj)
        return param_objlist

    def _get_filter_obj(self, sensor_def, sensor_obj):

        # create our basic filter that is needed no matter what
        filter_obj = api.Filter()
        filter_obj.sensor = api.Sensor()
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
            raise HandlerError(err(filter_def))

        # not_flag optional
        def_not_flag = filter_def.get('not_flag', None)

        # value required
        def_value = filter_def.get('value', None)
        if not def_value:
            err = "Filter {!r} requires a 'value' key!".format
            raise HandlerError(err(filter_def))

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
            manuallog.debug(dbg(filter_def, str(filter_obj)))

        if not found_match:
            err = "Invalid filter {!r}".format
            raise HandlerError(err(filter_def))

        return filter_obj

    def _apply_options_obj(self, options, obj, dest):

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
                manuallog.debug(dbg(k, v, om))

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
                    raise HandlerError(err(k, valid_type, valid_values_str))

                if valid_type == int:
                    try:
                        v = int(v)
                    except:
                        err = (
                            "Option {!r} value {!r} is not an integer"
                        ).format
                        raise HandlerError(err(k, v))

                if valid_type == str:
                    if not type(v) in [str, unicode]:
                        err = (
                            "Option {!r} value {!r} is not a string"
                        ).format
                        raise HandlerError(err(k, v))

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
                        raise HandlerError(err(k, v, valid_values))
                    else:
                        v = value_match

                # update obj with k = v
                setattr(obj, k, v)

                break

        dbg = "Options {!r} updated to: {}".format
        manuallog.debug(dbg(options, str(obj)))
        return obj

    @staticmethod
    def _chk_def_key(def_dict, key, keytypes, keysubtypes=None, req=False):
        if key not in def_dict:
            if req:
                err = "Definition {} missing 'filter' key!".format
                raise HandlerError(err(def_dict))
            return

        val = def_dict.get(key)
        if type(val) not in keytypes:
            err = (
                "'{}' key in definition dictionary must be a {}, you supplied "
                "a {}!"
            ).format
            raise HandlerError(err(key, keytypes, type(val)))

        if not keysubtypes or not val:
            return

        if type(val) == dict:
            subtypes = [type(x) for x in val.values()]
        else:
            subtypes = [type(x) for x in val]

        if not all([x in keysubtypes for x in subtypes]):
            err = (
                "'{}' key in definition dictionary must be a {} of {}s, "
                "you supplied {}!"
            ).format
            raise HandlerError(err(key, keytypes, keysubtypes, subtypes))

    def _empty_obj(self, api_object):
        is_list = getattr(api_object, '_list_properties', {})
        is_str = utils.is_str(api_object)
        if any([is_list, is_str]) and not api_object:
            return True
        else:
            return False

    def _get_ask_kwargs(self, **kwargs):
        ask_kwargs = {}
        if 'timeout' in kwargs:
            ask_kwargs['timeout'] = kwargs.pop('timeout')
        return ask_kwargs

    def _get_req_kwargs(self, **kwargs):
        REQ_KWARGS = constants.REQ_KWARGS
        req_kwargs = {}
        for i in kwargs:
            if i in REQ_KWARGS:
                req_kwargs[i] = kwargs[i]
        return req_kwargs

    def _find(self, api_object, **kwargs):
        req_kwargs = self._get_req_kwargs(**kwargs)
        try:
            search_str = '; '.join([str(x) for x in api_object])
        except:
            search_str = api_object
        mylog.debug("Searching for {}".format(search_str))
        try:
            found = self.session.find(api_object, **req_kwargs)
        except Exception as e:
            mylog.error(e)
            err = "No results found searching for {}!!".format
            raise HandlerError(err(search_str))

        if self._empty_obj(found):
            err = "No results found searching for {}!!".format
            raise HandlerError(err(search_str))

        mylog.debug("Found {}".format(found))
        return found

    def _get_q_obj_map(self, qtype):
        Q_OBJ_MAP = constants.Q_OBJ_MAP
        try:
            obj_map = Q_OBJ_MAP[qtype.lower()]
        except KeyError:
            err = "{} not a valid question type, must be one of {!r}".format
            raise HandlerError(err(qtype, Q_OBJ_MAP.keys()))
        return obj_map

    def _get_obj_map(self, obj):
        GET_OBJ_MAP = constants.GET_OBJ_MAP
        try:
            obj_map = GET_OBJ_MAP[obj.lower()]
        except KeyError:
            err = "{} not a valid object to get, must be one of {!r}".format
            raise HandlerError(err(obj, GET_OBJ_MAP.keys()))
        return obj_map

    def _get_multi(self, obj_map, **kwargs):
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # create a list object to append our searches to
        api_obj_multi = getattr(api, obj_map['multi'])()
        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    api_obj_single = getattr(api, obj_map['single'])()
                    setattr(api_obj_single, k, i)
                    api_obj_multi.append(api_obj_single)
            else:
                api_obj_single = getattr(api, obj_map['single'])()
                setattr(api_obj_single, k, v)
                api_obj_multi.append(api_obj_single)

        # find the multi list object
        found = self._find(api_obj_multi, **kwargs)
        return found

    def _get_single(self, obj_map, **kwargs):
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # we create a list object to append our single item searches to
        if obj_map.get('allfix', ''):
            found = getattr(api, obj_map['allfix'])()
        else:
            found = getattr(api, obj_map['all'])()

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    api_obj_single = getattr(api, obj_map['single'])()
                    setattr(api_obj_single, k, i)
                    found.append(self._find(api_obj_single, **kwargs))
            else:
                api_obj_single = getattr(api, obj_map['single'])()
                setattr(api_obj_single, k, v)
                found.append(self._find(api_obj_single, **kwargs))

        return found
