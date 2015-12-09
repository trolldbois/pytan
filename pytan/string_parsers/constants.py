#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Constants used by :mod:`string_parsers`"""

PARAM_RE = r'(?<!\\)\{(.*?)(?<!\\)\}'
"""
The regex that is used to parse parameters from a human string. Ex: ala {key1=value1}
"""

PARAM_SPLIT_RE = r'(?<!\\),'
"""
The regex that is used to split multiple parameters. Ex: key1=value1, key2=value2
"""

PARAM_KEY_SPLIT = '='
"""
The string that is used to split parameter key from parameter value. Ex: `key1`\ ``=``\ `value1`
"""

FILTER_RE = r',\s*that'
"""
The regex that is used to find filters in a string. Ex: `Sensor1`\ ``, that`` `contains blah`
"""

OPTION_RE = r',\s*opt:'
"""
The regex that is used to find options in a string. Ex: `Sensor1, that contains blah`\ ``, opt:``\ `ignore_case`\ ``, opt:``\ `max_data_age:3600`
"""

SELECTORS = ['id', 'name', 'hash']
"""
The search selectors that can be extracted from a string. Ex: ``name``:`Sensor1,` or ``id``:`1`, or ``hash``:`1111111`
"""

PARAM_DELIM = '||'
"""
The string to surround a parameter with when passing parameters to the SOAP API for a sensor in a question. Ex: ``||``\ `parameter_key`\ ``||``
"""

FILTER_MAPS = [
    {
        'human': ['<', 'less', 'lt', 'less than'],
        'operator': 'Less',
        'not_flag': 0,
        'help': "Filter for less than VALUE",
    },
    {
        'human': ['!<', 'notless', 'not less', 'not less than'],
        'operator': 'Less',
        'not_flag': 1,
        'help': "Filter for not less than VALUE",
    },
    {
        'human': ['<=', 'less equal', 'lessequal', 'le'],
        'operator': 'LessEqual',
        'not_flag': 0,
        'help': "Filter for less than or equal to VALUE",
    },
    {
        'human': ['!<=', 'not less equal', 'not lessequal'],
        'operator': 'LessEqual',
        'not_flag': 1,
        'help': "Filter for not less than or equal to VALUE",
    },
    {
        'human': ['>', 'greater', 'gt', 'greater than'],
        'operator': 'Greater',
        'not_flag': 0,
        'help': "Filter for greater than VALUE",
    },
    {
        'human': ['!>', 'not greater', 'notgreater', 'not greater than'],
        'operator': 'Greater',
        'not_flag': 1,
        'help': "Filter for not greater than VALUE",
    },
    {
        'human': ['=>', 'greater equal', 'greaterequal', 'ge'],
        'operator': 'GreaterEqual',
        'not_flag': 0,
        'help': "Filter for greater than or equal to VALUE",
    },
    {
        'human': ['!=>', 'not greater equal', 'notgreaterequal'],
        'operator': 'GreaterEqual',
        'not_flag': 1,
        'help': "Filter for not greater than VALUE",
    },
    {
        'human': ['=', 'equal', 'equals', 'eq'],
        'operator': 'Equal',
        'not_flag': 0,
        'help': "Filter for equals to VALUE",
    },
    {
        'human': [
            '!=', 'not equal', 'notequal', 'not equals', 'notequals', 'ne',
        ],
        'operator': 'Equal',
        'not_flag': 1,
        'help': "Filter for not equals to VALUE",
    },
    {
        'human': ['contains'],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': 0,
        'help': "Filter for contains VALUE (adds .* before and after VALUE)",
    },
    {
        'human': [
            'does not contain', 'doesnotcontain', 'not contains', 'notcontains'
        ],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'post_value': '.*',
        'not_flag': 1,
        'help': "Filter for does not contain VALUE (adds .* before and after VALUE)",
    },
    {
        'human': ['starts with', 'startswith'],
        'operator': 'RegexMatch',
        'post_value': '.*',
        'not_flag': 0,
        'help': "Filter for starts with VALUE (adds .* after VALUE)",
    },
    {
        'human': [
            'does not start with', 'doesnotstartwith', 'not starts with',
            'notstartswith',
        ],
        'operator': 'RegexMatch',
        'post_value': '.*',
        'not_flag': 1,
        'help': "Filter for does not start with VALUE (adds .* after VALUE)",
    },
    {
        'human': ['ends with', 'endswith'],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'not_flag': 0,
        'help': "Filter for ends with VALUE (adds .* before VALUE)",
    },
    {
        'human': [
            'does not end with', 'doesnotendwith', 'not ends with',
            'notstartswith',
        ],
        'operator': 'RegexMatch',
        'pre_value': '.*',
        'not_flag': 1,
        'help': "Filter for does bit end with VALUE (adds .* before VALUE)",
    },
    {
        'human': [
            'is not', 'not regex', 'notregex', 'not regex match',
            'notregexmatch', 'nre',
        ],
        'operator': 'RegexMatch',
        'not_flag': 1,
        'help': "Filter for non regular expression match for VALUE",
    },
    {
        'human': ['is', 'regex', 'regex match', 'regexmatch', 're'],
        'operator': 'RegexMatch',
        'not_flag': 0,
        'help': "Filter for regular expression match for VALUE",
    },
]
"""
Maps a given set of human strings into the various filter attributes used by the SOAP API. Also used to verify that a manually supplied filter via a definition is valid. Construct:
    * human: a list of human strings that can be used after '`, that`'. Ex: '`, that` ``contains`` ``value``'
    * operator: the filter operator used by the SOAP API when building a filter that matches `human`
    * not_flag: the value to set on `not_flag` when building a filter that matches `human`
    * pre_value: the prefix to add to the ``value`` when building a filter
    * post_value: the postfix to add to the ``value`` when building a filter
"""

OPTION_MAPS = [
    {
        'human': 'ignore_case',
        'attrs': {'ignore_case_flag': 1},
        'destination': 'filter',
        'valid_type': int,
        'help': "Make the filter do a case insensitive match",
    },
    {
        'human': 'match_case',
        'attrs': {'ignore_case_flag': 0},
        'destination': 'filter',
        'valid_type': int,
        'help': "Make the filter do a case sensitive match",
    },
    {
        'human': 'match_any_value',
        'attrs': {'all_values_flag': 0, 'all_times_flag': 0},
        'destination': 'filter',
        'valid_type': int,
        'help': "Make the filter match any value",
    },
    {
        'human': 'match_all_values',
        'attrs': {'all_values_flag': 1, 'all_times_flag': 1},
        'destination': 'filter',
        'valid_type': int,
        'help': "Make the filter match all values",
    },
    {
        'human': 'max_data_age',
        'attr': 'max_age_seconds',
        'human_type': 'seconds',
        'valid_type': int,
        'destination': 'filter',
        'help': "Re-fetch cached values older than N seconds",
    },
    {
        'human': 'value_type',
        'attr': 'value_type',
        'human_type': 'value_type',
        'valid_values': 'pytan.constants.SENSOR_TYPE_MAP.values()',
        'destination': 'filter',
        'valid_type': str,
        'help': "Make the filter consider the value type as VALUE_TYPE",
    },
    {
        'human': 'and',
        'attrs': {'and_flag': 1},
        'destination': 'group',
        'valid_type': int,
        'help': "Use 'and' for all of the filters supplied",
    },
    {
        'human': 'or',
        'attrs': {'and_flag': 0},
        'destination': 'group',
        'valid_type': int,
        'help': "Use 'or' for all of the filters supplied",
    },
]
"""
Maps a given human string into the various options for filters used by the SOAP API. Also used to verify that a manually supplied option via a definition is valid. Construct:
    * human: the human string that can be used after '`opt:`'. Ex: '`opt`:``value_type``:``value``'
    * destination: the type of object this option can be applied to (filter or group)
    * attrs: the attributes and their values used by the SOAP API when building a filter with an option that matches `human`
    * attr: the attribute used by the SOAP API when building a filter with an option that matches `human`. ``value`` is pulled from after a `:` when only attr exists for an option map, and not attrs.
    * valid_values: if supplied, the list of valid values for this option
    * valid_type: performs type checking on the value supplied to verify it is correct
    * human_type: the human string for the value type if the option requires a value
"""
