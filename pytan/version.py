"""Version info."""
from __future__ import absolute_import, division, print_function, unicode_literals

import platform
import sys

__version__ = "3.0.0"
"""Version for this product."""

__codename__ = "cauliflower"
"""Codename for this major version branch (alphabetical names of healthy foods)"""

__title__ = "pytan"
"""Title for this product"""

__url__ = "https://github.com/tanium/pytan"
"""URL for this product"""

__author__ = "Jim Olsen"
"""Author of this product"""

__email__ = "jim.olsen@tanium.com"
"""Email of author of this product"""

__description__ = "A python package that makes using the Tanium Server SOAP API easy."
"""Short description of this product"""

__license__ = "MIT"
"""License of this product"""

__copyright__ = "Copyright Tanium Inc. 2017"
"""Copyright of this product"""

__status__ = "production"
"""Status of this version of this product"""

__fullname__ = "Python for Tanium"
"""Full name of this product"""

__propername__ = "PyTan"
"""Reference name of this product"""

__shortname__ = "pytan"
"""Shortest name of this product possible"""

TOOL_DICT = {
    "tool_version": __version__,
    "tool_codename": __codename__,
    "tool_title": __title__,
    "tool_url": __url__,
    "tool_author": __author__,
    "tool_email": __email__,
    "tool_description": __description__,
    "tool_license": __license__,
    "tool_copyright": __copyright__,
    "tool_status": __status__,
    "tool_fullname": __fullname__,
    "tool_shortname": __shortname__,
    "tool_propername": __propername__,
    "tool_platform": platform.platform(),
    "tool_python_version": sys.version.replace("\n", " "),
}
"""Dictionary containing all of the values in this module for use in templating"""

PROD_STR = "{tool_fullname} v{tool_version}-{tool_codename}"
PROD_STR = PROD_STR.format(**TOOL_DICT)
"""Product string, and example of using TOOL_DICT for templating"""

# add PROD_STR to TOOL_DICT
TOOL_DICT["tool_prodstr"] = PROD_STR
