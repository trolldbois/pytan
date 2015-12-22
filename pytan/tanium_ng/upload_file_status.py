"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``upload_file_status``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T02-55-41Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class UploadFileStatus(BaseType):

    _soap_tag = 'upload_file_status'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.hash = None
        self.percent_complete = None
        self.file_cached = None
        self.file_parts = None
        # no list_properties defined


from .upload_file_list import UploadFileList

# Simple fix for type differences for text strings: str (3.x) vs unicode (2.x)

import sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa

SIMPLE_ARGS = {}
SIMPLE_ARGS['hash'] = text_type
SIMPLE_ARGS['percent_complete'] = int
SIMPLE_ARGS['file_cached'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['file_parts'] = UploadFileList

LIST_ARGS = {}
# no LIST_ARGS defined
