#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Encrypt/decrypt module for :mod:`pytan`"""

import base64


def vig_encode(key, string):
    """Obfuscates a string with a key using Vigenere cipher.

    Only useful for obfuscation, not real security!!

    Parameters
    ----------
    key : str
        * key to scrambled string with
    string : str
        * string to scramble with key

    Returns
    -------
    encoded_string : str
        * encoded string
    """
    string = str(string)
    encoded_chars = []
    for i in xrange(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    v_string = "".join(encoded_chars)
    encoded_string = base64.urlsafe_b64encode(v_string)
    encoded_string = '::{}::'.format(encoded_string)
    return encoded_string


def vig_decode(key, string):
    """De-obfuscates a string with a key using Vigenere cipher.

    Only useful for obfuscation, not real security!!

    Notes
    -----
    This will only work with strings that have been encoded with vig_encode(). "normal" strings will be returned as-is.

    Parameters
    ----------
    key : str
        * key that string is scrambled with
    string : str
        * string to unscramble with key

    Returns
    -------
    decoded_string : str
        * decoded string
    """
    if string.startswith('::') and string.endswith('::'):
        string = str(string[2:-2])
    else:
        return string

    v_string = base64.urlsafe_b64decode(string)

    decoded_chars = []
    for i in xrange(len(v_string)):
        key_c = key[i % len(key)]
        encoded_c = chr(abs(ord(v_string[i]) - ord(key_c) % 256))
        decoded_chars.append(encoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string
