from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import datetime
import hashlib
import os
import re
import shutil
import sys
import traceback

from io import open as uni_open

from . import IS_PY3, integer_types, uni_chr

CRYPT_WRAPPER = "::"
BACKUP_TIMESTAMP = "D%Y-%m-%dT%H-%M-%S-%f"
"""Format of datetime to prefix backup filenames."""


def get_valid_filename(s):
    s = s.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def orig_tb():
    exc_obj = sys.exc_info()

    m = "Original traceback: {}"
    m = m.format(''.join(traceback.format_exception(*exc_obj)))
    return m


def write_uni_file(path, out):
    with uni_open(path, "w", encoding="utf-8") as fh:
        fh.write(out)

    m = "Wrote {} bytes as unicode to file: '{}'".format(len(out), path)
    return m


def write_str_file(path, out):
    with open(path, "w",) as fh:
        fh.write(out)

    m = "Wrote {} bytes as str to file: '{}'".format(len(out), path)
    return m


def read_file(path):
    with uni_open(path, encoding="utf-8") as fh:
        ret = fh.read()
    return ret


def write_file(path, out):
    if IS_PY3:
        m = write_uni_file(path, out)
    else:
        if isinstance(out, str):
            m = write_str_file(path, out)
        else:
            m = write_uni_file(path, out)
    return m


def write_binary(path, out):
    with open(path, "wb") as fh:
        fh.write(out)

    m = "Wrote binary file '{}' as '{}' bytes"
    m = m.format(path, len(out))
    return m


def file_hash(path, hash_type="sha1", blocksize=65536):
    hasher = getattr(hashlib, hash_type)()

    with open(path, "rb") as fh:
        if blocksize:
            out = fh.read(blocksize)
            while len(out) > 0:
                hasher.update(out)
                out = fh.read(blocksize)
        else:
            out = fh.read()
            hasher.update(out)
    ret = hasher.hexdigest()
    return ret


def dict_path(path, source):
    if path.startswith('percentage('):
        points = path.lstrip('percentage(').rstrip(')')
        points = [
            resolve_path(path=p, source=source) for p in points.split(',')
        ]
        try:
            result = get_percentage(part=points[0], whole=points[1])
        except:
            result = ', '.join(points)
    else:
        result = resolve_path(path=path, source=source)
    return result


def get_percentage(part, whole):
    f = 100 * float(part) / float(whole)
    ret = "{0:.2f}%".format(f)
    return ret


def resolve_path(path, source):
    for i in path.split('/'):
        i2 = i.replace(" ", "_")
        if i in source:
            source = source[i]
        elif i2 in source:
            source = source[i2]
        else:
            return "Unable to find path (failed at '{}'): '{}'".format(i, path)
    return source


def b64encode(text):
    """Die."""
    text_bytes = text.encode("utf-8")
    text_enc = base64.b64encode(text_bytes)
    text_ret = text_enc.decode("utf-8")
    return text_ret


def b64decode(text):
    """Die."""
    text_bytes = text.encode("utf-8")
    text_dec = base64.b64decode(text_bytes)
    text_ret = text_dec.decode("utf-8")
    return text_ret


def vignere_cipher(text, key, inverse=False):
    """
    Vigenere Cipher

    The vigenere cipher is a symmetric key cipher that operates as a group of
    Caesar ciphers in sequence with different rotations:

        KEY         == boomboombo
        MESSAGE     == helloworld
        CIPHERTEXT  == jvopbrfqba

    The basic formula is as follows:
        E(m) = ((m1 + k1) % 26, (m2 + k2) % 26, ..., (mi + ki) % 26)
        D(m) = ((c1 - k1) % 26, (c2 - k2) % 26, ..., (ci - ki) % 26)

    Like other naive ciphers, this shouldn't be used. It is however the most
    secure naive cipher. It is helpful for obfuscation to prevent shoulder
    surfing and casual disk scanning of passwords.
    """
    chars = []
    for i in range(len(text)):
        text_char = text[i]
        key_char = key[i % len(key)]
        key_ord = ord(key_char) % 256

        if isinstance(text_char, integer_types):
            text_ord = text_char
        else:
            text_ord = ord(text_char)

        if inverse:
            abs_char = abs(text_ord - key_ord)
            new_char = uni_chr(abs_char)
        else:
            new_char = uni_chr(text_ord + key_ord)

        chars.append(new_char)

    ret = "".join(chars)
    return ret


def obfuscate(text, key, **kwargs):
    wrap = kwargs.get("crypt_wrapper", CRYPT_WRAPPER)

    if not text:
        return text

    if text.startswith(wrap) and text.endswith(wrap):
        return text

    vig_text = vignere_cipher(text=text, key=key, inverse=False)
    base_text = b64encode(vig_text)
    ret = "{0}{1}{0}".format(wrap, base_text)
    return ret


def deobfuscate(text, key, **kwargs):
    wrap = kwargs.get("crypt_wrapper", CRYPT_WRAPPER)

    if not text:
        return text

    if not (text.startswith(wrap) and text.endswith(wrap)):
        return text

    base_text = text.lstrip(wrap).rstrip(wrap)
    vig_text = b64decode(base_text)
    ret = vignere_cipher(text=vig_text, key=key, inverse=True)
    return ret


def int_check(value):
    try:
        ret = int(value)
    except:
        ret = None
    return ret


def makedir(path):
    """Make a directory and all leading directories as needed.

    Parameters
    ----------
    path : :obj:`str`
        * Directory to make
    """
    if not os.path.exists(path):
        m = "Making directory: {}"
        os.makedirs(path)
    else:
        m = "Directory exists: {}"
    m = m.format(path)
    return m


def backup_file(filename, src_dir, dest_dir, **kwargs):
    """Backup a file.

    Parameters
    ----------
    filename : :obj:`str`
        * filename to backup
    src_dir : :obj:`str`
        * path containing file to backup
    dest_dir : :obj:`str`
        * path to backup file to
    timestamp : :obj:`str`
        * datetime format to prefix backup file with

    Returns
    -------
    ret : (:obj:`bool`, :obj:`str`)
        * True : file was backed up
        * False : file was not backed up
    """
    makedir(dest_dir)

    timestamp = kwargs.get("timestamp", BACKUP_TIMESTAMP)
    dt_stamp = datetime.datetime.utcnow().strftime(timestamp)
    dest_filename = "{}_{}".format(dt_stamp, filename)

    src_path = os.path.join(src_dir, filename)
    dest_path = os.path.join(dest_dir, dest_filename)

    stat = "file '{}' from source path '{}' to destination path '{}'"
    stat = stat.format(filename, src_path, dest_path)

    if not os.path.exists(src_path):
        m = "Unable to backup up {} -- source path does not exist!"
        ret = False
    else:
        shutil.copyfile(src_path, dest_path)
        ret = True
        m = "Backed up {}"

    m = m.format(stat)
    return ret, m
