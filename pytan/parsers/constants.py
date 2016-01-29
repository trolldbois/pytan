DATE_FIELD_FALLBACKS = [
    'start_time',
    'expiration',
    'expiration_time',
    'creation_time',
    'modification_time',
    'mod_time',
    'last_download_progress_time',
    'end_time',
    'last_registration',
]

OP_MAP = {
    'L': {
        'operator': 'Less',
        'not_flag': 0,
        'help': "less than 'VALUE'",
    },
    'NL': {
        'operator': 'Less',
        'not_flag': 1,
        'help': "not less than 'VALUE'",
    },
    'LE': {
        'operator': 'LessEqual',
        'not_flag': 0,
        'help': "less than or equal to 'VALUE'",
    },
    'NLE': {
        'operator': 'LessEqual',
        'not_flag': 1,
        'help': "not less than or equal to 'VALUE'",
    },
    'G': {
        'operator': 'Greater',
        'not_flag': 0,
        'help': "greater than 'VALUE'",
    },
    'NG': {
        'operator': 'Greater',
        'not_flag': 1,
        'help': "not greater than 'VALUE'",
    },
    'GE': {
        'operator': 'GreaterEqual',
        'not_flag': 0,
        'help': "greater than or equal to 'VALUE'",
    },
    'NGE': {
        'operator': 'GreaterEqual',
        'not_flag': 1,
        'help': "not greater than or equal to 'VALUE'",
    },
    'E': {
        'operator': 'Equal',
        'not_flag': 0,
        'help': "equal to 'VALUE'",
    },
    'NE': {
        'operator': 'Equal',
        'not_flag': 1,
        'help': "not equal to 'VALUE'",
    },
    'C': {
        'operator': 'RegexMatch',
        'not_flag': 0,
        'pre_value': '.*',
        'post_value': '.*',
        'help': "matches regex '.*VALUE.*'",
    },
    'NC': {
        'operator': 'RegexMatch',
        'not_flag': 1,
        'pre_value': '.*',
        'post_value': '.*',
        'help': "does not match regex '.*VALUE.*'",
    },
    'SW': {
        'operator': 'RegexMatch',
        'not_flag': 0,
        'pre_value': '.*',
        'help': "matches regex '.*VALUE'",
    },
    'NSW': {
        'operator': 'RegexMatch',
        'not_flag': 1,
        'pre_value': '.*',
        'help': "does not match regex '.*VALUE'",
    },
    'EW': {
        'operator': 'RegexMatch',
        'not_flag': 0,
        'pre_value': '.*',
        'help': "matches regex 'VALUE.*'",
    },
    'NEW': {
        'operator': 'RegexMatch',
        'not_flag': 1,
        'pre_value': '.*',
        'help': "does not match regex 'VALUE.*'",
    },
    'R': {
        'operator': 'RegexMatch',
        'not_flag': 0,
        'help': "matches regex 'VALUE'",
    },
    'NR': {
        'operator': 'RegexMatch',
        'not_flag': 1,
        'help': "does not match regex 'VALUE'",
    },
    'GS': {
        'operator': 'Greater',
        'not_flag': 0,
        'help': 'greater than date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'NGS': {
        'operator': 'Greater',
        'not_flag': 1,
        'help': 'not greater than date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'GSE': {
        'operator': 'GreaterEqual',
        'not_flag': 0,
        'help': 'greater than or equal to date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'NGSE': {
        'operator': 'GreaterEqual',
        'not_flag': 1,
        'help': 'not greater than or equal to date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'LS': {
        'operator': 'Less',
        'not_flag': 0,
        'help': 'less than date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'NLS': {
        'operator': 'Less',
        'not_flag': 1,
        'help': 'not less than date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'LSE': {
        'operator': 'LessEqual',
        'not_flag': 0,
        'help': 'less than or equal to date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'NLSE': {
        'operator': 'LessEqual',
        'not_flag': 1,
        'help': 'not less than or equal to date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'SE': {
        'operator': 'Equal',
        'not_flag': 0,
        'help': 'equal to date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
    'NSE': {
        'operator': 'Equal',
        'not_flag': 1,
        'help': 'not equal to date from seconds in value',
        'value_helper': 'seconds_to_date',
        'field_fallbacks': DATE_FIELD_FALLBACKS,
        'type_fallbacks': {'value_type': 'BESDate', 'type': 'Date'},
    },
}

OPERATORS_PYTAN = {
    '<': OP_MAP['L'],
    'less': OP_MAP['L'],
    'l': OP_MAP['L'],
    '!<': OP_MAP['NL'],
    'not less': OP_MAP['NL'],
    'nl': OP_MAP['NL'],
    '<=': OP_MAP['LE'],
    'less equal': OP_MAP['LE'],
    'le': OP_MAP['LE'],
    '!<=': OP_MAP['NLE'],
    'not less equal': OP_MAP['NLE'],
    'nle': OP_MAP['NLE'],
    '>': OP_MAP['G'],
    'greater': OP_MAP['G'],
    'g': OP_MAP['G'],
    '!>': OP_MAP['NG'],
    'not greater': OP_MAP['NG'],
    'ng': OP_MAP['NG'],
    '=>': OP_MAP['GE'],
    'greater equal': OP_MAP['GE'],
    'ge': OP_MAP['GE'],
    '!=>': OP_MAP['NGE'],
    'not greater equal': OP_MAP['NGE'],
    'nge': OP_MAP['NGE'],
    '=': OP_MAP['E'],
    'equal': OP_MAP['E'],
    'equals': OP_MAP['E'],
    'eq': OP_MAP['E'],
    'e': OP_MAP['E'],
    '!=': OP_MAP['NE'],
    'not equal': OP_MAP['NE'],
    'neq': OP_MAP['NE'],
    'ne': OP_MAP['NE'],
    "~=": OP_MAP['C'],
    "contains": OP_MAP['C'],
    "in": OP_MAP['C'],
    "!~=": OP_MAP['NC'],
    "not contains": OP_MAP['NC'],
    "not in": OP_MAP['NC'],
    "starts": OP_MAP['SW'],
    "starts with": OP_MAP['SW'],
    "sw": OP_MAP['NSW'],
    "not starts": OP_MAP['NSW'],
    "nsw": OP_MAP['NSW'],
    "ends": OP_MAP['EW'],
    "ends with": OP_MAP['EW'],
    "ew": OP_MAP['NEW'],
    "not ends": OP_MAP['NEW'],
    "new": OP_MAP['NEW'],
    "is": OP_MAP['R'],
    "regex": OP_MAP['R'],
    "re": OP_MAP['R'],
    "is not": OP_MAP['NR'],
    "not regex": OP_MAP['NR'],
    "nre": OP_MAP['NR'],
    '>s': OP_MAP['GS'],
    'greater seconds': OP_MAP['GS'],
    '!>s': OP_MAP['NGS'],
    'not greater seconds': OP_MAP['NGS'],
    '>=s': OP_MAP['GSE'],
    'greater equal seconds': OP_MAP['GSE'],
    '!>=s': OP_MAP['NGSE'],
    'not greater equal seconds': OP_MAP['NGSE'],
    '<s': OP_MAP['LS'],
    'less seconds': OP_MAP['LS'],
    '!<s': OP_MAP['NLS'],
    'not less seconds': OP_MAP['NLS'],
    '<=s': OP_MAP['LSE'],
    'less equal seconds': OP_MAP['LSE'],
    '!<=s': OP_MAP['NLSE'],
    'not less equal seconds': OP_MAP['NLSE'],
    '=s': OP_MAP['SE'],
    'equal seconds': OP_MAP['SE'],
    '!=s': OP_MAP['NSE'],
    'not equal seconds': OP_MAP['NSE'],
}

OPERATORS_TANIUM = [
    'Equal', 'Greater', 'GreaterEqual', 'Less', 'LessEqual', 'RegexMatch', 'HashMatch',
]

SPEC_FIELD_FALLBACKS = ['name', 'url_regex']

TRUE_TYPES = (1, True, "yes", "y", "true", "t", "1")
FALSE_TYPES = (0, False, "no", "n", "false", "f", "0")

TYPES_MAP = {
    'S': {'t': 'String', 'h': 'standard lexicographical comparison (the default)'},
    'V': {'t': 'Version', 'h': 'version strings, e.g. 9.4.2 is less than 10.1.3'},
    'N': {'t': 'Numeric', 'h': 'numeric, decimal, floating point, and scientific notation'},
    'I': {'t': 'IPAddress', 'h': 'IP addresses'},
    'D': {'t': 'Date', 'h': 'a date in the format YYYY-MM-DD HH:MM:SS'},
    'BD': {'t': 'BESDate', 'h': 'a date in the format YYYY-MM-DD HH:MM:SS'},
    'WD': {'t': 'WMIDate', 'h': 'a date in the format yyyymmddHHMMSS.xxxxxx(+/-)UUU'},
    'TD': {
        't': 'TimeDiff',
        'h': 'amount of time, e.g. 2 years, 3 months, 18 days, 4 hours, 22 minutes, and 3.67 '
        'seconds, e.g. 4.2 hours (int + Y|MO|W|D|H|M|S)'},
    'DS': {'t': 'DataSize', 'h': 'data size, e.g. 125MB, 23K, 34.2 Gig (int + B|K|M|G|T)'},
    'NI': {'t': 'NumericInteger', 'h': 'be integer numeric values'},
}

CF_TYPES = {
    'string': TYPES_MAP['S'],
    'version': TYPES_MAP['V'],
    'numeric': TYPES_MAP['N'],
    'ipaddress': TYPES_MAP['I'],
    'date': TYPES_MAP['D'],
    'datasize': TYPES_MAP['DS'],
    'numericinteger': TYPES_MAP['NI'],
}

FILTER_VALUE_TYPES = {
    'string': TYPES_MAP['S'],
    'version': TYPES_MAP['V'],
    'numeric': TYPES_MAP['N'],
    'date': TYPES_MAP['BD'],
    'ipaddress': TYPES_MAP['I'],
    'wmidate': TYPES_MAP['WD'],
    'timediff': TYPES_MAP['TD'],
    'datasize': TYPES_MAP['DS'],
    'numericinteger': TYPES_MAP['NI'],
}

SHORT_TOKENS = {
    # get
    'f': 'field',
    't': 'type',
    'n': 'not_flag',
    'not': 'not_flag',
    'o': 'operator',
    'op': 'operator',
    'v': 'value',
    'val': 'value',  # unnamed on left, right, and get
    # left/right
    'p': 'param',
    'fa': 'filter_any_value',
    'fi': 'filter_ignore_case',
    'fm': 'filter_max_age',
    'fn': 'filter_not',
    'fo': 'filter_operator',
    'fv': 'filter_value',
    'fvt': 'filter_value_type',
    # right
    'k': 'kind',
    'l': 'lot',
    # lot
    'a': 'and_flag',
    'and': 'and_flag',
}

SEARCH_SPEC_TOKENS = ['value', 'field', 'type', 'not_flag', 'operator']
GROUP_SPEC_TOKENS = ['kind', 'lot']
KIND_VALUES = ['sensor', 'group']
LOT_SPEC_TOKENS = ['lot', 'and_flag', 'not_flag']

FILTER_SPEC_TOKENS = {
    'filter_value': 'value',
    'filter_not': 'not_flag',
    'filter_ignore_case': 'ignore_case_flag',
    'filter_max_age': 'max_age_seconds',
    'filter_all_values': 'all_values_flag',
    'filter_operator': 'operator',
    'filter_type': 'value_type',
}
