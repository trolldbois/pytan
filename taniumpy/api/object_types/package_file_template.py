
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PackageFileTemplate(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'file_template',
            simple_properties = {'hash': str,
                        'name': str,
                        'source': str,
                        'download_seconds': int},
            complex_properties = {},
            list_properties = {},
        )
        self.hash = None
        self.name = None
        self.source = None
        self.download_seconds = None
        
        



