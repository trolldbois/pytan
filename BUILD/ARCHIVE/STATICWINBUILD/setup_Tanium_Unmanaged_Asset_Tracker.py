# change me accordingly, rest is automatic
TOOL_NAME = "Tanium_Unmanaged_Asset_Tracker"

import os
import sys
import shutil
import zipfile
import imp

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


from distutils.core import setup
import py2exe # noqa


def spew(m):
    print("### [STATICWINBUILD] {}".format(m))


def write_file(filename, content):
    fh = open(filename, 'w+')
    fh.write(content)
    fh.close()
    spew("Wrote {!r}".format(filename))


def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file),)
    spew("Created zip file {!r} from {!r}".format(zip.filename, path))


def deltree(d):
    spew("Removing directory {!r}".format(d))
    shutil.rmtree(d)


def clean_old_file(f):
    if os.path.isfile(f):
        os.unlink(f)
        spew("Removed old file {!r}".format(f))


os.chdir(my_dir)

pyscript = '{}.py'.format(TOOL_NAME)
pyscript_path = '{}/bin/{}'.format(pytan_root_dir, pyscript)
a = imp.load_source('a', pyscript_path)
VERSION = a.__version__
DIST_DIR = "{}_dist_{}".format(TOOL_NAME, VERSION)
BUILD_DIR = "build"
ZIP_DIR = os.path.join(pytan_root_dir, "ZIP_DIST")

try:
    deltree(DIST_DIR)
    deltree(BUILD_DIR)
except:
    pass

setup(
    console=[pyscript_path],
    options={
        'py2exe': {
            'dist_dir': DIST_DIR,
            'packages': [
                'pytan',
                'taniumpy',
            ],
        },
    },
    data_files=[
        '{}/lib/taniumpy/request_body_template.xml'.format(pytan_root_dir),
    ],
)

spew("Finished building {!r} via py2exe".format(TOOL_NAME))

deltree(BUILD_DIR)

# create batch file for running here and for configuration

RUN_BATCH = ('''@echo off

set my_dir=%~dp0%
call %my_dir%\CONFIG.bat
set cmdline=
IF DEFINED username set cmdline=%cmdline% --username "%username%"
IF DEFINED password set cmdline=%cmdline% --password "%password%"
IF DEFINED host set cmdline=%cmdline% --host "%host%"
IF DEFINED port set cmdline=%cmdline% --port "%port%"
IF DEFINED loglevel set cmdline=%cmdline% --loglevel "%loglevel%"
IF DEFINED output_dir set cmdline=%cmdline% --output_dir "%output_dir%"
IF DEFINED pct set cmdline=%cmdline% --pct "%pct%"
IF DEFINED timeout set cmdline=%cmdline% --timeout "%timeout%"
IF DEFINED max_data_age set cmdline=%cmdline% --max_data_age "%max_data_age%"
IF DEFINED last_registration_hours set cmdline=%cmdline% --last_registration_hours "%last_registration_hours%"

IF "%debugformat%" == "true" set cmdline=%cmdline% --debugformat
IF "%saved%" == "true" set cmdline=%cmdline% --saved

cd %my_dir%
Tanium_Unmanaged_Asset_Tracker.exe %cmdline%
''')

CONFIG_BATCH = ('''@echo off

REM if username is not set here, it will be prompted for on the command line
set username=

REM if password is not set here, it will be prompted for on the command line
set password=

REM if host is not set here, it will be prompted for on the command line
set host=

REM optionally control which port to connect to (integer)
set port=

REM optionally control the logging / verbosity level (integer)
set loglevel=

REM optionally set the logging format to a more verbose logging format (true to enable)
set debugformat=false

REM optionally control the output directory
set output_dir=

REM optionally override the default percent to consider question data complete
set pct=

REM optionally override the default number of seconds before questions timeout
set timeout=

REM optionally override the default number of seconds to consider cached question data old
set max_data_age=

REM optionally used saved question results for unmanaged asset results (true to enable)
set saved=false

REM optionally override the default number of hours since last registration for considering
REM "active managed assets"
set last_registration_hours=

''')

README = ('''
Tanium Unmanaged Asset Tracker
===========================

This tool is a statically compiled windows EXE version of a
python script in the PyTan toolset.

It is used to get all managed clients from Tanium, then get all
unmanaged assets results, and cull out the truly managed assets
from the results of unmanaged assets and produce a CSV report of
"Truly" unmanaged assets.

Modify CONFIG.bat according to your needs, then use RUN.bat to
execute. Alternatively, just run Tanium_Unmanaged_Asset_Tracker.exe
directly.
''')

write_file(os.path.join(DIST_DIR, 'RUN.bat'), RUN_BATCH)
write_file(os.path.join(DIST_DIR, 'CONFIG.bat'), CONFIG_BATCH)
write_file(os.path.join(DIST_DIR, 'README.md'), README)

try:
    os.makedirs(ZIP_DIR)
except:
    pass

zf_name = "{}/{}.zip".format(ZIP_DIR, DIST_DIR)
clean_old_file(zf_name)
zf = zipfile.ZipFile(zf_name, 'w', zipfile.ZIP_DEFLATED)
zipdir(DIST_DIR, zf)
deltree(os.path.join(my_dir, DIST_DIR))
