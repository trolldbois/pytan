#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Provides an interactive console with pytan available as handler'''
__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '3.0.0'

import os
import sys
sys.dont_write_bytecode = True

my_file = os.path.abspath(sys.argv[0])
my_name = os.path.splitext(os.path.basename(my_file))[0]
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'pytan')
path_adds = [lib_dir]
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

import pytan
import pytan.utils.cmdline

if __name__ == "__main__":
    module = getattr(pytan.utils.cmdline, my_name)
    worker = module.Worker()
    version_check = worker.version_check(__version__)
    cons = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())
