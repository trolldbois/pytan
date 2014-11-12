
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class UploadFileList(BaseType):

    OBJECT_LIST_TAG = None

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='upload_file_list',
            simple_properties={},
            complex_properties={},
            list_properties={'upload_file': UploadFile},
        )
        
        
        self.upload_file = []

from upload_file import UploadFile

