# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""PyTan: A wrapper around Tanium's SOAP API in Python

Like saran wrap. But not.

This requires Python 2.7
"""
import sys
import os
# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging
from . import utils
from .exceptions import AppError
from . import constants
# from .reports import Reporter
# from . import req

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
api_dir = os.path.join(parent_dir, 'taniumpy')
path_adds = [parent_dir, api_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import api

mylog = logging.getLogger("pytan.handler")


def progressChanged(asker, pct):
    mylog.info("ProgressChanged on {0}: %{1:.2f} done...".format(asker, pct))


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

        # self.reporter = Reporter()

        if not username:
            raise AppError("Must supply username!")
        if not password:
            raise AppError("Must supply password!")
        if not host:
            raise AppError("Must supply host!")
        if not port:
            raise AppError("Must supply port!")
        try:
            int(port)
        except ValueError:
            raise AppError("port must be an integer!")

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
            raise AppError(chk_tpl(host, port, "FAILURE"))

    def _ask_saved(self, q_obj_map, **kwargs):
        q_args = {}
        if 'timeout' in kwargs:
            q_args['timeout'] = kwargs.pop('timeout')
        q_obj = self.get('saved_question', **kwargs)[0]
        asker = api.QuestionAsker(self.session, q_obj, **q_args)
        asker.run({'ProgressChanged': progressChanged})
        req_kwargs = self._get_req_kwargs(**kwargs)
        result = self.session.getResultData(q_obj, **req_kwargs)
        return result

    def ask(self, qtype, **kwargs):
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
            raise AppError(err(obj, api_attrs))

        # if there is a multi in obj_map, that means we can pass a list
        # type to the api. the list will an entry for each api_kw
        if obj_map['multi']:
            return self._get_multi(obj_map, **kwargs)

        # if there is a single in obj_map but not multi, that means
        # we have to find each object individually
        if obj_map['single']:
            return self._get_single(obj_map, **kwargs)

        err = "No single or multi search defined for {}".format
        raise AppError(err(obj))

    def _empty_obj(self, api_object):
        is_list = getattr(api_object, '_list_properties', {})
        is_str = utils.is_str(api_object)
        if any([is_list, is_str]) and not api_object:
            return True
        else:
            return False

    def _get_req_kwargs(self, **kwargs):
        REQ_KWARGS = constants.REQ_KWARGS
        req_kwargs = {}
        for i in kwargs:
            if i in REQ_KWARGS:
                req_kwargs[i] = kwargs[i]
        return req_kwargs

    def _find(self, api_object, **kwargs):
        req_kwargs = self._get_req_kwargs(**kwargs)
        mylog.debug("Searching for {}".format(api_object))
        found = self.session.find(api_object, **req_kwargs)
        if self._empty_obj(found):
            err = "No results found searching for {}!!".format
            raise AppError(err(api_object))
        mylog.debug("Found {}".format(found))
        return found

    def _get_q_obj_map(self, qtype):
        Q_OBJ_MAP = constants.Q_OBJ_MAP
        try:
            obj_map = Q_OBJ_MAP[qtype.lower()]
        except KeyError:
            err = "{} not a valid question type, must be one of {!r}".format
            raise AppError(err(qtype, Q_OBJ_MAP.keys()))
        return obj_map

    def _get_obj_map(self, obj):
        GET_OBJ_MAP = constants.GET_OBJ_MAP
        try:
            obj_map = GET_OBJ_MAP[obj.lower()]
        except KeyError:
            err = "{} not a valid object to get, must be one of {!r}".format
            raise AppError(err(obj, GET_OBJ_MAP.keys()))
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
