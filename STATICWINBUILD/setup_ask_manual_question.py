import os
import sys

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


from distutils.core import setup
import py2exe
setup(
    console=['../bin/ask_manual_question.py'],
    options={
        'py2exe': {
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
