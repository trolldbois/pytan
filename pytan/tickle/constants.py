# TODO currently, cElementTree is showing the fastest times. more testing needed
XML_ENGINE = "cet"
"""str of XML engine to use for XML de/serialization, must be one of XML_ENGINES"""
XML_ENGINES = {
    "cet": "xml.etree.cElementTree",
    "lxml": "lxml.etree",
    "et": "xml.etree.ElementTree",
}
"""
dict of valid XML_ENGINE values to use for XML de/serialization
also the order of priority to try for fallback if XML_ENGINE fails to import or is not set
"""
TAG_NAME = '_tickled_tag'
"""str of attribute to hold _SOAP_TAG of tanium_ng object so tickle can deserialize"""
LIST_NAME = '_tickled_list'
"""str of attribute to hold list of serialized tanium_ng objs"""
EXPLODE_NAME = '_tickled_explode'
"""str of attribute to identify JSON exploded property value in seriailzed dicts"""
INCLUDE_EMPTY = False
"""bool that controls if empty attributes will be included in serialized outputs"""
JSON_SORT_KEYS = True
"""bool that controls if the JSON string will be written with its keys sorted"""
JSON_INDENT = 2
"""int that controls how many spaces will be used to pretty print the JSON, None to disable"""
FLAT_WARN = {'_TICKLE_WARN': "Flattened objects can not be deserialized back later!!"}
"""dict to update serialized flat dicts with if FLAT=True"""
FLAT_SEP = '_'
"""str to seperate the tree of property names in serialized flat dicts with if FLAT=True"""

OBJECT_XPATH = ".//result_object/*"
"""str of xpath to find objects in Tanium SOAP API XML"""
RESULT_XPATH = ".//ResultXML"
"""str of xpath to find result data/result info in Tanium SOAP API XML"""
SSE_WRAP = (
    '''<return><ResultXML>
<![CDATA[<result_sets><result_set>
{SSE_DATA}
</result_set></result_sets>
]]>
</ResultXML>
</return>
''')
"""str of XML to wrap XML received from a server side data export with"""
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
"""str of Tanium's format for date time strings"""
