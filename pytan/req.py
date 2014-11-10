# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import time
import logging
import copy
import json
import re
from . import utils
from . import constants
from . import resp
from .exceptions import AuthorizationError
from .exceptions import AppError
from .exceptions import ManualQuestionParserError
from .exceptions import HttpError
from .exceptions import PickerError
from .packages import xmltodict


class Request(object):
    _sent = None
    xml_raw = ''
    xml_dict = {}
    XMLCLOG = logging.getLogger("pytan.request.xmlcreate").debug
    HTTPLOG = logging.getLogger("pytan.request.http").debug

    def __init__(self, handler, command, objtype, query):
        """handles the creation of XML for a SOAP request
        """
        super(Request, self).__init__()

        self.mylog = logging.getLogger("pytan.request")
        self.DLOG = self.mylog.debug
        self.ILOG = self.mylog.info
        self.WLOG = self.mylog.warn
        self.ELOG = self.mylog.error
        self.CLOG = self.mylog.critical

        self.handler = handler
        self.response_class = resp.Response
        self.command = command
        self.objtype = objtype
        self.query = query
        self.objects_dict = self.build_objects_dict()

    def __str__(self):
        str_tpl = "{}: '{}', Auth: {}, Sent: {}".format
        sent = self.sent_human or "Not Yet Sent"
        ret = str_tpl(
            self.__class__.__name__,
            self.query,
            self.auth_type,
            sent,
        )
        return ret

    def call_api(self):
        """makes a call to the SOAP API, returns a Response object,
        """
        time_tpl = 'Last Request {} took longer than {} seconds!'.format
        wait_tpl = (
            "Waiting {} secs, mr_passed {} != estimated_total {}, "
            "row_count: {}"
        ).format
        finish_tpl = "Question finished, rows: {}, servers: {}".format
        no_results = "No results returned, row_count = {}".format

        if self.command == "GetResultData":
            self.command = "GetResultInfo"

        # set sent time on request
        self.sent = time.time()

        try:
            # get the SOAP response and store it in response
            response = self.__send_api_request()
        except AuthorizationError:
            # if auth failed and we are using a session ID,
            # fallback to user/pass and retry the request
            # N.B. session ID's expire 5 minutes after their last use
            if self.handler.auth.via_session_id:
                self.AUTHLOG(
                    "Last request failed due to expired/invalid session ID, "
                    "retrying request with username/password"
                )
                self.handler.auth.auth_fallback()
                response = self.__send_api_request()
            else:
                raise

        if self.command == "GetResultInfo":
            full_results = False
            wait = constants.RESULT_SLEEP
            max_wait = constants.RESULT_MAX_WAIT
            current_wait = 1
            while full_results is not True:
                ri = response.get_result_info()

                if ri['mr_passed'] == ri['estimated_total']:
                    self.ILOG(finish_tpl(
                        ri['row_count'], ri['mr_passed']))

                    if ri['row_count'] == 0:
                        raise AppError(no_results(ri['row_count']))
                    full_results = True
                    break

                response = self.__send_api_request()
                current_wait += wait
                if current_wait > max_wait:
                    raise AppError(time_tpl(self, max_wait))

                self.ILOG(wait_tpl(
                    wait,
                    ri['mr_passed'],
                    ri['estimated_total'],
                    ri['row_count'],
                ))
                time.sleep(wait)

            self.command = "GetResultData"
            response = self.__send_api_request()

        return response

    def __send_api_request(self):
        """sends the request to the SOAP API"""
        send_tpl = "Sending {}, SOAP URL: {}".format
        recv_tpl = "Received {}, SOAP URL: {}".format

        # set token to user/pass or session ID accordingly
        self.handler.auth.update_token()

        # update auth_dict with current token
        self.auth_dict = copy.deepcopy(self.handler.auth.token)

        # build the xml request for the last request
        request_xml = self.build_request_xml_raw()
        self.handler.last_request = self

        self.HTTPLOG(send_tpl(self, self.handler.soap_url))
        # send the request XML as a SOAP post
        page = utils.soap_post(request_xml, self.handler.soap_url)
        self.__page_ok(page)

        response_class = getattr(self, 'response_class', resp.Response)

        # store the response in a Response object
        response = response_class(
            soap_url=self.handler.soap_url,
            request=self,
            page=page,
        )

        self.handler.last_response = response
        self.HTTPLOG(recv_tpl(response, self.handler.soap_url))

        # update auth token with last reponses session_id
        self.handler.auth.session_id = response.session_id

        # append this response to all responses
        self.handler.all_responses.append(response)
        return response

    def __page_ok(self, page):
        dbg1_tpl = 'Received SOAP Response {}:\n{}'.format
        notext_tpl = "No text from HTTP response: {}:\n{}".format
        non_200 = "Non 200 status code {!r} (RESPONSE: {})\n{}".format

        self.HTTPLOG(dbg1_tpl(
            page.status_code,
            page.text.encode(page.encoding),
        ))

        if not page.text:
            raise HttpError(notext_tpl(page, page.text))

        if not utils.page_ok(page):
            raise HttpError(non_200(
                page.status_code, page, page.text
            ))

    def build_objects_dict(self):
        if self.query is None:
            if self.objtype in ['action', 'group']:
                objects_dict = {self.objtype + 's': ''}
            else:
                objects_dict = {self.objtype: ''}
        else:
            if self.objtype in ['question', 'action']:
                prefixes = ['id']
            else:
                prefixes = constants.QUERY_PREFIXES
            objects_dict = {
                self.objtype: utils.parse_query_objects(
                    self.query, prefixes)
            }
        return objects_dict

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
              }
            }
          }
        }
        '''
        soap_req = {
            'object_list': self.objects_dict,
            'command': self.command,
        }
        soap_req.update(constants.REQ_APP_NS)
        soap_req.update(self.auth_dict)
        body = {'tanium_soap_request': soap_req}
        envelope = {'soap:Body': body}
        envelope.update(constants.REQ_ENVELOPE_NS)
        root = {'soap:Envelope': envelope}
        return root

    def build_request_xml_raw(self):
        dbg1_tpl = 'Created XML Request Dict:\n{}'.format
        dbg2_tpl = 'Created XML Request Raw:\n{}'.format
        self.xml_dict = self.build_request_xml_dict()
        self.XMLCLOG(dbg1_tpl(utils.jsonify(self.xml_dict)))
        self.xml_raw = xmltodict.unparse(self.xml_dict, pretty=True)
        self.XMLCLOG(dbg2_tpl(self.xml_raw))
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
        return utils.human_time(self._sent)

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


class AskManualQuestionRequest(Request):
    '''
    This is a more complicated Request, so we override different things
    '''

    def __init__(self, handler, sensors, question_filters=None,
                 question_options=None):
        """handles the creation of XML for ask_manual_question SOAP request
        """
        self.XMLCLOG = logging.getLogger("pytan.request.xmlcreate").debug

        self.mylog = logging.getLogger("pytan.request.manual_question")
        self.DLOG = self.mylog.debug
        self.ILOG = self.mylog.info
        self.WLOG = self.mylog.warn
        self.ELOG = self.mylog.error
        self.CLOG = self.mylog.critical

        self.handler = handler
        self.sensors = sensors
        self.question_filters = question_filters
        self.question_options = question_options
        self.command = 'AddObject'
        self.object_type = 'question'
        self.query = sensors
        self.sensor_objects = []
        self.response_class = resp.AddQuestionJobResponse

    def call_api(self):
        mt1_tpl = "Must supply sensors!".format
        if not utils.is_list(self.sensors):
            self.sensors = [self.sensors]

        if not self.sensors:
            raise ManualQuestionParserError(mt1_tpl())

        # update auth_dict with current token
        self.auth_dict = copy.deepcopy(self.handler.auth.token)

        self.sensor_maps = self.parse_sensors(self.sensors)
        self.objects_dict = self.build_objects_dict()
        print utils.jsonify(self.objects_dict)
        add_q_response = super(AskManualQuestionRequest, self).call_api()
        question_id = add_q_response.result
        response = self.handler.get_question_results(question_id)
        response.sensors = self.handler.gather_sensors_from_response(response)
        response.request = self
        return response

    def parse_sensors(self, sensors):
        '''
        param parsing:
          look for [.*] in each sensor
          tokenize [.*] in each sensor, store in indexed list to sensors, pop
        option parsing:
          split on all ', opt:'
          see if each opt starts with valid option, pop
        filter parsing:
          split on first ', that'
          first pass see if string starts with any type + " ", pop
          second pass see if string starts with any operators + " ", pop
          third pass, leftovers is value
        '''
        sensor_maps = self.parse_params(sensors)
        sensor_maps = self.parse_options(sensor_maps)
        sensor_maps = self.parse_filters(sensor_maps)
        sensor_maps = self.fetch_sensor_objects(sensor_maps)
        print utils.jsonify(sensor_maps, 2)
        return sensor_maps

    def parse_params(self, sensors):
        mt1_tpl = "More than one parameter passed in {!r}".format
        sensor_maps = []
        for s in sensors:
            sensor_map = {'original': s}
            # s=Folder Name Search with RegEx Match[Program Files,\,.*,No,No]

            params = constants.PARAM_RE.findall(s)
            # params=['Program Files,\,.*,No,No']

            if len(params) > 1:
                raise ManualQuestionParserError(mt1_tpl(s))
            elif len(params) == 1:
                param = params[0]
            else:
                param = ''
            # param=Program Files,\,.*,No,No

            if param:
                split_param = constants.PARAM_SPLIT_RE.split(param)
            else:
                split_param = []
            # split_param=['Program Files', '\\,.*', 'No', 'No']

            # remove params from the sensor
            sensor_name = constants.PARAM_RE.sub('', s)
            # sensor_name=Folder Name Search with RegEx Match

            sensor_map['name'] = sensor_name
            sensor_map['params'] = split_param
            sensor_maps.append(sensor_map)
        return sensor_maps

    def parse_options(self, sensor_maps):
        mt1_tpl = "Invalid option specification {!r} in {!r}".format
        for sm in sensor_maps:
            split_option = re.split(r',\s*opt:', sm['name'])

            if len(split_option) == 1:
                sm['options'] = []
                continue

            sensor_name = split_option[0].strip()
            option_str = split_option[1].strip()

            # TODO: if option_str.lower() == 'help': print help

            opt_match = self.get_opt_match(sensor_name, option_str)
            if not opt_match:
                raise ManualQuestionParserError(
                    mt1_tpl(option_str, sm['original']))

            sm['name'] = sensor_name
            if 'options' not in sm:
                sm['options'] = []
            sm['options'].append(opt_match)

        return sensor_maps

    def parse_filters(self, sensor_maps):
        mt1_tpl = "Invalid filter specification {!r} in {!r}".format
        for sm in sensor_maps:
            # split_filter = sm['name'].split(', that', 1)
            split_filter = re.split(r',\s*that', sm['name'])

            if len(split_filter) == 1:
                sm['filters'] = {}
                continue

            sensor_name = split_filter[0].strip()
            filter_str = split_filter[1].strip()

            # TODO: if filter_str.lower() == 'help': print help

            fm_match = self.get_fm_match(sensor_name, filter_str)
            if not fm_match:
                raise ManualQuestionParserError(
                    mt1_tpl(filter_str, sm['original']))

            sm['name'] = sensor_name
            sm['filters'] = fm_match

        return sensor_maps

    def get_fm_match(self, sensor_name, filter_str):
        filter_type, new_filter_str = self.get_filter_type(filter_str)
        fm_match = {}
        for fm in constants.FILTER_MAPS:
            if fm_match:
                break
            for fm_human in fm['human']:
                fm_humanspaced = fm_human + " "
                if new_filter_str.startswith(fm_humanspaced):
                    filter_val = new_filter_str[len(fm_humanspaced):]
                    fm_match = {
                        'sensor': sensor_name,
                        'value': filter_val,
                        'type': filter_type,
                    }
                    fm_match = dict(fm.items() + fm_match.items())
                    break
        return fm_match

    def get_opt_match(self, sensor_name, option_str):
        mt1_tpl = "Option {!r} requires a value in {}".format
        opt_match = []
        for om in constants.OPTION_MAPS:
            if opt_match:
                break
            if option_str.startswith(om['human']):
                if om['human'].endswith(':'):
                    opt_str = option_str.split(':')
                    if len(opt_str) != 2:
                        raise ManualQuestionParserError(
                            mt1_tpl(option_str, om.get('value')))
                    opt_match = [{om['operator']: opt_str[1]}]
                else:
                    opt_match = om['operators']
                break
        return opt_match

    @staticmethod
    def get_filter_type(filter_str):
        filter_type = ''
        new_filter_str = filter_str
        result_types = constants.RESULT_TYPE_MAP.values()
        for rt in result_types:
            rtspaced = rt + " "
            if filter_str.lower().startswith(rtspaced.lower()):
                new_filter_str = filter_str[len(rtspaced):]
                filter_type = rt
                break
        return filter_type, new_filter_str

    def fetch_sensor_objects(self, sensor_maps):
        '''
        this does double duty:
        asks for each sensor individually to make sure it exists
        gets the sensor object so that we can handle parameters
        '''
        nomatch_tpl = ("Sensor {!r} NOT FOUND!!").format
        not_fnd_tpl = (
            "ERROR: Sensor {!r} does not take any parameters and "
            "you supplied: {}"
        ).format

        for sm in sensor_maps:
            try:
                sresp = self.handler.get_sensor_object(sm['name'])
                sobj = sresp.get_sensor_objects()
                sm['object'] = sobj
                self.sensor_objects.append(sobj)
            except Exception as e:
                self.DLOG(e)
                raise ManualQuestionParserError(nomatch_tpl(sm['name']))
            smpd = sobj['parameter_definition'] or {}
            if not smpd and sm['params']:
                raise ManualQuestionParserError(
                    not_fnd_tpl(sm['name'], sm['params']))

        return sensor_maps

    def build_objects_dict(self):

        sselects = []
        for sensor_map in self.sensor_maps:
            sid = sensor_map['object']['id']
            shash = sensor_map['object']['hash']
            sparam_def = sensor_map['object']['parameter_definition'] or {}
            params = sensor_map['params']

            param_dicts = []
            for pd_idx, pd in enumerate(sparam_def.get('parameters') or []):
                param_key = '{0}{1}{0}'.format(
                    constants.PARAM_DELIM, pd['key'])
                try:
                    passed_param = params[pd_idx]
                except IndexError:
                    passed_param = ''
                if not passed_param:
                    continue
                param_dict = {'key': param_key, 'value': passed_param}
                param_dicts.append(param_dict)

            if param_dicts:
                sselect = {'parameter': param_dicts}
                sselect = {'source_id': sid, 'parameters': sselect}
                sfilter = {'id': sid, 'hash': shash}
            else:
                sselect = {'hash': shash}
                sfilter = {'hash': shash}

            sselect = {'sensor': sselect, 'filter': sfilter}
            sselects.append(sselect)

        objects_dict = {'select': sselects}
        objects_dict = {'selects': objects_dict}
        objects_dict = {'question': objects_dict}
        return objects_dict


class AddParseQuestionRequest(Request):
    def __init__(self, **kwargs):
        kwargs['command'] = 'AddObject'
        kwargs['objtype'] = 'question'
        super(AddParseQuestionRequest, self).__init__(**kwargs)
        self.response_class = resp.AddParseQuestionResponse

    def build_objects_dict(self):
        objects_dict = {'parse_job': {'question_text': self.query}}
        return objects_dict


class AddParseResultGroupRequest(Request):
    def __init__(self, **kwargs):
        kwargs['command'] = 'AddObject'
        kwargs['objtype'] = 'question'
        super(AddParseResultGroupRequest, self).__init__(**kwargs)
        self.response_class = resp.AddQuestionJobResponse

    def build_objects_dict(self):
        objects_dict = {'parse_result_group': self.query}
        return objects_dict


class AskParsedQuestionRequest(Request):
    '''
    This is a more complicated Request, so we override different things
    '''

    def __init__(self, handler, query, picker=None):

        self.mylog = logging.getLogger("pytan.request.parsed_question")
        self.DLOG = self.mylog.debug
        self.ILOG = self.mylog.info
        self.WLOG = self.mylog.warn
        self.ELOG = self.mylog.error
        self.CLOG = self.mylog.critical

        self.handler = handler
        self.query = query
        self.picker = picker
        self.command = 'AskParsedQuestion'
        self.objtype = 'question'

    def call_api(self):
        paramerr_tpl = (
            "Parsing parameterized questions is not supported by SOAP API "
            "please use ask_manual_question instead"
        ).format
        nomatch_tpl = ("No matches for {}").format
        manymatch_tpl = ("Too many matches for {}").format
        picker_list = "INDEX: {}, parsedq: {}".format
        pick_tpl = (
            "Re-run with picker=$INDEX, where $INDEX is "
            "one of the following:\n{}"
        ).format
        match_tpl = "parse_result match for {!r}: {!r}".format
        picknum_tpl = "Picker must be a number".format
        perr_tpl = (
            "Invalid picker index {}, re-run with picker=-1 to see picker "
            "index list"
        ).format

        if constants.PARAM_RE.search(self.query):
            raise AppError(paramerr_tpl())

        # set sent time on request
        self.sent = time.time()

        # update auth_dict with current token
        self.auth_dict = copy.deepcopy(self.handler.auth.token)

        parse_question_response = self.handler.add_parse_question_job(
            self.query,
        )

        prg_list = parse_question_response.result

        picker_indexes = "\n".join([
            picker_list(xidx, x['question_text'])
            for xidx, x in enumerate(prg_list)
        ])

        if self.picker is None:
            parse_match = [
                x for x in prg_list
                if x['question_text'].lower() == self.query.lower()
            ]

            if len(parse_match) == 0:
                self.ELOG(nomatch_tpl(self.query))
                raise PickerError(pick_tpl(picker_indexes))
            elif len(parse_match) > 1:
                self.ELOG(manymatch_tpl(self.query))
                raise PickerError(pick_tpl(picker_indexes))
            else:
                parse_match = parse_match[0]
        else:
            try:
                self.picker = int(self.picker)
            except:
                raise PickerError(picknum_tpl())

            if self.picker == -1:
                raise PickerError(pick_tpl(picker_indexes))

            try:
                parse_match = prg_list[self.picker]
            except IndexError:
                raise PickerError(perr_tpl(self.picker))

        self.ILOG(match_tpl(self.query, json.dumps(parse_match)))

        add_prg_response = self.handler.add_parse_result_group_job(parse_match)
        question_id = add_prg_response.result
        response = self.handler.get_question_results(question_id)
        response.sensors = self.handler.gather_sensors_from_response(response)
        response.request = self
        return response

    def build_objects_dict(self):
        pass

    def build_request_xml_dict(self):
        pass

    def build_request_xml_raw(self):
        pass


class AskSavedQuestionRequest(Request):
    def __init__(self, **kwargs):
        kwargs['command'] = 'GetResultData'
        kwargs['objtype'] = 'saved_question'
        super(AskSavedQuestionRequest, self).__init__(**kwargs)

    def call_api(self):
        utils.check_single_query(self.query)
        response = super(AskSavedQuestionRequest, self).call_api()
        response.sensors = self.handler.gather_sensors_from_response(response)
        return response


class QuestionResultsRequest(Request):
    def __init__(self, **kwargs):
        kwargs['command'] = 'GetResultData'
        kwargs['objtype'] = 'question'
        super(QuestionResultsRequest, self).__init__(**kwargs)


class GetObjectRequest(Request):
    def __init__(self, **kwargs):
        kwargs['command'] = 'GetObject'
        super(GetObjectRequest, self).__init__(**kwargs)


class GetAllObjectRequest(GetObjectRequest):
    def __init__(self, **kwargs):
        kwargs['query'] = None
        super(GetAllObjectRequest, self).__init__(**kwargs)


class GetServerInfoRequest(GetObjectRequest):
    def __init__(self, **kwargs):
        kwargs['objtype'] = 'server_info'
        kwargs['query'] = None
        super(GetServerInfoRequest, self).__init__(**kwargs)
        self.response_class = resp.GetServerInfoResponse
