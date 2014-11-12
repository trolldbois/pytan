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
# from .reports import Reporter
from . import req
from . import api


class Handler(object):
    last_response = None
    last_request = None
    all_responses = []
    app_version = 'Unknown'

    '''
    Calls that actually return something:
    ActionList
    '''
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

        self.mylog = logging.getLogger("pytan")
        self.DLOG = self.mylog.debug
        self.ILOG = self.mylog.info
        self.WLOG = self.mylog.warn
        self.ELOG = self.mylog.error
        self.CLOG = self.mylog.critical

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
        # self.server_info = self.get_server_info()
        self.session = api.Session(self.__host, self.__port)
        self.session.authenticate(self.__username, self.__password)

    def __str__(self):
        str_tpl = "Handler for {}, Version: {}".format
        ret = str_tpl(self.soap_url, self.version_info)
        return ret

    @property
    def version_info(self):
        ver = 'Unknown'
        return ver

    def test_app_port(self):
        """validates that the SOAP port on the SOAP host can be reached"""
        chk_tpl = "Port test to {}:{} {}".format
        if utils.port_check(self.__host, self.__port):
            self.DLOG(chk_tpl(self.__host, self.__port, "SUCCESS"))
        else:
            raise AppError(chk_tpl(self.__host, self.__port, "FAILURE"))

    def ask_manual_question(self, sensors, question_filters=None,
                            question_options=None):
        '''
        examples for sensors input:
        $sensorname[$params],$filter
        ='Computer Name'
        ='name:Computer Name'
        ='id:202'
        ="Folder Name Search with RegEx Match[Program Files,.*,No,No]
        ="Folder Name Search with RegEx Match[]
        ="Folder Name Search with RegEx Match
        =["Folder Name Search with RegEx Match[Program Files,.*,No,No]",
        "Computer Name"]
        ="Operating System, contains Windows"
        ="Folder Name Search with RegEx Match[Program Files,.*,No,No], is .*"
        '''
        request = req.AskManualQuestionRequest(
            handler=self,
            sensors=sensors,
            question_filters=question_filters,
            question_options=question_options,
        )
        response = request.call_api()
        return response

        # orig_response = self.call_api(orig_request)
        # question_id = orig_response.get_question_id()
        # response = self.get_question_results(question_id)
        # response.request = orig_response.request
        # response.sensors = sensor_objects

    def ask_parsed_question(self, query, picker=None):
        request = req.AskParsedQuestionRequest(
            handler=self, query=query, picker=picker,
        )
        response = request.call_api()
        return response

    def add_parse_question_job(self, query):
        """sends a parse question Request and returns the response
        """
        request = req.AddParseQuestionRequest(handler=self, query=query)
        response = request.call_api()
        return response

    def add_parse_result_group_job(self, query):
        request = req.AddParseResultGroupRequest(handler=self, query=query)
        response = request.call_api()
        return response

    def ask_saved_question(self, query):
        """sends a saved question Request and returns the response
        """
        request = req.AskSavedQuestionRequest(handler=self, query=query)
        response = request.call_api()
        return response

    def get_question_results(self, query):
        """sends a get question request and returns a SoapResponse object
        can only ask for questions by ID
        """
        request = req.QuestionResultsRequest(handler=self, query=query)
        response = request.call_api()
        return response

    def gather_sensors_from_response(self, response):
        sensor_hashes = response.get_sensor_hashes()
        sensor_hashes = [
            'hash:%s' % x for x in sensor_hashes if str(x) != '0'
        ]
        sensor_objects = []
        if sensor_hashes:
            response = self.get_sensor_object(sensor_hashes)
            sensor_objects = response.get_sensor_objects()
        return sensor_objects

    def get_object(self, objtype, query):
        """sends a get saved question request and returns a SoapResponse
        object
        """
        request = req.GetObjectRequest(
            handler=self,
            objtype='saved_question',
            query=query,
        )
        response = request.call_api()
        return response

    def get_server_info(self):
        """sends a get server_info and returns a SoapResponse object
        """
        request = req.GetServerInfoRequest(
            handler=self,
        )
        response = request.call_api()
        server_info = response.get_server_info()
        return server_info
