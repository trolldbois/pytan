import os
import sys
import shutil

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


from distutils.core import setup
import py2exe # noqa

VERSION = "1.0.2"
DIST_DIR = "Tanium_Sensor_Analysis_Tool_dist_{}".format(VERSION)
BUILD_DIR = "build"

try:
    shutil.rmtree(os.path.join(my_dir, DIST_DIR))
    shutil.rmtree(os.path.join(my_dir, BUILD_DIR))
except:
    pass

setup(
    console=['../bin/Tanium_Sensor_Analysis_Tool.py'],
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
        '../lib/taniumpy/request_body_template.xml',
    ],
)

shutil.rmtree(os.path.join(my_dir, BUILD_DIR))

# create batch file for running here and for configuration
