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
    (
        0,
        {
            'handler': 'INFO',
            'ask_manual': 'WARN',
            'ask_manual_human': 'WARN',
            'api.session': 'WARN',
            'api.session.auth': 'WARN',
            'api.session.http': 'WARN',
            'api.session.http.body': 'WARN',
        }
    ),
    (1, {'handler': 'DEBUG'}),
    (2, {'ask_manual': 'DEBUG'}),
    (3, {'ask_manual_human': 'DEBUG'}),
    (7, {'api.session': 'DEBUG'}),
    (8, {'api.session.auth': 'DEBUG'}),
    (9, {'api.session.http': 'DEBUG'}),
    (10, {'api.session.http.body': 'DEBUG'}),
]

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

GET_OBJ_MAP = {
    'action': {
        'single': 'Action',
        'multi': None,
        'all': 'ActionList',
        'search': ['id'],
    },
    'client': {
        'single': None,
        'multi': None,
        'all': 'ClientStatus',
        'search': [],
    },
    'group': {
        'single': 'Group',
        'multi': 'GroupList',
        'all': 'GroupList',
        'search': ['id', 'name'],
    },
    'package': {
        'single': 'PackageSpec',
        'multi': None,
        'allfix': 'PackageSpecList',
        'all': 'PackageSpec',
        'search': ['id', 'name'],
    },
    'question': {
        'single': 'Question',
        'multi': None,
        'all': 'QuestionList',
        'search': ['id'],
    },
    'saved_action': {
        'single': 'SavedAction',
        'multi': 'SavedActionList',
        'all': 'SavedActionList',
        'search': ['id'],
    },
    'saved_question': {
        'single': 'SavedQuestion',
        'multi': None,
        'all': 'SavedQuestionList',
        'search': ['id', 'name'],
    },
    'sensor': {
        'single': 'Sensor',
        'multi': 'SensorList',
        'all': 'SensorList',
        'search': ['id', 'name', 'hash'],
    },
    'setting': {
        'single': 'SystemSetting',
        'multi': 'SystemSettingsList',
        'all': 'SystemSettingsList',
        'search': ['id', 'name'],
    },
    'user': {
        'single': 'User',
        'multi': None,
        'all': 'UserList',
        'search': ['id'],
    },
    'userrole': {
        'single': None,
        'multi': None,
        'all': 'UserRoleList',
        'search': [],
    },
    'whitelisted_url': {
        'single': 'WhiteListedUrlList',
        'multi': None,
        'all': 'WhiteListedUrlList',
        'search': ['id'],
    },
}

Q_OBJ_MAP = {
    'saved': {
        'api': 'SavedQuestion',
        'handler': 'ask_saved',
    },
    'manual': {
        'api': 'Question',
        'handler': 'ask_manual',
    },
    'manual_human': {
        'api': 'Question',
        'handler': 'ask_manual_human',
    },
}

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
]

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

PARAM_RE = re.compile(r'\{(.*?)\}')
PARAM_SPLIT_RE = re.compile(r'(?<!\\),')
PARAM_KEY_SPLIT = '='
FILTER_RE = re.compile(r',\s*that', re.IGNORECASE)
OPTION_RE = re.compile(r',\s*opt:', re.IGNORECASE)
SELECTORS = ['id', 'name', 'hash']
PARAM_DELIM = '||'

FILTER_MAPS = [
    {
        'human': ['<', 'less', 'lt'],
        'operator': 'Less',
        'not_flag': 0,
    },
    {
        'human': ['!<', 'notless', 'not less'],
        'operator': 'Less',
        'not_flag': 1,
    },
    {
        'human': ['<=', 'less equal', 'lessequal', 'le'],
        'operator': 'LessEqual',
        'not_flag': 0,
    },
    {
        'human': ['!<=', 'not less equal', 'not lessequal'],
        'operator': 'LessEqual',
        'not_flag': 1,
    },
    {
        'human': ['>', 'greater', 'gt'],
        'operator': 'Greater',
        'not_flag': 0,
    },
    {
        'human': ['!>', 'not greater', 'notgreater'],
        'operator': 'Greater',
        'not_flag': 1,
    },
    {
        'human': ['=>', 'greater equal', 'greaterequal', 'ge'],
        'operator': 'GreaterEqual',
        'not_flag': 0,
    },
    {
        'human': ['!=>', 'not greater equal', 'notgreaterequal'],
        'operator': 'GreaterEqual',
        'not_flag': 1,
    },
    {
        'human': ['=', 'equal', 'equals', 'eq'],
        'operator': 'Equal',
        'not_flag': 0,
    },
    {
        'human': [
            '!=', 'not equal', 'notequal', 'not equals', 'notequals', 'ne',
        ],
        'operator': 'Equal',
        'not_flag': 0,
    },
    {
        'human': ['contains'],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': 0,
    },
    {
        'human': [
            'does not contain', 'doesnotcontain', 'not contains', 'notcontains'
        ],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': 1,
    },
    {
        'human': ['starts with', 'startswith'],
        'operator': 'RegexMatch',
        'post_value': '.*',
        'not_flag': 0,
    },
    {
        'human': [
            'does not start with', 'doesnotstartwith', 'not starts with',
            'notstartswith',
        ],
        'operator': 'RegexMatch',
        'post_value': '.*',
        'not_flag': 1,
    },
    {
        'human': ['ends with', 'endswith'],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'not_flag': 0,
    },
    {
        'human': [
            'does not end with', 'doesnotendwith', 'not ends with',
            'notstartswith',
        ],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'not_flag': 1,
    },
    {
        'human': [
            'is not', 'not regex', 'notregex', 'not regex match',
            'notregexmatch', 'nre',
        ],
        'operator': 'RegexMatch',
        'not_flag': 1,
    },
    {
        'human': ['is', 'regex', 'regex match', 'regexmatch', 're'],
        'operator': 'RegexMatch',
        'not_flag': 0,
    },
]

OPTION_MAPS = [
    {
        'human': 'ignore_case',
        'attrs': {'ignore_case_flag': 1},
        'destination': 'filter',
        'valid_type': int,
    },
    {
        'human': 'match_case',
        'attrs': {'ignore_case_flag': 0},
        'destination': 'filter',
        'valid_type': int,
    },
    {
        'human': 'match_any_value',
        'attrs': {'all_values_flag': 0, 'all_times_flag': 0},
        'destination': 'filter',
        'valid_type': int,
    },
    {
        'human': 'match_all_values',
        'attrs': {'all_values_flag': 1, 'all_times_flag': 1},
        'destination': 'filter',
        'valid_type': int,
    },
    {
        'human': 'max_data_age:',
        'attr': 'max_age_seconds',
        'human_type': 'seconds',
        'valid_type': int,
        'destination': 'filter',
    },
    {
        'human': 'value_type:',
        'attr': 'value_type',
        'human_type': 'value_type',
        'valid_values': 'constants.SENSOR_TYPE_MAP.values()',
        'destination': 'filter',
        'valid_type': str,
    },
    {
        'human': 'and',
        'attrs': {'and_flag': 1},
        'destination': 'group',
        'valid_type': int,
    },
    {
        'human': 'or',
        'attrs': {'and_flag': 0},
        'destination': 'group',
        'valid_type': int,
    },
]
