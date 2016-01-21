import re
import logging

MYLOG = logging.getLogger(__name__)

from pytan.parsers.constants import ESCAPED_COMMAS, SHORT_TOKENS

ESCAPED_COMMAS_RE = re.compile(ESCAPED_COMMAS)


class TokenParser(object):

    def __init__(self, orig_str, **kwargs):
        self.UNNAMED_KEY = kwargs.get('unnamed_key', 'value')
        self.ORIG_STR = orig_str
        self.TOKENS = tokens = self.get_tokens(orig_str)
        self.PARSED_TOKENS = parsed_tokens = self.parse_tokens(tokens)
        self.RESULT = self.get_result(parsed_tokens)

    def get_result(self, parsed_tokens):
        result = parsed_tokens
        return result

    def get_tokens(self, orig_str):
        result = ESCAPED_COMMAS_RE.split(orig_str)
        result = [x.lstrip() for x in result]
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
        m = "{} Parsed token {!r} into: {!r}"
        m = m.format(self.me, token, result)
        MYLOG.debug(m)
        return result

    def map_key(self, key):
        key = key.lower().strip()
        if key in SHORT_TOKENS:
            key = SHORT_TOKENS[key]
        if key.startswith('p_'):
            key = key.replace('p_', 'param_')
        return key

    @property
    def me(self):
        me = self.__class__.__name__
        result = "{}()"
        result = result.format(me)
        return result


class FindTokenParser(TokenParser):

    def get_result(self, parsed_tokens):
        spec_tokens = ['value', 'field', 'type', 'not_flag', 'operator']
        idx_tracker = {}
        result = {}
        for token in parsed_tokens:
            key, value = token
            if key not in spec_tokens:
                continue
            if key in idx_tracker:
                idx = idx_tracker[key] + 1
            else:
                idx = 0
            idx_tracker[key] = idx
            result[idx] = result.get(idx, {})
            result[idx][key] = value
            m = "{} Associated token {!r} with sub spec index {}: {}"
            m = m.format(self.me, token, idx, result[idx])
            MYLOG.debug(m)

        result = [v for k, v in sorted(result.items())]
        return result


def token_parser(orig_str, **kwargs):
    parser = TokenParser(orig_str, **kwargs)
    result = parser.RESULT
    return result


def find_token_parser(orig_str, **kwargs):
    parser = FindTokenParser(orig_str, **kwargs)
    result = parser.RESULT
    return result
