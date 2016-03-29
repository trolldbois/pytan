
PARAMETER_DEFAULTS = {
    'sensor_delimiter': '||',
    'action_delimiter': '',
    'auto_default': True,
    'extras_allowed': True,
    'missing_prompt': True,  # TODO!!!
}

FILTER_DEFAULTS = {
    'not_flag': None,
    'ignore_case_flag': None,
    'operator': 'RegexMatch',
    'value_type': 'String',
    'max_age_seconds': None,
    'all_values_flag': None,
    'value': None,
}

CACHE_FILTER_DEFAULTS = {
    'field': None,
    'value': None,
    'operator': 'RegexMatch',
    'type': 'String',
    'not_flag': None,
}

QUESTION_DEFAULTS = {
    'expire_seconds': None,
    'skip_lock_flag': None,
}

GROUP_DEFAULTS = {
    'and_flag': None,
    'not_flag': None,
}
