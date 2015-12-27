import io
import re
import sys
import csv
import time
import json
import base64
import logging
import datetime

from pytan import PytanError
from pytan.tickle.constants import XML_ENGINE, XML_ENGINES

MYLOG = logging.getLogger(__name__)


class XMLEngineError(PytanError):
    pass


class DeserializeError(PytanError):
    pass


class ObjectTypeError(PytanError):
    pass


class LimitCheckError(PytanError):
    pass


ET = None

if XML_ENGINE in XML_ENGINES:
    try:
        __import__(XML_ENGINES[XML_ENGINE])
        ET = sys.modules[XML_ENGINES[XML_ENGINE]]
        m = "Using {} for XML engine"
        m = m.format(XML_ENGINES[XML_ENGINE])
        MYLOG.debug(m)
        FALLBACK = False
    except ImportError as e:
        m = "XML engine {} failed to import: {}"
        m = m.format(XML_ENGINES[XML_ENGINE], e)
        MYLOG.warning(m)
        FALLBACK = True
else:
    FALLBACK = True

if FALLBACK:
    for k, v in XML_ENGINES.items():
        try:
            __import__(v)
            ET = sys.modules[v]
            m = "Using {} for XML engine"
            m = m.format(v)
            MYLOG.debug(m)
        except ImportError as e:
            m = "XML engine {} failed to import: {}"
            m = m.format(XML_ENGINES[XML_ENGINE], e)
            MYLOG.debug(m)

if ET is None:
    err = "Failed to import any XML Engine!"
    MYLOG.critical(err)
    raise XMLEngineError(err)


# CONVENIENCE WRAPPERS AROUND TICKLE CLASSES::

def to_xml(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into an XML body using ObjectToXML"""
    tickle_val = ToXML(obj, **kwargs)
    result = tickle_val.XML
    return result


def to_dict(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a dict using ToJSON"""
    tickle_val = ToJSON(obj, **kwargs)
    result = tickle_val.DICT
    return result


def to_json(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a JSON string using ToJSON"""
    tickle_val = ToJSON(obj, **kwargs)
    result = tickle_val.JSON
    return result


def to_csv(obj, **kwargs):
    """Serialize tanium_ng object ``obj`` into a CSV string using ToJSON"""
    # TODO FIGURE OUT ResultSet
    kwargs['skips'] = kwargs.get('skips', [])
    kwargs['sort'] = kwargs.get('sort', [])

    kwargs['flat'] = True

    tickle_val = ToJSON(obj, **kwargs)
    flat_obj = tickle_val.DICT

    if LIST_NAME in flat_obj:
        kwargs['rows'] = flat_obj[LIST_NAME]
    else:
        kwargs['rows'] = [flat_obj]

    default_sort = ['id', 'name', 'description']
    default_skip = [TAG_NAME, LIST_NAME, EXPLODE_NAME]
    default_skip += list(FLAT_WARN.keys())

    kwargs['sort'] += default_sort
    kwargs['skips'] += default_skip

    result = csvdictwriter(**kwargs)
    return result


def from_json(jsonstr, **kwargs):
    """Deserialize a JSON string into a tanium_ng object sing FromJSON"""
    tickle_val = FromJSON(jsonstr=jsonstr, **kwargs)
    result = tickle_val.OBJ
    return result


def from_dict(pyobj, **kwargs):
    """Deserialize a dict or list of dicts into a tanium_ng object using FromJSON"""
    tickle_val = FromJSON(pyobj=pyobj, **kwargs)
    result = tickle_val.OBJ
    return result


def from_xml(xml, **kwargs):
    """Deserialize ``xml`` from XML into a tanium_ng object using FromXML."""
    tickle_val = FromXML(xml=xml, **kwargs)
    result = tickle_val.OBJ
    return result


def from_sse_xml(xml, **kwargs):
    """Wraps a Result Set XML from a server side export in the appropriate tags and returns a
    ResultSet object

    Parameters
    ----------
    x : str
        * str of XML to convert to a ResultSet object

    Returns
    -------
    rs : :class:`tanium_ng.result_set.ResultSet`
        * x converted into a ResultSet object
    """
    rs_xml = SSE_WRAP.format(SSE_DATA=xml)
    result = from_xml(rs_xml, **kwargs)
    return result


# OBJECT HANDLING METHODS


def shrink_obj(obj, attrs=None):
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
    if attrs is None:
        attrs = ['name', 'id', 'hash']

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
    return [
        dict(zip(p.sql_response.columns, x)) for x in p.sql_response.result_row
    ]


def create_cf_listobj(specs):
    """pass."""
    result = tanium_ng.CacheFilterList()
    if not isinstance(specs, (list, tuple)):
        specs = [specs]
    for spec in specs:
        result.append(create_cf_obj(**spec))
    return result


def create_cf_obj(field, value, operator=None, field_type=None, not_flag=None, **kwargs):
    """pass."""
    result = tanium_ng.CacheFilter()
    result.field = field
    result.value = value
    if operator is not None:
        result.operator = operator
    if field_type is not None:
        result.type = field_type
    if not_flag is not None:
        result.not_flag = not_flag
    return result


def create_selectlist_obj(specs):
    """pass."""
    result = tanium_ng.SelectList()
    for spec in specs:
        result.append(create_select_obj(spec))
    return result


def create_select_obj(spec):
    """pass."""
    result = tanium_ng.Select()
    result.sensor = tanium_ng.Sensor()

    if 'parameters' in spec:
        result.sensor.source_id = spec['sensor_object'].id
        result.sensor.parameters = create_parameter_objlist(spec['parameters'])
    else:
        result.sensor.id = spec['sensor_object'].id

    if 'filter' in spec:
        result.filter = create_filter_obj(spec)
    return result


def create_filter_obj(spec):
    """pass."""
    filter_spec = spec['filter']
    result = tanium_ng.Filter()
    result.sensor = tanium_ng.Sensor()
    result.sensor.hash = spec['sensor_object'].hash  # needs to be hash, id no work!
    result.value = filter_spec['value']
    result.operator = filter_spec.get('operator', 'Equal')  # tanium default operator is Less!
    return result


def create_parameter_objlist(parameters, **kwargs):
    """pass."""
    result = tanium_ng.ParameterList()
    for k, v in parameters.items():
        result.append(create_parameter_obj(key=k, val=v, **kwargs))
    return result


def create_parameter_obj(key, val, delim='||'):
    """pass."""
    result = tanium_ng.Parameter()
    result.key = '{0}{1}{0}'.format(delim, key)
    result.value = val
    return result


def create_filterlist_obj(spec):
    """pass."""
    result = tanium_ng.FilterList()
    result.append(create_filter_obj(spec))
    return result


def create_group_with_filter_obj(spec):
    """pass."""
    result = tanium_ng.Group()
    result.filters = create_filterlist_obj(spec)
    return result


def create_parent_group_obj(specs):
    """pass."""
    result = tanium_ng.Group()
    result.sub_groups = tanium_ng.GroupList()
    parent_sub = tanium_ng.Group()
    parent_sub.sub_groups = tanium_ng.GroupList()
    result.sub_groups.append(parent_sub)

    for idx, spec in enumerate(specs):
        # if they supplied a group object, use that instead of creating one
        if 'group_object' in spec:
            print("using group object instead of filter")
            parent_sub.sub_groups.append(spec['group_object'])
            continue

        first = idx == 0
        this_and = spec['filter'].get('and_flag', None)

        # if this is the first spec
        # add a group with a filter from this spec to the current parent_sub
        if first:
            new_group = create_group_with_filter_obj(spec)
            print('first: creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)

            if this_and is not None:
                print('applying and_flag {} to parent_sub'.format(this_and))
                parent_sub.and_flag = this_and
            continue

        # if this spec does not have and_flag
        # add a group with a filter from this spec to the current parent_sub
        if this_and is None:
            new_group = create_group_with_filter_obj(spec)
            print('not first: and is None, creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)
            continue

        # if this spec does have an and_flag and it doesn't match the current
        # parent_sub's and, create a new parent_sub
        # add a group with a filter from this spec to the new parent_sub
        if parent_sub.and_flag != this_and:
            print('not first:, and is {} creating a new parent_sub'.format(this_and))
            parent_sub = tanium_ng.Group()
            parent_sub.and_flag = this_and
            parent_sub.sub_groups = tanium_ng.GroupList()
            result.sub_groups.append(parent_sub)

            new_group = create_group_with_filter_obj(spec)
            print('not first: creating a new group and adding to parent_sub')
            print(spec['filter'])
            parent_sub.sub_groups.append(new_group)
            continue

        new_group = create_group_with_filter_obj(spec)
        print('catch all: creating a new group and adding to parent_sub')
        print(spec['filter'])
        parent_sub.sub_groups.append(new_group)
        continue

    recurse_group(result)
    return result


def recurse_group(g, level=1):
    """pass"""
    sglen = len(g.sub_groups or [])
    flen = len(g.filters or [])

    a = "level: {}, and_flag: {}, filters: {}, sub_groups: {}"
    a = a.format(level, g.and_flag, flen, sglen)
    print(a)

    if g.filters:
        for i in g.filters:
            f = "operator: {0.operator} value: {0.value}".format(i)
            m = "level: {}, and_flag: {}, filter: {}"
            m = m.format(level, g.and_flag, f)
            print(m)

    if g.sub_groups:
        for i in g.sub_groups:
            recurse_group(i, level + 1)


def create_question_obj(left=[], right=[]):
    """pass."""
    result = tanium_ng.Question()
    result.selects = create_selectlist_obj(left)
    if right:
        result.group = create_parent_group_obj(right)
    return result


def check_tanium_obj(obj):
    if not isinstance(obj, tanium_ng.BaseType):
        err = "{} must be a tanium_ng object, type: {}"
        err = err.format(obj, type(obj))
        raise ObjectTypeError(err)


def check_limits(objects, **kwargs):
    """pass."""
    specs = kwargs.get('specs', [])

    check_tanium_obj(objects)

    # coerce single items into a list
    objects_class = objects.__class__.__name__
    if not objects_class.endswith('List'):
        new_class = objects_class + 'List'
        new_objects = getattr(tanium_ng, new_class)()
        new_objects.append(objects)
        objects = new_objects

    limit_map = [
        {'k': 'limit_min', 'm': "{} items or more", 'e': '>='},
        {'k': 'limit_max', 'm': "{} items or less", 'e': '<='},
        {'k': 'limit_exact', 'm': "{} items exactly", 'e': '=='},
    ]

    for l in limit_map:
        limit_val = kwargs.get(l['k'], None)

        if limit_val is None:
            m = "check_limits(): found {}, skipped {} (not supplied)"
            m = m.format(objects, l['k'], )
            MYLOG.debug(m)
            continue

        limit_val = int(limit_val)
        e = "len(objects) {} limit_val".format(l['e'])
        limit_pass = eval(e)

        p = "check_limits(): found {}, {} {} (must be {})"
        limit_msg = l['m'].format(limit_val)

        if limit_pass:
            m = p.format(objects, 'PASSED', l['k'], limit_msg)
            MYLOG.debug(m)
        else:
            # get the str of each objects for printing in exception
            objtxt = '\n\t'.join([str(x) for x in objects])

            # get the specs txt if any specs
            specstxt = "\n"
            if specs:
                specstxt = "\nspecs:\n\t" + "\n\t".join([str(x) for x in specs]) + "\n"

            err_pre = p.format(objects, 'FAILED', l['k'], limit_msg)
            err = "{}{}returned items:\n\t{}"
            err = err.format(err_pre, specstxt, objtxt)
            MYLOG.critical(err)
            raise LimitCheckError(err)


def question_start_time(q):
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
    expire_dt = timestr_to_datetime(q.expiration)
    expire_seconds_delta = datetime.timedelta(seconds=q.expire_seconds)
    start_time_dt = expire_dt - expire_seconds_delta
    start_time = datetime_to_timestr(start_time_dt)
    result = (start_time, start_time_dt)
    return result


def create_options_obj(**kwargs):
    result = tanium_ng.Options()

    for k, v in kwargs.items():
        if hasattr(result, k):
            m = "Setting Options attribute {!r} to value '{}'".format
            MYLOG.debug(m(k, v))
            setattr(result, k, v)
    return result


def get_row_headers(rows_list, **kwargs):
    """Utility to get all the keys for a list of dicts"""
    headers = list(set([h for r in rows_list for h in r]))
    return headers


def sort_headers(headers, **kwargs):
    sort = kwargs.get('sort', [])
    headers = sorted(headers)
    if isinstance(sort, list) and sort:
        new_headers = []
        for s in sort:
            for idx, h in enumerate(headers):
                if h.lower() == s.lower():
                    new_headers.append(headers.pop(idx))
        headers = new_headers + headers
    return headers


def fix_newlines(val):
    # turn \n into \r\n
    if isinstance(val, string_types):
        val = MISSING_CR_RE.sub(r"\1\r\n", val)
    return val


def csvdictwriter(rows, **kwargs):
    """returns the rows (list of dicts) as a CSV string"""
    headers = kwargs.get('headers', []) or get_row_headers(rows)
    skips = kwargs.get('skips', [])
    sort = kwargs.get('sort', True)
    linefix = kwargs.get('linefix', True)

    if skips:
        headers = [x for x in headers if x.lower() not in [y.lower() for y in skips]]

    if sort not in [False, None]:
        headers = sort_headers(headers, **kwargs)

    if linefix:
        rows = [{k: fix_newlines(v) for k, v in x.items()} for x in rows]

    # TODO test on py2

    csv_io = io.StringIO()
    writer = csv.DictWriter(
        csv_io,
        fieldnames=headers,
        quoting=csv.QUOTE_NONNUMERIC,
        extrasaction='ignore',
    )

    writer.writeheader()
    writer.writerows(rows)
    csv_str = csv_io.getvalue()
    return csv_str


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
    result = datetime.datetime.strptime(timestr, TIME_FORMAT)
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
    result = dt.strftime(TIME_FORMAT)
    return result


def json_read(f):
    return json.loads(read_file(f))


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


from pytan import string_types, integer_types, range, b
from pytan import tanium_ng, xmltodict
from pytan.utils import read_file
from pytan.tickle.FromJSON import FromJSON
from pytan.tickle.FromXML import FromXML
from pytan.tickle.ToJSON import ToJSON
from pytan.tickle.ToXML import ToXML
from pytan.tickle.constants import (
    LIST_NAME, TAG_NAME, EXPLODE_NAME, FLAT_WARN, SSE_WRAP, MISSING_CR_TEXT, TIME_FORMAT
)

MISSING_CR_RE = re.compile(MISSING_CR_TEXT)
