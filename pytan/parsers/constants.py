OPERATORS_PYTAN_MAPS = {
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
}

OPERATORS_PYTAN = {
    '<': OPERATORS_PYTAN_MAPS['L'],
    'less': OPERATORS_PYTAN_MAPS['L'],
    'l': OPERATORS_PYTAN_MAPS['L'],
    '!<': OPERATORS_PYTAN_MAPS['NL'],
    'not less': OPERATORS_PYTAN_MAPS['NL'],
    'notless': OPERATORS_PYTAN_MAPS['NL'],
    'nl': OPERATORS_PYTAN_MAPS['NL'],
    '<=': OPERATORS_PYTAN_MAPS['LE'],
    'less equal': OPERATORS_PYTAN_MAPS['LE'],
    'lessequal': OPERATORS_PYTAN_MAPS['LE'],
    'le': OPERATORS_PYTAN_MAPS['LE'],
    '!<=': OPERATORS_PYTAN_MAPS['NLE'],
    'not less equal': OPERATORS_PYTAN_MAPS['NLE'],
    'notlessequal': OPERATORS_PYTAN_MAPS['NLE'],
    'nle': OPERATORS_PYTAN_MAPS['NLE'],
    '>': OPERATORS_PYTAN_MAPS['G'],
    'greater': OPERATORS_PYTAN_MAPS['G'],
    'g': OPERATORS_PYTAN_MAPS['G'],
    '!>': OPERATORS_PYTAN_MAPS['NG'],
    'not greater': OPERATORS_PYTAN_MAPS['NG'],
    'notgreater': OPERATORS_PYTAN_MAPS['NG'],
    'ng': OPERATORS_PYTAN_MAPS['NG'],
    '=>': OPERATORS_PYTAN_MAPS['GE'],
    'greater equal': OPERATORS_PYTAN_MAPS['GE'],
    'greaterequal': OPERATORS_PYTAN_MAPS['GE'],
    'ge': OPERATORS_PYTAN_MAPS['GE'],
    '!=>': OPERATORS_PYTAN_MAPS['NGE'],
    'not greater equal': OPERATORS_PYTAN_MAPS['NGE'],
    'notgreaterequal': OPERATORS_PYTAN_MAPS['NGE'],
    'nge': OPERATORS_PYTAN_MAPS['NGE'],
    '=': OPERATORS_PYTAN_MAPS['E'],
    'equal': OPERATORS_PYTAN_MAPS['E'],
    'equals': OPERATORS_PYTAN_MAPS['E'],
    'eq': OPERATORS_PYTAN_MAPS['E'],
    'e': OPERATORS_PYTAN_MAPS['E'],
    '!=': OPERATORS_PYTAN_MAPS['NE'],
    'not equal': OPERATORS_PYTAN_MAPS['NE'],
    'notequal': OPERATORS_PYTAN_MAPS['NE'],
    'not equals': OPERATORS_PYTAN_MAPS['NE'],
    'notequals': OPERATORS_PYTAN_MAPS['NE'],
    'neq': OPERATORS_PYTAN_MAPS['NE'],
    'ne': OPERATORS_PYTAN_MAPS['NE'],
    "~=": OPERATORS_PYTAN_MAPS['C'],
    "contains": OPERATORS_PYTAN_MAPS['C'],
    "in": OPERATORS_PYTAN_MAPS['C'],
    "!~=": OPERATORS_PYTAN_MAPS['NC'],
    "not contains": OPERATORS_PYTAN_MAPS['NC'],
    "not in": OPERATORS_PYTAN_MAPS['NC'],
    "starts": OPERATORS_PYTAN_MAPS['SW'],
    "starts with": OPERATORS_PYTAN_MAPS['SW'],
    "sw": OPERATORS_PYTAN_MAPS['NSW'],
    "not starts": OPERATORS_PYTAN_MAPS['NSW'],
    "not starts with": OPERATORS_PYTAN_MAPS['NSW'],
    "nsw": OPERATORS_PYTAN_MAPS['NSW'],
    "ends": OPERATORS_PYTAN_MAPS['EW'],
    "ends with": OPERATORS_PYTAN_MAPS['EW'],
    "ew": OPERATORS_PYTAN_MAPS['NEW'],
    "not ends": OPERATORS_PYTAN_MAPS['NEW'],
    "not ends with": OPERATORS_PYTAN_MAPS['NEW'],
    "new": OPERATORS_PYTAN_MAPS['NEW'],
    "is": OPERATORS_PYTAN_MAPS['R'],
    "regex": OPERATORS_PYTAN_MAPS['R'],
    "regex match": OPERATORS_PYTAN_MAPS['R'],
    "re": OPERATORS_PYTAN_MAPS['R'],
    "is not": OPERATORS_PYTAN_MAPS['NR'],
    "not regex": OPERATORS_PYTAN_MAPS['NR'],
    "not regex match": OPERATORS_PYTAN_MAPS['NR'],
    "nre": OPERATORS_PYTAN_MAPS['NR'],
}

OPERATORS_TANIUM = ['Equal', 'Greater', 'GreaterEqual', 'Less', 'LessEqual', 'RegexMatch']

SPEC_FIELD_FALLBACKS = ['name', 'url_regex']

TRUE_TYPES = (1, True, "yes", "y", "true", "t", "1")
FALSE_TYPES = (0, False, "no", "n", "false", "f", "0")


FIELD_TYPES_MAP = {
    'S': {'t': 'String', 'h': 'standard lexicographical comparison (the default)'},
    'V': {'t': 'Version', 'h': 'version strings, e.g. 9.4.2 is less than 10.1.3'},
    'N': {'t': 'Numeric', 'h': 'numeric, decimal, floating point, and scientific notation'},
    'I': {'t': 'IPAddress', 'h': 'IP addresses'},
    'D': {'t': 'Date', 'h': 'a date in the format YYYY-MM-DD HH:MM:SS'},
    'DS': {'t': 'DataSize', 'h': 'data size, e.g. 125MB, 23K, 34.2 Gig (int + B|K|M|G|T)'},
    'NI': {'t': 'NumericInteger', 'h': 'be integer numeric values'},
}

FIELD_TYPES = {
    'string': FIELD_TYPES_MAP['S'],
    'version': FIELD_TYPES_MAP['V'],
    'numeric': FIELD_TYPES_MAP['N'],
    'ipaddress': FIELD_TYPES_MAP['I'],
    'date': FIELD_TYPES_MAP['D'],
    'datasize': FIELD_TYPES_MAP['DS'],
    'numericinteger': FIELD_TYPES_MAP['NI'],
}

ESCAPED_COMMAS = r'(?<!\\),'

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
}
