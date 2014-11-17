
# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#

from .base import BaseType


class SavedActionRowIdList(BaseType):

    _soap_tag = 'saved_action_row_id_list'

    def __init__(self):
        BaseType.__init__(
            self,
            simple_properties={'row_id': int},
            complex_properties={},
            list_properties={},
        )
        self.row_id = None
        
        



