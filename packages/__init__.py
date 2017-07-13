"""Adds paths to the PYTHONPATH so normal import usage can occur for external packages.

Directories under this package:

    * any: contains python packages that work for any OS
    * windows: contains python packages that work only for Windows
    * tanium: contains python packages written and maintained by Tanium
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import sys

THIS_FILE = __file__
"""This file, ala ``/github/pytan/packages/__init__.py``"""

THIS_PATH = os.path.abspath(os.path.dirname(THIS_FILE))
"""The path from this file, ala ``/github/pytan/packages``"""

ANY_PATH = os.path.join(THIS_PATH, "any")
"""The non-platform specific library path, ala ``/github/pytan/packages/any``"""

if ANY_PATH not in sys.path:
    sys.path.insert(0, ANY_PATH)

TANIUM_PATH = os.path.join(THIS_PATH, "tanium")
"""The tanium library path, ala ``/github/pytan/packages/tanium``"""

if TANIUM_PATH not in sys.path:
    sys.path.insert(0, TANIUM_PATH)

THIS_PLATFORM = platform.system().lower()
"""Platform for this system."""

THIS_PLATFORM_PATH = os.path.join(THIS_PATH, THIS_PLATFORM)
"""The platform specific library path, ala ``/github/pytan/packages/windows``"""

if os.path.exists(THIS_PLATFORM_PATH) and THIS_PLATFORM not in sys.path:
    sys.path.insert(0, THIS_PLATFORM_PATH)
