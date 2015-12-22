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

# from pytan.utils import taniumpy  # noqa
# from pytan.utils import constants  # noqa
# from pytan import utils  # noqa
# self = handler  # noqa


# Computer Name, that =:TPT1.pytanlab.com
spec1 = {
    'sensor': {'value': "Computer Name"},
    # 'sensor_object': {'id': 3, 'hash': "3409330187"},  # NEEDED FROM SENSOR
    'filter': {'value': "TPT1.pytanlab.com", 'operator': 'Equal', 'and_flag': 1},
    # NEEDED FROM USER
    # 'group': {'value': 492},
    # 'group_object': None,  # NEEDED FROM USER
}

# Computer Name
spec2 = {
    'sensor': {'value': "Computer Name"},
    # 'sensor_object': {'id': 3, 'hash': "3409330187"},  # NEEDED FROM SENSOR
}

# Folder Contents{folderPath=C:\\Program Files}, that =:Folder : Windows NT
spec3 = {
    'sensor': {'value': "Folder Contents"},
    # 'sensor_object': {'id': 508, 'hash': "3881863289"},  # NEEDED FROM SENSOR
    'parameters': {'folderPath': 'C:\\Program Files'},  # NEEDED FROM USER
    'filter': {'value': "Folder : Windows NT", 'operator': 'Equal', 'and_flag': 1},
    # NEEDED FROM USER
}

# Folder Contents{folderPath=C:\\Program Files}, that re:Folder : Windows NT
spec5 = {
    'sensor': {'value': "Folder Contents"},
    # 'sensor_object': {'id': 508, 'hash': "3881863289"},  # NEEDED FROM SENSOR
    'parameters': {'folderPath': 'C:\\Program Files'},  # NEEDED FROM USER
    'filter': {'value': ".*", 'operator': 'RegexMatch', 'and_flag': 0},  # NEEDED FROM USER
}

# Folder Contents{folderPath=C:\\Program Files}
spec4 = {
    'sensor': {'value': "Folder Contents"},
    # 'sensor_object': {'id': 508, 'hash': "3881863289"},  # NEEDED FROM SENSOR
    'parameters': {'folderPath': 'C:\\Program Files'},  # NEEDED FROM USER
}

# # left = [spec1, spec4]
# # right = [spec1, spec3, spec5]
# v = handler.ask_manual(left=[spec1, spec4], right=[spec1, spec3, spec5], get_results=False)
# # x = handler.get_groups({'value': 615}, limit_exact=1)

# q = v.question_object
# group = q.group
# pytan.utils.tanium_obj.recurse_group(group)
