
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ParseJob(BaseType):

    _OBJECT_LIST_TAG = 'parse_job'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='parse_job',
            simple_properties={'question_text': str,
                        'parser_version': int},
            complex_properties={},
            list_properties={},
        )
        self.question_text = None
        self.parser_version = None
        
        



