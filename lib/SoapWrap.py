#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Tanium Python Wrapper Class

Like saran wrap. But not.

This requires Python 2.7

Reference for Tanium's SOAP API: http://kb.tanium.com/SOAP
"""
import os
import sys
import logging
import time
import csv
import json
import StringIO
import re

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

import requests
import SoapErrors
import SoapConstants
import SoapUtil
import xmltodict

# disable warning messages about insecure HTTPS validation
requests.packages.urllib3.disable_warnings()


class SoapWrap:

    def __init__(self, username=None, password=None, host=None, port="443",
                 protocol='https', soap_path="/soap", loglevel=0,
                 logfile=None, debugformat=False, **kwargs):

        # setup the console logging handler
        SoapUtil.setup_console_logging()
        # create all the loggers and set their levels based on loglevel
        SoapUtil.set_log_levels(loglevel)
        # change the format of console logging handler if need be
        SoapUtil.change_console_format(debugformat)
        self.transform = SoapTransform()

        self.swlog = logging.getLogger("SoapWrap")
        self.DLOG = self.swlog.debug
        self.ILOG = self.swlog.info
        self.WLOG = self.swlog.warn
        self.ELOG = self.swlog.error

        self.HTTPLOG = logging.getLogger("SoapWrap.http").debug
        self.AUTHLOG = logging.getLogger("SoapWrap.auth").debug
        self.RILOG = logging.getLogger("SoapWrap.result_infos").debug

        SOAP_TPL = ("{}{}").format
        APP_TPL = ("{}://{}:{}").format
        # use port 444 if you have direct access to it, direct access to API
        # instead of using apache forwarder @ 443

        self.last_http_response = None
        self.last_response = None
        self.last_request = None

        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__soap_path = soap_path
        self.__username = username
        self.__password = password
        self.all_responses = []
        self.app_version = 'Unknown'

        self.__env_overrides()

        if not self.__host:
            raise SoapErrors.AppError("Must supply host!")
        if not self.__username:
            raise SoapErrors.AppError("Must supply username!")
        if not self.__password:
            raise SoapErrors.AppError("Must supply password!")

        # kwargs here allows SoapWrap instantiation to pass
        # SHOW_SESSION_ID to SoapAuth
        self.auth = SoapAuth(self.__username, self.__password, **kwargs)
        self.app_url = APP_TPL(self.__protocol, self.__host, self.__port)
        self.soap_url = SOAP_TPL(self.app_url, self.__soap_path)

        self.test_app_port()
        self.server_info = self.get_server_info()

    def __str__(self):
        STR_TPL = (
            "SoapWrap to {}, Version: {}"
        ).format
        ret = STR_TPL(self.soap_url, self.server_info['Settings']['Version'])
        return ret

    def __env_overrides(self):
        """looks for OS environment variables and overrides the corresponding
        attribute if they exist
        """
        OR_TPL = ("Overriding {!r} with OS environment variable {!r}").format
        OS_ENV_MAP = {
            'SOAP_USERNAME': 'self.__username',
            'SOAP_PASSWORD': 'self.__password',
            'SOAP_HOSTNAME': 'self.__host',
            'SOAP_PORT': 'self.__port',
            'SOAP_PROTOCOL': 'self.__protocol',
            'SOAP_PATH': 'self.__soap_path',
        }

        for os_env_var, class_var in OS_ENV_MAP.iteritems():
            if not os_env_var in os.environ.keys():
                continue

            if not os.environ[os_env_var]:
                continue

            self.DLOG(OR_TPL(os.environ[os_env_var], os_env_var))
            setattr(self, class_var, os.environ[os_env_var])

    def __page_ok(self, page):
        """return True if the page object is not None and has a status code
        of 200
        """
        valid_status = [200]
        page_ok = False
        if not page:
            return page_ok
        if page.status_code not in valid_status:
            return page_ok
        page_ok = True
        return page_ok

    def __call_api(self, request):
        """makes a call to the SOAP API, returns a SoapResponse object,
        expects a SoapRequest object as request
        """
        TIME_TPL = ('Last Request {} took longer than {} seconds!').format

        if request.command == "GetResultData":
            request.command = "GetResultInfo"

        # set sent time on request
        request.sent = time.time()

        try:
            # get the SOAP response and store it in response
            response = self.__send_request(request)
        except SoapErrors.AuthorizationError:
            # if auth failed and we are using a session ID,
            # fallback to user/pass and retry the request
            # N.B. session ID's expire 5 minutes after their last use
            if self.auth.via_session_id:
                self.AUTHLOG(
                    "Last request failed due to expired/invalid session ID, "
                    "retrying request with username/password"
                )
                self.auth.auth_fallback()
                response = self.__send_request(request)
            else:
                raise

        if request.command == "GetResultInfo":
            # TODO: ADD LONGER WAIT TIME FOR HIGHER est_total
            # TO BE NICER TO API
            full_results = False
            wait = 1
            max_wait = 600
            current_wait = 1
            while full_results is not True:
                result_xml = response.inner_return
                result_infos = result_xml['result_infos']
                result_info = result_infos['result_info']
                self.RILOG((
                    "GetResultInfo result_infos: {}"
                ).format(result_infos))
                mr_passed = result_info['mr_passed']
                est_total = result_info['estimated_total']
                if mr_passed == est_total:
                    full_results = True
                response = self.__send_request(request)
                current_wait += 1
                if current_wait > max_wait:
                    raise SoapErrors.AppError(TIME_TPL(request, max_wait))
                time.sleep(wait)

            request.command = "GetResultData"
            response = self.__send_request(request)

        return response

    def __send_request(self, request):
        """sends the request to the SOAP API"""
        SEND_TPL = ("Sending {}, SOAP URL: {}").format
        RECV_TPL = ("Received {}, SOAP URL: {}").format

        # set token to user/pass or session ID accordingly
        self.auth.update_token()

        # update last_requests auth_dict with current token
        request.auth_dict = self.auth.token

        self.DLOG(SEND_TPL(request, self.soap_url))

        # build the xml request for the last request
        request_xml = request.build_request_xml_raw()
        self.last_request = request

        # send the request XML as a SOAP post
        http_response = self.soap_post(request_xml)

        # store the response in a SoapResponse object
        response = SoapResponse(
            soap_url=self.soap_url,
            request=request,
            http_response=http_response,
        )
        self.last_response = response
        self.DLOG(RECV_TPL(response, self.soap_url))

        # update auth token with last reponses session_id
        self.auth.session_id = response.session_id

        # append this response to all responses
        self.all_responses.append(response)

        return response

    def __check_single_query(self, query):
        ERR_TPL = (
            "Too many list items!! string or list with single string "
            "required, you passed in {}"
        ).format

        if SoapUtil.is_list(query):
            if len(query) != 1:
                raise Exception(ERR_TPL(query))

    def __parse_query_objects(self, args, prefixes):
        if SoapUtil.is_list(args):
            parsed_args = []
            for i in args:
                parsed_arg = self.__parse_query_objects(i, prefixes)
                if parsed_arg:
                    parsed_args.append(parsed_arg)
            return parsed_args
        p = {}
        args = str(args)
        for prefix in prefixes:
            inner_pre = prefix + ':'
            if args.startswith(inner_pre):
                p = {prefix: args.lstrip(inner_pre)}
                break
        if not p:
            p = {prefixes[0]: args}
        return p

    def __build_objects_dict(self, objtype, objquery, prefixes=None):
        if prefixes is None:
            prefixes = SoapConstants.QUERY_PREFIXES
        objects_dict = {
            objtype: self.__parse_query_objects(objquery, prefixes)
        }
        return objects_dict

    def test_app_port(self):
        """validates that the SOAP port on the SOAP host can be reached"""
        CHK_TPL = ("Port test to {}:{} {}").format
        if SoapUtil.port_check(self.__host, self.__port):
            self.DLOG(CHK_TPL(self.__host, self.__port, "SUCCESS"))
        else:
            raise SoapErrors.AppError(
                CHK_TPL(self.__host, self.__port, "FAILURE")
            )

    def http_get(self, url, headers={}):
        """perform an HTTP get using the requests module - this is
        so we always bypass SSL verification, and wrap exceptions into a
        requests-like object
        """
        ER1_TPL = ("SSL Error in HTTP GET to {!r}: {}").format
        try:
            ret = requests.get(url, verify=False, headers=headers)
            self.last_http_response = ret
        except requests.exceptions.SSLError as e:
            raise SoapErrors.AppError(ER1_TPL(url, e))
        return ret

    def http_post(self, url, data, headers={}):
        """perform an HTTP post using the requests module - this is
        so we always bypass SSL verification, and wrap exceptions into a
        requests-like object
        """
        ER1_TPL = ("SSL Error in HTTP POST to {!r}: {}").format
        try:
            ret = requests.post(url, data=data, verify=False, headers=headers)
            self.last_http_response = ret
        except requests.exceptions.SSLError as e:
            raise SoapErrors.AppError(ER1_TPL(url, e))
        return ret

    def soap_post(self, data, url=None):
        """uses http_post to perform a SOAPAction call to url with data"""
        DBG1_TPL = ('Received SOAP Response {}:\n{}').format
        if not url:
            url = self.soap_url
        headers = {'SOAPAction': '""'}
        ret = self.http_post(url=url, data=data, headers=headers)
        self.HTTPLOG(DBG1_TPL(ret.status_code, ret.text.encode(ret.encoding)))
        return ret

    def get_parse_groups(self, question):
        """sends a parse question Request and returns the response

        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        ERR1_TPL = ("No inner_return returned from last response").format
        ERR2_TPL = ("No parse results returned for {!r}").format
        DBUG1_TPL = (
            "No matching questions for {!r}, full list of questions: {}"
        ).format
        DBUG2_TPL = ("Matching parse_result for {!r}: {!r}").format

        object_type = 'question'
        request_args = {
            'command': 'AddObject',
            'object_type': object_type,
            'objects_dict': {'parse_job': {'question_text': question}},
            'auth_dict': self.auth.token,
        }

        request = SoapRequest(**request_args)
        response = self.__call_api(request)

        response.prg_match = None

        result_obj = getattr(response, 'inner_return', {})

        if not result_obj:
            self.ELOG(ERR1_TPL())
            return response

        prgs_all = result_obj.get('parse_result_groups', {})
        prgs_all = prgs_all.get('parse_result_group', [])
        response.prgs_all = prgs_all

        if not prgs_all:
            self.ELOG(ERR2_TPL(question))
            return response

        prg_match = [
            x for x in prgs_all
            if x['question_text'].lower() == question.lower()
        ]

        if not prg_match:
            self.DLOG(DBUG1_TPL(
                question.lower(),
                [x['question_text'] for x in prgs_all],
            ))
            return response

        prg_match = prg_match[0]
        response.prg_match = prg_match
        self.DLOG(DBUG2_TPL(question.lower(), prg_match))

        return response

    def ask_parsed_question(self, question, picker=None):
        PICK_TPL = (
            "Re-run with picker=$INDEX, where $INDEX is "
            "one of the following:\n{}"
        ).format
        PERR_TPL = (
            "Invalid picker index {}, re-run with picker=-1 to see picker "
            "index list"
        ).format
        QRET_TPL = ("Question ID {} returned from AddObject on {}").format
        QERR_TPL = ("No question ID returned from AddObject on {}").format

        response = self.get_parse_groups(question)
        prg_match = getattr(response, 'prg_match', {})
        prgs_all = getattr(response, 'prgs_all', [])
        picker_indexes = "\n".join([
            ("INDEX: {}, parsedq: {}").format(xidx, x['question_text'])
            for xidx, x in enumerate(prgs_all)
        ])

        if picker == -1:
            raise SoapErrors.PickerError(PICK_TPL(picker_indexes))

        if not prg_match and picker is None:
            raise SoapErrors.PickerError(PICK_TPL(picker_indexes))

        if picker:
            try:
                prg_match = prgs_all[picker]
            except IndexError:
                raise SoapErrors.PickerError(PERR_TPL(picker))

        response = self.add_parse_group(prg_match)
        result_object = getattr(response, 'inner_return', {})
        question_id = result_object.get('question', {}).get('id', '')

        response.question_id = question_id
        self.DLOG(QRET_TPL(question_id, prg_match))
        if not question_id:
            raise SoapErrors.AppError(QERR_TPL(prg_match))

        response = self.get_question_results(question_id)
        return response

    def add_parse_group(self, parse_group):
        object_type = 'question'
        objects_dict = {'parse_result_group': parse_group}
        request_args = {
            'command': 'AddObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def ask_saved_question(self, query):
        """sends a saved question Request and returns the response

        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        self.__check_single_query(query)
        object_type = 'saved_question'
        objects_dict = self.__build_objects_dict(object_type, query)
        request_args = {
            'command': 'GetResultData',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        response.sensors = self.gather_sensors_from_response(response)
        return response

    def get_question_results(self, query):
        """sends a get question request and returns a SoapResponse object
        can only ask for questions by ID
        :return: :class:`SoapResponse`
        """
        object_type = 'question'
        objects_dict = self.__build_objects_dict(object_type, query, ['id'])
        request_args = {
            'command': 'GetResultData',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        response.sensors = self.gather_sensors_from_response(response)
        return response

    def gather_sensors_from_response(self, response):
        inner_return = response.inner_return
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        header_list = result_set['cs']
        header_list = header_list['c']
        sensor_hashes = list(set([x['wh'] for x in header_list]))
        sensor_hashes = [
            'hash:%s' % x for x in sensor_hashes if x != '0'
        ]
        sensor_objects = []
        if sensor_hashes:
            response = self.get_sensor_object(sensor_hashes)
            sensor_objects = response.inner_return['sensor']
        return sensor_objects

    def get_saved_question_object(self, query):
        """sends a get saved question request and returns a SoapResponse
        object
        :return: :class:`SoapResponse`
        """
        object_type = 'saved_question'
        objects_dict = self.__build_objects_dict(object_type, query)
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_all_saved_question_objects(self):
        """sends a get all saved question request and returns a SoapResponse
        object
        :return: :class:`SoapResponse`
        """
        object_type = 'saved_question'
        objects_dict = {object_type: ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_question_object(self, query):
        """sends a get question request and returns a SoapResponse object
        can only ask for questions by ID
        :return: :class:`SoapResponse`
        """
        object_type = 'question'
        objects_dict = self.__build_objects_dict(object_type, query, ['id'])
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_all_question_objects(self):
        """sends a get all question request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        object_type = 'question'
        objects_dict = {object_type: ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_sensor_object(self, query):
        """sends a get sensor request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        object_type = 'sensor'
        objects_dict = self.__build_objects_dict(object_type, query)
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_all_sensor_objects(self):
        """sends a get all sensors request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        object_type = 'sensor'
        objects_dict = {object_type: ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_package_object(self, query):
        """sends a get package request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        object_type = 'package_spec'
        objects_dict = self.__build_objects_dict(object_type, query)
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_all_package_objects(self):
        """sends a get all packages request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        object_type = 'package_spec'
        objects_dict = {object_type: ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_action_object(self, query):
        """sends a get action request and returns a SoapResponse object
        can only ask for action by id (by name broken in API)
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        object_type = 'action'
        objects_dict = self.__build_objects_dict(object_type, query, ['id'])
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_all_action_objects(self):
        """sends a get all actions request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        object_type = 'action'
        objects_dict = {'actions': ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_group_object(self, query):
        """sends a get group request and returns a SoapResponse object
        :param query: string or list of queries
        :return: :class:`SoapResponse`
        """
        object_type = 'group'
        objects_dict = self.__build_objects_dict(object_type, query)
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_all_group_objects(self):
        """sends a get all groups request and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        object_type = 'group'
        objects_dict = {'groups': ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        return response

    def get_server_info(self):
        """sends a get server_info and returns a SoapResponse object
        :return: :class:`SoapResponse`
        """
        #<object_list><server_info/></object_list>
        object_type = 'server_info'
        objects_dict = {object_type: ''}
        request_args = {
            'command': 'GetObject',
            'object_type': object_type,
            'objects_dict': objects_dict,
            'auth_dict': self.auth.token,
        }
        request = SoapRequest(**request_args)
        response = self.__call_api(request)
        server_info = response.inner_return['Diagnostics']
        server_info = {k: v for j in server_info for k, v in j.iteritems()}
        return server_info


class SoapRequest(object):
    def __init__(self, auth_dict, object_type, objects_dict, command):
        """handles the creation of XML for a SOAP request

        :param auth_dict: dict of authorization info to include in XML
        :param command: string to set command XML element to
        :param objects_dict: dict of objects to include in object_list element
        """
        super(SoapRequest, self).__init__()
        self.XMLCLOG = logging.getLogger("SoapWrap.xmlcreate").debug

        try:
            self.caller_method = SoapUtil.get_caller_method()
        except:
            self.caller_method = self.command

        self.xml_raw = ''
        self.xml_dict = {}

        self.auth_dict = auth_dict
        self.object_type = object_type
        self.objects_dict = objects_dict
        self.command = command

    def __str__(self):
        STR_TPL = (
            "{} for {!r} of {!r}, Sent: {}, Auth: {}"
        ).format
        sent = self.sent_human or "Not Yet Sent"
        ret = STR_TPL(
            self.__class__.__name__,
            self.caller_method,
            self.objects_dict,
            sent,
            self.auth_type,
        )
        return ret

    def build_request_xml_dict(self):
        """builds the xml envelope needed for a SOAP request

        request.command should be a valid SOAP command, i.e. the following:
          GetObject
          GetResultData

        request.auth_dict should be one of the following:
          # session id based auth
          {'session': '$SESSION_ID'}
          # username/password based auth
          {'auth': {'username': '$USERNAME', 'password': '$PASSWORD'}}

        request.objects_dict should be something like one of the following:
          # get a single sensor
          {'sensor': {'name': 'Computer Name'}}
          {'sensor': {'id': '65'}}
          {'sensor': {'hash': '2940242'}}

          # get all sensors
          {'sensor': {'name': ''}}
        """
        '''
        example format for the dictionary we need to build
        {
          "soap:Envelope": {
            "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
            "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "soap:Body": {
              "tanium_soap_request": {
                "@xmlns": "urn:TaniumSOAP",
                "session": "...",
                "command": "GetResultData",
                "object_list": {
                  "question": {
                    "id": "19473"
                   }
                },
                "ID": "0",
                "ContextID": "0"
              }
            }
          }
        }
        '''
        soap_req = {
            'object_list': self.objects_dict,
            'command': self.command,
            'ID': '0',
            'ContextID': '0',
        }
        soap_req.update(SoapConstants.REQ_APP_NS)
        soap_req.update(self.auth_dict)
        body = {'tanium_soap_request': soap_req}
        envelope = {'soap:Body': body}
        envelope.update(SoapConstants.REQ_ENVELOPE_NS)
        root = {'soap:Envelope': envelope}
        return root

    def build_request_xml_raw(self):
        DBG1_TPL = ('Created XML Request Dict:\n{}').format
        DBG2_TPL = ('Created XML Request Raw:\n{}').format
        self.xml_dict = self.build_request_xml_dict()
        self.XMLCLOG(DBG1_TPL(SoapUtil.jsonify(self.xml_dict)))
        self.xml_raw = xmltodict.unparse(self.xml_dict, pretty=True)
        self.XMLCLOG(DBG2_TPL(self.xml_raw))
        return self.xml_raw

    @property
    def auth_type(self):
        """returns the auth type of self.auth_dict"""
        auth_type = "Undefined"
        if not hasattr(self, 'auth_dict'):
            return auth_type

        keys = self.auth_dict.keys()
        if 'auth' in keys:
            auth_type = 'user/pass'
        elif 'session' in keys:
            auth_type = 'session'
        return auth_type

    @property
    def sent_human(self):
        """returns the time the request was sent in human friendly format"""
        if not hasattr(self, '_sent'):
            return None
        return SoapUtil.human_time(self._sent)

    @property
    def sent(self):
        """returns the time the request was sent"""
        if not hasattr(self, '_sent'):
            return None
        return self._sent

    @sent.setter
    def sent(self, value):
        """sets the time the request was sent"""
        self._sent = value


class SoapResponse(object):

    def __init__(self, soap_url, request, http_response):
        super(SoapResponse, self).__init__()
        self.XMLPLOG = logging.getLogger("SoapWrap.xmlparse").debug
        self.everything_ok = False
        self.received = time.time()

        # URL to SOAP in question
        self.soap_url = soap_url

        # request = SoapRequest object
        self.request = request

        # http_response = requests module object
        self.http_response = http_response

        self.check_response_ok(self.http_response)
        self.outer_xml = self.get_outer_xml(self.http_response)
        self.outer_return = self.get_outer_return(self.outer_xml)
        self.command = self.get_command(self.outer_return)
        self.check_auth_ok(self.command)
        self.check_command_ok(self.command)
        self.session_id = self.get_session_id(self.outer_return)
        self.inner_return = self.get_inner_return(
            self.command, self.outer_return)

    def __str__(self):
        received = self.received_human or "Not Yet Sent"
        STR_TPL = (
            "SoapResponse from: {}, len: {}, on: {}, {}"
        ).format
        ret = STR_TPL(
            self.soap_url,
            len(self.http_response.text),
            received,
            self.request,
        )
        return ret

    def get_outer_xml(self, http_response):
        """chew up the raw text from the http_response into a dict"""
        NOTEXT_TPL = ("No text converted from HTTP response: {}").format
        OUTER_ERR = ("Exception while converting outer XML: {}").format

        text = http_response.text

        if not text:
            raise SoapErrors.HttpError(NOTEXT_TPL(text))

        text = text.encode('utf-8')

        try:
            outer_xml = xmltodict.parse(text)
        except Exception as e:
            raise SoapErrors.BadResponseError(OUTER_ERR(e))

        return outer_xml

    def get_outer_return(self, outer_xml):
        P1_TPL = ("Parsed outer return from XML:\n{}").format
        OUTER_ERR = ("Exception while parsing outer XML: {}").format
        try:
            outer_envelope = outer_xml['soap:Envelope']
            outer_body = outer_envelope['soap:Body']
            outer_return = outer_body['t:return']
        except Exception as e:
            raise SoapErrors.OuterReturnError(OUTER_ERR(e))
        self.XMLPLOG(P1_TPL(SoapUtil.jsonify(outer_return)))
        return outer_return

    def get_command(self, outer_return):
        P1_TPL = ("Parsed command from outer return: {}").format
        command = outer_return['command']
        self.XMLPLOG(P1_TPL(SoapUtil.jsonify(command)))
        return command

    def check_auth_ok(self, command):
        AUTH_ERR = ("Authorization failure in {} (COMMAND: {!r})").format
        auth_ok = 'Forbidden' not in command
        if not auth_ok:
            raise SoapErrors.AuthorizationError(AUTH_ERR(self, self.command))
        return auth_ok

    def check_response_ok(self, http_response):
        NON_200 = ("Non 200 status code {!r} (RESPONSE: {})").format
        valid_codes = [200]
        response_ok = http_response.status_code in valid_codes
        if not response_ok:
            raise SoapErrors.HttpError(NON_200(
                self.http_response.status_code, self.http_response.text
            ))
        return response_ok

    def check_command_ok(self, command):
        BAD_ERR = ("Bad Command Return in {} (COMMAND: {!r})").format
        command_ok = 'Bad Request' not in command
        if not command_ok:
            raise SoapErrors.BadRequestError(
                BAD_ERR(self, self.command.replace('\n', ''))
            )
        return command_ok

    def get_session_id(self, outer_return):
        P1_TPL = ("Parsed session from outer return: {}").format
        session_id = outer_return['session']
        self.XMLPLOG(P1_TPL(SoapUtil.jsonify(session_id)))
        return session_id

    def get_inner_return(self, command, outer_return):
        P1_TPL = ("Parsed inner return from outer return: {}").format
        XML_ERR = ("Exception getting inner ResultXML: {}").format
        OBJ_ERR = ("Exception getting inner result_object: {}").format
        UNK_ERR = ("Unknown command: {}, unable to get inner return").format

        inner_return = None
        result_xml_commands = ['GetResultData', 'GetResultInfo']
        result_obj_commands = ['GetObject', 'AddObject', 'DeleteObject']
        if command in result_xml_commands:
            self.XMLPLOG("Parsing ResultXML from outer return")
            try:
                inner_return = xmltodict.parse(outer_return['ResultXML'])
            except Exception as e:
                raise SoapErrors.InnerReturnError(XML_ERR(e))
        elif command in result_obj_commands:
            self.XMLPLOG("Parsing result_object from outer return")
            try:
                if SoapUtil.is_str(outer_return['result_object']):
                    inner_return = eval(outer_return['result_object'])
                else:
                    inner_return = outer_return['result_object']
            except Exception as e:
                raise SoapErrors.InnerReturnError(OBJ_ERR(e))
        else:
            raise SoapErrors.UnknownCommandError(UNK_ERR(self.command))

        self.XMLPLOG(P1_TPL(SoapUtil.jsonify(inner_return)))
        return inner_return

    @property
    def received_human(self):
        return SoapUtil.human_time(self.received)


class SoapAuth(object):
    def __init__(self, username, password, **kwargs):
        super(SoapAuth, self).__init__()

        self.AUTHLOG = logging.getLogger("SoapWrap.auth").debug
        self._username = username
        self._password = password
        self.session_id = None
        self._token = {}

        constant_args = [
            'SHOW_SESSION_ID',
        ]
        for a in constant_args:
            v = kwargs.get(a) or getattr(SoapConstants, a)
            setattr(self, a, v)
        self.update_token()

    def __str__(self):
        STR_TPL = (
            "SoapAuth {}"
        ).format
        ret = STR_TPL(self.token_type_details)
        return ret

    def update_token(self):
        """updates self.token with either session ID or user/pass auth"""
        UPD_TPL = ("SOAP Token updated to: {}").format
        if self.session_id:
            token = self.token_session_id
        else:
            token = self.token_userpass
        if self._token != token:
            self._token = token
            self.AUTHLOG(UPD_TPL(self.token_type_details))

    def auth_fallback(self):
        """removes the session ID from the token, and reverts back to
        user and password auth"""
        self.session_id = None
        self.update_token()

    def session_id_text(self, session_id):
        """returns session ID if SHOW_SESSION_ID = True"""
        if self.SHOW_SESSION_ID:
            id_text = session_id
        else:
            id_text = "..."
        return id_text

    @property
    def token(self):
        """returns the token"""
        if not hasattr(self, '_token'):
            return None
        return self._token

    @token.setter
    def token(self, value):
        """sets the token"""
        self._token = value

    @property
    def via_session_id(self):
        """returns True if self.token dict has 'session' in it"""
        return 'session' in self._token.keys()

    @property
    def via_userpass(self):
        """returns True if token dict has 'auth' in it"""
        return 'auth' in self._token.keys()

    @property
    def token_type_details(self):
        """returns token type and details in text form"""
        TOK_TPL = ('auth type: {} [{}: "{}"]').format
        token_details = "NONE"
        token_type = "UNKNOWN"
        if self.via_session_id:
            token_predetails = 'ID'
            token_details = self.session_id_text(self._token.get('session'))
            token_type = 'session ID'
        elif self.via_userpass:
            token_predetails = 'username'
            token_details = self._token.get('auth').get('username')
            token_type = 'username/password'
        else:
            token_predetails = 'None'
            token_details = 'None'
            token_type = 'Not yet set'

        token_type_details = TOK_TPL(
            token_type, token_predetails, token_details
        )
        return token_type_details

    @property
    def token_userpass(self):
        """returns a dictionary that has 'auth': SOAP element: auth,
        $username, $password
        """
        token = {
            'auth': {'username': self._username, 'password': self._password}
        }
        return token

    @property
    def token_session_id(self):
        """returns a dictionary that has 'session': '$session_id' """
        token = {'session': self.session_id}
        return token


class SoapTransform(object):

    def __init__(self):
        self.logger = logging.getLogger("SoapWrap.transform")
        self.DLOG = self.logger.debug
        self.ILOG = self.logger.info
        self.WLOG = self.logger.warn
        self.ELOG = self.logger.error

    def write_response(self, response, fname=None, fdir=None, format='csv',
                       **kwargs):
        # kwargs passthrus:
        # HEADER_SORT_PRIORITY: sort_headers()
        # ADD_TYPE_TO_HEADERS: parse_resultxml()
        # ADD_SENSOR_TO_HEADERS: parse_resultxml()
        # EXPAND_GROUPED_COLUMNS: parse_resultxml()
        # HIDE_COUNT_COLUMN: parse_resultxml()

        WRITE_TPL = ("Writing response to file: {}").format
        BADF_ERR = ("Unsupported format: {!r}, must be one of {r}").format

        objtype = response.request.object_type

        HEADER_SORT_PRIORITY = [
            '%s.%s' % (objtype, x) for x in SoapConstants.HEADER_SORT_PRIORITY
        ]

        if response.command == 'GetObject':
            if 'HEADER_SORT_PRIORITY' not in kwargs:
                kwargs['HEADER_SORT_PRIORITY'] = HEADER_SORT_PRIORITY

        if fname is None:
            fname = self.get_fn(response, format)

        if 'fprefix' in kwargs:
            fname = ("{}_{}").format(kwargs['fprefix'], fname)

        if fdir is None:
            fdir = os.path.curdir

        fpath = os.path.join(fdir, fname)

        formats = {
            'csv': 'get_csv',
            'xls': 'get_xls',
            'json': 'get_json',
            'xml': 'get_xml',
            'raw.xml': 'get_rawxml',
            'http_response': 'get_http_response',
        }

        if format in formats:
            fout = getattr(self, formats[format])(response, **kwargs)
        else:
            raise SoapErrors.TransformError(BADF_ERR(
                format, ', '.join(formats.keys())
            ))

        self.ILOG(WRITE_TPL(fpath))

        x = open(fpath, 'w+')
        x.write(fout)
        x.close()
        return fpath

    def get_fn(self, response, format):
        max_len = 80
        s = str(response.request.objects_dict)
        s = re.sub(r'[^\w,:]', '', s)
        s = s.replace(':', '_')
        s = s.replace(',', '+')
        s = s[0:max_len]

        base_fn = []
        base_fn.append(response.request.caller_method)
        base_fn.append(s)
        base_fn.append(SoapUtil.get_now())
        base_fn = '__'.join(base_fn)
        fn = ("{}.{}").format(base_fn, format)
        return fn

    def get_rows(self, response, **kwargs):
        """transforms response.inner_return into a list of dicts"""
        if response.command == 'GetObject':
            rows = self.parse_result_object(response, **kwargs)
        elif response.command == 'GetResultData':
            rows = self.parse_resultxml(response, **kwargs)

        # utf cleanup
        for row in rows:
            for k in row:
                row[k] = SoapUtil.utf_clean(row[k])

        return rows

    ## XML

    ## JSON
    def get_json(self, response, **kwargs):
        rows_list = self.get_rows(response, **kwargs)
        fout = json.dumps(rows_list, sort_keys=True, indent=4)
        return fout

    ## CSV
    def get_csv(self, response, **kwargs):
        rows_list = self.get_rows(response, **kwargs)
        fout = self.csvdictwriter(rows_list, **kwargs)
        return fout

    ## CSV
    def get_all_headers(self, rows_list):
        headers = []
        for row_dict in rows_list:
            [headers.append(h) for h in row_dict.keys() if h not in headers]
        return headers

    ## CSV
    def sort_headers(self, headers, **kwargs):
        header_sort_priority = kwargs.get('HEADER_SORT_PRIORITY', [])
        if header_sort_priority is False:
            return headers
        sorted_headers = sorted(headers)
        if header_sort_priority:
            p_headers = []
            for kp in header_sort_priority:
                for kidx, k in enumerate(sorted_headers):
                    if k.endswith(kp):
                        p_headers.append(sorted_headers.pop(kidx))
            p_headers += sorted_headers
            sorted_headers = p_headers
        return sorted_headers

    ## CSV
    def csvlistwriter(self, rows_list):
        '''unused'''
        csv_io = StringIO.StringIO()
        headers = rows_list.pop(0)
        writer = csv.writer(csv_io, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        writer.writerows(rows_list)
        csv_str = csv_io.getvalue()
        return csv_str

    ## CSV
    def csvdictwriter(self, rows_list, **kwargs):
        """returns the rows_list (list of dicts) as a CSV string"""
        csv_io = StringIO.StringIO()
        headers = self.get_all_headers(rows_list)
        headers = self.sort_headers(headers, **kwargs)
        writer = csv.DictWriter(
            csv_io, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writerow(dict((h, h) for h in headers))
        writer.writerows(rows_list)
        csv_str = csv_io.getvalue()
        return csv_str

    ## result_object
    def flatten_obj(self, fullobj, prefix=None):
        flat = {}
        # print fullobj, prefix
        if SoapUtil.is_dict(fullobj):
            for k, v in fullobj.iteritems():
                if prefix:
                    k = ('{}.{}').format(prefix, k)
                if SoapUtil.is_dict(v):
                    # print 'dict found: ', k, v
                    flat.update(self.flatten_obj(v, k))
                elif SoapUtil.is_list(v):
                    # print 'list found: ', k, v
                    for idx, item in enumerate(v):
                        itempre = ('{}{}').format(k, idx)
                        flat.update(self.flatten_obj(item, itempre))
                else:
                    # print 'other found: ', k, v
                    if v and SoapUtil.is_str(v):
                        v = v.replace('\n', '\r\n')
                    flat[k] = v
        elif SoapUtil.is_list(fullobj):
            flat[prefix] = ", ".join(fullobj)
        else:
            flat[prefix] = fullobj
        return flat

    ## result_object
    def parse_result_object(self, response, **kwargs):
        """
        example breakdown of result_object for GetObject on sensor:

        single sensor return:
        dict:result_object:
            dict:sensor:
                dict:sensor_details:

        multiple sensors return:
        dict:result_object:
            list:sensor:
                dict:sensor_details:

        all sensors return:
        dict:result_object:
            dict:sensors:
                list:sensor:
                    dict:sensor_details:
        """
        ERR1 = (
            "Unexpected error when parsing inner return: {}"
        ).format
        ERR2 = (
            "inner return contains neither a list or dictionary "
            "unable to parse out result object(s): {}"
        ).format

        try:
            return_items = response.inner_return.items()[0]
            prefix = return_items[0]
            results = return_items[1]
        except Exception as e:
            raise Exception(ERR1(e))

        # handle "all" responses
        if SoapUtil.is_dict(results):
            single_prefix = prefix[:-1]
            if single_prefix in results.keys():
                prefix = single_prefix
                results = results[prefix]

        if SoapUtil.is_list(results):
            rows = [self.flatten_obj(x, prefix) for x in results]
        elif SoapUtil.is_dict(results):
            rows = [self.flatten_obj(results, prefix)]
        else:
            raise Exception(ERR2(response.inner_return))

        return rows

    ## ResultXML
    def parse_resultxml(self, response, **kwargs):
        """
        breakdown of ResultXML for GetResultData:

        dict:result_sets:
            dict:result_set:
                dict:cs:
                    list:c: # column data
                        dict:
                            str:dn # column name
                            int:wh # column grouping
                            int:rt # result type (see RESULT_TYPE_MAP{})
                dict:rs:
                    list:r: # row data
                        dict:
                            list:c: # one entry per column for this row
                                dict:
                                    str/list:v # value for this row&column
        """
        inner_return = response.inner_return
        sensors = getattr(response, 'sensors', [])
        if not SoapUtil.is_list(sensors):
            sensors = [sensors]

        kwargs = {
            k: kwargs.get(k, v)
            for k, v in SoapConstants.PARSE_RESULT_XML_ARGS.iteritems()
        }

        headers = self.get_headers(inner_return)

        if kwargs.get('ADD_TYPE_TO_HEADERS', False):
            headers = self.add_type_to_headers(headers)

        if kwargs.get('ADD_SENSOR_TO_HEADERS', False):
            headers = self.add_sensor_to_headers(headers, sensors)

        rows = self.get_resultxml_rows(inner_return, headers)

        if kwargs.get('HIDE_COUNT_COLUMN', True):
            rows, headers = self.remove_count_column(rows, headers)

        if kwargs.get('EXPAND_GROUPED_COLUMNS', False):
            rows = self.expand_grouped_columns(rows, headers)
        else:
            rows = self.flatten_grouped_columns(rows)
        return rows

    ## ResultXML
    def get_headers(self, inner_return):
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        header_list = result_set['cs']
        header_list = header_list['c']
        headers = []
        for header_dict in header_list:
            header_name = SoapUtil.utf_clean(header_dict['dn'])
            header_type = SoapConstants.RESULT_TYPE_MAP.get(
                header_dict['rt'], 'Unknown',
            )
            header_wh = header_dict['wh']
            headers.append({
                'name': header_name,
                'wh': header_wh,
                'type': header_type,
            })
        return headers

    ## ResultXML
    def add_type_to_headers(self, headers):
        for x in headers:
            x['name'] = "%s (%s)" % (x['name'], x['type'])
        return headers

    ## ResultXML
    def add_sensor_to_headers(self, headers, sensors):
        for h in headers:
            sensor = [x for x in sensors if x['hash'] == h['wh']]
            if sensor:
                sensor = sensor[0]
            else:
                sensor = {}
            if not sensor:
                continue
            h['name'] = "%s: %s" % (sensor.get('name'), h['name'])
        return headers

    ## ResultXML
    def remove_count_column(self, rows, headers):
        COUNT_HEADERS = ['Count (NumericDecimal)', 'Count']
        rows = [
            {k: v for k, v in row.iteritems() if k not in COUNT_HEADERS}
            for row in rows
        ]
        headers = [x for x in headers if x['name'] not in COUNT_HEADERS]
        return rows, headers

    ## ResultXML
    def get_resultxml_rows(self, inner_return, headers):
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        row_lists = result_set['rs']
        row_lists = row_lists['r']
        row_lists = [x['c'] for x in row_lists]
        row_lists = [
            [SoapUtil.utf_clean(y['v']) for y in x] for x in row_lists
        ]
        rows = []
        for row_list in row_lists:
            row_entry = {}
            for col_idx, col_data in enumerate(row_list):
                header = headers[col_idx]['name']
                row_entry[header] = col_data
            rows.append(row_entry)
        return rows

    ## ResultXML
    def flatten_grouped_columns(self, rows):
        rows = [
            {k: self.excel_list(v) for k, v in row.iteritems()}
            for row in rows
        ]
        return rows

    ## ResultXML
    def excel_list(self, l):
        if SoapUtil.is_list(l):
            l = [str(SoapUtil.utf_clean(x)) for x in l]
            l = '\r\n'.join(l)
        return l

    ## ResultXML
    def expand_grouped_columns(self, rows, headers):
        new_rows = []
        for row in rows:
            values_with_list = [SoapUtil.is_list(v) for v in row.values()]
            if not any(values_with_list):
                new_rows.append(row)
                continue
            for k in row:
                if not SoapUtil.is_list(row[k]):
                    continue
                header = [x for x in headers if x['name'] == k][0]
                wh_friends = [x for x in headers if x['wh'] == header['wh']]
                for v_idx, v in enumerate(row[k]):
                    new_rows.append(self.build_new_row(
                        row, wh_friends, v_idx, headers
                    ))
        return new_rows

    ## ResultXML
    def build_new_row(self, row, wh_friends, v_idx, headers):
        new_row = {}
        for h in headers:
            if h not in wh_friends:
                # if this column is not correlated to the column we are
                # working on and it is a multi line return, set it to empty
                if SoapUtil.is_list(row[h['name']]):
                    new_row[h['name']] = ""
                # if this column is not correlated to the column we are working
                # on and it's a single line return, set it to the same value
                else:
                    new_row[h['name']] = row[h['name']]
            else:
                # if this column is correlated to the column we are working on
                # set the value to the indexed value of this value
                new_row[h['name']] = row[h['name']][v_idx]
        return new_row
