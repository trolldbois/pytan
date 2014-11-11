

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from xml.etree import ElementTree as ET

class SavedActionRowId:
    def __init__(self, val=None):
        self.val = val

    def toSOAPElement(
        el = ET.Element('saved_action_row_id')
        el.text = str(val)
        return el
