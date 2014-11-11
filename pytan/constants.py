#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Constant variables"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging
import re

# debug log format
DEBUG_FORMAT = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(name)s %(message)s'
)

# info log format
INFO_FORMAT = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s: %(message)s'
)

# log levels to turn on extra loggers (higher the level the more verbose)
LOG_LEVEL_MAPS = [
    (0, {
        'pytan': 'INFO',
        'pytan.request': 'INFO',
        'pytan.request.manual_question': 'INFO',
        'pytan.request.parsed_question': 'INFO',
        'pytan.request.http': 'WARN',
        'pytan.auth': 'WARN',
        'pytan.reporter': 'WARN',
        'pytan.request.xmlcreate': 'WARN',
        'pytan.response.xmlparse': 'WARN',
        'pytan.packages.requests': 'WARN',
        'pytan.packages.requests.packages': 'WARN',
        'pytan.packages.requests.packages.urllib3': 'WARN',
        'pytan.packages.requests.packages.urllib3.connectionpool': 'WARN',
        'pytan.packages.requests.packages.urllib3.poolmanager': 'WARN',
        'pytan.packages.requests.packages.urllib3.util': 'WARN',
        'pytan.packages.requests.packages.urllib3.util.retry': 'WARN',
    }),
    (1, {
        'pytan': 'DEBUG',
        'pytan.request': 'DEBUG',
        'pytan.request.manual_question': 'DEBUG',
        'pytan.request.parsed_question': 'DEBUG',
    }),
    (2, {
        'pytan.reporter': 'DEBUG',
    }),
    (3, {
        'pytan.auth': 'DEBUG',
    }),
    (4, {
        'pytan.request.xmlcreate': 'DEBUG',
        'pytan.response.xmlparse': 'DEBUG',
    }),
    (5, {
        'pytan.request.http': 'DEBUG',
    }),
    (10, {
        'pytan.packages.requests': 'DEBUG',
        'pytan.packages.requests.packages': 'DEBUG',
        'pytan.packages.requests.packages.urllib3': 'DEBUG',
        'pytan.packages.requests.packages.urllib3.connectionpool': 'DEBUG',
        'pytan.packages.requests.packages.urllib3.poolmanager': 'DEBUG',
        'pytan.packages.requests.packages.urllib3.util': 'DEBUG',
        'pytan.packages.requests.packages.urllib3.util.retry': 'DEBUG',
    }),
]

# Used by pytan.req.Request.call_api() for how long a GetResultInfo
# loop is allowed to go on for
RESULT_MAX_WAIT = 500

# Used by pytan.req.Request.call_api() for long to sleep in between
# GetResultInfo checks
RESULT_SLEEP = 2

# Used by pytan.reports.Reporter.parse_resultxml() to determine what the
# numeric type value for a column maps to
RESULT_TYPE_MAP = {
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

# Used by pytan.req.Request.build_objects_dict() to figure out
# what valid query prefixes can be used
QUERY_PREFIXES = ['name', 'id', 'hash']

# Used by pytan.auth.Auth.session_id_text() to control whether
#or not SOAP Session IDs are included in any logging outputs
SHOW_SESSION_ID = False

# Used by pytan.req.Request.build_request_xml_dict() for
# creating the Soap Request XML
REQ_ENVELOPE_NS = {
    "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

# Used by pytan.req.Request.build_request_xml_dict() for
# creating the Soap Request XML
REQ_APP_NS = {
    "@xmlns": "urn:TaniumSOAP",
}

# Used by pytan.reports.Reporter.write_response() to determine
# supported formats
TRANSFORM_FORMATS = {
    'csv': 'get_csv',
    # 'xls': 'get_xls',
    'json': 'get_json',
    'xml': 'get_xml',
    'raw.xml': 'get_rawxml',
    'raw.response': 'get_rawresponse',
    'raw.request': 'get_rawrequest',
}

# Used by pytan.reports.Reporter.write_response() as boolean kwargs
# defaults for passthrus for parse_resultxml():
TRANSFORM_BOOL_KWARGS = {
    'ADD_TYPE_TO_HEADERS': False,
    'ADD_SENSOR_TO_HEADERS': False,
    'EXPAND_GROUPED_COLUMNS': False,
}

# Used by bin/ scripts to provide help for TRANSFORM_BOOL_KWARGS
TRANSFORM_BOOL_HELP = {
    'ADD_TYPE_TO_HEADERS': "Appends the column type to each column header for "
    "question results",
    'ADD_SENSOR_TO_HEADERS': "Prepends the associated sensor name the column "
    "originates from for question results",
    'EXPAND_GROUPED_COLUMNS': "Expand carriage return seperated values into "
    "sensor related rows",
}

# Used by pytan.reports.Reporter.write_response() for kwargs
# defaults for passthrus for sort_headers():
TRANSFORM_HEADER_SORT_PRIORITY = [
    'name',
    'id',
    'description',
    'hash',
    'value_type',
]

# Used by pytan.req.AskManualQuestionRequest.parse_params() to extract
# params from the sensor name
PARAM_RE = re.compile(r'\[(.*?)\]')

# Used by pytan.req.AskManualQuestionRequest.parse_params() to split
# the params by unescaped commas
PARAM_SPLIT_RE = re.compile(r'(?<!\\),')

# Used by pytan.req.AskManualQuestionRequest.parse_question_filters()
# and parse_filter() to find filters in a string
FILTER_RE = re.compile(r',\s*that', re.IGNORECASE)

# Used by pytan.req.AskManualQuestionRequest.parse_question_filters()
# and parse_options() to find filters in a string
OPTION_RE = re.compile(r',\s*opt:', re.IGNORECASE)

# Used by pytan.req.AskManualQuestionRequest.build_objects_dict()
# when creating the XML tag for a param name
PARAM_DELIM = '||'

# Used by pytan.req.AskManualQuestionRequest.get_fm_match() to
# parse a sensor name for a filter
FILTER_MAPS = [
    {
        'human': ['<', 'less', 'lt'],
        'operator': 'Less',
        'not_flag': '0',
    },
    {
        'human': ['!<', 'notless', 'not less'],
        'operator': 'Less',
        'not_flag': '1',
    },
    {
        'human': ['<=', 'less equal', 'lessequal', 'le'],
        'operator': 'LessEqual',
        'not_flag': '0',
    },
    {
        'human': ['!<=', 'not less equal', 'not lessequal'],
        'operator': 'LessEqual',
        'not_flag': '1',
    },
    {
        'human': ['>', 'greater', 'gt'],
        'operator': 'Greater',
        'not_flag': '0',
    },
    {
        'human': ['!>', 'not greater', 'notgreater'],
        'operator': 'Greater',
        'not_flag': '1',
    },
    {
        'human': ['=>', 'greater equal', 'greaterequal', 'ge'],
        'operator': 'GreaterEqual',
        'not_flag': '0',
    },
    {
        'human': ['!=>', 'not greater equal', 'notgreaterequal'],
        'operator': 'GreaterEqual',
        'not_flag': '1',
    },
    {
        'human': ['=', 'equal', 'equals', 'eq'],
        'operator': 'Equal',
        'not_flag': '0',
    },
    {
        'human': [
            '!=', 'not equal', 'notequal', 'not equals', 'notequals', 'ne',
        ],
        'operator': 'Equal',
        'not_flag': '0',
    },
    {
        'human': ['contains'],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': '0',
    },
    {
        'human': [
            'does not contain', 'doesnotcontain', 'not contains', 'notcontains'
        ],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': '1',
    },
    {
        'human': ['starts with', 'startswith'],
        'operator': 'RegexMatch',
        'post_value': '.*',
        'not_flag': '0',
    },
    {
        'human': [
            'does not start with', 'doesnotstartwith', 'not starts with',
            'notstartswith',
        ],
        'operator': 'RegexMatch',
        'post_value': '.*',
        'not_flag': '1',
    },
    {
        'human': ['ends with', 'endswith'],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'not_flag': '0',
    },
    {
        'human': [
            'does not end with', 'doesnotendwith', 'not ends with',
            'notstartswith',
        ],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'not_flag': '1',
    },
    {
        'human': [
            'is not', 'not regex', 'notregex', 'not regex match',
            'notregexmatch', 'nre',
        ],
        'operator': 'RegexMatch',
        'not_flag': '1',
    },
    {
        'human': ['is', 'regex', 'regex match', 'regexmatch', 're'],
        'operator': 'RegexMatch',
        'not_flag': '0',
    },
]

# Used by pytan.req.AskManualQuestionRequest.get_opt_match() to
# parse a sensor name for options
OPTION_MAPS = [
    {
        'human': 'ignore_case',
        'operators': [{'ignore_case_flag': 1}],
        'destination': 'filter',
    },
    {
        'human': 'match_case',
        'operators': [{'ignore_case_flag': 0}],
        'destination': 'filter',
    },
    {
        'human': 'match_any_value',
        'operators': [{'all_values_flag': 0}, {'all_times_flag': 0}],
        'destination': 'filter',
    },
    {
        'human': 'match_all_values',
        'operators': [{'all_values_flag': 1}, {'all_times_flag': 1}],
        'destination': 'filter',
    },
    {
        'human': 'max_data_age:',
        'operator': 'max_age_seconds',
        'value': 'seconds',
        'destination': 'filter',
    },
    {
        'human': 'and',
        'operators': [{'and_flag': 1}],
        'destination': 'group',
    },
    {
        'human': 'or',
        'operators': [{'and_flag': 0}],
        'destination': 'group',
    },
]

# Used by pytan.req.AskManualQuestionRequest.build_objects_dict() to
# specify per sensor option defaults
DEFAULT_FILTER_OPTIONS = {
    'ignore_case_flag': 1,
    'all_values_flag': 0,
    'all_times_flag': 0,
    'max_age_seconds': 0,
}
