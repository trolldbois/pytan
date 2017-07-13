"""Version info."""
from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "1.1.0"
__codename__ = "avocado"
__title__ = "tanium_kit"
__url__ = "https://github.com/tanium/tanium_kit"
__author__ = "Jim Olsen"
__email__ = "jim.olsen@tanium.com"
__description__ = "Collection of python utility modules."
__license__ = "MIT"
__copyright__ = "Copyright Tanium Inc. 2017"
__status__ = "production"

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
}

STRING = "{tool_title} v{tool_version}-{tool_codename}"
STRING = STRING.format(**TOOL_DICT)
TOOL_DICT["tool_string"] = STRING
