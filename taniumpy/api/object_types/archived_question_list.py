
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class ArchivedQuestionList(BaseType):

    _OBJECT_LIST_TAG = 'archived_questions'

    def __init__(self):
        BaseType.__init__(
            self,
            soap_tag='archived_questions',
            simple_properties={},
            complex_properties={},
            list_properties={'archived_question': ArchivedQuestion},
        )
        
        
        self.archived_question = []

from archived_question import ArchivedQuestion

