"""This is a regex based XML cleaner that will replace unsupported characters"""
import sys
import re
import logging

# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    unichr = chr  # noqa
    binary_type = bytes  # noqa

    def b(s):  # noqa
        return s.encode("latin-1")

    def u(s):  # noqa
        return s
else:
    string_types = basestring,  # noqa
    unichr = unichr  # noqa
    binary_type = str  # noqa

    def b(s):  # noqa
        return s

    # Workaround for standalone backslash
    def u(s):
        return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")  # noqa


mylog = logging.getLogger(__name__)

XML_1_0_VALID_HEX = [
    [0x0009],  # TAB
    [0x000A],  # LINEFEED
    [0x000D],  # CARRIAGE RETURN
    [0x0020, 0xD7FF],  # VALID CHARACTER RANGE 1
    [0xE000, 0xFFFD],  # VALID CHARACTER RANGE 2
]
"""Valid Unicode characters for XML documents:
    (any Unicode character, excluding the surrogate blocks, FFFE, and FFFF)
    #x9,
    #xA,
    #xD,
    [#x20-#xD7FF],
    [#xE000-#xFFFD],
    [#x10000-#x10FFFF]

Source: http://www.w3.org/TR/REC-xml/#NT-Char
"""

XML_1_0_RESTRICT_HEX = [
    [0x007F, 0x0084],  # one C0 control character and all but one C1 control
    [0x0086, 0x009F],  # one C0 control character and all but one C1 control
    [0xFDD0, 0xFDEF],  # control characters/permanently assigned to non-characters
]
"""Restricted/discouraged Unicode characters for XML documents:
    [#x7F-#x84],
    [#x86-#x9F],
    [#xFDD0-#xFDEF],
    [#x1FFFE-#x1FFFF],
    [#x2FFFE-#x2FFFF],
    [#x3FFFE-#x3FFFF],
    [#x4FFFE-#x4FFFF],
    [#x5FFFE-#x5FFFF],
    [#x6FFFE-#x6FFFF],
    [#x7FFFE-#x7FFFF],
    [#x8FFFE-#x8FFFF],
    [#x9FFFE-#x9FFFF],
    [#xAFFFE-#xAFFFF],
    [#xBFFFE-#xBFFFF],
    [#xCFFFE-#xCFFFF],
    [#xDFFFE-#xDFFFF],
    [#xEFFFE-#xEFFFF],
    [#xFFFFE-#xFFFFF],
    [#x10FFFE-#x10FFFF]

Source: http://www.w3.org/TR/REC-xml/#NT-Char
"""

# If this python build supports unicode ranges above 10000, add to the valid range
if sys.maxunicode > 0x10000:
    XML_1_0_VALID_HEX.append((0x10000, min(sys.maxunicode, 0x10FFFF)))

# Add control characters and non-characters to the restricted range if this python
# build supports the applicable range
for i in [hex(i) for i in range(1, 17)]:
    if not sys.maxunicode >= int('{}FFFF'.format(i), 0):
        continue
    XML_1_0_RESTRICT_HEX.append([
        int('{}FFFE'.format(i), 0),
        int('{}FFFF'.format(i), 0),
    ])

XML_1_0_VALID_UNI_LIST = ['-'.join([unichr(y) for y in x]) for x in XML_1_0_VALID_HEX]
"""A list of valid unicode characters"""

XML_1_0_VALID_UNI_TEXT = u('').join(XML_1_0_VALID_UNI_LIST)
"""The text string containing valid unicode characters"""

INVALID_UNICODE_RAW_RE = u(r'[^{}]').format(XML_1_0_VALID_UNI_TEXT)
"""The raw regex string to use when replacing invalid characters"""

INVALID_UNICODE_RE = re.compile(INVALID_UNICODE_RAW_RE, re.U)
"""The regex object to use when replacing invalid characters"""

XML_1_0_RESTRICT_UNI_LIST = ['-'.join([unichr(y) for y in x]) for x in XML_1_0_RESTRICT_HEX]
"""A list of restricted unicode characters"""

XML_1_0_RESTRICT_UNI_TEXT = u('').join(XML_1_0_RESTRICT_UNI_LIST)
"""The text string containing restricted unicode characters"""

RESTRICT_UNICODE_RAW_RE = u(r'[{}]').format(XML_1_0_RESTRICT_UNI_TEXT)
"""The raw regex string to use when replacing restricted characters"""

RESTRICT_UNICODE_RE = re.compile(RESTRICT_UNICODE_RAW_RE, re.U)
"""The regex object to use when replacing restricted characters"""

DEFAULT_REPLACEMENT = u('\uFFFD')
"""The default character to use when replacing characters"""

DEFAULT_ENCODING = 'utf-8'
"""The default encoding to use if none supplied"""


def fix_string_type(text, **kwargs):
    """pass."""
    encoding = kwargs.get('encoding', DEFAULT_ENCODING)
    result = text
    if isinstance(text, binary_type):
        try:
            # if orig_str is not unicode, decode the string into unicode with encoding
            result = text.decode(encoding, 'xmlcharrefreplace')
        except:
            m = "Falling back to latin1 for decoding, unable to decode as UTF-8!"
            mylog.warning(m)
            try:
                # if can't decode as encoding, fallback to latin1
                result = text.decode('latin1', 'xmlcharrefreplace')
            except:
                m = "Unable to decode as latin-1 or UTF-8, decoding as UTF-8 and ignoring errors"
                mylog.warning(m)
                result = u(text, 'utf-8', errors='ignore')
    return result


def xml_cleaner(text, **kwargs):
    """Removes invalid /restricted characters per XML 1.0 spec

    Parameters
    ----------
    s : str
        * str to clean
    encoding : str, optional
        * default: 'utf-8'
        * encoding of `s`
    clean_xml_restricted : bool, optional
        * default: True
        * remove restricted characters from `s` or not

    Returns
    -------
    str
        * the cleaned version of `s`
    """
    clean_xml_restricted = kwargs.get('clean_xml_restricted', True)
    clean_xml_invalid = kwargs.get('clean_xml_invalid', True)
    xml_replace_char = kwargs.get('xml_replace_char', DEFAULT_REPLACEMENT)

    result = text
    if clean_xml_invalid or clean_xml_restricted:
        kwargs['text'] = text
        result = fix_string_type(**kwargs)

        # encode the string as utf-8
        result = text.encode('utf-8', 'xmlcharrefreplace')

        # decode the string from utf-8 into unicode
        result = result.decode('utf-8', 'xmlcharrefreplace')

    if clean_xml_invalid:
        # replace any invalid unicode characters
        result, cnt = INVALID_UNICODE_RE.subn(xml_replace_char, result)

        # if any invalid characters found, print how many were replaced
        if cnt:
            m = "Replaced {} invalid characters that match regex {!r}"
            m = m.format(cnt, INVALID_UNICODE_RE.pattern)
            mylog.info(m)

    if clean_xml_restricted:
        # replace any restricted unicode characters
        result, cnt = RESTRICT_UNICODE_RE.subn(xml_replace_char, text)

        # if any restricted characters found, print how many were replaced
        if cnt:
            m = "Replaced {} restricted characters that match the regex {!r}"
            m = m.format(cnt, RESTRICT_UNICODE_RE.pattern)
            mylog.info(m)

    return result
