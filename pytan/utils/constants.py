#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Constants for :mod:`pytan`."""

import sys

DEFAULTS = {
    'logfile_enable': False,
    'logfile_output': "~/pytan.log",
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
    'session_id': '',
    'host': '',
    'port': 443,
    'config_file': "~/.pytan_config.json",
}

HANDLER_ARGS = {
    # pytan.handler.Handler args:
    'username': str,
    'password': str,
    'session_id': str,
    'host': str,
    'port': int,
    'loglevel': int,
    'loggmt': bool,
    'logconsole_enable': bool,
    'logconsole_formatter': str,
    'logfile_enable': bool,
    'logfile_output': str,
    'logfile_formatter': str,
    'config_file': str,
    # pytan.session.Session args:
    'soap_request_headers': dict,
    'http_debug': bool,
    'http_auth_retry': bool,
    'http_retry_count': int,
    'auth_connect_timeout_sec': int,
    'auth_response_timeout_sec': int,
    'info_connect_timeout_sec': int,
    'info_response_timeout_sec': int,
    'soap_connect_timeout_sec': int,
    'soap_response_timeout_sec': int,
    'stats_loop_enabled': bool,
    'stats_loop_sleep_sec': int,
    'stats_loop_targets': dict,
    'record_all_requests': bool,
}
"""
List of handler args that map to DEFAULTS['$ARG'] in constants
"""

LOG_LEVEL_MAPS = {
    'pytan.session.stats': 0,
    'pytan.handler': 1,
    'pytan.utils.historyconsole': 1,
    'pytan.utils.calc': 1,
    'pytan.utils.tanium_obj': 1,
    'pytan.pollers.action': 2,
    'pytan.pollers.question': 2,
    'pytan.pollers.sse': 2,
    'pytan.pollers.action.progress': 3,
    'pytan.pollers.question.progress': 3,
    'pytan.pollers.sse.progress': 3,
    'pytan.pollers.action.resolver': 4,
    'pytan.pollers.question.resolver': 4,
    'pytan.pollers.sse.resolver': 4,
    'pytan.utils.parsers': 0,
    'pytan.session': 6,
    'pytan.utils.network': 7,
    'pytan.session.http': 7,
    'pytan.session.auth': 8,
    'pytan.session.body': 9,
    'pytan.utils.xml_clean': 9,
    'pytan.utils.log': 10,
    'pytan.utils.external.requests': 11,
    'pytan.utils.external.requests.packages.urllib3': 11,
    'pytan.utils.external.requests.packages.urllib3.connectionpool': 11,
    'pytan.utils.external.requests.packages.urllib3.poolmanager': 11,
    'pytan.utils.external.requests.packages.urllib3.util.retry': 11,
}
"""
Map for pytan loggers into python loggings system.

Format is::

    {
        'logger name': int,
    }

Where:

    * logger_name: name of pytan logger in python logging system
    * int: loglevel for INFO messages from this logger, int+10 = loglevel for DEBUG messages
"""

DEFAULT_LOGGER_LEVEL = "WARN"
"""Set all pytan loggers in LOG_LEVEL_MAPS to this level before setting them to INFO or DEBUG"""

OVERRIDE_PYTAN_LEVEL = 30
"""If loglevel supplied is >= to this level, then set ALL loggers (pytan or not) to DEBUG"""

SENSOR_TYPE_MAP = {
    0: 'Hash',
    # SENSOR_RESULT_TYPE_STRING
    1: 'String',
    # SENSOR_RESULT_TYPE_VERSION
    2: 'Version',
    # SENSOR_RESULT_TYPE_NUMERIC
    3: 'NumericDecimal',
    # SENSOR_RESULT_TYPE_DATE_BES
    4: 'BESDate',
    # SENSOR_RESULT_TYPE_IPADDRESS
    5: 'IPAddress',
    # SENSOR_RESULT_TYPE_DATE_WMI
    6: 'WMIDate',
    #  e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes:
    # 'TimeDiff', and 3.67 seconds" or "4.2 hours"
    # (numeric + "Y|MO|W|D|H|M|S" units)
    7: 'TimeDiff',
    #  e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
    8: 'DataSize',
    9: 'NumericInteger',
    10: 'VariousDate',
    11: 'RegexMatch',
    12: 'LastOperatorType',
}
"""
Maps a Result type from the Tanium SOAP API from an int to a string
"""

GET_OBJ_MAP = {
    'action': {
        'single': 'Action',
        'multi': None,
        'all': 'ActionList',
        'search': ['id'],
        'manual': False,
        'delete': False,
        'create_json': True,
    },
    'client': {
        'single': None,
        'multi': None,
        'all': 'ClientStatus',
        'search': [],
        'manual': True,
        'delete': False,
        'create_json': False,
    },
    'group': {
        'single': 'Group',
        'multi': 'GroupList',
        'all': 'GroupList',
        'search': ['id', 'name'],
        'manual': True,
        'delete': True,
        'create_json': True,
    },
    'package': {
        'single': 'PackageSpec',
        'multi': None,
        'allfix': 'PackageSpecList',
        'all': 'PackageSpec',
        'search': ['id', 'name'],
        'manual': True,
        'delete': True,
        'create_json': True,
    },
    'question': {
        'single': 'Question',
        'multi': None,
        'all': 'QuestionList',
        'search': ['id'],
        'manual': False,
        'delete': False,
        'create_json': True,
    },
    'saved_action': {
        'single': 'SavedAction',
        'multi': 'SavedActionList',
        'all': 'SavedActionList',
        'search': ['id', 'name'],
        'manual': True,
        'delete': False,
        'create_json': False,  # AddObject returns null, unknown why
    },
    'saved_question': {
        'single': 'SavedQuestion',
        'multi': None,
        'all': 'SavedQuestionList',
        'search': ['id', 'name'],
        'manual': True,
        'delete': True,
        'create_json': True,
    },
    'sensor': {
        'single': 'Sensor',
        'multi': 'SensorList',
        'all': 'SensorList',
        'search': ['id', 'name', 'hash'],
        'manual': False,
        'delete': True,
        'create_json': True,
    },
    'setting': {
        'single': 'SystemSetting',
        'multi': 'SystemSettingList',
        'all': 'SystemSettingList',
        'search': ['id', 'name'],
        'manual': True,
        'delete': False,
        'create_json': False,
    },
    'user': {
        'single': 'User',
        'multi': None,
        'all': 'UserList',
        'search': ['id'],
        'manual': True,
        'delete': True,
        'create_json': True,
    },
    'userrole': {
        'single': None,
        'multi': None,
        'all': 'UserRoleList',
        'search': [],
        'manual': True,
        'delete': False,
        'create_json': False,
    },
    'whitelisted_url': {
        'single': 'WhiteListedUrlList',
        'multi': None,
        'all': 'WhiteListedUrlList',
        'search': [],
        'manual': True,
        'delete': True,
        'create_json': True,
    },
}
"""
Maps an object type from a human friendly string into various aspects:

    * single: The :mod:`TaniumPy` object used to find singular instances of this object type
    * multi: The :mod:`TaniumPy` object used to find multiple instances of this object type
    * all: The :mod:`TaniumPy` object used to find all instances of this object type
    * search: The list of attributes that can be used with the Tanium SOAP API for searches
    * manual: Whether or not this object type is allowed to do a manual search, that is -- allow
      the user to specify an attribute that is not in search, which will get ALL objects of that
      type then search for a match based on attribute values for EVERY key/value pair supplied
    * delete: Whether or not this object type can be deleted
    * create_json: Whether or not this object type can be created by importing from JSON
"""

EXPORT_MAPS = {
    'ResultSet': {
        'csv': [
            {
                'key': 'header_sort',
                'valid_types': [bool, list, tuple],
                'valid_list_types': ['str', 'unicode'],
            },
            {
                'key': 'sensors',
                'valid_types': [list, tuple],
                'valid_list_types': ['taniumpy.Sensor'],
            },
            {
                'key': 'header_add_sensor',
                'valid_types': [bool],
                'valid_list_types': [],
            },
            {
                'key': 'header_add_type',
                'valid_types': [bool],
                'valid_list_types': [],
            },
            {
                'key': 'expand_grouped_columns',
                'valid_types': [bool],
                'valid_list_types': [],
            },
        ],
        'json': [],
        'xml': [],
    },
    'BaseType': {
        'csv': [
            {
                'key': 'header_sort',
                'valid_types': [bool, list, tuple],
                'valid_list_types': ['str', 'unicode'],
            },
            {
                'key': 'explode_json_string_values',
                'valid_types': [bool],
                'valid_list_types': [],
            },
        ],
        'json': [
            {
                'key': 'include_type',
                'valid_types': [bool],
                'valid_list_types': [],
            },
            {
                'key': 'explode_json_string_values',
                'valid_types': [bool],
                'valid_list_types': [],
            },
        ],
        'xml': [
            {
                'key': 'minimal',
                'valid_types': [bool],
                'valid_list_types': [],
            },
        ]
    },

}
"""
Maps a given TaniumPy object to the list of supported export formats for each object type, and the
valid optional arguments for each export format. Optional arguments construct:
    * key: the optional argument name itself
    * valid_types: the valid python types that are allowed to be passed as a value to `key`
    * valid_list_types: the valid python types in str format that are allowed to be passed in a
      list, if list is one of the `valid_types`
"""

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
"""
Tanium's format for date time strings
"""

SSE_FORMAT_MAP = [
    ('csv', '0', 0),
    ('xml', '1', 1),
    ('xml_obj', '1', 1),
    ('cef', '2', 2),
]
"""
Mapping of human friendly strings to API integers for server side export
"""

SSE_RESTRICT_MAP = {
    1: ['6.5.314.4300'],
    2: ['6.5.314.4300'],
}
"""
Mapping of API integers for server side export format to version support
"""

SSE_CRASH_MAP = ['6.5.314.4300']
"""
Mapping of versions to watch out for crashes/handle bugs for server side export
"""

PYTAN_KEY = "mT1er@iUa1kP9pelSW"
"""
Key used for obfuscation/de-obfsucation
"""

Q_COMPLETE_PCT_DEFAULT = 99
Q_POLLING_SECS_DEFAULT = 5
Q_OVERRIDE_TIMEOUT_SECS_DEFAULT = 0
Q_EXPIRATION_ATTR = 'expiration'
Q_EXPIRY_FALLBACK_SECS = 600
Q_STR_ATTRS = [
    'object_info',
    'polling_secs',
    'override_timeout_secs',
    'complete_pct',
    'expiration',
]

S_STR_ATTRS = [
    'export_id',
    'polling_secs',
    'timeout_secs',
    'sse_status',
]
"""Class attributes to include in __str__ output"""

S_POLLING_SECS_DEFAULT = 2
"""default value for self.polling_secs"""

S_TIMEOUT_SECS_DEFAULT = 600
"""default value for self.timeout_secs"""

A_COMPLETE_PCT_DEFAULT = 100
"""default value for self.complete_pct"""

A_ACTION_DONE_KEY = 'success'
"""key in action_result_map that maps to an action being done"""

A_RUNNING_STATUSES = ["active", "open"]
"""values for status attribute of action object that mean the action is running"""

A_EXPIRATION_ATTR = 'expiration_time'
"""attribute of self.obj that contains the expiration for this object"""

EMAP = {}
EMAP['L'] = {}
EMAP['L']['operator'] = 'Less'
EMAP['L']['not_flag'] = 0
EMAP['L']['help'] = "less than 'VALUE'"
EMAP['NL'] = {}
EMAP['NL']['operator'] = 'Less'
EMAP['NL']['not_flag'] = 1
EMAP['NL']['help'] = "not less than 'VALUE'"
EMAP['LE'] = {}
EMAP['LE']['operator'] = 'LessEqual'
EMAP['LE']['not_flag'] = 0
EMAP['LE']['help'] = "less than or equal to 'VALUE'"
EMAP['NLE'] = {}
EMAP['NLE']['operator'] = 'LessEqual'
EMAP['NLE']['not_flag'] = 1
EMAP['NLE']['help'] = "not less than or equal to 'VALUE'"
EMAP['G'] = {}
EMAP['G']['operator'] = 'Greater'
EMAP['G']['not_flag'] = 0
EMAP['G']['help'] = "greater than 'VALUE'"
EMAP['NG'] = {}
EMAP['NG']['operator'] = 'Greater'
EMAP['NG']['not_flag'] = 1
EMAP['NG']['help'] = "not greater than 'VALUE'"
EMAP['GE'] = {}
EMAP['GE']['operator'] = 'GreaterEqual'
EMAP['GE']['not_flag'] = 0
EMAP['GE']['help'] = "greater than or equal to 'VALUE'"
EMAP['NGE'] = {}
EMAP['NGE']['operator'] = 'GreaterEqual'
EMAP['NGE']['not_flag'] = 1
EMAP['NGE']['help'] = "not greater than or equal to 'VALUE'"
EMAP['E'] = {}
EMAP['E']['operator'] = 'Equal'
EMAP['E']['not_flag'] = 0
EMAP['E']['help'] = "equal to 'VALUE'"
EMAP['NE'] = {}
EMAP['NE']['operator'] = 'Equal'
EMAP['NE']['not_flag'] = 1
EMAP['NE']['help'] = "not equal to 'VALUE'"
EMAP['C'] = {}
EMAP['C']['operator'] = 'RegexMatch'
EMAP['C']['not_flag'] = 0
EMAP['C']['pre_value'] = '.*'
EMAP['C']['post_value'] = '.*'
EMAP['C']['help'] = "matches regex '.*VALUE.*'"
EMAP['NC'] = {}
EMAP['NC']['operator'] = 'RegexMatch'
EMAP['NC']['not_flag'] = 1
EMAP['NC']['pre_value'] = '.*'
EMAP['NC']['post_value'] = '.*'
EMAP['NC']['help'] = "does not match regex '.*VALUE.*'"
EMAP['SW'] = {}
EMAP['SW']['operator'] = 'RegexMatch'
EMAP['SW']['not_flag'] = 0
EMAP['SW']['pre_value'] = '.*'
EMAP['SW']['help'] = "matches regex '.*VALUE'"
EMAP['NSW'] = {}
EMAP['NSW']['operator'] = 'RegexMatch'
EMAP['NSW']['not_flag'] = 1
EMAP['NSW']['pre_value'] = '.*'
EMAP['NSW']['help'] = "does not match regex '.*VALUE'"
EMAP['EW'] = {}
EMAP['EW']['operator'] = 'RegexMatch'
EMAP['EW']['not_flag'] = 0
EMAP['EW']['pre_value'] = '.*'
EMAP['EW']['help'] = "matches regex 'VALUE.*'"
EMAP['NEW'] = {}
EMAP['NEW']['operator'] = 'RegexMatch'
EMAP['NEW']['not_flag'] = 1
EMAP['NEW']['pre_value'] = '.*'
EMAP['NEW']['help'] = "does not match regex 'VALUE.*'"
EMAP['R'] = {}
EMAP['R']['operator'] = 'RegexMatch'
EMAP['R']['not_flag'] = 0
EMAP['R']['help'] = "matches regex 'VALUE'"
EMAP['NR'] = {}
EMAP['NR']['operator'] = 'RegexMatch'
EMAP['NR']['not_flag'] = 1
EMAP['NR']['help'] = "does not match regex 'VALUE'"

OPERATORS_EXTENDED = {
    '<': EMAP['L'],
    'less': EMAP['L'],
    'l': EMAP['L'],
    '!<': EMAP['NL'],
    'not less': EMAP['NL'],
    'notless': EMAP['NL'],
    'nl': EMAP['NL'],
    '<=': EMAP['LE'],
    'less equal': EMAP['LE'],
    'lessequal': EMAP['LE'],
    'le': EMAP['LE'],
    '!<=': EMAP['NLE'],
    'not less equal': EMAP['NLE'],
    'notlessequal': EMAP['NLE'],
    'nle': EMAP['NLE'],
    '>': EMAP['G'],
    'greater': EMAP['G'],
    'g': EMAP['G'],
    '!>': EMAP['NG'],
    'not greater': EMAP['NG'],
    'notgreater': EMAP['NG'],
    'ng': EMAP['NG'],
    '=>': EMAP['GE'],
    'greater equal': EMAP['GE'],
    'greaterequal': EMAP['GE'],
    'ge': EMAP['GE'],
    '!=>': EMAP['NGE'],
    'not greater equal': EMAP['NGE'],
    'notgreaterequal': EMAP['NGE'],
    'nge': EMAP['NGE'],
    '=': EMAP['E'],
    'equal': EMAP['E'],
    'equals': EMAP['E'],
    'eq': EMAP['E'],
    'e': EMAP['E'],
    '!=': EMAP['NE'],
    'not equal': EMAP['NE'],
    'notequal': EMAP['NE'],
    'not equals': EMAP['NE'],
    'notequals': EMAP['NE'],
    'neq': EMAP['NE'],
    'ne': EMAP['NE'],
    "~=": EMAP['C'],
    "contains": EMAP['C'],
    "in": EMAP['C'],
    "!~=": EMAP['NC'],
    "not contains": EMAP['NC'],
    "not in": EMAP['NC'],
    "starts": EMAP['SW'],
    "starts with": EMAP['SW'],
    "sw": EMAP['NSW'],
    "not starts": EMAP['NSW'],
    "not starts with": EMAP['NSW'],
    "nsw": EMAP['NSW'],
    "ends": EMAP['EW'],
    "ends with": EMAP['EW'],
    "ew": EMAP['NEW'],
    "not ends": EMAP['NEW'],
    "not ends with": EMAP['NEW'],
    "new": EMAP['NEW'],
    "is": EMAP['R'],
    "regex": EMAP['R'],
    "regex match": EMAP['R'],
    "re": EMAP['R'],
    "is not": EMAP['NR'],
    "not regex": EMAP['NR'],
    "not regex match": EMAP['NR'],
    "nre": EMAP['NR'],
}

OPERATORS = ['Equal', 'Greater', 'GreaterEqual', 'Less', 'LessEqual', 'RegexMatch']
SINGLE_FIX = ['PackageSpecList']
SPEC_FIELD_FALLBACKS = ['name', 'url_regx', 'id']

TRUE_TYPES = [1, True, "1", "True"]
FALSE_TYPES = [0, False, "0", "False"]

TMAP = {}
TMAP['S'] = {'t': 'String', 'h': 'standard lexicographical comparison (the default)'}
TMAP['V'] = {'t': 'Version', 'h': 'version strings, e.g. 9.4.2 is less than 10.1.3'}
TMAP['N'] = {'t': 'Numeric', 'h': 'numeric, decimal, floating point, and scientific notation'}
TMAP['I'] = {'t': 'IPAddress', 'h': 'IP addresses'}
TMAP['D'] = {'t': 'Date', 'h': 'a date in the format YYYY-MM-DD HH:MM:SS'}
TMAP['DS'] = {'t': 'DataSize', 'h': 'data size, e.g. 125MB, 23K, 34.2 Gig (int + B|K|M|G|T)'}
TMAP['NI'] = {'t': 'NumericInteger', 'h': 'be integer numeric values'}

FIELD_TYPES = {
    'string': TMAP['S'],
    'version': TMAP['V'],
    'numeric': TMAP['N'],
    'ipaddress': TMAP['I'],
    'date': TMAP['D'],
    'datasize': TMAP['DS'],
    'numericinteger': TMAP['NI'],
}

HELP_GET = "Use GetObject to find {} objects with cache filters to limit the results"
HELP_SQ_GETQ = "Use GetObject to get the last question asked by a saved question"
HELP_SQ_RD = (
    "Use GetResultInfo on a saved question in order to issue a new question, "
    "which refreshes the data for that saved question"
)
HELP_SQ_RESQ = (
    "Use GetObject to re-fetch the saved question in order get the ID of the newly asked question"
)

HELP_PJ = "Use AddObject to add a ParseJob for question_text and get back ParseResultGroups"
HELP_PJ_ADD = "Use AddObject to add the Question object from the chosen ParseResultGroup"
HELP_GRD = "Use GetResultData to get answers for an object"
HELP_GRD_SSE = "Issue a GetResultData to start a Server Side Export and get an export_id"
