import os
import re
import sys
import glob
# import time
import pprint
import string
import shutil
import logging
import platform
import base64

PY3 = sys.version_info[0] == 3
if PY3:
    string_types = str,  # noqa
else:
    string_types = basestring,  # noqa


def filter_filename(filename):
    """Utility to filter a string into a valid filename"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename


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


def clean_it(f):
    result = []
    if os.path.exists(f):
        shutil.rmtree(f)
        result.append("Removed {}".format(f))
    return result


def clean_up(p, pattern):
    result = []
    for i in get_files(p, pattern):
        result += clean_it(i)
    return result


def get_files(p, pattern='*'):
    result = glob.glob(os.path.join(p, pattern))
    return result


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


def get_type(o, name='Object'):
    result = "{}: {!r} type: {}".format(name, o, type(o).__name__)
    return result


def capcase(val):
    """convert some_string or some-string to SomeString"""
    val = [a[0].upper() + (a[1:]if len(a) > 0 else '') for a in re.split('[-_]', val)]
    result = ''.join(val)
    return result


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


def read_file(f):
    with open(f) as fh:
        result = fh.read()
    return result


def write_file(f, c):
    result = []
    d = os.path.dirname(f)

    if d and not os.path.exists(d):
        result.append("Creating directory: {}".format(d))
        os.makedirs(d)

    with open(f, 'w') as fh:
        fh.write(c)
    result.append("Wrote {} bytes to file: {}".format(len(c), f))
    return result


def get_all_logs(**kwargs):
    """Get all loggers currently known to pythons logging system`."""
    logger_dict = logging.Logger.manager.loggerDict
    all_loggers = {k: v for k, v in logger_dict.items() if isinstance(v, logging.Logger)}
    all_loggers['root'] = logging.getLogger()
    return all_loggers


def set_all_logs(**kwargs):
    """Set all loggers that the logging system knows about to a given logger level."""
    level = kwargs.get('level', 'DEBUG')
    propagate = kwargs.get('propagate', None)

    all_loggers = get_all_logs()
    msgs = []

    for name, logger in sorted(all_loggers.items()):
        logger.setLevel(getattr(logging, level))
        if propagate is True:
            logger.propagate = True
        elif propagate is False:
            logger.propagate = False

    m = "set_all_levels(): set loggers {!r} to level {!r} with propagate: {}"
    m = m.format(', '.join(all_loggers), level, propagate)
    msgs.append(m)
    return msgs


def create_log_handler(**kwargs):
    """Utility to create a logging handler."""
    level = kwargs.get('level', 'DEBUG')
    formatter = kwargs.get('formatter', '%(levelname)-8s [%(name)s] %(message)s')
    output = kwargs.get('output', 'sys.stdout')
    name = kwargs.get('name', 'console')
    handler = kwargs.get('handler', 'StreamHandler')

    if isinstance(output, string_types) and output.startswith('sys.'):
        try:
            output = eval(output)
        except Exception as e:
            err = "Unable to evaluate log output as string {}, exception: {}"
            err = err.format(output, e)
            raise Exception(err)

    try:
        output = os.path.expanduser(output)
    except:
        pass

    loghandler = getattr(logging, handler)(output)
    loghandler.set_name(name)
    loghandler.setLevel(getattr(logging, level))
    loghandler.setFormatter(logging.Formatter(formatter))
    return loghandler


def add_log_handler(logger, handler, **kwargs):
    """Utility to add a handler to a specific logger"""
    added = False
    if handler.name not in [h.name for h in logger.handlers]:
        logger.addHandler(handler)
        added = True
    return added


def remove_log_handler(logger, name, **kwargs):
    """Utility to remove a handler or all handlers from a logger"""
    removed = False
    for handler in logger.handlers:
        if handler.name == name:
            logger.removeHandler(handler)
            removed = True
    return removed


def print_loglevels(**kwargs):
    """Utility to print info about each logger."""
    loggers = get_all_logs()
    m = "logger {!r} will log {!r} and higher messages"
    for logger_name, logger_obj in sorted(loggers.items()):
        logger_lvl = logging.getLevelName(logger_obj.level)
        print(m.format(logger_name, logger_lvl))


def coerce_list(o):
    if isinstance(o, (list, tuple)):
        result = list(o)
    else:
        result = [o]
    return result


def _get_group_hierarchy(g, level=1):
    def get_map(t, m):
        return m[t] if t in m else m['*']

    def mn(not_flag):
        m = {None: ' ---- ', 1: ' isnt ', 0: ' is   ', '*': ' ???? '}
        return get_map(not_flag, m)

    def ma(and_flag):
        m = {None: ' --- ', 1: ' and ', 0: ' or  ', '*': ' ??? '}
        return get_map(and_flag, m)

    grp_m = (
        "  lvl{:<2} lot:{:<4} subgroups={:<3} filters={:<3} and_flag:{:<6} not_flag:{:<5} "
        "id: {:<15} name:{} query:{}"
    ).format
    filt_m = (
        "    [filter] hash:{:<13} source_hash:{:<13} operator:{:<13} value_type:{:<9} "
        "not_flag:{:<5} value:'{}'"
    ).format
    result = []
    lot = getattr(g, 'lot', None)
    sglen = len(g.sub_groups or [])
    flen = len(g.filters or [])
    result.append(
        grp_m(level, lot, sglen, flen, ma(g.and_flag), mn(g.not_flag), g.id, g.name, g.text)
    )
    if g.filters:
        result += [filt_m(
            f.sensor.hash, f.sensor.source_hash, f.operator, f.value_type, mn(f.not_flag), f.value
        ) for f in g.filters]
    if g.sub_groups:
        for i in g.sub_groups:
            result += _get_group_hierarchy(i, level + 1)
    return result


def get_group_hierarchy(group):
    if group is None:
        result = 'No group object to parse!'
    else:
        result = '\n'.join(_get_group_hierarchy(group))
    return result

def vig_encode(key, string):
    """Obfuscate a string with a key using Vigenere cipher.

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
    for i in range(len(string)):
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
    for i in range(len(v_string)):
        key_c = key[i % len(key)]
        encoded_c = chr(abs(ord(v_string[i]) - ord(key_c) % 256))
        decoded_chars.append(encoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string
