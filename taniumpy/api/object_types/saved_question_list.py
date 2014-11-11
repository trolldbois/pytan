

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from .base import BaseType

class SavedQuestionList(BaseType):

    OBJECT_LIST_TAG = 'saved_questions'

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='saved_questions',
            simple_properties={  },
            complex_properties={ 'cache_info': CacheInfo },
            list_properties={ 'saved_question': SavedQuestion },
        )
        
        self.cache_info = None
        self.saved_question = []

from saved_question import SavedQuestion
from cache_info import CacheInfo

