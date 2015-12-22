"""Object Serializer/Deserializer for Tanium SOAP XML tag: ``white_listed_urls``

* License: MIT
* Copyright: Copyright Tanium Inc. 2015
* Generated from ``console.wsdl`` by ``build_tanium_ng.py`` on D2015-12-22T00-06-10Z-0400
* Version of ``console.wsdl``: 0.0.1
* Tanium Server version of ``console.wsdl``: 6.5.314.3400
* Version of PyTan: 4.0.0

"""
from .base import BaseType


class WhiteListedUrlList(BaseType):

    _soap_tag = 'white_listed_urls'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties=SIMPLE_ARGS,
            complex_properties=COMPLEX_ARGS,
            list_properties=LIST_ARGS,
        )
        # no simple_properties defined
        # no complex_properties defined
        self.white_listed_url = []


from .white_listed_url import WhiteListedUrl

SIMPLE_ARGS = {}
# no SIMPLE_ARGS defined

COMPLEX_ARGS = {}
# no COMPLEX_ARGS defined

LIST_ARGS = {}
LIST_ARGS['white_listed_url'] = WhiteListedUrl
