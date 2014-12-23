#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Build the markdown docs for the bin/ scripts'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.0'

import os
import sys
import glob
import imp
import tempfile
from string import Template

sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

from pytan import utils
import md_doctester

utils.version_check(__version__)

bin_dir = os.path.join(parent_dir, 'bin')
ini_output_dir = os.path.join(my_dir, 'bin_doc')
md_output_dir = os.path.join(my_dir, 'doc', 'source', '_static', 'bin_doc')

conf_temp = """[CONFIG]
mainheader: {0} Readme
output_blocks: true
valid_blocks: true
basename: {1}
contact: Jim Olsen <jim.olsen@tanium.com>

""".format

head_temp = """[{name}]
headerdepth: {depth}
cmd: {cmd}
validtests: {tests}
""".format

example_subs = {
    'API_INFO': "-u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1",
    "TMP": tempfile.gettempdir(),
}


def read_file(f):
    with open(f) as fh:
        out = fh.read()
    return out


def write_file(f, c):
    with open(f, 'w') as fh:
        fh.write(c)
    print "Wrote file: {}".format(f)


def get_help_cmd(b):
    if 'shell' in b:
        return 'echo "" | {} -h'.format(b)
    else:
        return '{} -h'.format(b)


if not os.path.isdir(ini_output_dir):
    os.makedirs(ini_output_dir)

old_files = glob.glob(ini_output_dir + '/*.*')
if old_files:
    for x in old_files:
        print "Cleaning up old file {}".format(x)
        os.unlink(x)

py_files = {}
bin_files = glob.glob(os.path.join(bin_dir, '*.py'))
for x in bin_files:
    out = []
    a_base = os.path.basename(x)
    a_name = os.path.splitext(a_base)[0]
    a_proper = a_name.replace('_', ' ').title()
    out.append(conf_temp(a_proper, a_name))

    a = imp.load_source('a', x)
    py_files[a_name] = a.__doc__
    examples = [
        {
            'name': '{} Help'.format(a_proper),
            'cmd': get_help_cmd(a_base),
            'depth': '1',
            'notes': [
                a.__doc__
            ],
            'tests': 'exitcode',
        },
    ]

    a_examples = getattr(a, 'examples', [])

    for e in a_examples:
        if 'depth' not in e:
            e['depth'] = "1"
        for k, v in e.iteritems():
            if type(v) not in [str, unicode]:
                continue
            t = Template(v)
            e[k] = t.safe_substitute(example_subs)
        examples.append(e)

    for e in examples:
        head = head_temp(**e)
        for idx, n in enumerate(e.get('notes', [])):
            head += 'notes{}: {}\n'.format(idx, n)
        for k, v in e.iteritems():
            if k in ['name', 'cmd', 'depth', 'notes', 'tests']:
                continue
            head += "{}: {}\n".format(k, v)
        out.append(head)

    out = '\n'.join(out)
    out_file = a_name + '.ini'
    out_path = os.path.join(ini_output_dir, out_file)
    write_file(out_path, out)

# md_doctester.setup_logging(debug=True)
if not os.path.isdir(md_output_dir):
    os.makedirs(md_output_dir)

old_files = glob.glob(md_output_dir + '/*.*')
if old_files:
    for x in old_files:
        print "Cleaning up old file {}".format(x)
        os.unlink(x)

os.environ["PATH"] += os.pathsep + bin_dir
ini_files = glob.glob(os.path.join(ini_output_dir, '*.ini'))
for x in ini_files:
    print "Running MDTest against {}".format(x)
    mdtest_args = {}
    mdtest_args['filehandle'] = open(x, 'r')
    mdtest_args['outdir'] = md_output_dir
    mdtest_args['github_token'] = '3e5d528c1494e87ae95615988510ae8bbf599cba'
    # mdtest_args['skipconvert'] = True
    mdtest = md_doctester.MDTest(**mdtest_args)


index_file = os.path.join(md_output_dir, 'index.md')
index_out = []
index_out.append("""PyTan Command Line Scripts
==========================
""")

for x, y in py_files.iteritems():
    index_out.append("  * **[{0}]({0}.html)**: {1}".format(x, y))

index_out.append('\n')
index_out = '\n'.join(index_out)

write_file(index_file, index_out)

print "Running MDTest against {}".format(index_file)
mdtest_args = {}
mdtest_args['filehandle'] = open(index_file, 'r')
mdtest_args['outdir'] = md_output_dir
mdtest_args['github_token'] = '3e5d528c1494e87ae95615988510ae8bbf599cba'
mdtest_args['convertonly'] = True
mdtest = md_doctester.MDTest(**mdtest_args)
