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
import suds

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

# debug log format (rather verbose, used for files only unless debug=True)
lfdebug = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(message)s'
)
# info log format (used for console output when debug=False)
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
    return time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())


def port_check(address, port, timeout=5):
    try:
        return socket.create_connection((address, port), timeout)
    except:
        return False


class TaniumWrap:

    def __init__(self, username=None, password=None, host='localhost',
                 port="443", loglevel=0, logfile=None, wsdl_uri="HOSTED",
                 soap_location="/soap"):
        logging_setup(loglevel)
        self.soap_host = host
        self.soap_port = port
        self.soap_location = soap_location
        self._soap_session_username = username
        self._soap_session_password = password
        self._soap_session_id = None
        self._set_now()
        self._env_overrides()
        self.test_tanium_port_access()
        self._define_wsdl_uri(wsdl_uri)
        self._define_soap_uri()
        self.soap_client = self.get_soap_client()
        logger.info('we need more stuff!')

    def ask_saved_question(self, question):
        pass

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

    def get_soap_client(self):
        soap_client = suds.client.Client(
            self.wsdl_uri,
            location=self.soap_uri,
        )
        return soap_client

    def print_soap_methods(self):
        print self.soap_client.__str__()

    def _env_overrides(self):
        # OS environment variable overrides
        OS_ENV_MAP = {
            'TAN_USER': 'self._soap_session_username',
            'TAN_PASS': 'self._soap_session_password',
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

    def _set_now(self):
        self._now = get_now()

    def _define_wsdl_uri(self, wsdl_uri):
        if wsdl_uri == "HOSTED":
            self.wsdl_uri = ((
                "https://{}:{}/console/console.wsdl"
            ).format(self.soap_host, self.soap_port))
        else:
            self.wsdl_uri = wsdl_uri
        logger.debug((
            "WSDL URI: {}"
        ).format(self.wsdl_uri))

    def _define_soap_uri(self):
        self.soap_uri = ((
            "https://{}:{}{}"
        ).format(self.soap_host, self.soap_port, self.soap_location))
        logger.debug((
            "SOAP URI: {}"
        ).format(self.soap_uri))


if __name__ == '__main__':
    tan_user = 'JTANIUM1\Jim Olsen'
    tan_pass = 'Evinc3d!'
    tan_host = '172.16.31.128'
    loglevel = 3

    tw = TaniumWrap(
        username=tan_user, password=tan_pass, host=tan_host, loglevel=loglevel)
