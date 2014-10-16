#!/usr/bin/python -i
#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Tanium Python Wrapper Class

Like saran wrap. But not.

This requires Python 2.7

Reference for Tanium's SOAP API: http://kb.tanium.com/SOAP
'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

# static variable for how many minutes a session id will be valid
SESSION_TIMEOUT = 5

# static variable to control whether or not SOAP Session IDs are included
# in any outputs
SHOW_SESSION_ID = False

import os
import sys
import logging
import getpass
#import inspect
#import tempfile
import socket
import time
import csv
import StringIO
import re
from datetime import datetime
from collections import defaultdict
import xml.etree.cElementTree as ET
#import xml.etree.ElementTree as ET

# ElementTree FUN!
NS_SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NS_XSD = "http://www.w3.org/2001/XMLSchema"
NS_DICT = {"xmlns:xsi": NS_XSI, "xmlns:xsd": NS_XSD}
APP_NS = {'xmlns': "urn:TaniumSOAP"}

# make it so ElementTree produces Elements with soap: prefix instead of ns0:
ET.register_namespace('soap', NS_SOAP_ENV)
for attr, uri in NS_DICT.items():
    ET.register_namespace(attr.split(":")[1], uri)

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

# for debugging support
from console_support import *
import requests

# disable warning messages about insecure HTTPS validation
requests.packages.urllib3.disable_warnings()

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

# debug log format; rather verbose, used for files only unless loglevel >= 1
lfdebug = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(message)s'
)

# info log format; used for console output when loglevel = 0
lfinfo = logging.Formatter('%(levelname)-8s %(message)s')

# create a logger called apiwrap and set it's default level to DEBUG
logger = logging.getLogger("apiwrap")
logger.setLevel(logging.DEBUG)

# create a logger called httplogger and set it's default level to DEBUG
# use httplog to send messages to this logger at the debug level
httplogger = logging.getLogger("http")
httplogger.setLevel(logging.DEBUG)
httplog = httplogger.debug

# create a logger called xmlcreatelogger and set it's default level to DEBUG
# use xmlcreatelog to send messages to this logger at the debug level
xmlcreatelogger = logging.getLogger("xmlcreate")
xmlcreatelogger.setLevel(logging.DEBUG)
xmlcreatelog = xmlcreatelogger.debug

# create a logger called xmlparselogger and set it's default level to DEBUG
# use xmlparselog to send messages to this logger at the debug level
xmlparselogger = logging.getLogger("xmlparse")
xmlparselogger.setLevel(logging.DEBUG)
xmlparselog = xmlparselogger.debug


def version_check(reqver):
    LOG_TPL = (
        "{}: {} version {}, required {}").format
    if not __version__ >= reqver:
        s = "Script and API Version mismatch!"
        logging.error(LOG_TPL(s, __file__, __version__, reqver))
        sys.exit(100)
    s = "Script and API Version match"
    logging.debug(LOG_TPL(s, __file__, __version__, reqver))


def logging_setup(loglevel=0):
    '''setup console logging'''
    # remove any old handlers, we're going to re-setup new handlers
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers
    [root_logger.removeHandler(x) for x in original_handlers]

    # add a console handler that goes to STDOUT
    console_handler = logging.StreamHandler(sys.__stdout__)
    console_handler.set_name('console')
    if loglevel == 0:
        # if loglevel is 0, set console handler to info level
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(lfinfo)
    else:
        # if loglevel is 1 or higher, set console handler to debug level
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(lfdebug)
    root_logger.addHandler(console_handler)

    log_level_map = {
        # level 1 just turns on debug logging
        # see more details about http communications at lvl 2
        'http': 2,
        # see the XML messages we create at lvl 3
        'xmlcreate': 3,
        # see the XML messages we parse at lvl 4
        'xmlparse': 4,
    }

    for loggername, loggerlvl in log_level_map.iteritems():
        if loglevel >= loggerlvl:
            #print 'setting %s to DEBUG' % loggername
            logging.getLogger(loggername).setLevel(logging.DEBUG)
        else:
            #print 'setting %s to INFO' % loggername
            logging.getLogger(loggername).setLevel(logging.INFO)


def get_now():
    return human_time(time.localtime())


def human_time(t, format='%Y_%m_%d-%H_%M_%S-%Z'):
    if type(t) in [type(float()), type(int())]:
        t = time.localtime(t)
    return time.strftime(format, t)


def datetime_diff(t=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    datetime diff of now - time
    """
    now = datetime.now()

    if type(t) in [type(int()), type(float())]:
        dtdiff = now - datetime.fromtimestamp(t)
    elif isinstance(t, datetime):
        dtdiff = now - t
    else:
        dtdiff = now - now

    #second_dtdiff = dtdiff.seconds
    #minute_dtdiff = dtdiff.seconds / 60
    #hour_dtdiff = minute_dtdiff / 60
    #day_dtdiff = dtdiff.days
    return dtdiff


def port_check(address, port, timeout=5):
    try:
        return socket.create_connection((address, port), timeout)
    except:
        return False


def prompt_username():
    print('Username: '),
    username = sys.stdin.readline()
    return username.strip()


def prompt_password():
    password = getpass.getpass(('Password: '))
    return password.strip()


def ns_urn(ns):
    '''return ns wrapped by {}'''
    return ('{{{}}}').format(ns)


def ns_prefix(elem, ns):
    '''return an element name with ns prefixed'''
    return ('{}{}').format(ns_urn(ns), elem)


def new_elem(name, value=None, ns=None, attribs=None, parent=None):
    if ns:
        name = ns_prefix(name, ns)
    if attribs is None:
        attribs = {}
    if parent is None:
        elem = ET.Element(name, **attribs)
    else:
        elem = ET.SubElement(parent, name, **attribs)
    if value:
        elem.text = value
    return elem


def indent(elem, level=0):
    '''indents an ElementTree object elem'''
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def xml_clean_ns(elem):
    '''removes all namespace qualifiers from ElementTree object elem'''
    ns_match = re.compile(r'{.*?}')

    for child_elem in elem.getiterator():
        child_elem.tag = re.sub(ns_match, '', child_elem.tag)
        for k in child_elem.attrib.keys():
            if ns_match.search(k):
                del child_elem.attrib[k]


def xml_tree(elem):
    '''returns the elem object as an ElementTree object'''
    if not ET.iselement(elem):
        elem = ET.fromstring(elem)
    return elem


def xml_pretty(elem):
    '''returns the xml for ElementTree object elem as a pretty XML
    string
    '''
    elem = xml_tree(elem)
    indent(elem)
    xml_pretty = ET.tostring(elem)
    return xml_pretty


def xml_csv(xml_rows):
    '''returns the xml for the response as a CSV string'''
    csv_io = StringIO.StringIO()
    writer = csv.writer(csv_io, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(xml_rows)
    csv_io.seek(0)
    xml_csv = csv_io.read()
    return xml_csv


def xml_excel(TODO):
    '''returns the xml for the response as an XML doc in StringIO obj'''
    # TODO
    xml_excel = StringIO.StringIO()
    return xml_excel


def build_dict_from_xml(elem):
    '''converts an ElementTree object elem to a python dict'''
    elem = xml_tree(elem)

    d = {elem.tag: {} if elem.attrib else None}
    children = list(elem)
    if children:
        dd = defaultdict(list)
        for dc in map(build_dict_from_xml, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {
            elem.tag: {
                k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()
            }
        }
    if elem.attrib:
        d[elem.tag].update(('@' + k, v) for k, v in elem.attrib.iteritems())
    if elem.text:
        text = elem.text.strip()
        if children or elem.attrib:
            if text:
                d[elem.tag]['#text'] = text
        else:
            d[elem.tag] = text
    return d


def build_xml_from_dict(parentelem, xml_dict):
    for objname, objvalue in xml_dict.iteritems():
        if type(objvalue) == type(dict()):
            objelem = new_elem(objname, parent=parentelem)
            build_xml_from_dict(objelem, objvalue)
        # TODO: add support for lists
        else:
            new_elem(objname, objvalue, parent=parentelem)


class SoapRequest(object):
    def __init__(self, command, auth_dict, objects_dict):
        super(SoapRequest, self).__init__()
        self.command = command
        self.auth_dict = auth_dict
        self.objects_dict = objects_dict
        self.xml_raw = ''

    def __str__(self):
        sent = self.sent_human or "Not Yet Sent"
        auth = self.auth_dict.keys()[0]
        if auth == 'auth':
            auth = 'user/pass'
        STR_TPL = (
            "{} for {!r} of {!r}, Sent: {}, Auth: {}"
        ).format
        ret = STR_TPL(
            self.__class__.__name__,
            self.command,
            self.objects_dict,
            sent,
            auth,
        )
        return ret

    def build_xml(self):
        '''builds the xml envelope needed for a SOAP request

        self.command should be a valid SOAP command, i.e. the following:
          GetObject
          GetResultData

        self.auth_dict should be one of the following:
          # session id based auth
          {'session': '$SESSION_ID'}
          # username/password based auth
          {'auth': {'username': '$USERNAME', 'password': '$PASSWORD'}}

        self.objects_dict should be something like one of the following:
          # get a single sensor
          {'sensor': {'name': 'Computer Name'}
          # get all sensors
          {'sensor': {'name': ''}}
        '''
        DBG_TPL = ('Created XML:\n{}').format
        xmltree = new_elem('Envelope', ns=NS_SOAP_ENV, attribs=NS_DICT)
        body_elem = new_elem('Body', ns=NS_SOAP_ENV, parent=xmltree)
        soap_req_elem = new_elem(
            'tanium_soap_request', parent=body_elem, attribs=APP_NS,
        )
        build_xml_from_dict(soap_req_elem, self.auth_dict)
        new_elem('command', self.command, parent=soap_req_elem)
        objlist_elem = new_elem('object_list', parent=soap_req_elem)
        build_xml_from_dict(objlist_elem, self.objects_dict)
        new_elem('ID', '0', parent=soap_req_elem)
        new_elem('ContextID', '0', parent=soap_req_elem)
        self.xmltree = xmltree
        self.xml_raw = xml_pretty(xmltree)
        xmlcreatelog(DBG_TPL(self.xml_raw))
        return self.xml_raw

    @property
    def sent_human(self):
        '''returns the time the request was sent in human friendly format'''
        if not hasattr(self, '_sent'):
            return None
        return human_time(self._sent)

    @property
    def sent(self):
        '''returns the time the request was sent'''
        if not hasattr(self, '_sent'):
            return None
        return self._sent

    @sent.setter
    def sent(self, value):
        '''sets the time the request was sent'''
        self._sent = value


class AskSavedQuestionRequest(SoapRequest):
    def __init__(self, saved_question, auth_dict):
        self.command = 'GetResultData'
        self.auth_dict = auth_dict
        self.objects_dict = {'saved_question': {'name': saved_question}}
        self.xml_raw = ''

    def xml_rows(self, xml_dict):
        '''returns the xml for the response as a list of lists, one
        for each row, headers in the first row
        '''
        result_sets = xml_dict.get('result_sets', {})
        result_set = result_sets.get('result_set', {})

        # get headers from xml response result_set
        cs = result_set.get('cs', {})
        xml_headers = cs.get('c', [])

        # extract the name for the header of each column
        headers = [x.get('dn', None) for x in xml_headers]

        # get rows from xml response result_set
        rs = result_set.get('rs', {})
        r = rs.get('r', [])
        xml_rows = [x.get('c', []) for x in r]

        # extract the row values for each column
        rows = [[y.get('v', None) for y in x] for x in xml_rows]

        # prepend headers to rows
        rows.insert(0, headers)
        return rows


class SoapResponse(object):

    def __init__(self, soap_url, request, http_response):
        super(SoapResponse, self).__init__()
        self.received = time.time()

        # URL to SOAP in question
        self.soap_url = soap_url

        # request = SoapRequest object
        self.request = request

        # http_response = requests module object
        self.http_response = http_response

        # extract some things from the requests object
        self.status_code = self.http_response.status_code
        self.text = self.http_response.text
        self.__parse_text(self.text)

    def __str__(self):
        received = self.received_human or "Not Yet Sent"
        STR_TPL = (
            "SoapResponse from {}, code {} on: {}, Request: {}"
        ).format
        ret = STR_TPL(self.soap_url, self.status_code, received, self.request)
        return ret

    def __parse_text(self, text):
        '''chew up the raw text from the http_response into XML'''
        DBG2_TPL = ('Parsed XML:\n{}').format
        CMD_TPL = ("response command: {}").format
        self.xmltree = xml_tree(text)
        xml_clean_ns(self.xmltree)
        self.xmldict = build_dict_from_xml(self.xmltree)
        self.xml_raw = xml_pretty(self.xmltree)
        xmlparselog(DBG2_TPL(self.xml_raw))

        env_elem = self.xmldict.get('Envelope', {})
        body_elem = env_elem.get('Body', {})
        self.returndict = body_elem.get('return', {})
        self.command = self.returndict.get('command', None)
        self.session_id = self.returndict.get('session', None)
        self.object_list = self.returndict.get('object_list', None)

        logger.debug(CMD_TPL(self.command))
        self.authok = True
        if 'Forbidden' in self.command:
            self.authok = False

        self.reqok = True
        if 'Bad Request' in self.command:
            self.reqok = False

        if not self.authok or not self.reqok or not self.command:
            return

        self.__parse_inner_results()

    def __parse_inner_results(self):
        '''look for results embedded in the returndict of the XML response'''

        #ResultXML is used for returns from command=GetResultData
        DBG3_TPL = ('Inner Result XML:\n{}').format
        self.ResultXML_dict = {}
        ResultXML = self.returndict.get('ResultXML', '')
        if ResultXML:
            ResultXML_tree = xml_tree(ResultXML)
            self.ResultXML_dict = build_dict_from_xml(ResultXML_tree)
            ResultXML_raw = xml_pretty(ResultXML_tree)
            xmlparselog(DBG3_TPL(ResultXML_raw))

        #result_object is used for returns from command=GetObject
        self.result_object = self.returndict.get('result_object', {})

    @property
    def received_human(self):
        '''returns the time the response was received in human friendly format
        '''
        return human_time(self.received)


class SoapAuth(object):
    def __init__(self, username, password):
        super(SoapAuth, self).__init__()
        self._username = username
        self._password = password
        self._session_id = None
        self._token = {}
        self.SESSION_TIMEOUT = SESSION_TIMEOUT
        self.SHOW_SESSION_ID = SHOW_SESSION_ID
        self.update_token()

    def __str__(self):
        STR_TPL = (
            "SoapAuth {}"
        ).format
        ret = STR_TPL(self.token_type_details)
        return ret

    def update_token(self):
        '''updates self.token with either session ID or user/pass auth'''
        UPD_TPL = ("SOAP Token updated to: {}").format
        if self.session_id_valid:
            token = self.token_session_id
        else:
            token = self.token_userpass
        if self._token != token:
            self._token = token
            logger.debug(UPD_TPL(self.token_type_details))

    def auth_fallback(self):
        '''removes the session ID from the token, and reverts back to
        user and password auth'''
        self.session_id = None
        self.update_token()

    def session_id_text(self, session_id):
        '''returns session ID if SHOW_SESSION_ID = True'''
        if self.SHOW_SESSION_ID:
            id_text = session_id
        else:
            id_text = "..."
        return id_text

    @property
    def token(self):
        '''returns the token'''
        if not hasattr(self, '_token'):
            return None
        return self._token

    @token.setter
    def token(self, value):
        '''sets the token'''
        self._token = value

    @property
    def session_id(self):
        '''returns the session_id'''
        if not hasattr(self, '_session_id'):
            return None
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        '''sets the session_id'''
        if self._session_id != value:
            self._session_id = value
            self._session_id_issued = time.time()
            self.update_token()

        if value is None:
            self._session_id_issued = None

    @property
    def session_id_issued(self):
        '''returns the session_id_issued'''
        if not hasattr(self, '_session_id_issued'):
            return None
        return self._session_id_issued

    @session_id_issued.setter
    def session_id_issued(self, value):
        '''sets the session_id_issued'''
        self._session_id_issued = value

    @property
    def session_id_valid(self):
        '''returns True if self.session_id is not empty and not yet expired,
        False otherwise - expiration is validated by looking at
        self.session_id_issued
        '''
        SESSION_TPL = (
            "Session ID {}: issued {}, minutes ago: {}, timeout: {} minutes"
        ).format

        if not self.session_id:
            return False

        dtdiff = datetime_diff(self.session_id_issued)
        minutes_dtdiff = dtdiff.seconds / 60
        hf_issued = human_time(self.session_id_issued)

        if self.SESSION_TIMEOUT < minutes_dtdiff:
            logger.debug(SESSION_TPL(
                'EXPIRED', hf_issued, minutes_dtdiff, self.SESSION_TIMEOUT,
            ))
            self._session_id = None
            self._session_id_issued = None
            return False

        logger.debug(SESSION_TPL(
            'VALID', hf_issued, minutes_dtdiff, self.SESSION_TIMEOUT,
        ))
        return True

    @property
    def via_session_id(self):
        '''returns True if self.token dict has 'session' in it'''
        return 'session' in self._token.keys()

    @property
    def via_userpass(self):
        '''returns True if token dict has 'auth' in it'''
        return 'auth' in self._token.keys()

    @property
    def token_type_details(self):
        '''returns token type and details in text form'''
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
        '''returns a dictionary that has 'auth': SOAP element: auth,
        $username, $password
        '''
        token = {
            'auth': {'username': self._username, 'password': self._password}
        }
        return token

    @property
    def token_session_id(self):
        '''returns a dictionary that has 'session': '$session_id' '''
        token = {'session': self.session_id}
        return token


class FailedPage(object):
    '''simple object to replicate requests-like object for exceptions'''
    # TODO subclass requests response object??
    def __init__(self, text):
        self.text = text
        self.status_code = -1


class SoapWrap:
    def __init__(self, username, password, host, port="443", protocol='https',
                 soap_path="/soap", loglevel=0, logfile=None,):

        logging_setup(loglevel)

        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__soap_path = soap_path

        self.__username = username
        self.__password = password

        self.last_request = None
        self.last_response = None
        self.all_responses = []

        self.__env_overrides()
        self.__app_ok()
        self.auth = SoapAuth(self.__username, self.__password)

    def __str__(self):
        STR_TPL = (
            "SoapWrap to {}, Healthy: {}"
        ).format
        ret = STR_TPL(self.soap_url, self.app_ok)
        return ret

    def __env_overrides(self):
        '''looks for OS environment variables and overrides the corresponding
        attribute if they exist'''
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

            logger.debug(OR_TPL(os.environ[os_env_var], os_env_var))
            setattr(self, class_var, os.environ[os_env_var])

    def __test_port(self):
        '''validates that the SOAP port on the SOAP host can be reached'''
        CHK_TPL = ("Port test to {}:{} {}").format
        if port_check(self.__host, self.__port):
            return True
        else:
            logger.error(CHK_TPL(self.__host, self.__port, "FAILED"))
            return False

    def __test_page(self):
        '''validates that the HTTP server is returning a valid response,
        will set self.app_version if so
        '''
        CHK_TPL = ("HTTP test to {} {} {}").format
        ER1_TPL = ("Returned Code: {}, Returned Page:\n{}").format
        page = self.http_get(self.app_url)
        page_code = getattr(page, 'status_code', None)
        page_text = getattr(page, 'text', None)
        if not self.__page_ok(page):
            ERROR = ER1_TPL(page_code, page_text)
            logging.error(CHK_TPL(self.app_url, "FAILED", ERROR))
            return False
        self.app_version = self.__extract_version(page)
        return True

    def __extract_version(self, page):
        '''extracts the serverVersion from the apps home page HTML'''
        ER2_TPL = ("Version info not found in applications home page").format
        version_regex = re.compile(r"flashvars.serverVersion.*'(.*)';")
        version_search = version_regex.search(page.text)
        if not version_search:
            logging.warn(ER2_TPL())
            return "Unknown"
        if len(version_search.groups()) != 1:
            logging.warn(ER2_TPL())
            return "Unknown"
        else:
            return version_search.groups()[0]

    def __page_ok(self, page):
        '''return True if the page object is not None and has a status code
        of 200
        '''
        valid_status = [200]
        if not page:
            return False
        if page.status_code not in valid_status:
            return False
        return True

    def __app_ok(self):
        '''runs test_port and test_page'''
        OK_TPL = ("Application at {} is healthy, version: {}").format
        self.app_ok = True
        if not self.__test_port():
            self.app_ok = False
            return self.app_ok

        if not self.__test_page():
            self.app_ok = False
            return self.app_ok
        logger.debug(OK_TPL(self.soap_url, self.app_version))
        return self.app_ok

    def __call_api(self):
        '''makes a call to the SOAP API, returns a SoapResponse object,
        expects a SoapRequest object to exist at self.request
        '''
        AUTH_TPL = (
            'Authorization {} for last request: {}').format
        BAD_TPL = (
            'Bad SOAP request for last request: {}').format

        self.last_response = None

        if not self.app_ok:
            return self.last_response

        # get the SOAP response and store it in self.response
        self.__send_request()

        # if bad request, log it and return response
        if not self.last_response.reqok:
            logger.error(BAD_TPL(self.last_request))
            return self.last_response

        # if auth failed and we are using a session ID, fallback to user/pass
        # and retry the request
        if not self.last_response.authok and self.auth.via_session_id:
            logger.warn(
                "Last request failed due to expired/invalid session ID, "
                "retrying request with username/password"
            )
            self.auth.auth_fallback()
            self.__send_request()

        # if auth is STILL failed, even if request was re-issued,
        # log an auth failure
        if not self.last_response.authok:
            logger.error(AUTH_TPL('FAILED', self.last_request))
        else:
            logger.debug(AUTH_TPL('SUCCESS', self.last_request))

        return self.last_response

    def __send_request(self):
        '''sends the request to the SOAP API'''
        # TODO: Figure out request sent time for multiple requests
        # TODO: ADD LOGIC FOR WAITING FOR FULL RESULT SET

        SEND_TPL = ("Sending {}, SOAP URL: {}").format
        RECV_TPL = ("Received {}, SOAP URL: {}").format

        # set token to user/pass or session ID accordingly
        self.auth.update_token()

        logger.debug(SEND_TPL(self.last_request, self.soap_url))

        # update last_requests auth_dict with current token
        self.last_request.auth_dict = self.auth.token

        # build the xml request for the last request
        request_xml = self.last_request.build_xml()

        # set sent time on last request
        self.last_request.sent = time.time()

        # send the request XML as a SOAP post
        http_response = self.soap_post(request_xml)

        # store the response in a SoapResponse object
        self.last_response = SoapResponse(
            soap_url=self.soap_url,
            request=self.last_request,
            http_response=http_response,
        )

        logger.debug(RECV_TPL(self.last_response, self.soap_url))

        # update auth token with last reponses session_id
        self.auth.session_id = self.last_response.session_id

        # append this response to all responses
        self.all_responses.append(self.last_response)

    @property
    def soap_url(self):
        '''returns the SOAP URL'''
        SOAP_TPL = ("{}{}").format
        self._soap_url = SOAP_TPL(self.app_url, self.__soap_path)
        return self._soap_url

    @property
    def app_url(self):
        '''returns the application URL'''
        APP_TPL = ("{}://{}:{}").format
        self._app_url = APP_TPL(self.__protocol, self.__host, self.__port)
        return self._app_url

    def ask_saved_question(self, saved_question):
        '''sends a saved question Request and returns a SoapResponse object'''
        request_args = {
            'auth_dict': self.auth.token,
            'saved_question': saved_question,
        }

        self.last_request = AskSavedQuestionRequest(**request_args)

        self.__call_api()
        return self.last_response

    def get_sensor(self, sensor):
        '''sends a get all sensors request and returns a SoapResponse object'''
        # TODO CONVERT TO NEW OBJECT STYLE
        command = 'GetObject'
        objects_dict = {'sensor': {'name': sensor}}
        request_args = {
            'command': command,
            'auth_dict': self.auth.token,
            'objects_dict': objects_dict,
        }

        self.last_request = SoapRequest(**request_args)
        self.__call_api()
        return self.last_response

    def get_all_sensors(self):
        '''sends a get all sensors request and returns a SoapResponse object'''
        # TODO CONVERT TO NEW OBJECT STYLE
        command = 'GetObject'
        objects_dict = {'sensor': {'name': ''}}
        request_args = {
            'command': command,
            'auth_dict': self.auth.token,
            'objects_dict': objects_dict,
        }

        self.last_request = SoapRequest(**request_args)
        self.__call_api()
        return self.last_response

    def ask_question(self, question):
        '''sends a question Request and returns a SoapResponse object'''
        # TODO
        pass

    def deploy_package(self, question):
        '''sends a deploy package Request and returns a SoapResponse object'''
        # TODO
        pass

    def deploy_action(self, question):
        '''sends a deploy action Request and returns a SoapResponse object'''
        # TODO
        pass

    def http_get(self, url, headers={}):
        '''perform an HTTP get using the requests module - this is
        so we always bypass SSL verification, and wrap exceptions into a
        requests-like object
        '''
        ER1_TPL = ("SSL Error in HTTP GET to {!r}: {}").format
        try:
            ret = requests.get(url, verify=False, headers=headers)
        except requests.exceptions.SSLError as e:
            ret = FailedPage(ER1_TPL(url, e))
        return ret

    def http_post(self, url, data, headers={}):
        '''perform an HTTP post using the requests module - this is
        so we always bypass SSL verification, and wrap exceptions into a
        requests-like object
        '''
        ER1_TPL = ("SSL Error in HTTP POST to {!r}: {}").format
        try:
            ret = requests.post(url, data=data, verify=False, headers=headers)
        except requests.exceptions.SSLError as e:
            ret = FailedPage(ER1_TPL(url, e))
        return ret

    def soap_post(self, data, url=None):
        '''uses http_post to perform a SOAPAction call to url with data'''
        DBG1_TPL = ('Received SOAP Response {}:\n{}').format
        if not url:
            url = self.soap_url
        headers = {'SOAPAction': '""'}
        ret = self.http_post(url=url, data=data, headers=headers)
        httplog(DBG1_TPL(ret.status_code, ret.text))
        return ret


if __name__ == '__main__':
    user = 'JTANIUM1\Jim Olsen'
    password = 'Evinc3d!'
    host = '172.16.31.128'
    port = '443'

    badsslhost = '127.0.0.1'
    badsslport = 4443
    non_host = '172.16.31.129'

    loglevel = 1
    '''
    from threaded_http import threaded_http
    threaded_http(port=4443)

    print ('### TEST: bad https host: {}:{}').format(badsslhost, badsslport)
    badssl = SoapWrap(
        user,
        password,
        badsslhost,
        port=badsslport,
        protocol='https',
        loglevel=loglevel,
    )

    print ('### TEST: bad http host: {}:{}').format(badsslhost, badsslport)
    badssl = SoapWrap(
        user,
        password,
        badsslhost,
        port=badsslport,
        protocol='http',
        loglevel=loglevel,
    )

    print ('### TEST: non-existant host: {}:{}').format(non_host, port)
    test_non_host = SoapWrap(
        user,
        password,
        non_host,
        port=port,
        protocol='https',
        loglevel=loglevel,
    )
    '''
    print ('### TEST: good host: {}:{}').format(host, port)
    sw = SoapWrap(
        user,
        password,
        host,
        port=port,
        protocol='https',
        loglevel=loglevel,
    )

    result1 = sw.ask_saved_question('Installed Applications')
    print xml_csv(sw.last_request.xml_rows(result1.ResultXML_dict))
    #sq2_result = sw.list_sensors()
