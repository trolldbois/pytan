
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PackageFileTemplateList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='package_file_template_list',
            simple_properties={},
            complex_properties={},
            list_properties={'file_template': PackageFileTemplate},
        )
        
        
        self.file_template = []

from package_file_template import PackageFileTemplate

