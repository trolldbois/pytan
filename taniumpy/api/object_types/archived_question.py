
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ArchivedQuestion(BaseType):

    OBJECT_LIST_TAG = 'archived_question'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag = 'archived_question',
            simple_properties = {'id': int},
            complex_properties = {},
            list_properties = {},
        )
        self.id = None
        
        



