"""A regex based XML cleaner that will replace unsupported characters."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import re
import sys

_VERSION = sys.version_info
IS_PY2 = _VERSION[0] == 2
IS_PY3 = _VERSION[0] == 3

if IS_PY2:
    string_types = basestring,  # noqa
    integer_types = (int, long)  # noqa
    text_type = unicode  # noqa
    unichr = unichr  # noqa
    binary_type = str
elif IS_PY3:
    string_types = str,
    integer_types = int,
    text_type = str
    binary_type = bytes
    unichr = chr

LOG = logging.getLogger(__name__.split(".")[-1])

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
    if not sys.maxunicode >= int("{}FFFF".format(i), 0):
        continue
    restrict_range = [int("{}FFFE".format(i), 0), int("{}FFFF".format(i), 0)]
    XML_1_0_RESTRICT_HEX.append(restrict_range)

XML_1_0_VALID_UNI_LIST = ["-".join([unichr(y) for y in x]) for x in XML_1_0_VALID_HEX]
"""A list of valid unicode characters"""

XML_1_0_VALID_UNI_TEXT = "".join(XML_1_0_VALID_UNI_LIST)
"""The text string containing valid unicode characters"""

INVALID_UNICODE_RAW_RE = r"[^{}]".format(XML_1_0_VALID_UNI_TEXT)
"""The raw regex string to use when replacing invalid characters"""

INVALID_UNICODE_RE = re.compile(INVALID_UNICODE_RAW_RE, re.U)
"""The regex object to use when replacing invalid characters"""

XML_1_0_RESTRICT_UNI_LIST = [
    "-".join([unichr(y) for y in x]) for x in XML_1_0_RESTRICT_HEX
]
"""A list of restricted unicode characters"""

XML_1_0_RESTRICT_UNI_TEXT = "".join(XML_1_0_RESTRICT_UNI_LIST)
"""The text string containing restricted unicode characters"""

RESTRICT_UNICODE_RAW_RE = r"[{}]".format(XML_1_0_RESTRICT_UNI_TEXT)
"""The raw regex string to use when replacing restricted characters"""

RESTRICT_UNICODE_RE = re.compile(RESTRICT_UNICODE_RAW_RE, re.U)
"""The regex object to use when replacing restricted characters"""

DEFAULT_REPLACEMENT = "\uFFFD"
"""The default character to use when replacing characters"""

DEFAULT_ENCODING = "utf-8"
"""The default encoding to use if none supplied"""

QUOTES_MAP = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
}
"""Mapping of smart quotes to replace with their ascii counterpart."""


def bytes_to_str(text, **kwargs):
    """Die."""
    encoding = kwargs.get("encoding", DEFAULT_ENCODING)
    errors = kwargs.get("encoding_errors", "replace")

    ok = "Decoded from bytes using '{}' errors '{}'{}{}"

    if isinstance(text, binary_type):
        pre = " (pre type '{}' len '{}')".format(type(text).__name__, len(text))
        text = text.decode(encoding, errors)
        post = " (post type '{}' len '{}')".format(type(text).__name__, len(text))
        LOG.debug(ok.format(encoding, errors, pre, post))
    return text


def str_to_bytes(text, **kwargs):
    """Die."""
    encoding = kwargs.get("encoding", DEFAULT_ENCODING)
    errors = kwargs.get("encoding_errors", "xmlcharrefreplace")

    ok = "Encoded to bytes using '{}' errors '{}'{}{}"
    if isinstance(text, string_types):
        pre = " (pre type '{}' len '{}')".format(type(text).__name__, len(text))
        text = text.encode(encoding, errors)
        post = " (post type '{}' len '{}')".format(type(text).__name__, len(text))
        LOG.debug(ok.format(encoding, errors, pre, post))
    return text


def clean_chars(text, name, regex, **kwargs):
    """Die."""
    case = kwargs.get(name, True)
    rc = kwargs.get("clean_char", DEFAULT_REPLACEMENT)

    ok = "[{} = {}] regex: {!r}, replace character {!r}, found {} characters: {!r}{}{}"

    if case:
        matches = regex.findall(text)
        pre = " (pre type '{}' len '{}')".format(type(text).__name__, len(text))
        if matches:
            text = regex.sub(rc, text)
        post = " (post type '{}' len '{}')".format(type(text).__name__, len(text))
        LOG.debug(ok.format(name, case, regex.pattern, rc, len(matches), matches, pre, post))
    return text


def decode_recode(text, **kwargs):
    """Die."""
    keys = ["clean_invalid", "clean_restricted"]
    vals = [kwargs.get(k, True) for k in keys]
    if any(vals):
        # convert our str object back to a bytes object with xmlcharrefreplace
        text = str_to_bytes(text, **kwargs)
        # convert our bytes object back to a str object
        text = bytes_to_str(text, **kwargs)
    return text


def clean_quotes(text, name, **kwargs):
    """Die."""
    case = kwargs.get(name, True)
    if case:
        for k, v in QUOTES_MAP.items():
            text = text.replace(k, v)
    return text


def clean(text, **kwargs):
    """Die."""
    # ensure that any bytes object is a str object
    text = bytes_to_str(text, **kwargs)
    # decode text from str to bytes, and back to str again
    text = decode_recode(text, **kwargs)
    # replace invalid characters using the INVALID XML RE
    text = clean_chars(text, "clean_invalid", INVALID_UNICODE_RE, **kwargs)
    # replace restricted characters using the INVALID XML RE
    text = clean_chars(text, "clean_restricted", RESTRICT_UNICODE_RE, **kwargs)
    # replace smart quotes with normal quotes
    text = clean_quotes(text, "clean_quotes", **kwargs)
    return text


def get_etree():
    """Die."""
    etree = None
    engines = ["xml.etree.cElementTree", "lxml.etree", "xml.etree.ElementTree"]
    for engine in engines:
        if engine in sys.modules:
            etree = sys.modules[engine]
            break

        try:
            __import__(engine)
            etree = sys.modules[engine]
            m = "Using {} for XML engine"
            LOG.debug(m.format(engine))
            break
        except ImportError as e:
            m = "XML engine {} failed to import: {}"
            LOG.warning(m.format(engine, e))

    if etree is None:
        err = "Failed to import any XML Engine!"
        raise Exception(err)
    return etree


def add_console_log():
    """Die."""
    handlers = [LOG.handlers, LOG.parent.handlers]
    if not any(handlers):
        hf = logging.Formatter("[%(name)-12s] [%(funcName)-15s] %(levelname)-8s %(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(hf)
        LOG.addHandler(ch)


if __name__ == "__main__":
    LOG.setLevel(logging.DEBUG)
    add_console_log()
    etree = get_etree()
    TESTS = {
        "XML as bytes with invalid and restricted characters": b"<root><v>TEST.\xc3\xa6\xc2\xad\xc2\xb6\x17\x04\xc3\xa8\xc2\x80\xc2\x80  \x04 \x01h\xc3\xa7\xc2\x8d\xc2\x95\xc3\xa5\xc2\x81\xc2\xa5\xc3\xa7\xc2\x89\xc2\xa1\xc3\xa6\xc2\xa5\xc2\xb4\xc3\xa6\xc2\xb1\xc2\xa1\xc3\xa6\xc2\xb9\xc2\x85\xc3\xa7\xc2\x89\xc2\xa3\xc3\xa7\xc2\x81\xc2\xb9\xc3\xa6\xc2\xa5\xc2\xb4\xc3\xa6\xc2\xb9\xc2\xaf\xc3\xa6\xc2\x95\xc2\x8b</v></root>\r\n",
        "XML as bytes with special double quotes": b"<root>\r\n    <v>Comunica\xc3\xa7\xc3\xa3o com PABX</v>\r\n    <v>\xc3\x90\xc3\x85\xc2\xb3\xc3\x87\xc3\x8d\xc2\xa8\xc3\x97\xc3\x80\xc3\x83\xc3\xa6\xc2\xb0\xc2\xb2\xc3\x88\xc2\xab\xc3\x8c\xc3\x97\xc2\xbc\xc3\xbe V2.7.02</v>\r\n    <v>\xe2\x80\x9cC:\\WINDOWS\\system32\\ctfmon.exe\xe2\x80\x9d</v>\r\n</root>\r\n",
        "XML as bytes with surrogates": b"<root>\r\n    <v>\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\x87\xc2\xb1\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\x83\xc2\xbb\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xad\xc2\xb9\xc2\xa4\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd__\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\x87\xc2\xb1\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\x8f\xc2\xb5\xc3\x8d\xc2\xb3\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\xaf\xc2\xbf\xc2\xbd\xc3\x9e\xc2\xb9\xc3\xaf\xc2\xbf\xc2\xbd\xc3\x8b\xc2\xbe</v>\r\n</root>\r\n",
    }

    x = []
    for test_name, test_data in TESTS.items():
        s = ""
        s += "**********************************\n"
        s += " * TEST NAME: {}\n".format(test_name)
        print(s)

        cleaned = clean(test_data)
        if IS_PY2:
            etree_obj = etree.fromstring(cleaned.encode("utf-8"))
        else:
            etree_obj = etree.fromstring(cleaned)
        etree_bytes = etree.tostring(etree_obj, "utf-8")
        etree_txt = bytes_to_str(etree_bytes)

        s += (
            " * Dirty          string type {!r} ==> {!r}\n"
            " * Cleaned        string type {!r} ==> {!r}\n"
            " * Etree          object type {!r} ==> {!r}\n"
            " * Etree tostring  bytes type {!r} ==> {!r}\n"
            " * Etree tostring    str type {!r} ==> {!r}\n"
            "**********************************\n"
        ).format(
            type(test_data).__name__, test_data,
            type(cleaned).__name__, cleaned,
            type(etree_obj), etree_obj,
            type(etree_bytes).__name__, etree_bytes,
            type(etree_txt).__name__, etree_txt,
        )
        print(s)
        x.append(s)

    for s in x:
        print(s)
