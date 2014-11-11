

# Copyright (c) 2014 Tanium Inc
#
# Generated from console.wsdl version 0.0.1     
#
#


from xml.etree import ElementTree as ET

class Permission:
    def __init__(self, val=None):
        self.val = val

    def toSOAPElement(
        el = ET.Element('permission')
        el.text = str(val)
        return el
