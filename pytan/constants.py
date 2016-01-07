"""Constants for :mod:`pytan`."""
from collections import OrderedDict

CRED_DEFAULTS = {}
CRED_DEFAULTS['username'] = ''
CRED_DEFAULTS['password'] = ''
CRED_DEFAULTS['domain'] = ''
CRED_DEFAULTS['secondary'] = ''
CRED_DEFAULTS['session_id'] = ''
CRED_DEFAULTS['persistent'] = False

SESSION_DEFAULTS = {}
SESSION_DEFAULTS['host'] = ''
SESSION_DEFAULTS['port'] = 443
SESSION_DEFAULTS['protocol'] = 'https'
SESSION_DEFAULTS['port_fallback'] = 444
SESSION_DEFAULTS['session_fallback'] = True
SESSION_DEFAULTS['retry_count'] = 5
SESSION_DEFAULTS['record_all'] = False
SESSION_DEFAULTS['force_version'] = ''
SESSION_DEFAULTS['connect_secs'] = 5
SESSION_DEFAULTS['connect_secs_soap'] = 15
SESSION_DEFAULTS['response_secs'] = 15
SESSION_DEFAULTS['response_secs_soap'] = 540
SESSION_DEFAULTS['clean_xml_restricted'] = True
SESSION_DEFAULTS['clean_xml_invalid'] = True
SESSION_DEFAULTS['https_proxy'] = ''
SESSION_DEFAULTS['request_headers'] = {
    'Accept-Encoding': 'gzip',
    'User-Agent': '{title}/{version}',
}

HANDLER_DEFAULTS = {}
HANDLER_DEFAULTS['logfile_enable'] = False
HANDLER_DEFAULTS['logfile_output'] = "~/pytan.log"
HANDLER_DEFAULTS['logfile_name'] = "pytan_file"
HANDLER_DEFAULTS['logfile_handler'] = "FileHandler"
HANDLER_DEFAULTS['logfile_level'] = "NOTSET"
HANDLER_DEFAULTS['logfile_formatter'] = '%(asctime)s %(levelname)-8s [%(name)s] %(message)s'
HANDLER_DEFAULTS['logconsole_enable'] = True
HANDLER_DEFAULTS['logconsole_output'] = 'sys.stdout'
HANDLER_DEFAULTS['logconsole_handler'] = "StreamHandler"
HANDLER_DEFAULTS['logconsole_name'] = "pytan_console"
HANDLER_DEFAULTS['logconsole_level'] = "NOTSET"
HANDLER_DEFAULTS['logconsole_formatter'] = '%(levelname)-8s [%(name)s] %(message)s'
HANDLER_DEFAULTS['loglevel'] = 0
HANDLER_DEFAULTS['config_file'] = "~/.pytan_config.json"
HANDLER_DEFAULTS.update(CRED_DEFAULTS)
HANDLER_DEFAULTS.update(SESSION_DEFAULTS)


# short hand reference to python
OFF = 'NOTSET'  # python logging int: 0
DEBUG = 'DEBUG'  # python logging int: 10
INFO = 'INFO'  # python logging int: 20
WARN = 'WARNING'  # python logging int: 30
ERR = 'ERROR'  # python logging int: 40
CRIT = 'CRITICAL'  # python logging int: 50
# {0: ERR, 1: WARN, 10: INFO, 20: DEBUG}
LOGGER_LEVELS = [OFF, DEBUG, INFO, WARN, ERR, CRIT]

LOGMAP = {}
LOGMAP['pytan'] = 0
LOGMAP['pytan.handler'] = 1
LOGMAP['pytan.tanium_ng'] = 0
LOGMAP['pytan.tickle'] = 0
LOGMAP['pytan.tickle.tools'] = 0
LOGMAP['pytan.pollers.question'] = 3
LOGMAP['pytan.pollers.sse'] = 4
LOGMAP['pytan.pollers.question.progress'] = 5
LOGMAP['pytan.pollers.sse.progress'] = 5
LOGMAP['pytan.pollers.question.resolver'] = 6
LOGMAP['pytan.pollers.sse.resolver'] = 6
LOGMAP['pytan.parsers.filterobject'] = 7
LOGMAP['pytan.parsers.getobject'] = 8
LOGMAP['pytan.parsers.spec'] = 9
LOGMAP['pytan.session.help'] = 10
LOGMAP['pytan.session'] = 11
LOGMAP['pytan.session.http'] = 12
LOGMAP['pytan.session.auth'] = 13
LOGMAP['pytan.session.body'] = 14
LOGMAP['pytan.xml_clean'] = 16
LOGMAP['pytan.excelwriter'] = 0
LOGMAP['pytan.ext.requests'] = 20
LOGMAP['pytan.ext.requests.packages.urllib3'] = 21
LOGMAP['pytan.ext.requests.packages.urllib3.connectionpool'] = 22
LOGMAP['pytan.ext.requests.packages.urllib3.poolmanager'] = 23
LOGMAP['pytan.ext.requests.packages.urllib3.util.retry'] = 24

DEFAULT_LEVEL = "WARN"
"""Set all logs in LOGMAP to this level before setting them to INFO or DEBUG"""

OVERRIDE_LEVEL = 50
"""If loglevel supplied is >= to this level, then set ALL loggers (pytan or not) to DEBUG"""

DEBUG_BUMP = 20
"""Loggers in LOGMAP will log at DEBUG if loglevel is >= the loggers level + DEBUG_BUMP"""

PYTAN_KEY = "mT1er@iUa1kP9pelSW"
"""Key used for obfuscation/de-obfsucation of password when writing/reading user config"""

XMLNS = {
    'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'xsd': 'http://www.w3.org/2001/XMLSchema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'typens': 'urn:TaniumSOAP',
}
"""The namespace mappings for use in SOAP_REQUEST_BODY by Session"""

SOAP_REQUEST_BODY = (
    '''<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="{soapenv}" xmlns:xsd="{xsd}" xmlns:xsi="{xsi}">
<SOAP-ENV:Body>
  <typens:tanium_soap_request xmlns:typens="{typens}">
    <command>$command</command>
    <object_list>$object_list</object_list>
    $options
  </typens:tanium_soap_request>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
''')
"""
The XML template used for all SOAP Requests in string form
{} variables will be replaced with keys from XMLNS
$ variables will be replaced with strings from the objects during request time
"""

SOAP_CONTENT_TYPE = 'text/xml; charset=utf-8'

SESSION_OPTS = OrderedDict()
SESSION_OPTS['host'] = {
    'help': 'Hostname/ip of Tanium SOAP Server',
}
SESSION_OPTS['port'] = {
    'help': 'Port to use of Tanium SOAP Server',
}
SESSION_OPTS['port_fallback'] = {
    'help': 'Fallback port to use of Tanium SOAP Server',
}
SESSION_OPTS['https_proxy'] = {
    'help': 'Proxy to use when connecting to the Tanium SOAP Server',
}
SESSION_OPTS['retry_count'] = {
    'help': 'Number of times to retry when an HTTP error occurs',
}
SESSION_OPTS['record_all'] = {
    'help': 'Record all requests in ALL_RESPONSES',
}
SESSION_OPTS['force_version'] = {
    'help': 'Ignore the version of the Tanium server and force PyTan version as this',
}
SESSION_OPTS['connect_secs'] = {
    'help': 'Number of seconds before timing out on all non-SOAP connections',
}
SESSION_OPTS['connect_secs_soap'] = {
    'help': 'Number of seconds before timing out on all SOAP connections',
}
SESSION_OPTS['response_secs'] = {
    'help': 'Number of seconds before timing out on all non-SOAP responses',
}
SESSION_OPTS['response_secs_soap'] = {
    'help': 'Number of seconds before timing out on all SOAP responses',
}

AUTH_OPTS = OrderedDict()
AUTH_OPTS['username'] = {
    'help': 'Name of user to authenticate against Tanium with',
    'short': 'u',
}
AUTH_OPTS['password'] = {
    'help': 'Password of user to authenticate against Tanium with',
    'short': 'p',
}
AUTH_OPTS['domain'] = {
    'help': 'Domain of user to authenticate against Tanium with',
}
AUTH_OPTS['secondary'] = {
    'help': 'Secondary of user to authenticate against Tanium with',
}
AUTH_OPTS['session_id'] = {
    'help': 'session ID to authenticate against Tanium with (will be used in favor of '
    'username/password/domain/secondary if both are suppleid).',
}
AUTH_OPTS['persistent'] = {
    'help': 'Get a persistent session_id (lasts up to 1 week between uses)',
}

HANDLER_OPTS = OrderedDict()
HANDLER_OPTS['logfile_enable'] = {
    'help': 'Enable logging to file in --logfile_output',
}
HANDLER_OPTS['logfile_output'] = {
    'help': "Log file to write to if --logfile_enable true",
}
HANDLER_OPTS['logfile_level'] = {
    'help': "Only show file logs at this level or above (NOTSET logs all levels)",
    'choices': LOGGER_LEVELS,
}
HANDLER_OPTS['logfile_formatter'] = {
    'help': 'Python logging format to use for file logging',
}
HANDLER_OPTS['logconsole_enable'] = {
    'help': 'Enable logging to the console',
}
HANDLER_OPTS['logconsole_level'] = {
    'help': "Only show console logs at this level or above (NOTSET logs all levels)",
    'choices': LOGGER_LEVELS,
}
HANDLER_OPTS['logconsole_formatter'] = {
    'help': 'Python logging format to use for console logging',
}
HANDLER_OPTS['loglevel'] = {
    'help': 'Logging level to use, increase for more verbosity '
    '(0 = no logging, {} and up turns on all logging)'.format(OVERRIDE_LEVEL),
    'short': 'l',
}
HANDLER_OPTS['config_file'] = {
    'help': "PyTan User Config file to use for PyTan arguments",
}

SHELL_OPTS = OrderedDict()
SHELL_OPTS['PyTan Authentication Options'] = AUTH_OPTS
SHELL_OPTS['PyTan Session Options'] = SESSION_OPTS
SHELL_OPTS['PyTan Handler Options'] = HANDLER_OPTS
