"""Constants for :mod:`pytan`."""

import sys

HANDLER_DEFAULTS = {
    'logfile_enable': False,
    'logfile_output': "~/pytan.log",
    'logfile_name': "pytan_file",
    'logfile_handler': "FileHandler",
    'logfile_level': "NOTSET",
    'logfile_formatter': '%(asctime)s %(levelname)-8s [%(name)s] %(message)s',
    'logconsole_enable': True,
    'logconsole_output': sys.stdout,
    'logconsole_handler': "StreamHandler",
    'logconsole_name': "pytan_console",
    'logconsole_level': "NOTSET",
    'logconsole_formatter': '%(levelname)-8s [%(name)s] %(message)s',
    'loglevel': 0,
    'loggmt': True,
    'username': '',
    'password': '',
    'domain': '',
    'secondary': '',
    'session_id': '',
    'host': '',
    'port': 443,
    'config_file': "~/.pytan_config.json",
}

LOGMAP = {
    'pytan': 0,
    # 'pytan.session.stats': 0,
    'pytan.handler': 2,
    'pytan.tanium_ng': 0,
    'pytan.tickle': 0,
    # 'pytan.pollers.action': 3,
    'pytan.pollers.question': 3,
    'pytan.pollers.sse': 4,
    # 'pytan.pollers.action.progress': 5,
    'pytan.pollers.question.progress': 5,
    'pytan.pollers.sse.progress': 5,
    # 'pytan.pollers.action.resolver': 6,
    'pytan.pollers.question.resolver': 6,
    'pytan.pollers.sse.resolver': 6,
    'pytan.parsers.filterobject': 7,
    'pytan.parsers.getobject': 8,
    'pytan.parsers.spec': 9,
    'pytan.session.help': 10,
    'pytan.session': 11,
    'pytan.session.http': 12,
    'pytan.session.auth': 13,
    'pytan.session.body': 14,
    'pytan.xml_clean': 16,
    'pytan.requests': 20,
    'pytan.requests.packages.urllib3': 21,
    'pytan.requests.packages.urllib3.connectionpool': 22,
    'pytan.requests.packages.urllib3.poolmanager': 23,
    'pytan.requests.packages.urllib3.util.retry': 24,
}

DEFAULT_LEVEL = "WARN"
"""Set all logs in LOGMAP to this level before setting them to INFO or DEBUG"""

OVERRIDE_LEVEL = 50
"""If loglevel supplied is >= to this level, then set ALL loggers (pytan or not) to DEBUG"""

DEBUG_BUMP = 20
"""Loggers in LOGMAP will log at DEBUG if loglevel is >= the loggers level + DEBUG_BUMP"""

PYTAN_KEY = "mT1er@iUa1kP9pelSW"
"""Key used for obfuscation/de-obfsucation of password when writing/reading user config"""

AUTH_CONNECT = 5
"""number of seconds before timing out for a connection while authenticating"""

AUTH_RESPONSE = 15
"""number of seconds before timing out for a response while authenticating"""

INFO_CONNECT = 5
"""number of seconds before timing out for a connection while getting server info"""

INFO_RESPONSE = 15
"""number of seconds before timing out for a response while getting server info"""

SOAP_CONNECT = 15
"""number of seconds before timing out for a connection while sending a SOAP Request"""

SOAP_RESPONSE = 540
"""number of seconds before timing out for a response while sending a SOAP request"""

XMLNS = {
    'SOAP-ENV': 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"',
    'xsd': 'xmlns:xsd="http://www.w3.org/2001/XMLSchema"',
    'xsi': 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
    'typens': 'xmlns:typens="urn:TaniumSOAP"',
}
"""The namespace mappings for use in SOAP_REQUEST_BODY by Session"""

SOAP_REQUEST_BODY = (
    '<SOAP-ENV:Envelope {SOAP-ENV} {xsd} {xsi}>\n'
    '<SOAP-ENV:Body>\n'
    '  <typens:tanium_soap_request {typens}>\n'
    '    <command>$command</command>\n'
    '    <object_list>$object_list</object_list>\n'
    '    $options\n'
    '  </typens:tanium_soap_request>\n'
    '</SOAP-ENV:Body>\n'
    '</SOAP-ENV:Envelope>\n'
)
"""The XML template used for all SOAP Requests in string form"""

REQUEST_HEADERS = {'Accept-Encoding': 'gzip'}
"""dictionary of headers to add to every HTTP GET/POST"""

RETRY_COUNT = 5
"""number of times to retry HTTP GET/POST's if the connection times out/fails"""

AUTH_RETRY = True
"""retry HTTP GET/POST's with username/password if session_id fails or not"""

DEFAULT_PORT = 443
"""port to connect to"""

DEFAULT_HOST = None
"""host to connect to"""

RECORD_ALL_REQUESTS = False
"""Controls whether each requests response object is appended to the
ALL_REQUESTS_RESPONSES list in Session
"""

FORCE_SERVER_VERSION = ''
"""
In the case where the user wants to have pytan act as if the server is a specific version,
regardless of what server_version is.
"""

STATS_LOOP = False
"""enable the statistics loop thread or not"""

STATS_LOOP_SLEEP = 5
"""seconds to sleep in between printing the statistics when stats_loop_enabled is True """

STATS_LOOP_TARGETS = [
    {'Version': 'Settings/Version'},
    {'Active Questions': 'Active Question Cache/Active Question Estimate'},
    {'Clients': 'Active Question Cache/Active Client Estimate'},
    {'Strings': 'String Cache/Total String Count'},
    {'Handles': 'System Performance Info/HandleCount'},
    {'Processes': 'System Performance Info/ProcessCount'},
    {'Memory Available': (
        'percentage(System Performance Info/PhysicalAvailable,System Performance Info/'
        'PhysicalTotal)'
    )
    },
]
"""list of dictionaries with the key being the section of info.json to print info from, and
the value being the item with in that section to print the value
"""
