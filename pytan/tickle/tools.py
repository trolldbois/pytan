import os
import json
import base64
import logging
import datetime

from pytan import PytanError, integer_types, range, b, text_type
from pytan.tanium_ng import GroupList, Group, BaseType
from pytan.ext import xmltodict
from pytan.utils import read_file, write_file
from pytan.tickle.constants import TANIUM_TIME_FORMAT, HUMAN_TIME_FORMAT

MYLOG = logging.getLogger(__name__)


class ObjectTypeError(PytanError):
    pass


# TANIUM_NG

def clean_group(obj):
    """Sets ID to null on a group object and all of it's sub_groups, needed for 6.5"""
    if isinstance(obj, GroupList):
        obj.group = [clean_group(g) for g in obj.group]
    elif isinstance(obj, Group):
        obj.id = None
        if obj.sub_groups:
            obj.sub_groups = clean_group(obj.sub_groups)
    return obj


def str_obj(obj, **kwargs):
    def_attrs = ['id', 'name', 'query_text', 'expiration']
    attrs = kwargs.get('attrs', def_attrs)
    attr_str = kwargs.get('attr_str', '{}:"{}"').format
    class_name = obj.__class__.__name__
    if attrs:
        result = [attr_str(a, getattr(obj, a)) for a in attrs if getattr(obj, a, None) is not None]
        if result:
            result = ', '.join(result)
            result = '{}: {}'.format(class_name, result)
        else:
            result = str(obj)
    else:
        result = str(obj)
    return result


def shrink_obj(obj, **kwargs):
    """Returns a new class of obj with only id/name/hash defined

    Parameters
    ----------
    obj : :class:`tanium_ng.base.BaseType`
        * Object to shrink
    attrs : list of str
        * default: None
        * list of attribute str's to copy over to new object, will default to
        ['name', 'id', 'hash'] if None

    Returns
    -------
    new_obj : :class:`tanium_ng.base.BaseType`
        * Shrunken object
    """
    attrs = kwargs.get('attrs', ['name', 'id', 'hash'])
    new_obj = obj.__class__()
    [setattr(new_obj, a, getattr(obj, a)) for a in attrs if getattr(obj, a, None) is not None]
    return new_obj


def plugin_zip(p):
    """Maps columns to values for each row in a plugins sql_response and returns a list of dicts

    Parameters
    ----------
    p : :class:`tanium_ng.plugin.Plugin`
        * plugin object

    Returns
    -------
    dict
        * the columns and result_rows of the sql_response in Plugin object zipped up into a
        dictionary
    """
    result_row = p.sql_response.result_row
    result = [dict(zip(p.sql_response.columns, x)) for x in result_row]
    return result


def is_ng(obj):
    if not isinstance(obj, BaseType):
        err = "{} must be a tanium_ng object, type: {}"
        err = err.format(obj, type(obj))
        MYLOG.error(err)
        raise ObjectTypeError(err)


# TIME

def get_now(**kwargs):
    """Get current time in human friendly format """
    result = human_time(dt=datetime.datetime.utcnow(), **kwargs)
    return result


def human_time(dt, **kwargs):
    """Get datetime object in human friendly format"""
    dtformat = kwargs.get('dtformat', HUMAN_TIME_FORMAT)
    result = dt.strftime(dtformat)
    return result


def secs_from_now(secs=0, **kwargs):
    """Get time in Tanium SOAP API format `secs` from now"""
    dtformat = kwargs.get('dtformat', TANIUM_TIME_FORMAT)
    from_now = datetime.datetime.utcnow() + datetime.timedelta(seconds=secs)
    result = from_now.strftime(dtformat)
    return result


def str_to_dt(timestr, **kwargs):
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
    result = datetime.datetime.strptime(timestr, TANIUM_TIME_FORMAT)
    return result


def dt_to_str(dt, **kwargs):
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
    result = dt.strftime(TANIUM_TIME_FORMAT)
    return result


def q_start(q):
    """Caclulates the start time of a question by doing q.expiration - q.expire_seconds

    Parameters
    ----------
    q : :class:`tanium_ng.Question`
        * Question object to calculate start time for

    Returns
    -------
    tuple : str, datetime
        * a tuple containing the start time first in str format for Tanium Server API, second in
        datetime object format
    """
    expire_dt = str_to_dt(q.expiration)
    expire_seconds_delta = datetime.timedelta(seconds=q.expire_seconds)
    start_time_dt = expire_dt - expire_seconds_delta
    start_time = dt_to_str(start_time_dt)
    result = (start_time, start_time_dt)
    return result


# SERIALIZE/DESERIALIZE


def read_json_file(f):
    contents = read_file(f)
    result = json.loads(contents)
    return result


def jsonify(obj, **kwargs):
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
    indent = kwargs.get('json_indent', 2)
    sort = kwargs.get('json_sort', True)
    result = json.dumps(obj, indent=indent, sort_keys=sort)
    return result


def xml_pretty(x, **kwargs):
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
    pretty_xml = kwargs.get('pretty_xml', True)
    indent = kwargs.get('indent', '  ')
    x_parsed = xmltodict.parse(x)
    x_unparsed = xmltodict.unparse(x_parsed, pretty=pretty_xml, indent=indent)
    if pretty_xml:
        result = x_unparsed
    else:
        result = x
    return result


def xml_pretty_resultxml(x, **kwargs):
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
    x_unparsed = xml_pretty(x_find, **kwargs)
    return x_unparsed


def xml_pretty_resultobj(x, **kwargs):
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
    x_find = x_parsed["soap:Envelope"]["soap:Body"]["t:return"]["result-object"]
    x_unparsed = xml_pretty(x_find, **kwargs)
    return x_unparsed


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
    result = string
    if string and not (string.startswith('::') and string.endswith('::')):
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            key_ord = ord(key_c) % 256
            string_c = string[i]
            if isinstance(string_c, integer_types):
                string_ord = string_c
            else:
                string_ord = ord(string_c)
            encoded_c = chr(string_ord + key_ord)
            encoded_chars.append(encoded_c)
        encoded_str = "".join(encoded_chars)
        string_enc = base64.urlsafe_b64encode(b(encoded_str)).decode()
        result = '::{}::'.format(text_type(string_enc))
    return result


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


def b64encode(val):
    """pass."""
    result = base64.b64encode(b(val))
    return result


def json_pretty(s, **kwargs):
    result = jsonify(json.loads(s))
    return result


def simple_xml_check(xml, **kwargs):
    xml_defs = ['<?xml version', '<soap:Envelope']
    xml_defs_found = [x for x in xml_defs if x in xml[0:2000]]
    if not xml_defs_found:
        err = "Simple XML check failed, no XML strings found matching {}"
        err = err.format(', '.join(xml_defs))
        raise PytanError(err)
    return xml


def get_body(body, **kwargs):
    kwargs['pretty_xml'] = kwargs.get('pretty_xml', False)
    pre = kwargs.get('pre', '')

    body_type = 'unknown'
    ext = 'txt'

    if not body:
        body = ''
        body_type = 'empty'
        ext = 'txt'

    type_map = [
        {'body_type': 'xml', 'ext': 'xml', 'method': simple_xml_check},
        {'body_type': 'json', 'ext': 'json', 'method': json_pretty},
        {'body_type': 'xml', 'ext': 'xml', 'method': xml_pretty},
    ]

    for t in type_map:
        if body_type != 'unknown':
            continue
        try:
            body = t['method'](body, **kwargs)
            body_type = t['body_type']
            ext = t['ext']
            break
        except:
            pass

    if body_type == 'xml' and kwargs['pretty_xml']:
        try:
            body = xml_pretty(body, **kwargs)
        except:
            body_type = 'unknown_xml'

    result = {pre + 'body': body, pre + 'body_type': body_type, pre + 'ext': ext}
    return result


def get_bodies(response, **kwargs):
    """Uses :func:`xml_pretty` to pretty print the request and response bodies from the
    response object
    """
    result = {}
    result.update(get_body(response.request.body, pre='request', **kwargs))
    result.update(get_body(response.text, pre='response', **kwargs))
    result['sent'] = human_time(response.pytan_sent)
    result['received'] = human_time(response.pytan_received)
    result['obj'] = response
    return result


def get_all_bodies(all_responses, **kwargs):
    result = [get_bodies(x, **kwargs) for x in all_responses]
    return result


def write_all_bodies(all_responses, **kwargs):
    output_dir = kwargs.get('output_dir', os.curdir)
    bodies = get_all_bodies(all_responses, **kwargs)
    for x in bodies:
        request_fn = '{sent}_request_{requestbody_type}.{requestext}'.format(**x)
        msgs = write_file(os.path.join(output_dir, request_fn), x['requestbody'])
        for m in msgs:
            print(m)

        response_fn = '{received}_response_{responsebody_type}.{responseext}'.format(**x)
        msgs = write_file(os.path.join(output_dir, response_fn), x['responsebody'])
        for m in msgs:
            print(m)
