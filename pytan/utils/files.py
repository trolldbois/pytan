import os
import glob
import string
import json
import platform
from ..version import __version__
from . import exceptions


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


def write_file(f, c):
    d = os.path.dirname(f)

    if not os.path.exists(d):
        print "Creating directory: {}".format(d)
        os.makedirs(d)

    with open(f, 'w') as fh:
        fh.write(c)
    print "Wrote file: {}".format(f)


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
    for k, v in fixes.iteritems():
        ret = ret.replace(k, v)
    return ret


def clean_it(f):
    if os.path.exists(f):
        os.unlink(f)
        print "Removed {}".format(f)


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
    m = "PyTan v{} is not greater than {} v{}".format
    if not __version__ >= version:
        raise exceptions.VersionMismatchError(m(__version__, my_name, version))
    return True
