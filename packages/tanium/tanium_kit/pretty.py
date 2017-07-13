"""Homegrown utility libraries for tanium_pam4."""
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging

LOG = logging.getLogger(__name__.split(".")[-1])

GUESS_MAP = {"{": "json", "[": "json", "<": "xml"}
"""Dict that maps first character in ``text`` to a given type if ``text_type`` == 'guess'."""

TEXT_TYPE_MAP = {
    "xml": ["pretty_xml"],  # ``text_type`` of 'xml' will try xml only
    "json": ["pretty_json"],  # ``text_type`` of 'json' will try json only
    "brute": ["pretty_xml", "pretty_json"],  # ``text_type`` of 'brute' will try xml THEN json
    "guess": [],  # listed here only because it is a valid text_type
}
"""Dict that maps ``text_type`` to a list of functions to try to pretty ``text`` with."""


def pretty_xml(text, **kwargs):
    """Die."""
    text = to_xml(from_xml(text, **kwargs), **kwargs)
    return text


def pretty_json(text, **kwargs):
    """Die."""
    text = to_json(from_json(text, **kwargs), **kwargs)
    return text


def from_xml(text, **kwargs):
    """Die."""
    import xmltodict  # EXTERNAL PACKAGE DEPENDENCY
    obj = xmltodict.parse(text)
    return obj


def to_xml(obj, pretty=True, indent="  ", **kwargs):
    """Die."""
    import xmltodict  # EXTERNAL PACKAGE DEPENDENCY
    text = xmltodict.unparse(obj, pretty=pretty, indent=indent)
    return text


def from_json(text, **kwargs):
    """Die."""
    obj = json.loads(text)
    return obj


def to_json(obj, indent=2, sort_keys=True, skipkeys=True, **kwargs):
    """Die."""
    text = json.dumps(obj, indent=indent, sort_keys=sort_keys, skipkeys=skipkeys)
    return text


def pretty_text(text, name="text", text_type="guess", **kwargs):
    """Try to pretty ``text`` as ``text_type``.

    Notes
    ------
    * Errors during prettifying get wrapped, logged, and ignored.
    * If text_type is not in :data:`TEXT_TYPE_MAP`, text is returned unchanged.
    * If text is empty, text is returned unchanged.

    Parameters
    ----------
    text : str
        * text to pretty
    name : str, optional
        * human name to refer to ``text`` as
    text_type : str, optional
        * default : guess
        * type of ``text`` to try and pretty as

    Returns
    -------
    text : str
        * prettified ``text`` as ``text_type``, if possible
    """
    # do not try to pretty empty text
    if not text:
        return text

    # try to guess ``text_type`` based off of the first non-whitespace character of ``text``
    if text_type == "guess":
        # get the first non-whitespace character of ``text``
        first_char = text.strip()[0]
        # get the corresponding value of ``first_char`` from ``guess_map``
        text_type = GUESS_MAP.get(first_char, "unknown")
        m = "Guessed text type of {} as '{}' by looking at character '{}'"
        LOG.debug(m.format(name, text_type, first_char))

    # get the list of functions to try to pretty ``text`` with
    try_types = TEXT_TYPE_MAP.get(text_type, [])

    # if try_types is an empty list, ``text_type`` is not supported
    if not try_types:
        m = "pretty text of '{}' to '{}' unsupported (must be one of: {})"
        LOG.warning(m.format(name, text_type, ', '.join(TEXT_TYPE_MAP)))
        return text

    for try_type in try_types:
        try_func = globals()[try_type]
        try:
            text = try_func(text, **kwargs)
            m = "{} to '{}' using '{}' successful"
            LOG.debug(m.format(name, text_type, try_type))
            break
        except Exception as e:
            m = "{} to '{}' using '{}' unsuccessful, error: {}"
            LOG.warning(m.format(name, text_type, try_type, e))
            continue
    return text
