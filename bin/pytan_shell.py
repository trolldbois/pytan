#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '3.0.0'

import os
import sys
sys.dont_write_bytecode = True
my_filepath = os.path.abspath(sys.argv[0])
my_file = os.path.basename(my_filepath)
my_name = os.path.splitext(my_file)[0]
my_dir = os.path.dirname(my_filepath)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

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
    'filter': {'value': "TPT1.pytanlab.com", 'operator': 'Equal', 'and_flag': 0},  # NEEDED FROM USER
    'group': {'value': 492},
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
    'filter': {'value': "Folder : Windows NT", 'operator': 'Equal', 'and_flag': 0},  # NEEDED FROM USER
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

left = [spec1, spec4]
right = [spec1, spec3, spec5]
