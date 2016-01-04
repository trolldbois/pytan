#!/usr/bin/env python3 -i
"""Python shell for PyTan"""
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '4.0.0'

# BEGIN BOOTSTRAP CODE

# statically defined path
PYTAN_PATH = "~/gh/pytan"

import os
import sys
sys.dont_write_bytecode = True

# list of paths to insert at beginning of PYTHONPATH
path_adds = []

# add PYTAN_PATH to path_adds
path_adds.append(PYTAN_PATH)

# get parent_dir and add to path_adds (allows scripts that live in bin/ to work automatically)
my_filepath = os.path.abspath(sys.argv[0])
my_file = os.path.basename(my_filepath)
my_name = os.path.splitext(my_file)[0]
my_dir = os.path.dirname(my_filepath)
parent_dir = os.path.dirname(my_dir)
path_adds.append(parent_dir)

# if OS Environment "PYTAN_PATH" is set, add that to path_adds
if 'PYTAN_PATH' in os.environ:
    path_adds.append(os.environ['PYTAN_PATH'])

# expand user directories and get the absolute path of all path_adds
path_adds = [os.path.abspath(os.path.expanduser(aa)) for aa in path_adds]

# add the path_adds to beginning of PYTHONPATH
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

# END BOOTSTRAP CODE

import pytan  # noqa
from pytan import tickle  # noqa
i = "pytan.shell.{}".format(my_name)
__import__(i)
module = eval(i)
worker = module.Worker()

if __name__ == "__main__":
    version_check = worker.version_check(__version__)
    console = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())


# q = 'computer name and ip route details and ip address and installed applications'
# v = handler.ask_parsed(question_text=q, picker=1, sse=False)
# rd = v.question_results
# # rd = handler.get_result_data(v.question_object)
