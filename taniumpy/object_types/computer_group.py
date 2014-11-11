

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from .base import BaseType

class ComputerGroup(BaseType):

    OBJECT_LIST_TAG = 'computer_group'

    def __init__(self):
        BaseType.__init__(self,
            soap_tag='computer_group',
            simple_properties={ 'id': int,
                        'name': str,
                        'deleted_flag': int },
            complex_properties={ 'computer_specs': ComputerSpecList },
            list_properties={  },
        )
        self.id = None
        self.name = None
        self.deleted_flag = None
        self.computer_specs = None
        

from computer_spec_list import ComputerSpecList

