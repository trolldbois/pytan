"""Constants for :mod:`pytan`."""
from collections import OrderedDict

ARGS_ORDER = ['cmdline_args', 'osenvironment_args', 'configfile_args', 'default_args']

CRED_DEFAULTS = {
    'username': '',
    'password': '',
    'domain': '',
    'secondary': '',
    'session_id': '',
    'persistent': False,
}

SESSION_DEFAULTS = {
    'host': '',
    'port': 443,
    'protocol': 'https',
    'port_fallback': 444,
    'session_fallback': True,
    'retry_count': 5,
    'record_all': False,
    'force_version': '',
    'connect_secs': 5,
    'connect_secs_soap': 15,
    'response_secs': 15,
    'response_secs_soap': 540,
    'clean_xml_restricted': True,
    'clean_xml_invalid': True,
    'https_proxy': '',
    'request_headers': {'Accept-Encoding': 'gzip', 'User-Agent': '{title}/{version}'},
}

HANDLER_DEFAULTS = {
    'logfile_enable': False,
    'logfile_output': "~/pytan.log",
    'logfile_name': "pytan_file",
    'logfile_handler': "FileHandler",
    'logfile_level': "NOTSET",
    'logfile_formatter': '%(asctime)s %(levelname)-8s [%(name)s] %(message)s',
    'logconsole_enable': True,
    'logconsole_output': 'sys.stdout',
    'logconsole_handler': "StreamHandler",
    'logconsole_name': "pytan_console",
    'logconsole_level': "NOTSET",
    'logconsole_formatter': '%(levelname)-8s [%(name)s] %(message)s',
    'loglevel': 0,
    'config_file': "~/.pytan_config.json",
}

HANDLER_DEFAULTS.update(CRED_DEFAULTS)
HANDLER_DEFAULTS.update(SESSION_DEFAULTS)

# short hand reference to python logging levels
DEBUG = 'DEBUG'  # python logging int: 10
INFO = 'INFO'  # python logging int: 20
WARNING = 'WARNING'  # python logging int: 30
ERROR = 'ERROR'  # python logging int: 40
CRITICAL = 'CRITICAL'  # python logging int: 50

LOGGER_LEVELS = [DEBUG, INFO, WARNING, ERROR, CRITICAL]

PYTAN_BASE_LOGS = {0: ERROR, 1: WARNING, 5: INFO, 15: DEBUG}
AUTH_LOGS = {0: ERROR, 1: WARNING, 6: INFO, 16: DEBUG}
BODY_LOGS = {0: ERROR, 1: WARNING, 7: INFO, 30: DEBUG}
CONNECTION_LOGS = {0: ERROR, 1: WARNING, 8: INFO, 25: DEBUG}
HANDLER_LOGS = {0: ERROR, 1: WARNING, 5: INFO, 6: DEBUG}
PARSER_LOGS = {0: ERROR, 1: WARNING, 7: INFO, 17: DEBUG}
PROGRESS_LOGS = {0: ERROR, 1: WARNING, 5: INFO, 16: DEBUG}
RESOLVER_LOGS = {0: ERROR, 1: WARNING, 10: INFO, 30: DEBUG}
TICKLE_LOGS = {0: ERROR, 1: WARNING, 25: INFO, 40: DEBUG}
BUILDER_LOGS = {0: ERROR, 1: WARNING, 20: INFO, 35: DEBUG}
ERRORS_ONLY = {0: ERROR}
EVERYTHING = {0: DEBUG}

LOGMAP = {
    'pytan': PYTAN_BASE_LOGS,
    'pytan.excelwriter': TICKLE_LOGS,
    'pytan.ext.requests': CONNECTION_LOGS,
    'pytan.ext.requests.packages.urllib3': CONNECTION_LOGS,
    'pytan.ext.requests.packages.urllib3.connectionpool': CONNECTION_LOGS,
    'pytan.ext.requests.packages.urllib3.poolmanager': CONNECTION_LOGS,
    'pytan.ext.requests.packages.urllib3.util.retry': CONNECTION_LOGS,
    'pytan.handler': HANDLER_LOGS,
    'pytan.handler_args': HANDLER_LOGS,
    'pytan.handler_logs': HANDLER_LOGS,
    'pytan.parsers.coerce': PARSER_LOGS,  # PARSER_LOGS
    'pytan.parsers.specs': PARSER_LOGS,  # PARSER_LOGS
    'pytan.parsers.tokens': PARSER_LOGS,  # PARSER_LOGS
    'pytan.pollers.question': PYTAN_BASE_LOGS,
    'pytan.pollers.question.progress': PROGRESS_LOGS,
    'pytan.pollers.question.resolver': RESOLVER_LOGS,
    'pytan.pollers.sse': PYTAN_BASE_LOGS,
    'pytan.pollers.sse.progress': PROGRESS_LOGS,
    'pytan.pollers.sse.resolver': RESOLVER_LOGS,
    'pytan.session': HANDLER_LOGS,
    'pytan.session.auth': AUTH_LOGS,
    'pytan.session.body': BODY_LOGS,
    'pytan.session.help': CONNECTION_LOGS,
    'pytan.session.http': CONNECTION_LOGS,
    'pytan.store': PYTAN_BASE_LOGS,
    'pytan.store.credstore': AUTH_LOGS,
    'pytan.tanium_ng': TICKLE_LOGS,
    'pytan.tickle': TICKLE_LOGS,
    'pytan.tickle.deserialize': TICKLE_LOGS,
    'pytan.tickle.serialize': TICKLE_LOGS,
    'pytan.tickle.tools': TICKLE_LOGS,  # TICKLE_LOGS,
    'pytan.builders': BUILDER_LOGS,
    'pytan.builders.filters': BUILDER_LOGS,
    'pytan.builders.groups': BUILDER_LOGS,
    'pytan.builders.params': BUILDER_LOGS,
    'pytan.builders.questions': BUILDER_LOGS,
    'pytan.builders.selects': BUILDER_LOGS,
    'pytan.xml_clean': BODY_LOGS,
}

OVERRIDE_LEVEL = 50
"""If loglevel supplied is >= to this level, then set ALL loggers (pytan or not) to DEBUG"""

PYTAN_KEY = "mT1er@iUa1kP9pelSW"
"""Key used for obfuscation/de-obfsucation of password when writing/reading user config"""

XMLNS = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'xsd': 'http://www.w3.org/2001/XMLSchema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    't': 'urn:TaniumSOAP',
    'encodingStyle': 'http://schemas.xmlsoap.org/soap/encoding/',
}
"""The XML namespace mappings for all SOAP XML bodies"""

SOAP_REQUEST_BODY = (
    '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="{soap}" xmlns:xsd="{xsd}" soap:encodingStyle="{encodingStyle}">
  <soap:Body xmlns:t="{t}" xmlns:xsi="{xsi}">
    <t:tanium_soap_request>
      <command>$command</command>
      <object_list>$object_list</object_list>
      $options
    </t:tanium_soap_request>
  </soap:Body>
</soap:Envelope>
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

SUPER_VERBOSE = False
