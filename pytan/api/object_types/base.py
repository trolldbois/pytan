# Copyright (c) 2014 Tanium Inc
#

import io
import xml.etree.ElementTree as ET


class BaseType(object):
    def __init__(self, soap_tag, simple_properties, complex_properties,
                 list_properties):
        self._soap_tag = soap_tag
        self._simple_properties = simple_properties
        self._complex_properties = complex_properties
        self._list_properties = list_properties

    def __getitem__(self, n):
        """Allow automatic indexing into lists.

        Only supported on types that have a single property
        that is in list_properties

        """
        if len(self._list_properties) == 1:
            return getattr(self, self._list_properties.items()[0][0])[n]
        else:
            raise Exception(
                'Not simply a list type, __getitem__ not supported'
            )

    def __len__(self):
        """Allow len() for lsits.

        Only supported on types that have a single property
        that is in list_properties

        """
        if len(self._list_properties) == 1:
            return len(getattr(self, self._list_properties.items()[0][0]))
        else:
            raise Exception('Not simply a list type, len() not supported')

    def __str__(self):
        class_name = self.__class__.__name__
        val = ''
        if len(self._list_properties) == 1:
            val = ', len: {}'.format(len(self))
        else:
            if getattr(self, 'name', ''):
                val = ', name: {!r}'.format(self.name)
            elif getattr(self, 'id', ''):
                val = ', id: {!r}'.format(self.id)
            else:
                vals = [
                    '{}: {!r}'.format(p, getattr(self, p, ''))
                    for p in sorted(self._simple_properties)
                ]
                if vals:
                    vals = "\t" + "\n\t".join(vals)
                    val = ', vals:\n{}'.format(vals)
        ret = '{}{}'.format(class_name, val)
        return ret

    def append(self, n):
        """Allow adding to list.

        Only supported on types that have a single property
        that is in list_properties

        """
        if len(self._list_properties) == 1:
            getattr(self, self._list_properties.items()[0][0]).append(n)
        else:
            raise Exception(
                'Not simply a list type, append not supported'
            )

    def toSOAPElement(self, minimal=False):
        root = ET.Element(self._soap_tag)
        for p in self._simple_properties:
            el = ET.Element(p)
            val = getattr(self, p)
            if val is not None:
                el.text = str(val)
            if val is not None or not minimal:
                root.append(el)
        for p in self._complex_properties:
            val = getattr(self, p)
            if val is not None or not minimal:
                if isinstance(val, BaseType):
                    root.append(val.toSOAPElement(minimal=minimal))
                else:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.append(str(val))
        for p, t in self._list_properties.iteritems():
            vals = getattr(self, p)
            if not vals:
                continue
            for val in vals:
                root.append(val.toSOAPElement(minimal=minimal))

        return root

    def toSOAPBody(self, minimal=False):
        out = io.BytesIO()
        ET.ElementTree(self.toSOAPElement(minimal=minimal)).write(out)
        return out.getvalue()

    @classmethod
    def fromSOAPElement(cls, el):
        result = cls()
        for p, t in result._simple_properties.iteritems():
            pel = el.find("./{}".format(p))
            if pel is not None and pel.text:
                setattr(result, p, t(pel.text))
            else:
                setattr(result, p, None)
        for p, t in result._complex_properties.iteritems():
            elems = el.findall('./{}'.format(p))
            if len(elems) > 1:
                raise Exception(
                    'Unexpected: {} elements for property'.format(p)
                )
            elif len(elems) == 1:
                setattr(
                    result,
                    p,
                    result._complex_properties[p].fromSOAPElement(elems[0]),
                )
            else:
                setattr(result, p, None)
        for p, t in result._list_properties.iteritems():
            setattr(result, p, [])
            elems = el.findall('./{}'.format(p))
            for elem in elems:
                getattr(result, p).append(t.fromSOAPElement(elem))

        return result

    @classmethod
    def fromSOAPBody(cls, body):
        """Parse body (text) and produce Python tanium objects.

        This method assumes a single result_object, which
        may be a list or a single object.

        """
        tree = ET.fromstring(body)
        result_object = tree.find(".//result_object/*")
        if result_object is None:
            return None  # no results, not an error
        # based on the tag of the matching element,
        # find the appropriate tanium_type and deserialize
        from object_list_types import OBJECT_LIST_TYPES
        if result_object.tag not in OBJECT_LIST_TYPES:
            raise Exception('Unknown type {}'.format(result_object.tag))
        r = OBJECT_LIST_TYPES[result_object.tag].fromSOAPElement(result_object)
        r._RESULT_OBJECT = result_object
        return r
