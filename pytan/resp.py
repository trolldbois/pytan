# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging
import time
from . import utils
from .exceptions import BadResponseError
from .exceptions import OuterReturnError
from .exceptions import AuthorizationError
from .exceptions import BadRequestError
from .exceptions import InnerReturnError
from .exceptions import UnknownCommandError
from .packages import xmltodict


class Response(object):
    def __init__(self, soap_url, request, page):
        super(Response, self).__init__()
        self.XMLPLOG = logging.getLogger("pytan.response.xmlparse").debug
        self.received = time.time()

        # URL to SOAP in question
        self.soap_url = soap_url

        # request = Request object
        self.request = request

        # page = requests module object
        self.page = page

        self.outer_xml = self.get_outer_xml()
        self.outer_return = self.get_outer_return()
        self.command = self.get_command()
        self.check_auth_ok()
        self.check_command_ok()
        self.session_id = self.get_session_id()
        self.inner_return = self.get_inner_return()
        self.result = self.inner_return

    def __str__(self):
        received = self.received_human or "Not Yet Sent"
        str_tpl = "{} from: {}, len: {}, Rcvd: {}".format
        ret = str_tpl(
            self.__class__.__name__,
            self.soap_url,
            len(self.page.text),
            received,
        )
        return ret

    def get_outer_xml(self):
        """chew up the raw text from the page into a dict"""
        outer_err = "Exception while converting outer XML: {}".format
        try:
            text = self.page.text
            text = text.encode('utf-8')
            outer_xml = xmltodict.parse(
                text, postprocessor=utils.jsonprocessor)
        except Exception as e:
            raise BadResponseError(outer_err(e))
        return outer_xml

    def get_outer_return(self):
        p1_tpl = "Parsed outer return from XML:\n{}".format
        outer_err = "Exception while parsing outer XML: {}".format
        try:
            outer_envelope = self.outer_xml['soap:Envelope']
            outer_body = outer_envelope['soap:Body']
            outer_return = outer_body['t:return']
        except Exception as e:
            raise OuterReturnError(outer_err(e))
        self.XMLPLOG(p1_tpl(utils.jsonify(outer_return)))
        return outer_return

    def get_command(self):
        p1_tpl = "Parsed command from outer return: {}".format
        command = self.outer_return['command']
        self.XMLPLOG(p1_tpl(utils.jsonify(command)))
        return command

    def check_auth_ok(self):
        auth_err = "Authorization failure in {} ({})".format
        auth_ok = 'Forbidden' not in self.command
        if not auth_ok:
            raise AuthorizationError(auth_err(self, self.command))
        return auth_ok

    def check_command_ok(self):
        bad_err = "Bad Command Return in {} ({})".format
        command_ok = self.request.command == self.command
        if not command_ok:
            raise BadRequestError(
                bad_err(self, self.command.replace('\n', ''))
            )
        return command_ok

    def get_session_id(self):
        p1_tpl = "Parsed session from outer return: {}".format
        session_id = self.outer_return['session']
        self.XMLPLOG(p1_tpl(utils.jsonify(session_id)))
        return session_id

    def get_inner_return(self):
        p1_tpl = "Parsed inner return from outer return: {}".format
        xml_err = "Exception getting inner ResultXML: {}".format
        obj_err = "Exception getting inner result_object: {}".format
        unk_err = "Unknown command: {}, unable to get inner return".format

        result_xml_commands = ['GetResultData', 'GetResultInfo']
        result_obj_commands = ['GetObject', 'AddObject', 'DeleteObject']
        if self.command in result_xml_commands:
            self.XMLPLOG("Parsing ResultXML from outer return")
            try:
                inner_return = xmltodict.parse(
                    self.outer_return['ResultXML'],
                    postprocessor=utils.jsonprocessor,
                )
            except Exception as e:
                raise InnerReturnError(xml_err(e))
        elif self.command in result_obj_commands:
            self.XMLPLOG("Parsing result_object from outer return")
            try:
                if utils.is_str(self.outer_return['result_object']):
                    inner_return = eval(self.outer_return['result_object'])
                else:
                    inner_return = self.outer_return['result_object']
            except Exception as e:
                raise InnerReturnError(obj_err(e))
        else:
            raise UnknownCommandError(unk_err(self.command))

        self.XMLPLOG(p1_tpl(utils.jsonify(inner_return)))
        return inner_return

    ## SPECIFICS TO BE MOVED
    def get_result_info(self):
        obj_err = "Exception getting result info: {}".format
        try:
            result_info = self.inner_return['result_infos']['result_info']
            self.XMLPLOG(utils.jsonify(result_info))
        except Exception as e:
            raise InnerReturnError(obj_err(e))
        return result_info

    def get_sensor_hashes(self):
        obj_err = "Exception getting sensor hashes: {}".format
        try:
            result_sets = self.inner_return['result_sets']
            result_set = result_sets['result_set']
            header_list = result_set['cs']
            header_list = header_list['c']
            sensor_hashes = list(set([x['wh'] for x in header_list]))
        except Exception as e:
            raise InnerReturnError(obj_err(e))
        return sensor_hashes

    def get_sensor_objects(self):
        obj_err = "Exception getting sensor objects: {}".format
        try:
            sensor_objects = self.inner_return['sensor']
        except Exception as e:
            raise InnerReturnError(obj_err(e))
        return sensor_objects

    @property
    def received_human(self):
        return utils.human_time(self.received)


class AddQuestionJobResponse(Response):
    def __init__(self, **kwargs):
        super(AddQuestionJobResponse, self).__init__(**kwargs)
        self.result = self.get_question_id()

    def get_question_id(self):
        qret_tpl = "Question ID {!r} returned".format
        obj_err = "Exception getting question id: {}".format
        try:
            question_id = self.inner_return['question']['id']
        except Exception as e:
            raise InnerReturnError(obj_err(e))
        self.XMLPLOG(qret_tpl(question_id))
        return question_id


class GetServerInfoResponse(Response):
    def __init__(self, **kwargs):
        super(GetServerInfoResponse, self).__init__(**kwargs)
        self.result = self.get_server_info()

    def get_server_info(self):
        obj_err = "Exception getting server info: {}".format
        try:
            server_info = self.inner_return['Diagnostics']
            server_info = {k: v for j in server_info for k, v in j.iteritems()}
        except Exception as e:
            raise InnerReturnError(obj_err(e))
        return server_info


class AddParseQuestionResponse(Response):
    def __init__(self, **kwargs):
        super(AddParseQuestionResponse, self).__init__(**kwargs)
        self.result = self.get_parse_result_groups()

    def get_parse_result_groups(self):
        obj_err = "Exception getting server info: {}".format
        try:
            prgs = self.inner_return['parse_result_groups']
            prg_list = prgs['parse_result_group']
        except Exception as e:
            raise InnerReturnError(obj_err(e))
        return prg_list
