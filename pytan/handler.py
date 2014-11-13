# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""PyTan: A wrapper around Tanium's SOAP API in Python

Like saran wrap. But not.

This requires Python 2.7
"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging
from . import utils
from .exceptions import AppError
from . import constants
# from .reports import Reporter
# from . import req
from . import api

mylog = logging.getLogger("pytan")


class Handler(object):
    last_response = None
    last_request = None
    all_responses = []
    app_version = 'Unknown'

    def __init__(self, username=None, password=None, host=None, port="443",
                 loglevel=0, logfile=None, debugformat=False, **kwargs):
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

        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password

        if not self.__host:
            raise AppError("Must supply host!")
        if not self.__username:
            raise AppError("Must supply username!")
        if not self.__password:
            raise AppError("Must supply password!")

        app_tpl = "https://{}:{}".format
        soap_tpl = "{}/soap".format

        self.app_url = app_tpl(self.__host, self.__port)
        self.soap_url = soap_tpl(self.app_url)
        self.test_app_port()
        self.session = api.Session(self.__host, self.__port)
        self.session.authenticate(self.__username, self.__password)

    def __str__(self):
        str_tpl = "Handler for {}".format
        ret = str_tpl(self.session)
        return ret

    def test_app_port(self):
        """validates that the SOAP port on the SOAP host can be reached"""
        chk_tpl = "Port test to {}:{} {}".format
        if utils.port_check(self.__host, self.__port):
            mylog.debug(chk_tpl(self.__host, self.__port, "SUCCESS"))
        else:
            raise AppError(chk_tpl(self.__host, self.__port, "FAILURE"))

    def get_all(self, obj, **kwargs):
        obj_map = self._get_obj_map(obj)
        api_obj_all = getattr(api, obj_map['all'])()
        found = self._find(api_obj_all)
        return found

    def get(self, obj, **kwargs):
        obj_map = self._get_obj_map(obj)
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]

        # if the api doesn't support filtering for this object,
        # return all objects of this type
        if not api_attrs:
            return self.get_all(obj)

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

    def _find(self, api_object):
        mylog.debug("Searching for {}".format(api_object))
        found = self.session.find(api_object)
        is_list = getattr(found, '_list_properties', {})
        is_str = utils.is_str(found)
        if any([is_list, is_str]) and not found:
            err = "No results found searching for {}!!".format
            raise AppError(err(api_object))
        return found

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
        found = self._find(api_obj_multi)
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
                    found.append(self._find(api_obj_single))
            else:
                api_obj_single = getattr(api, obj_map['single'])()
                setattr(api_obj_single, k, v)
                found.append(self._find(api_obj_single))

        return found
