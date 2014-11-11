

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from .base import BaseType

class SavedActionApproval(BaseType):

    OBJECT_LIST_TAG = 'saved_action_approval'

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='saved_action_approval',
            simple_properties={ 'id': int,
                        'name': str,
                        'approved_flag': int },
            complex_properties={ 'metadata': MetadataList },
            list_properties={  },
        )
        self.id = None
        self.name = None
        self.approved_flag = None
        self.metadata = None
        

from metadata_list import MetadataList

