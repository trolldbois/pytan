import re
import logging

from pytan import PytanError, string_types

from pytan.constants import SUPER_VERBOSE
from pytan.parsers.constants import (
    SHORT_TOKENS, SEARCH_SPEC_TOKENS, FILTER_SPEC_TOKENS, GROUP_SPEC_TOKENS, LOT_SPEC_TOKENS
)

MYLOG = logging.getLogger(__name__)

ESCAPED_COMMAS = r'(?<!\\),'
ESCAPED_COMMAS_RE = re.compile(ESCAPED_COMMAS)


class TokenizeError(PytanError):
    pass


class Tokenize(object):

    def __init__(self, orig_str, unnamed_key='value'):
        if not isinstance(orig_str, string_types):
            err = "Must supply a string to turn into tokens! Supplied type {!r}; value {!r}"
            err = err.format(type(orig_str).__name__, orig_str)
            MYLOG.error(err)
            raise TokenizeError(err)

        self.UNNAMED_KEY = unnamed_key
        self.ORIG_STR = orig_str
        self.TOKENS = tokens = self.get_tokens(orig_str)
        self.RESULT = self.parse_tokens(tokens)
        m = "Parsed string '{}' into tokens: {!r}"
        m = m.format(orig_str, self.RESULT)
        MYLOG.info(m)

    def get_tokens(self, orig_str):
        result = ESCAPED_COMMAS_RE.split(orig_str)
        result = [x.lstrip() for x in result]
        if SUPER_VERBOSE:
            m = "{} Discovered {} tokens in string: '{}'"
            m = m.format(self.me, len(result), orig_str)
            MYLOG.debug(m)
        return result

    def parse_tokens(self, tokens):
        result = [self.parse_token(t) for t in self.TOKENS]
        return result

    def parse_token(self, token):
        if ':' in token:
            key, value = token.split(':', 1)
        else:
            key, value = self.UNNAMED_KEY, token
        key = self.map_key(key)
        result = (key, value)
        if SUPER_VERBOSE:
            m = "{} Parsed token {!r} into: {!r}"
            m = m.format(self.me, token, result)
            MYLOG.debug(m)
        return result

    def map_key(self, key):
        key = key.lower().strip()
        if key in SHORT_TOKENS:
            key = SHORT_TOKENS[key]
        return key

    @property
    def me(self):
        me = self.__class__.__name__
        result = "{}()"
        result = result.format(me)
        return result


def search_spec_from_tokens(tokens):
    idx_tracker = {}
    result = {}
    for token in tokens:
        key, value = token
        if key not in SEARCH_SPEC_TOKENS:
            continue
        if key in idx_tracker:
            idx = idx_tracker[key] + 1
        else:
            idx = 0
        idx_tracker[key] = idx
        result[idx] = result.get(idx, {})
        result[idx][key] = value
        m = "search_spec_from_tokens(): Associated token {!r} with sub spec index {}: {}"
        m = m.format(token, idx, result[idx])
        MYLOG.debug(m)
    result = [v for k, v in sorted(result.items())]
    m = "search_spec_from_tokens(): Created spec {!r} from parsed tokens {!r}"
    m = m.format(result, tokens)
    MYLOG.debug(m)
    return result


def filter_spec_from_tokens(tokens):
    result = {}
    for token in tokens:
        key, value = token
        if key not in FILTER_SPEC_TOKENS:
            continue
        real_key = FILTER_SPEC_TOKENS[key]
        if real_key not in result:
            result[real_key] = value
    m = "filter_spec_from_tokens(): Created spec {!r} from parsed tokens {!r}"
    m = m.format(result, tokens)
    MYLOG.debug(m)
    return result


def named_param_spec_from_tokens(tokens):
    result = {}
    for token in tokens:
        key, value = token
        if key != 'param' or ':' not in value:
            continue
        param_key, param_value = value.split(':', 1)
        result[param_key] = param_value
    m = "named_params_spec_from_tokens(): Created spec {!r} from parsed tokens {!r}"
    m = m.format(result, tokens)
    MYLOG.debug(m)
    return result


def unnamed_param_spec_from_tokens(tokens):
    values = []
    for token in tokens:
        key, value = token
        if key != 'param' or ':' in value:
            continue
        values.append(value)
    result = {'values': values}
    m = "unnamed_params_spec_from_tokens(): Created spec {!r} from parsed tokens {!r}"
    m = m.format(result, tokens)
    MYLOG.debug(m)
    return result


def lot_spec_from_tokens(tokens):
    result = {}
    for token in tokens:
        key, value = token
        if key not in LOT_SPEC_TOKENS:
            continue
        result[key] = value
    m = "lot_spec_from_tokens(): Created spec {!r} from parsed tokens {!r}"
    m = m.format(result, tokens)
    MYLOG.debug(m)
    return result


def group_spec_from_tokens(tokens):
    result = {}
    for token in tokens:
        key, value = token
        if key not in GROUP_SPEC_TOKENS:
            continue
        result[key] = value
    m = "group_spec_from_tokens(): Created spec {!r} from parsed tokens {!r}"
    m = m.format(result, tokens)
    MYLOG.debug(m)
    return result


def tokenize(orig_str, **kwargs):
    parser = Tokenize(orig_str, **kwargs)
    result = parser.RESULT
    return result


def search_tokenize(orig_str):
    tokens = tokenize(orig_str)
    result = search_spec_from_tokens(tokens)
    return result


def left_tokenize(orig_str):
    tokens = tokenize(orig_str)
    search_spec = search_spec_from_tokens(tokens)
    filter_spec = filter_spec_from_tokens(tokens)
    named_param_spec = named_param_spec_from_tokens(tokens)
    unnamed_param_spec = unnamed_param_spec_from_tokens(tokens)

    if not search_spec:
        err = "No search spec defined in left string '{}'!"
        err = err.format(orig_str)
        MYLOG.error(err)
        raise TokenizeError(err)

    result = {}
    result['search_spec'] = search_spec
    result['filter_spec'] = filter_spec
    result['named_param_spec'] = named_param_spec
    result['unnamed_param_spec'] = unnamed_param_spec
    return result


def right_tokenize(orig_str):
    # if group in tokens, turn into group_spec, otherwise turn into left spec
    tokens = tokenize(orig_str)
    search_spec = search_spec_from_tokens(tokens)
    filter_spec = filter_spec_from_tokens(tokens)
    named_param_spec = named_param_spec_from_tokens(tokens)
    unnamed_param_spec = unnamed_param_spec_from_tokens(tokens)
    group_spec = group_spec_from_tokens(tokens)
    kind = group_spec.get('kind', '')

    if not search_spec:
        err = "No search keys defined in right string '{}'!"
        err = err.format(orig_str)
        MYLOG.error(err)
        raise TokenizeError(err)

    if not filter_spec and not kind == 'group':
        err = "No filter keys defined in right string '{}'!"
        err = err.format(orig_str)
        MYLOG.error(err)
        raise TokenizeError(err)

    result = {}
    result['search_spec'] = search_spec
    result['named_param_spec'] = named_param_spec
    result['unnamed_param_spec'] = unnamed_param_spec
    result['filter_spec'] = filter_spec
    result['group_spec'] = group_spec
    return result


def lot_tokenize(orig_str):
    tokens = tokenize(orig_str, unnamed_key='lot')
    result = lot_spec_from_tokens(tokens)
    return result
