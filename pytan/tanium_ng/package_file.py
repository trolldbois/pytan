"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``file``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class PackageFile(BaseType):

    _soap_tag = 'file'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.hash = None
        self.name = None
        self.size = None
        self.source = None
        self.download_seconds = None
        self.trigger_download = None
        self.cache_status = None
        self.status = None
        self.bytes_downloaded = None
        self.bytes_total = None
        self.download_start_time = None
        self.last_download_progress_time = None
        self.deleted_flag = None
        self.file_status = None
        # no list_properties defined


from .package_file_status_list import PackageFileStatusList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['hash'] = str
SIMPLE_ARGS['name'] = str
SIMPLE_ARGS['size'] = int
SIMPLE_ARGS['source'] = str
SIMPLE_ARGS['download_seconds'] = int
SIMPLE_ARGS['trigger_download'] = int
SIMPLE_ARGS['cache_status'] = str
SIMPLE_ARGS['status'] = int
SIMPLE_ARGS['bytes_downloaded'] = int
SIMPLE_ARGS['bytes_total'] = int
SIMPLE_ARGS['download_start_time'] = str
SIMPLE_ARGS['last_download_progress_time'] = str
SIMPLE_ARGS['deleted_flag'] = int

COMPLEX_ARGS = {}
COMPLEX_ARGS['file_status'] = PackageFileStatusList

LIST_ARGS = {}
# no LIST_ARGS defined
