import os
import io
import re
import csv
import time
import glob
import json
import pprint
import string
import base64
import shutil
import socket
import logging
import platform
import datetime

from . import integer_types, range
from . import exceptions, constants, xmltodict

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
    for i in range(len(string)):
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
        for i in range(len(string_dec)):
            key_c = key[i % len(key)]
            key_ord = ord(key_c) % 256
            string_c = string_dec[i]

            if isinstance(string_c, integer_types):
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


def port_check(address, port, timeout=5):
    """Check if `address`:`port` can be reached within `timeout`

    Parameters
    ----------
    address : str
        * hostname/ip address to check `port` on
    port : int
        * port to check on `address`
    timeout : int, optional
        * timeout after N seconds of not being able to connect

    Returns
    -------
    :mod:`socket` or False :
        * if connection succeeds, the socket object is returned, else False is returned
    """
    try:
        return socket.create_connection((address, port), timeout)
    except socket.error:
        return False


def test_app_port(host, port, **kwargs):
    """Validates that `host`:`port` can be reached using :func:`port_check`

    Parameters
    ----------
    host : str
        * hostname/ip address to check `port` on
    port : int
        * port to check on `host`

    Raises
    ------
    exceptions.HandlerError : :exc:`exceptions.HandlerError`
        * if `host`:`port` can not be reached
    """
    chk_tpl = "Port test to {}:{} {}".format
    if port_check(host, port):
        mylog.debug(chk_tpl(host, port, "SUCCESS"))
    else:
        raise exceptions.NetworkError(chk_tpl(host, port, "FAILURE"))


def get_percent(base, amount, text=None, textformat="{0:.2f}%"):
    """Utility method for getting percentage of base out of amount

    Parameters
    ----------
    base: int, float
    amount: int, float
    text: bool

    Returns
    -------
    percent : the percentage of base out of amount
    """
    if 0 in [base, amount]:
        result = float(0)
    else:
        result = (100 * (float(base) / float(amount)))

    if text:
        result = textformat.format(result)
    return result


def get_base(percent, amount):
    """Utility method for getting base for percentage of amount

    Parameters
    ----------
    percent: int, float
    amount: int, float

    Returns
    -------
    base : the base from percentage of amount
    """
    result = int((percent * amount) / 100.0)
    return result


def get_now_dt(gmt=True):
    """pass."""
    if gmt:
        result = datetime.datetime.utcnow()
    else:
        result = datetime.datetime.now()
    return result


def get_now(gmt=True):
    """Get current time in human friendly format """
    now = get_now_dt(gmt)
    result = human_time(now)
    return result


def human_time(dt, dtformat='D%Y-%m-%dT%H-%M-%S', tz=True):
    """Get time in human friendly format"""
    result = dt.strftime(dtformat)
    if tz:
        tz_pre = '-' if time.altzone > 0 else '+'
        add_tz = 'Z{}{:0>2}{:0>2}'
        add_tz = add_tz.format(tz_pre, abs(time.altzone) // 3600, abs(time.altzone // 60) % 60)
        result = result + add_tz
    return result


def seconds_from_now(secs=0, gmt=True, tformat='%Y-%m-%dT%H:%M:%S'):
    """Get time in Tanium SOAP API format `secs` from now

    Parameters
    ----------
    secs : int
        * seconds from now to get time str
    tz : str, optional
        * time zone to return string in, default is 'utc' - supplying anything else will supply
        local time

    Returns
    -------
    str :
        * time `secs` from now in Tanium SOAP API format
    """
    if secs is None:
        secs = 0

    now = get_now_dt(gmt)
    from_now = now + datetime.timedelta(seconds=secs)
    result = from_now.strftime(tformat)
    return result


def timestr_to_datetime(timestr):
    """Get a datetime.datetime object for `timestr`

    Parameters
    ----------
    timestr : str
        * date & time in taniums format

    Returns
    -------
    datetime.datetime
        * the datetime object for the timestr
    """
    result = datetime.datetime.strptime(timestr, constants.TIME_FORMAT)
    return result


def datetime_to_timestr(dt):
    """Get a timestr for `dt`

    Parameters
    ----------
    dt : datetime.datetime
        * datetime object

    Returns
    -------
    timestr: str
        * the timestr for `dt` in taniums format
    """
    result = dt.strftime(constants.TIME_FORMAT)
    return result


def jsonify(v, indent=2, sort_keys=True):
    """Turns python object `v` into a pretty printed JSON string

    Parameters
    ----------
    v : object
        * python object to convert to JSON

    indent : int, 2
        * number of spaces to indent JSON string when pretty printing

    sort_keys : bool, True
        * sort keys of JSON string when pretty printing

    Returns
    -------
    str :
        * JSON pretty printed string
    """
    return json.dumps(v, indent=indent, sort_keys=sort_keys)


def xml_pretty(x, pretty=True, indent='  ', **kwargs):
    """Uses :mod:`xmltodict` to pretty print an XML str `x`

    Parameters
    ----------
    x : str
        * XML string to pretty print

    Returns
    -------
    str :
        * The pretty printed string of `x`
    """

    x_parsed = xmltodict.parse(x)
    x_unparsed = xmltodict.unparse(x_parsed, pretty=pretty, indent=indent)
    return x_unparsed


def xml_pretty_resultxml(x):
    """Uses :mod:`xmltodict` to pretty print an the ResultXML element in XML str `x`

    Parameters
    ----------
    x : str
        * XML string to pretty print

    Returns
    -------
    str :
        * The pretty printed string of ResultXML in `x`
    """

    x_parsed = xmltodict.parse(x)
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]["ResultXML"]
    x_unparsed = xml_pretty(x_find)
    return x_unparsed


def xml_pretty_resultobj(x):
    """Uses :mod:`xmltodict` to pretty print an the result-object element in XML str `x`

    Parameters
    ----------
    x : str
        * XML string to pretty print

    Returns
    -------
    str :
        * The pretty printed string of result-object in `x`
    """

    x_parsed = xmltodict.parse(x)
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]
    x_find = x_parsed["result-object"]
    x_unparsed = xmltodict.unparse(x_find, pretty=True, indent='  ')
    return x_unparsed


def csvdictwriter(rows_list, **kwargs):
    """returns the rows_list (list of dicts) as a CSV string"""
    def get_all_headers(rows_list):
        """Utility to get all the keys for a list of dicts"""
        headers = []
        [headers.append(h) for x in rows_list for h in x.keys() if h not in headers]
        return headers

    csv_io = io.BytesIO()
    headers = kwargs.get('headers', []) or get_all_headers(rows_list)
    writer = csv.DictWriter(
        csv_io,
        fieldnames=headers,
        quoting=csv.QUOTE_NONNUMERIC,
        extrasaction='ignore',
    )
    writer.writerow(dict((h, h) for h in headers))
    writer.writerows(rows_list)
    csv_str = csv_io.getvalue()
    return csv_str


def pretty_dict(d, indent=0, parent=True):
    """Pretty print a dictionary"""
    strs = []
    for k, v in d.items():
        ktxt = "{}{}: ".format('  ' * indent, k)
        new_indent = indent + 1
        if isinstance(v, (dict)):
            strs.append(ktxt)
            strs += pretty_dict(v, new_indent, False)
        elif isinstance(v, (list, tuple)):
            strs.append(ktxt)
            new_strs = [pretty_dict(a, new_indent, False) for a in v]
            for a in new_strs:
                strs += a
        else:
            strs.append("{}{}".format(ktxt, v))
    if parent:
        strs = '\n'.join(strs)
    return strs


def debug_list(debuglist):
    """Utility function to print the variables for a list of objects"""
    for x in debuglist:
        debug_obj(x)


def debug_obj(debugobj):
    """Utility function to print the variables for an object"""
    pprint.pprint(vars(debugobj))


def introspect(obj, depth=0):
    """Utility function to dump all info about an object"""
    import types
    print("{}{}: {}\n".format(depth * "\t", obj, [x for x in dir(obj) if x[:2] != "__"]))
    depth += 1
    for x in dir(obj):
        if x[:2] == "__":
            continue
        subobj = getattr(obj, x)
        print("{}{}: {}".format(depth * "\t", x, subobj))
        if isinstance(subobj, types.InstanceType) and dir(subobj) != []:
            introspect(subobj, depth=depth + 1)
            print("")
