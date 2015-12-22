"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``white_listed_url``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class WhiteListedUrl(BaseType):

    _soap_tag = 'white_listed_url'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        self.id = None
        self.chunk_id = None
        self.download_seconds = None
        self.url_regex = None
        self.metadata = None
        # no list_properties defined


from .metadata_list import MetadataList

SIMPLE_ARGS = {}
SIMPLE_ARGS['id'] = int
SIMPLE_ARGS['chunk_id'] = str
SIMPLE_ARGS['download_seconds'] = int
SIMPLE_ARGS['url_regex'] = str

COMPLEX_ARGS = {}
COMPLEX_ARGS['metadata'] = MetadataList

LIST_ARGS = {}
# no LIST_ARGS defined
