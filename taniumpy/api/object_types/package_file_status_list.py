
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class PackageFileStatusList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'package_file_status_list',
            simple_properties = {},
            complex_properties = {},
            list_properties = {'status': PackageFileStatus},
        )
        
        
        self.status = []

from package_file_status import PackageFileStatus

