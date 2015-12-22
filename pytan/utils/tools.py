import os
import glob
import string
import json
import platform
import base64
import logging
import shutil
import re
from ..external import six
from ..version import __version__
from . import exceptions

mylog = logging.getLogger(__name__)


def filter_filename(filename):
    """Utility to filter a string into a valid filename"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename


def json_read(f):
    return json.loads(read_file(f))


def read_file(f):
    with open(f) as fh:
        out = fh.read()
    return out


def write_file(f, c, thislog=None):
    if thislog is None:
        thislog = mylog

    d = os.path.dirname(f)

    if not os.path.exists(d):
        thislog.info("Creating directory: {}".format(d))
        os.makedirs(d)

    with open(f, 'w') as fh:
        fh.write(c)
    thislog.info("Wrote {} bytes to file: {}".format(len(c), f))


def get_name_title(t):
    fixes = {
        'Xml': 'XML',
        'Json': 'JSON',
        'Csv': 'CSV',
        'Pytan': 'PyTan',
        'Api': 'API',
        'Resultset': 'ResultSet',
        'Resultinfo': 'ResultInfo',
    }
    ret = t.replace('_', ' ').strip().title()
    for k, v in fixes.items():
        ret = ret.replace(k, v)
    return ret


def clean_it(f, thislog=None):
    if thislog is None:
        thislog = mylog

    if os.path.exists(f):
        shutil.rmtree(f)
        thislog.info("Removed {}".format(f))


def clean_up(p, pattern):
    for i in get_files(p, pattern):
        clean_it(i)


def get_files(p, pattern='*'):
    return glob.glob(os.path.join(p, pattern))


def determine_os_ver():
    os_system = platform.system()
    if os_system.lower() == 'darwin':
        os_name = 'OS X'
        os_version = platform.mac_ver()[0]
        os_version = "{} {}".format(os_name, os_version)
    elif os_system.lower() == 'windows':
        os_name = os_system
        os_version = platform.release()
        os_patch = platform.win32_ver()[2]
        os_version = "{} {} {}".format(os_name, os_version, os_patch)
    elif os_system.lower() == 'linux':
        os_version = ' '.join(platform.linux_distribution())
    else:
        raise Exception("OS System not coded for: {}".format(os_system))
    return os_version


def version_check(my_name, version):
    if not __version__ >= version:
        err = "PyTan v{} is not greater than {} v{}"
        err = err.format(__version__, my_name, version)
        mylog.critical(err)
        raise exceptions.VersionMismatchError(err)
    return True


def obfuscate(key, string):
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
    encoded_chars = []
    for i in six.moves.range(len(string)):
        key_c = key[i % len(key)]
        key_ord = ord(key_c) % 256
        string_c = string[i]
        string_ord = ord(string_c)
        encoded_c = chr(string_ord + key_ord)
        encoded_chars.append(encoded_c)

    encoded_str = "".join(encoded_chars)
    string_enc = base64.urlsafe_b64encode(encoded_str)
    result = '::{}::'.format(string_enc)
    return result


def print_type(o, name='Object'):
    print("{}: {!r} type: {}".format(name, o, type(o).__name__))


def deobfuscate(key, string):
    """De-obfuscates a string with a key using Vigenere cipher.

    Only useful for obfuscation, not real security!!

    Notes
    -----
    This will only work with strings that have been encoded with obfuscate(). "normal" strings
    will be returned as-is.

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
    result = string
    if string.startswith('::') and string.endswith('::'):
        string_enc = str(result[2:-2])
        string_dec = base64.urlsafe_b64decode(string_enc)

        decoded_chars = []
        for i in six.moves.range(len(string_dec)):
            key_c = key[i % len(key)]
            key_ord = ord(key_c) % 256
            string_c = string_dec[i]

            if isinstance(string_c, six.integer_types):
                string_ord = string_c
            else:
                string_ord = ord(string_c)

            abs_c = abs(string_ord - key_ord)
            actual_c = chr(abs_c)
            decoded_chars.append(actual_c)

        decoded_str = "".join(decoded_chars)
        result = decoded_str
    return result


def capcase(val):
    """convert some_string or some-string to SomeString"""
    val = [a[0].upper() + (a[1:]if len(a) > 0 else '') for a in re.split('[-_]', val)]
    result = ''.join(val)
    return result
