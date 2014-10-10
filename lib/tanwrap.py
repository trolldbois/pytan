#!/usr/bin/python -i
#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Tanium Python Wrapper Class

Like saran wrap. But not.

This requires Python 2.7 and Suds.
Suds can be found at: https://fedorahosted.org/suds/

Reference for Suds: https://fedorahosted.org/suds/wiki/Documentation
Reference for Tanium's SOAP API: http://kb.tanium.com/SOAP
'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '0.1'

import os
import sys
import logging
#import inspect
#import tempfile
import socket
import time

try:
    import suds
except:
    logging.critical(
        "Suds python library not available in PYTHONPATH, please download "
        "and install from https://fedorahosted.org/suds"
    )
    raise

# static variable for how many minutes a session id will be valid
SESSION_TIMEOUT = 5

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
#toolset_dir = os.path.dirname(my_dir)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.append(x)

from console_support import *

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

# debug log format; rather verbose, used for files only unless loglevel >= 1
lfdebug = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(message)s'
)
# info log format; used for console output when loglevel = 0
lfinfo = logging.Formatter('%(levelname)-8s %(message)s')

# create a logger called tanwrap and set it's default level to DEBUG
logger = logging.getLogger("tanwrap")
logger.setLevel(logging.DEBUG)


def logging_setup(loglevel=0):
    '''setup console logging'''
    # remove any old handlers, we're going to re-setup new handlers
    [logger.removeHandler(x) for x in logger.handlers]

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
    logging.getLogger().addHandler(console_handler)

    log_level_map = {
        # see soap messages (in & out) and http headers at lvl 2
        'suds.client': 2,
        # see more details about soap messages and http headers at lvl 3
        'suds.transport': 3,
        # see digestion of the schema at lvl 4
        'suds.xsd.schema': 4,
        # see digestion WSDL at lvl 5
        'suds.wsdl': 5,
    }

    for loggername, loggerlvl in log_level_map.iteritems():
        if loglevel >= loggerlvl:
            #print 'setting %s to DEBUG' % loggername
            logging.getLogger(loggername).setLevel(logging.DEBUG)
        else:
            #print 'setting %s to INFO' % loggername
            logging.getLogger(loggername).setLevel(logging.INFO)

'''
    # setup file logging
    if logfile:
        add_file_log(logfile)


def add_file_log(logfile=None, logdir=None):
    if not logfile:
        if not logdir:
            logdir = tempfile.gettempdir()
        parent_func = inspect.stack()[1][3]
        now = get_now()
        logfilename = ('{}_{}.log').format(parent_func, now)
        logfile = os.path.join(logdir, logfilename)
    basename = os.path.basename(logfile)
    try:
        [L.removeHandler(x) for x in L.handlers if x.name is basename]
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(lfdebug)
        L.addHandler(file_handler)
        logging.info(('Logging to: {}').format(logfile))
        return logfile
    except Exception as e:
        logging.error((
            'Problem setting up file logging to {}: {}'
        ).format(logfile, e))
'''


def get_now():
    return human_time(time.localtime())


def human_time(t, format='%Y_%m_%d-%H_%M_%S-%Z'):
    return time.strftime(format, t)


def port_check(address, port, timeout=5):
    try:
        return socket.create_connection((address, port), timeout)
    except:
        return False


class TaniumWrap:

    def __init__(self, username, password, host, port="443", loglevel=0,
                 logfile=None, wsdl_uri="HOSTED", soap_location="/soap"):

        logging_setup(loglevel)

        self.soap_host = host
        self.soap_port = port
        self.soap_location = soap_location
        self.__soap_session_username = username
        self.__soap_session_password = password
        self.__soap_session_id = None
        self.__soap_session_issued = None

        self.__set_now()
        self.__env_overrides()
        self.test_tanium_port_access()
        self.__define_wsdl_uri(wsdl_uri)
        self.__define_soap_uri()
        self.get_sc()
        self.__update_sc_token()

        logger.info('we need more stuff!')

    def ask_saved_question(self, saved_question):
        sc_object1 = self.sc.factory.create('saved_question')
        sc_object1.name = saved_question

        object_list = self.sc.factory.create('object_list')
        object_list.saved_question = sc_object1

        result = self.call_sc("GetResultData", object_list)
        return result

    def call_sc(self, command, object_list):
        self.__update_sc_token()
        self.last_request_params = self.__sc_token.copy()
        self.last_request_params['object_list'] = object_list
        self.last_request_params['command'] = command
        self.last_result = self.sc.service.Request(**self.last_request_params)
        self.__check_last_result_session()
        return self.last_result

    def test_tanium_port_access(self):
        if port_check(self.soap_host, self.soap_port):
            logger.debug((
                "Port test to {}:{} successful"
            ).format(self.soap_host, self.soap_port))
        else:
            logger.error((
                "Port test to {}:{} failed"
            ).format(self.soap_host, self.soap_port))
            sys.exit(100)

    def get_sc(self):
        self.sc = suds.client.Client(
            self.wsdl_uri,
            location=self.soap_uri,
        )

    def print_sc_methods(self):
        print self.sc.__str__()

    def __env_overrides(self):
        # OS environment variable overrides
        OS_ENV_MAP = {
            'TAN_USER': 'self.__soap_session_username',
            'TAN_PASS': 'self.__soap_session_password',
            'TAN_HOST': 'self.soap_host',
            'TAN_PASS': 'self.soap_port',
            'TAN_WSDL': 'self.wsdl_uri',
        }

        for os_env_var, class_var in OS_ENV_MAP.iteritems():
            if not os_env_var in os.environ.keys():
                continue

            if not os.environ[os_env_var]:
                continue

            logger.debug((
                "Overriding {!r} with OS environment variable {!r}"
            ).format(os.environ[os_env_var], os_env_var))
            setattr(self, class_var, os.environ['TAN_USER'])

    def __set_now(self):
        self._now = get_now()

    def __define_wsdl_uri(self, wsdl_uri):
        if wsdl_uri == "HOSTED":
            self.wsdl_uri = ((
                "https://{}:{}/console/console.wsdl"
            ).format(self.soap_host, self.soap_port))
        else:
            self.wsdl_uri = wsdl_uri
        logger.debug((
            "WSDL URI: {}"
        ).format(self.wsdl_uri))

    def __define_soap_uri(self):
        self.soap_uri = ((
            "https://{}:{}{}"
        ).format(self.soap_host, self.soap_port, self.soap_location))
        logger.debug((
            "SOAP URI: {}"
        ).format(self.soap_uri))

    def __update_sc_token(self):
        if self.__session_id_valid():
            logger.debug((
                "Using session for Soap Client Token"
            ))
            self.__define_sc_token_session()
        else:
            logger.debug((
                "Using username/password for Soap Client Token"
            ))
            self.__define_sc_token_userpass()

    def __session_id_valid(self):
        if not self.__soap_session_id:
            return False
        if not self.__soap_session_issued:
            return False
        now = time.time()
        oldest = (now - (SESSION_TIMEOUT * 60))
        if self.__soap_session_issued < oldest:
            logger.debug((
                "Session ID expired - older than {} ({} minutes ago)"
            ).format(oldest, SESSION_TIMEOUT))
            self.__soap_session_id = None
            return False
        logger.debug((
            "Session ID still valid"
        ))
        return True

    def __define_sc_token_userpass(self):
        token = self.sc.factory.create('auth')
        token.username = self.__soap_session_username
        token.password = self.__soap_session_password
        self.__sc_token = {'auth': token}

    def __define_sc_token_session(self):
        self.__sc_token = {'session': self.__soap_session_id}

    def __check_last_result_session(self):
        if not hasattr(self.last_result, 'session'):
            return
        if self.__soap_session_id != self.last_result.session:
            logger.debug((
                "Updating session ID from last SOAP Response to {}"
            ).format(self.last_result.session))
            self.__soap_session_id = self.last_result.session
            self.__soap_session_issued = time.time()
        self.__update_sc_token()


if __name__ == '__main__':
    tan_user = 'JTANIUM1\Jim Olsen'
    tan_pass = 'Evinc3d!'
    tan_host = '172.16.31.128'
    loglevel = 1

    tw = TaniumWrap(tan_user, tan_pass, tan_host, loglevel=loglevel)
    sq1_result = tw.ask_saved_question('Installed Applications')
    print "session id from SOAP result:"
    print sq1_result.session
