
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PackageFileList(BaseType):

    OBJECT_LIST_TAG = 'package_files'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='package_files',
            simple_properties={},
            complex_properties={},
            list_properties={'file': PackageFile},
        )
        
        
        self.file = []

from package_file import PackageFile

