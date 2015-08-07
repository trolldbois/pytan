#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""This is a regex based XML cleaner that will replace unsupported characters"""
import sys
import re
import logging

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

mylog = logging.getLogger("XMLCleaner")


class EncodingUnknownError(Exception):
    pass


'''
Source: http://www.w3.org/TR/REC-xml/#NT-Char

Valid Unicode characters for XML documents:
    (any Unicode character, excluding the surrogate blocks, FFFE, and FFFF)
    #x9,
    #xA,
    #xD,
    [#x20-#xD7FF],
    [#xE000-#xFFFD],
    [#x10000-#x10FFFF]

Restricted/discouraged Unicode characters for XML documents:
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
'''

XML_1_0_VALID_HEX = [
    [0x0009],  # TAB
    [0x000A],  # LINEFEED
    [0x000D],  # CARRIAGE RETURN
    [0x0020, 0xD7FF],  # VALID CHARACTER RANGE 1
    [0xE000, 0xFFFD],  # VALID CHARACTER RANGE 2
]

XML_1_0_RESTRICTED_HEX = [
    [0x007F, 0x0084],  # one C0 control character and all but one C1 control
    [0x0086, 0x009F],  # one C0 control character and all but one C1 control
    [0xFDD0, 0xFDEF],  # control characters/permanently assigned to non-characters
]

# If this python build supports unicode ranges above 10000, add to the valid range
if sys.maxunicode > 0x10000:
    XML_1_0_VALID_HEX.append((0x10000, min(sys.maxunicode, 0x10FFFF)))

# Add control characters and non-characters to the restricted range if this python
# build supports the applicable range
for i in [hex(i) for i in range(1, 17)]:
    if not sys.maxunicode >= int('{}FFFF'.format(i), 0):
        continue
    XML_1_0_RESTRICTED_HEX.append([
        int('{}FFFE'.format(i), 0),
        int('{}FFFF'.format(i), 0),
    ])

XML_1_0_VALID_UNI = ['-'.join([unichr(y) for y in x]) for x in XML_1_0_VALID_HEX]
INVALID_UNICODE_RAW_RE = ur'[^{}]'.format(''.join(XML_1_0_VALID_UNI))
INVALID_UNICODE_RE = re.compile(INVALID_UNICODE_RAW_RE, re.U)

XML_1_0_RESTRICTED_UNI = ['-'.join([unichr(y) for y in x]) for x in XML_1_0_RESTRICTED_HEX]
RESTRICTED_UNICODE_RAW_RE = ur'[{}]'.format(''.join(XML_1_0_RESTRICTED_UNI))
RESTRICTED_UNICODE_RE = re.compile(RESTRICTED_UNICODE_RAW_RE, re.U)
DEFAULT_REPLACEMENT = u'\uFFFD'


def replace_invalid_unicode(text, replacement=None):
    if replacement is None:
        replacement = DEFAULT_REPLACEMENT
    s, cnt = INVALID_UNICODE_RE.subn(replacement, text)
    return s, cnt, INVALID_UNICODE_RE


def replace_restricted_unicode(text, replacement=None):
    if replacement is None:
        replacement = DEFAULT_REPLACEMENT
    s, cnt = RESTRICTED_UNICODE_RE.subn(replacement, text)
    return s, cnt, RESTRICTED_UNICODE_RE


def xml_cleaner(s, encoding='utf-8', clean_restricted=True, log_messages=True,
                show_bad_characters=False, **kwargs):
    """removes invalid /restricted characters per XML 1.0 spec"""

    if type(s) == str:
        try:
            # if orig_str is not unicode, decode the string into unicode with encoding
            s = s.decode(encoding, 'xmlcharrefreplace')
        except:
            if log_messages:
                m = "Falling back to latin1 for decoding, unable to decode as UTF-8!".format
                mylog.warning(m())
            try:
                # if can't decode as encoding, fallback to latin1
                s = s.decode('latin1', 'xmlcharrefreplace')
            except:
                if log_messages:
                    m = (
                        "Unable to decode as latin-1 or UTF-8, decoding document as UTF-8 and "
                        "ignoring errors"
                    ).format
                    mylog.warning(m())
                s = unicode(s, 'utf-8', errors='ignore')

    # encode the string as utf-8
    pass1 = s.encode('utf-8', 'xmlcharrefreplace')

    # decode the string from utf-8 into unicode
    pass2 = pass1.decode('utf-8', 'xmlcharrefreplace')

    # replace any invalid unicode characters
    pass3, pass3_cnt, pass3_re = replace_invalid_unicode(pass2)

    # if any invalid characters found, print how many were replaced
    if pass3_cnt and log_messages:
        m = "Replaced {} invalid characters that match regex {!r}".format
        mylog.warning(m(pass3_cnt, pass3_re.pattern))
        if show_bad_characters and log_messages:
            matches = pass3_re.findall(pass2)
            m = "Invalid characters found: {!r}".format
            mylog.debug(m(matches))

    if not pass3_cnt and log_messages:
        m = "No invalid characters found that match regex {!r}".format
        mylog.debug(m(pass3_re.pattern))

    if not clean_restricted:
        return pass3

    # replace any restricted unicode characters
    pass4, pass4_cnt, pass4_re = replace_restricted_unicode(pass3)

    # if any restricted characters found, print how many were replaced
    if pass4_cnt and log_messages:
        m = (
            "Replaced {} restricted characters that match the regex {!r}"
        ).format
        mylog.warning(m(pass4_cnt, pass4_re.pattern))
        if show_bad_characters and log_messages:
            matches = pass4_re.findall(pass3)
            m = "Restricted characters found: {!r}".format
            mylog.debug(m(matches))

    if not pass4_cnt and log_messages:
        m = "No restricted characters found that match regex {!r}".format
        mylog.debug(m(pass4_re.pattern))

    return pass4
