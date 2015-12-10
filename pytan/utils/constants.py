#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Constants for :mod:`pytan`"""

DEBUG_FORMAT = (
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(name)s %(message)s'
)
"""
Logging format for debugformat=True
"""

INFO_FORMAT = '%(asctime)s %(levelname)-8s %(name)s: %(message)s'
"""
Logging format for debugformat=False
"""

LOG_LEVEL_MAPS = [
    (
        0,
        {
            'stats': 'DEBUG',
            'method_debug': 'DEBUG',
        },
        'Sets all loggers to only output at WARNING or above except for stats & method_debug',
    ),
    (
        1,
        {
            'pytan': 'INFO',
            'pytan.pollers.QuestionPoller': 'INFO',
            'pytan.pollers.ActionPoller': 'INFO',
            'pytan.pollers.SSEPoller': 'INFO',
        },
        'Pytan poller loggers show output at INFO or above',
    ),
    (
        2,
        {
            'pytan': 'DEBUG',
            'pytan.handler': 'INFO',
            'pytan.pollers.QuestionPoller.progress': 'INFO',
            'pytan.pollers.ActionPoller.progress': 'INFO',
            'pytan.pollers.SSEPoller.progress': 'INFO',
            'pytan.pollers.QuestionPoller': 'DEBUG',
            'pytan.pollers.ActionPoller': 'DEBUG',
            'pytan.pollers.SSEPoller': 'DEBUG',
        },
        'Pytan handler logger show output at INFO or above, poller logs at DEBUG or above, and poller progress logs at INFO or above',
    ),
    (
        3,
        {
            'pytan.handler': 'DEBUG',
            'pytan.pollers.QuestionPoller.progress': 'DEBUG',
            'pytan.pollers.ActionPoller.progress': 'DEBUG',
            'pytan.pollers.SSEPoller.progress': 'DEBUG',
            'pytan.pollers.QuestionPoller.resolver': 'INFO',
            'pytan.pollers.ActionPoller.resolver': 'INFO',
            'pytan.pollers.SSEPoller.resolver': 'INFO',
        },
        'Pytan handler logger show output at DEBUG or above, poller progress at DEBUG or above, and poller resolver at INFO or above',
    ),
    (
        4,
        {
            'pytan.handler.ask_manual': 'DEBUG',
            'pytan.pollers.QuestionPoller.resolver': 'DEBUG',
            'pytan.pollers.ActionPoller.resolver': 'DEBUG',
            'pytan.pollers.SSEPoller.resolver': 'DEBUG',
        },
        'Pytan ask manual logger show output at DEBUG or above and poller resolver at DEBUG or above',
    ),
    (
        5,
        {
            'pytan.handler.ask_manual_human': 'DEBUG',
        },
        'Pytan ask manual human logger show output at DEBUG or above',
    ),
    (
        6,
        {
            'pytan.handler.timing': 'DEBUG',
            'XMLCleaner': 'DEBUG',
        },
        'Pytan timing and XMLCleaner loggers show output at DEBUG or above',
    ),
    (
        7,
        {
            'pytan.sessions.Session': 'DEBUG',
        },
        'Taniumpy session loggers show output at DEBUG or above',
    ),
    (
        8,
        {
            'pytan.sessions.Session.auth': 'DEBUG',
        },
        'PyTan session authentication loggers show output at DEBUG or above',
    ),
    (
        9,
        {
            'pytan.sessions.Session.http': 'DEBUG',
        },
        'PyTan session http loggers show output at DEBUG or above',
    ),
    (
        10,
        {
            'pytan.handler.prettybody': 'DEBUG',
        },
        'Pytan handler pretty XML body loggers show output at DEBUG or above',
    ),
    (
        11,
        {
            'pytan.sessions.Session.http.body': 'DEBUG',
        },
        'PyTan session raw XML body loggers show output at DEBUG or above',
    ),
    (
        12,
        {
            'requests': 'DEBUG',
            'requests.packages.urllib3': 'DEBUG',
            'requests.packages.urllib3.connectionpool': 'DEBUG',
            'requests.packages.urllib3.poolmanager': 'DEBUG',
            'requests.packages.urllib3.util.retry': 'DEBUG',
        },
        'Requests package show logging at DEBUG or above',
    ),

]
"""
Map for loglevel(int) -> logger -> logger level(logging.INFO|WARN|DEBUG|...). Higher loglevels will include all levels up to and including that level. Contains a list of tuples, each tuple consisting of:
    * int, loglevel
    * dict, `{{logger_name: logger_level}}` for this loglevel
    * str, description of this loglevel
"""

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
    * manual: Whether or not this object type is allowed to do a manual search, that is -- allow the user to specify an attribute that is not in search, which will get ALL objects of that type then search for a match based on attribute values for EVERY key/value pair supplied
    * delete: Whether or not this object type can be deleted
    * create_json: Whether or not this object type can be created by importing from JSON
"""

Q_OBJ_MAP = {
    'saved': {
        'handler': 'ask_saved',
    },
    'manual': {
        'handler': 'ask_manual',
    },
    '_manual': {
        'handler': '_ask_manual',
    },
    'parsed': {
        'handler': 'ask_parsed',
    },
}
"""
Maps a question type from a human friendly string into the handler method that supports each type
"""

REQ_KWARGS = [
    'hide_errors_flag',
    'include_answer_times_flag',
    'row_counts_only_flag',
    'aggregate_over_time_flag',
    'most_recent_flag',
    'include_hashes_flag',
    'hide_no_results_flag',
    'use_user_context_flag',
    'script_data',
    'return_lists_flag',
    'return_cdata_flag',
    'pct_done_limit',
    'context_id',
    'sample_frequency',
    'sample_start',
    'sample_count',
    'suppress_scripts',
    'suppress_object_list',
    'row_start',
    'row_count',
    'sort_order',
    'filter_string',
    'filter_not_flag',
    'recent_result_buckets',
    'cache_id',
    'cache_expiration',
    'cache_sort_fields',
    'include_user_details',
    'include_hidden_flag',
    'use_error_objects',
    'use_json',
    'json_pretty_print',
    'cache_filters',
]
"""
A list of arguments that will be pulled from any respective kwargs for most calls to :class:`taniumpy.session.Session`
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
Maps a given TaniumPy object to the list of supported export formats for each object type, and the valid optional arguments for each export format. Optional arguments construct:
    * key: the optional argument name itself
    * valid_types: the valid python types that are allowed to be passed as a value to `key`
    * valid_list_types: the valid python types in str format that are allowed to be passed in a list, if list is one of the `valid_types`
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

PYTAN_USER_CONFIG = "~/.pytan_config.json"
"""
Default path to file to use for Handler parameter overrides
"""

PYTAN_KEY = "mT1er@iUa1kP9pelSW"
"""
Key used for obfuscation/de-obfsucation
"""

HANDLER_ARG_DEFAULTS = {
    'username': None,
    'password': None,
    'session_id': None,
    'host': None,
    'port': 443,
    'loglevel': 0,
    'debugformat': False,
    'gmt_log': False,
}
"""
Map of handler arguments and their defaults
"""
