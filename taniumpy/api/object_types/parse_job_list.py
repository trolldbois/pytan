
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParseJobList(BaseType):

    OBJECT_LIST_TAG = 'parse_jobs'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'parse_jobs',
            simple_properties = {},
            complex_properties = {},
            list_properties = {'parse_job': ParseJob},
        )
        
        
        self.parse_job = []

from parse_job import ParseJob

