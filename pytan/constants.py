#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Constant variables"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging

# debug log format
DEBUG_FORMAT = logging.Formatter(
    '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
    '%(levelname)-8s %(name)s %(message)s'
)

# info log format
INFO_FORMAT = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s %(message)s'
)

LOG_LEVEL_MAPS = [
    (0, {
        'PyTan': 'INFO',
        'PyTan.sensor_parser': 'WARN',
        'PyTan.auth': 'WARN',
        'PyTan.transform': 'WARN',
        'PyTan.result_infos': 'WARN',
        'PyTan.xmlcreate': 'WARN',
        'PyTan.xmlparse': 'WARN',
        'PyTan.http': 'WARN',
        'requests': 'WARN',
        'requests.packages': 'WARN',
        'requests.packages.urllib3': 'WARN',
        'requests.packages.urllib3.connectionpool': 'WARN',
        'requests.packages.urllib3.poolmanager': 'WARN',
        'requests.packages.urllib3.util': 'WARN',
        'requests.packages.urllib3.util.retry': 'WARN',
    }),
    (1, {
        'PyTan': 'DEBUG',
    }),
    (2, {
        'PyTan.result_infos': 'DEBUG',
        'PyTan.transform': 'DEBUG',
        'PyTan.sensor_parser': 'DEBUG',
    }),
    (3, {
        'PyTan.auth': 'DEBUG',
    }),
    (4, {
        'PyTan.xmlcreate': 'DEBUG',
        'PyTan.xmlparse': 'DEBUG',
    }),
    (5, {
        'PyTan.http': 'DEBUG',
    }),
    (10, {
        'requests': 'DEBUG',
        'requests.packages': 'DEBUG',
        'requests.packages.urllib3': 'DEBUG',
        'requests.packages.urllib3.connectionpool': 'DEBUG',
        'requests.packages.urllib3.poolmanager': 'DEBUG',
        'requests.packages.urllib3.util': 'DEBUG',
        'requests.packages.urllib3.util.retry': 'DEBUG',
    }),
]

# Used by SoapWrap.call_api() for how long a GetResultInfo loop is allowed
# to go on for
RESULT_MAX_WAIT = 500

# Used by SoapWrap.call_api() for long to sleep in between
# GetResultInfo checks
RESULT_SLEEP = 2

# Used by SoapWrap.SoapWrap for environment variable override mappings
OS_ENV_MAP = {
    'SOAP_USERNAME': 'self.__username',
    'SOAP_PASSWORD': 'self.__password',
    'SOAP_HOSTNAME': 'self.__host',
    'SOAP_PORT': 'self.__port',
    'SOAP_PROTOCOL': 'self.__protocol',
    'SOAP_PATH': 'self.__soap_path',
}

# Used by SoapWrap.SoapTransform.parse_resultxml() to determine what the
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

# Used by SoapWrap.SoapWrap.__build_objects_dict() to figure out
# what valid query prefixes can be used
QUERY_PREFIXES = ['name', 'id', 'hash']

# Used by SoapWrap.SoapAuth.session_id_text() to control whether
#or not SOAP Session IDs are included in any logging outputs
SHOW_SESSION_ID = False

# Used by SoapWrap.SoapRequest.build_request_xml_dict() for
# creating the Soap Request XML
REQ_ENVELOPE_NS = {
    "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

# Used by SoapWrap.SoapRequest.build_request_xml_dict() for
# creating the Soap Request XML
REQ_APP_NS = {
    "@xmlns": "urn:TaniumSOAP",
}

# Used by SoapWrap.SoapTransform.write_response() to determine
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

# Used by SoapWrap.SoapTransform.write_response() as boolean kwargs
# defaults for passthrus for parse_resultxml():
TRANSFORM_BOOL_KWARGS = {
    'ADD_TYPE_TO_HEADERS': False,
    'ADD_SENSOR_TO_HEADERS': False,
    'EXPAND_GROUPED_COLUMNS': False,
}
TRANSFORM_BOOL_HELP = {
    'ADD_TYPE_TO_HEADERS': "Appends the column type to each column header for "
    "question results",
    'ADD_SENSOR_TO_HEADERS': "Prepends the associated sensor name the column "
    "originates from for question results",
    'EXPAND_GROUPED_COLUMNS': "Expand carriage return seperated values into "
    "sensor related rows",
}

# Used by SoapWrap.SoapTransform.write_response() for kwargs
# defaults for passthrus for sort_headers():
TRANSFORM_HEADER_SORT_PRIORITY = [
    'name',
    'id',
    'description',
    'hash',
    'value_type',
]

PARAM_RE = r'\[(.*?)\]'
PARAM_SPLIT_RE = r'(?<!\\),'
PARAM_DELIM = '||'

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
        'operator': 'RegExMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': '0',
    },
    {
        'human': [
            'does not contain', 'doesnotcontain', 'not contains', 'notcontains'
        ],
        'operator': 'RegExMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': '1',
    },
    {
        'human': ['starts with', 'startswith'],
        'operator': 'RegExMatch',
        'post_value': '.*',
        'not_flag': '0',
    },
    {
        'human': [
            'does not start with', 'doesnotstartwith', 'not starts with',
            'notstartswith',
        ],
        'operator': 'RegExMatch',
        'post_value': '.*',
        'not_flag': '1',
    },
    {
        'human': ['ends with', 'endswith'],
        'operator': 'RegExMatch',
        'pre_value': '.*',
        'not_flag': '0',
    },
    {
        'human': [
            'does not end with', 'doesnotendwith', 'not ends with',
            'notstartswith',
        ],
        'operator': 'RegExMatch',
        'pre_value': '.*',
        'not_flag': '1',
    },
    {
        'human': [
            'is not', 'not regex', 'notregex', 'not regex match',
            'notregexmatch', 'nre',
        ],
        'operator': 'RegExMatch',
        'not_flag': '1',
    },
    {
        'human': ['is', 'regex', 'regex match', 'regexmatch', 're'],
        'operator': 'RegExMatch',
        'not_flag': '0',
    },
]

OPTION_MAPS = [
    {
        'human': 'ignore_case',
        'operators': [{'ignore_case_flag': '1'}],
    },
    {
        'human': 'match_case',
        'operators': [{'ignore_case_flag': '0'}],
    },
    {
        'human': 'match_any_value',
        'operators': [{'all_values_flag': '0'}, {'all_times_flag': '0'}],
    },
    {
        'human': 'match_all_values',
        'operators': [{'all_values_flag': '1'}, {'all_times_flag': '1'}],
    },
    {
        'human': 'max_data_age:',
        'operator': 'max_age_seconds',
        'value': 'seconds',
    },
]
