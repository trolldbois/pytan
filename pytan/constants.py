"""Constants for :mod:`pytan`."""

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
HANDLER_DEFAULTS['loggmt'] = True
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
LOGMAP['pytan.requests'] = 20
LOGMAP['pytan.requests.packages.urllib3'] = 21
LOGMAP['pytan.requests.packages.urllib3.connectionpool'] = 22
LOGMAP['pytan.requests.packages.urllib3.poolmanager'] = 23
LOGMAP['pytan.requests.packages.urllib3.util.retry'] = 24

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
