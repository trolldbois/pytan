"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``status``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class PackageFileStatus(BaseType):

    _soap_tag = 'status'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.server_id = None
        self.server_name = None
        self.status = None
        self.cache_status = None
        self.cache_message = None
        self.bytes_downloaded = None
        self.bytes_total = None
        self.download_start_time = None
        self.last_download_progress_time = None
        # no complex_properties defined
        # no list_properties defined


# no extra imports used

SIMPLE_ARGS = {}
SIMPLE_ARGS['server_id'] = int
SIMPLE_ARGS['server_name'] = str
SIMPLE_ARGS['status'] = int
SIMPLE_ARGS['cache_status'] = str
SIMPLE_ARGS['cache_message'] = str
SIMPLE_ARGS['bytes_downloaded'] = int
SIMPLE_ARGS['bytes_total'] = int
SIMPLE_ARGS['download_start_time'] = str
SIMPLE_ARGS['last_download_progress_time'] = str

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
# no LIST_ARGS defined
