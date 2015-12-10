#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Functions for use by BUILD scripts'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.4'

import sys
sys.dont_write_bytecode = True

import os
import glob
import string
import json
import StringIO
import platform
from random import randint


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


class ExecWrap(object):
    def main(self, code_block, name='', verbose=True):
        print "executing code block for: {}".format(name)

        if verbose:
            print "Code block:\n{}".format(code_block)

        exec_globals = {}
        exec_locals = {}

        code_stdout = StringIO.StringIO()
        code_stderr = StringIO.StringIO()

        sys.stdout = code_stdout
        sys.stderr = code_stderr

        try:
            exec(code_block, exec_globals, exec_locals)
        except:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            code_stdout_val = code_stdout.getvalue()
            code_stderr_val = code_stderr.getvalue()
            print "Exception occurred!!"
            print "Code block:\n{}".format(code_block)
            print "Code stdout:\n{}".format(code_stdout_val)
            print "Code stderr:\n{}".format(code_stderr_val)
            raise

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        code_stdout_val = code_stdout.getvalue()
        code_stderr_val = code_stderr.getvalue()

        try:
            response_objects = list(exec_locals['handler'].session.ALL_REQUESTS_RESPONSES)
        except:
            response_objects = []
            print "unable to fetch response objects from session!"

        if verbose:
            print "{}".format("_" * 80)
            print "Code stdout:\n{}".format(code_stdout_val)
            print "Code stderr:\n{}".format(code_stderr_val)
            print "# of response_objects passed back: {}".format(len(response_objects))
            print "{}".format("_" * 80)

        return code_stdout_val, code_stderr_val, response_objects


def templatize(val, subs):
    subs["RANDINT"] = randint(1, 9999)
    val_template = string.Template(val)
    new_val = val_template.safe_substitute(subs)
    return new_val


def template_dict(d, all_subs):
    # replace any ${} vars with matching key/values from all_subs
    for k, v in d.iteritems():
        if type(v) in [str, unicode]:
            new_v = templatize(v, all_subs)
        elif type(v) in [list, tuple]:
            new_v = [templatize(x, all_subs) for x in v]
        elif type(v) in [dict]:
            new_v = template_dict(v, all_subs)
        else:
            new_v = v
        d[k] = new_v
    return d


def create_script(d, template_key, output_dir, filename_template):
    if d.get(template_key):
        script_out = string.Template(d[template_key]).safe_substitute(**d)
        script_out = string.Template(script_out).safe_substitute(**d)
        script_file = string.Template(filename_template).safe_substitute(**d)
        script_path = os.path.join(output_dir, script_file)
        write_file(script_path, script_out)
        os.chmod(script_path, 0755)


def process_example(example_idx, example_dict, sub_dict):
    # print "Before parse: {script_name}: {name}".format(script_name=script_def['script_name'], **example_def)

    # prepend command line with stdin re-direct for interactive console scripts
    if '-i' in sub_dict.get('pyopts', ''):
        example_dict['cmd'] = 'echo "" | ' + example_dict['cmd']
        if 'noerror' in example_dict['tests']:
            fixed = example_dict['tests'].split(',')
            fixed = [x.strip() for x in fixed if x.strip() != 'noerror']
            example_dict['tests'] = ', '.join(fixed)

    # set depth to 1 if no depth specified
    example_dict['depth'] = example_dict.get('depth', 1)

    # expand all variables in the example dict with key/value pairs from all_subs
    example_dict = template_dict(example_dict, sub_dict)

    # print "After parse: {script_name}: {name}".format(script_name=script_def['script_name'], **example_def)

    # for k, v in example_def.iteritems():
    #     debug_out = "   example #{} for {} {}: {}".format
    #     print debug_out(example_idx, script_def['script_name'], k, v)

    skips = ['name', 'cmd', 'depth', 'notes', 'tests']
    others = ["{}: {}".format(k, v) for k, v in example_dict.iteritems() if k not in skips]
    example_dict['others_out'] = '\n'.join(others)

    notes = example_dict.get('notes', '').strip().splitlines()
    notes = [x for x in notes if x]
    notes = ['notes{}: {}'.format(idx, n) for idx, n in enumerate(notes)]
    example_dict['notes_out'] = '\n'.join(notes)

    return example_dict


def spew(t, verbose=False):
    if verbose:
        print t


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
