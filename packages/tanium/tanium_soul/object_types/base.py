# Copyright (c) 2015 Tanium Inc
#

import csv
import io
import json
import re

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


class IncorrectTypeException(Exception):
    """Raised when a property is not of the expected type"""
    def __init__(self, property, expected, actual):
        self.property = property
        self.expected = expected
        self.actual = actual
        err = 'Property {} is not of type {}, got {}'.format
        Exception.__init__(self, err(property, str(expected), str(actual)))


class BaseType(object):

    _soap_tag = None

    def __init__(self, simple_properties, complex_properties,
                 list_properties):
        self._initialized = False
        self._simple_properties = simple_properties
        self._complex_properties = complex_properties
        self._list_properties = list_properties
        self._initialized = True
        # ADDED IN 2.3.0
        self._CHANGED = False
        self._ADDED = False
        self._STR_CONFIG = {
            "str_only_attrs": ["name", "id"],
            "str_skip_attrs": [],
            "str_skip_vals": [None],
            "str_all_attrs": False,
            "str_all_simple_attrs": False,
            "str_items": False,
            "str_multiline": False,
            "str_indent": 2,
        }
        self._PRIMARY_ATTR = "name"

    # UPDATED IN 2.3.0
    def __getitem__(self, n):
        list_properties = getattr(self, "_list_properties", {})
        if list_properties:
            list_attr = list_properties.keys()[0]
            list_obj = getattr(self, list_attr)

            if isinstance(n, int):
                ret = list_obj[n]
            else:
                ret = [x for x in list_obj if str(getattr(x, self._PRIMARY_ATTR, None)) == n]
                if len(ret) == 0:
                    m = "No items found in {o} where primary attribute {p} == {n}"
                    m = m.format(o=self, p=self._PRIMARY_ATTR, n=n)
                    raise Exception(m)
                elif len(ret) > 1:
                    m = "More than one items found in {o} where primary attribute {p} == {n}: {r}"
                    m = m.format(o=self, p=self._PRIMARY_ATTR, n=n, r=ret)
                    raise Exception(m)
                else:
                    ret = ret[0]
        else:
            m = "Not simply a list type, __getitem__ not supported"
            raise Exception(m)
        return ret

    # UPDATED IN 2.3.0
    def __len__(self):
        """Allow len() for lists and items.

        len() on item will return the number of attributes that are not None.
        len() on list will return the number of items in list.
        """
        list_properties = getattr(self, "_list_properties", {})
        if list_properties:
            ret = len(getattr(self, list_properties.keys()[0]))
        else:
            simple_properties = sorted(getattr(self, "_simple_properties", {}))
            complex_properties = sorted(getattr(self, "_complex_properties", {}))
            vals = {k: getattr(self, k, None) for k in simple_properties + complex_properties}
            ret = len([k for k, v in vals.items() if v is not None])
        return ret

    # ADDED IN 2.3.0
    def str_obj(self, **str_config):
        obj = str_config.get("obj", self)
        str_json = str_config.get("str_json", False)

        if isinstance(obj, BaseType):
            ret = obj.jsonify() if str_json else obj.__str__(**str_config)
        else:
            try:
                ret = json.dumps(obj, skipkeys=True, sort_keys=True, indent=2) if str_json else str(obj)
            except:
                ret = str(obj)
        return ret

    # ADDED IN 2.3.0
    def jsonify(self, **kwargs):
        obj = kwargs.get("obj", self)
        ret = obj.to_json(obj)
        return ret

    # ADDED IN 2.3.0
    def __eq__(self, other):
        # this is simple and problematic but should work for most base types
        # used for: obj in objlist, obj == obj

        this_json = self.str_obj(obj=self, str_json=True)
        other_json = self.str_obj(obj=other, str_json=True)

        ret = this_json == other_json
        return ret

    # ADDED IN 2.3.0
    @property
    def _get_tracker(self):
        if not hasattr(self, "_TRACKER"):
            self._TRACKER = []
        return self._TRACKER

    # ADDED IN 2.3.0
    def _track(self, t_attr="", t_old="", t_new="", t_action="Updated", **kwargs):
        track = {}
        track["action"] = t_action
        track["attr"] = t_attr
        track["obj"] = str(self)

        margs = {}
        margs.update(kwargs)
        margs.update(obj=t_old)
        track["old"] = self.str_obj(**margs)

        margs.update(obj=t_new)
        track["new"] = self.str_obj(**margs)
        self._get_tracker.append(track)
        return self

    # ADDED IN 2.3.0
    def _track_merge(self, other, **kwargs):
        other_first = kwargs.get("other_first", False)

        this_t = self._get_tracker
        other_t = other._get_tracker
        new_t = other_t + this_t if other_first else this_t + other_t
        # print("this: {}".format(self))
        # print("this tracker:\n{}".format("\n".join([str(x) for x in this_t])))

        # print("other: {}".format(other))
        # print("other tracker:\n{}".format("\n".join([str(x) for x in other_t])))

        # print("new tracker:\n{}".format("\n".join([str(x) for x in new_t])))
        self._TRACKER = new_t
        return self._get_tracker

    def _track_set(self, t_attr, t_new, t_action="Updated", **kwargs):
        t_old = getattr(self, t_attr, "")
        margs = {}
        margs.update(kwargs)
        margs.update(t_attr=t_attr, t_old=t_old, t_new=t_new, t_action=t_action)
        self._track(**margs)
        setattr(self, t_attr, t_new)
        self._CHANGED = True
        return self

    # ADDED IN 2.3.0
    def __repr__(self):
        return self.__str__()

    # UPDATED IN 2.3.0
    def __str__(self, **str_config):
        """New str method for 2.3.0.

        complex ex from User:
            simple_properties={
                'id': int,
                'name': str,
                'domain': str,
                'group_id': int,
                'deleted_flag': int,
                'last_login': str,
                'active_session_count': int,
                'local_admin_flag': int,
            }

        complex ex from User:
            complex_properties={
               'permissions': PermissionList,
               'roles': UserRoleList,
               'metadata': MetadataList,
            }
        list ex from UserList:
            list_properties={
                'user': User,
            }
        """
        # create this str config using self._STR_CONFIG and update this str config with any kwargs passed in
        this_sc = dict(**self._STR_CONFIG)
        this_sc.update(str_config)

        # get this object name
        obj_name = self.__class__.__name__
        # get this objects length
        obj_len = "Length={t}".format(t=len(self))

        # set a spacer based on str_indent
        spacer = " " * this_sc["str_indent"]

        # set a number of templates and joins based on str_multline
        attr_tmpl = ("{k}: {v}" if this_sc["str_multiline"] else "{k}: '{v}'").format
        multijoin = "\n{s}".format(s=spacer)
        singlejoin = ", "
        listjoin = multijoin if this_sc["str_multiline"] else singlejoin

        # create a sub str config with an increased indent for str_obj calls from this obj
        sub_sc = {k: v for k, v in this_sc.items() if k not in ["obj"]}
        sub_sc["str_indent"] += 2

        # get the simple attributes for this obj
        simple_properties = sorted(getattr(self, "_simple_properties", {}))
        # get the complex attributes for this obj
        complex_properties = sorted(getattr(self, "_complex_properties", {}))
        # get the list properties for this obj
        list_properties = getattr(self, "_list_properties", {})

        # get the values of all simple attrs
        simple_values = {k: getattr(self, k, None) for k in simple_properties}
        # get the values of all complex attrs
        complex_values = {k: getattr(self, k, None) for k in complex_properties}

        # filter the list of simple attrs based on str config
        # override str_all_attrs with str_all_simple_attrs if it is True
        m_sc = dict(**this_sc)
        m_sc["str_all_attrs"] = this_sc["str_all_simple_attrs"] or m_sc["str_all_attrs"]
        simple_attrs = self._str_filter_attrs(attrs_list=simple_properties, this_sc=m_sc)
        # filter the list of complex attrs based on str config
        complex_attrs = self._str_filter_attrs(attrs_list=complex_properties, this_sc=this_sc)

        # if there are no simple or complex attrs, and it is not a list object, rebuild simple_attrs
        # with str_all_attrs = True
        if not any([simple_attrs, complex_attrs, list_properties]):
            m_sc["str_all_attrs"] = True
            simple_attrs = self._str_filter_attrs(attrs_list=simple_properties, this_sc=m_sc)

        # filter simple attrs based on str_skip_vals
        simple_items = self._str_filter_vals(attrs_list=simple_attrs, vals_dict=simple_values, this_sc=this_sc)
        # filter complex attrs based on str_skip_vals
        complex_items = self._str_filter_vals(attrs_list=complex_attrs, vals_dict=complex_values, this_sc=this_sc)
        # run str_obj on complex item values using sub_sc
        complex_items = [(k, self.str_obj(obj=v, **sub_sc)) for k, v in complex_items]
        # get the list items if this is a list and str_items=True
        list_items = [x for x in self] if list_properties and this_sc["str_items"] else []

        # turn simple and complex and list values into text items
        simple_text_items = [attr_tmpl(k=k, v=v) for k, v in simple_items]
        complex_text_items = [attr_tmpl(k=k, v=v) for k, v in complex_items]
        list_text_items = [self.str_obj(obj=x, **sub_sc) for x in list_items]

        # put object name first in the output
        output_items = [obj_name]

        # put object length second if its a list
        if list_properties:
            output_items += [obj_len]

        # put all simple attrs next
        if simple_text_items:
            output_items += [listjoin.join(simple_text_items)]

        # put all complex attrs next
        if complex_text_items:
            output_items += [listjoin.join(complex_text_items)]

        # put all list items if its a list and str_items = True
        if list_properties and this_sc["str_items"]:
            item_type = list_properties.values()[0]
            item_is_bt = isinstance(item_type(), BaseType)
            gt1 = len(self) > 1
            use_multijoin = (item_is_bt and gt1) or this_sc["str_multiline"]
            if use_multijoin:
                list_text = multijoin.join(list_text_items)
                list_spacer = multijoin
            else:
                list_text = listjoin.join(list_text_items)
                list_spacer = ""
            list_text = "{s}[{t}]{s}".format(s=list_spacer, t=list_text or "Empty List!")
            output_items += [list_text]

        ret = listjoin.join(output_items)
        return ret

    @property
    def _get_list_attr(self):
        ret = self._list_properties.items()[0][0]
        return ret

    @property
    def _get_list(self):
        if len(self._list_properties) == 1:
            ret = getattr(self, self._get_list_attr)
        else:
            raise Exception('Not simply a list type, get_list not supported')
        return ret

    def _set_list(self, value):
        if len(self._list_properties) == 1:
            setattr(self, self._get_list_attr, value)
        else:
            raise Exception('Not simply a list type, set_list not supported')

    # ADDED IN 2.3.0
    def remove(self, n):
        if len(self._list_properties) == 1:
            getattr(self, self._get_list_attr).remove(n)
        else:
            raise Exception('Not simply a list type, remove not supported')

    # ADDED IN 2.3.0
    def _str_filter_attrs(self, attrs_list, this_sc):
        ret = []

        # put the only attrs in first if they exist
        for x in this_sc["str_only_attrs"]:
            if x not in ret and x not in this_sc["str_skip_attrs"]:
                ret.append(x)

        # use all attrs if all_attrs, elsewise only use attrs in only_attrs
        if this_sc["str_all_attrs"]:
            for x in attrs_list:
                if x not in ret and x not in this_sc["str_skip_attrs"]:
                    ret.append(x)
        return ret

    # ADDED IN 2.3.0
    def _str_filter_vals(self, attrs_list, vals_dict, this_sc):
        ret = []
        for k in attrs_list:
            v = vals_dict.get(k, None)
            if v not in this_sc["str_skip_vals"]:
                ret.append((k, v))
        return ret

    # PRE 2.3.0 CODE:
    # def __len__(self):
    #     """Allow len() for lists.

    #     Only supported on types that have a single property
    #     that is in list_properties

    #     """
    #     if len(self._list_properties) == 1:
    #         return len(getattr(self, self._list_properties.items()[0][0]))
    #     else:
    #         raise Exception('Not simply a list type, len() not supported')

    # PRE 2.3.0 CODE:
    # def __str__(self):
    #     class_name = self.__class__.__name__
    #     val = ''
    #     if len(self._list_properties) == 1:
    #         val = ', len: {}'.format(len(self))
    #     else:
    #         if getattr(self, 'name', ''):
    #             val += ', name: {!r}'.format(self.name)
    #         if getattr(self, 'id', ''):
    #             val += ', id: {!r}'.format(self.id)
    #         if not val:
    #             vals = [
    #                 '{}: {!r}'.format(p, getattr(self, p, ''))
    #                 for p in sorted(self._simple_properties)
    #             ]
    #             if vals:
    #                 vals = "\t" + "\n\t".join(vals)
    #                 val = ', vals:\n{}'.format(vals)
    #     ret = '{}{}'.format(class_name, val)
    #     return ret

    def __setattr__(self, name, value):
        """Enforce type, if name is a complex property"""
        if value is not None and \
                name != '_initialized' and \
                self._initialized and \
                name in self._complex_properties:
            if not isinstance(value, self._complex_properties[name]):
                raise IncorrectTypeException(
                    value,
                    self._complex_properties[name],
                    type(value)
                )
        super(BaseType, self).__setattr__(name, value)

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

    def toSOAPElement(self, minimal=False): # noqa
        root = ET.Element(self._soap_tag)
        for p in self._simple_properties:
            el = ET.Element(p)
            val = getattr(self, p)
            if val is not None:
                el.text = str(val)
            if val is not None or not minimal:
                root.append(el)
        for p, t in self._complex_properties.iteritems():
            val = getattr(self, p)
            if val is not None or not minimal:
                if val is not None and not isinstance(val, t):
                    raise IncorrectTypeException(p, t, type(val))
                if isinstance(val, BaseType):
                    child = val.toSOAPElement(minimal=minimal)
                    # the tag name is the property name,
                    # not the property type's soap tag
                    el = ET.Element(p)
                    if child.getchildren() is not None:
                        for child_prop in child.getchildren():
                            el.append(child_prop)
                    root.append(el)
                else:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.append(str(val))
        for p, t in self._list_properties.iteritems():
            vals = getattr(self, p)
            if not vals:
                continue
            # fix for str types in list props
            if issubclass(t, BaseType):
                for val in vals:
                    root.append(val.toSOAPElement(minimal=minimal))
            else:
                for val in vals:
                    el = ET.Element(p)
                    root.append(el)
                    if val is not None:
                        el.text = str(val)
                    if vals is not None or not minimal:
                        root.append(el)
        return root

    def toSOAPBody(self, minimal=False): # noqa
        out = io.BytesIO()
        ET.ElementTree(self.toSOAPElement(minimal=minimal)).write(out)
        return out.getvalue()

    @classmethod
    def fromSOAPElement(cls, el): # noqa
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
                if issubclass(t, BaseType):
                    getattr(result, p).append(t.fromSOAPElement(elem))
                else:
                    getattr(result, p).append(elem.text)

        return result

    @classmethod
    def fromSOAPBody(cls, body): # noqa
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

    def flatten_jsonable(self, val, prefix):
        result = {}
        if type(val) == list:
            for i, v in enumerate(val):
                result.update(self.flatten_jsonable(
                    v,
                    '_'.join([prefix, str(i)]))
                )
        elif type(val) == dict:
            for k, v in val.iteritems():
                result.update(self.flatten_jsonable(
                    v,
                    '_'.join([prefix, k] if prefix else k))
                )
        else:
            result[prefix] = val
        return result

    def to_flat_dict_explode_json(self, val, prefix=""):
        """see if the value is json. If so, flatten it out into a dict"""
        try:
            js = json.loads(val)
            return self.flatten_jsonable(js, prefix)
        except Exception:
            return None

    def to_flat_dict(self, prefix='', explode_json_string_values=False):  # noqa
        """Convert the object to a dict, flattening any lists or nested types
        """
        result = {}
        prop_start = '{}_'.format(prefix) if prefix else ''
        for p, _ in self._simple_properties.iteritems():
            val = getattr(self, p)
            if val is not None:
                json_out = None
                if explode_json_string_values:
                    json_out = self.to_flat_dict_explode_json(val, p)
                if json_out is not None:
                    result.update(json_out)
                else:
                    result['{}{}'.format(prop_start, p)] = val
        for p, _ in self._complex_properties.iteritems():
            val = getattr(self, p)
            if val is not None:
                result.update(val.to_flat_dict(
                    prefix='{}{}'.format(prop_start, p),
                    explode_json_string_values=explode_json_string_values,
                ))
        for p, _ in self._list_properties.iteritems():
            val = getattr(self, p)
            if val is not None:
                for ind, item in enumerate(val):
                    prefix = '{}{}_{}'.format(prop_start, p, ind)
                    if isinstance(item, BaseType):
                        result.update(item.to_flat_dict(
                            prefix=prefix,
                            explode_json_string_values=explode_json_string_values,
                        ))
                    else:
                        result[prefix] = item
        return result

    def explode_json(self, val):
        try:
            return json.loads(val)
        except Exception:
            return None

    def to_jsonable(self, explode_json_string_values=False, include_type=True):  # noqa
        result = {}
        if include_type:
            result['_type'] = self._soap_tag
        for p, _ in self._simple_properties.iteritems():
            val = getattr(self, p)
            if val is not None:
                json_out = None
                if explode_json_string_values:
                    json_out = self.explode_json(val)
                if json_out is not None:
                    result[p] = json_out
                else:
                    result[p] = val
        for p, _ in self._complex_properties.iteritems():
            val = getattr(self, p)
            if val is not None:
                result[p] = val.to_jsonable(
                    explode_json_string_values=explode_json_string_values,
                    include_type=include_type)
        for p, _ in self._list_properties.iteritems():
            val = getattr(self, p)
            if val is not None:
                result[p] = []
                for ind, item in enumerate(val):
                    if isinstance(item, BaseType):
                        result[p].append(item.to_jsonable(
                            explode_json_string_values=explode_json_string_values,
                            include_type=include_type))
                    else:
                        result[p].append(item)
        return result

    @staticmethod
    def to_json(jsonable, **kwargs):
        """Convert to a json string.

        jsonable can be a single BaseType instance of a list
        of BaseType

        """
        if type(jsonable) == list:
            return json.dumps(
                [item.to_jsonable(**kwargs) for item in jsonable],
                sort_keys=True,
                indent=2,
            )
        else:
            return json.dumps(
                jsonable.to_jsonable(**kwargs),
                sort_keys=True,
                indent=2,
            )

    @classmethod
    def _from_json(cls, jsonable):
        """Private helper to parse from JSON after type is instantiated"""
        result = cls()
        for p, t in result._simple_properties.iteritems():
            val = jsonable.get(p)
            if val is not None:
                setattr(result, p, t(val))
        for p, t in result._complex_properties.iteritems():
            val = jsonable.get(p)
            if val is not None:
                setattr(result, p, BaseType.from_jsonable(val))
        for p, t in result._list_properties.iteritems():
            val = jsonable.get(p)
            if val is not None:
                vals = []
                for item in val:
                    if issubclass(t, BaseType):
                        vals.append(BaseType.from_jsonable(item))
                    else:
                        vals.append(item)
                setattr(result, p, vals)
        return result

    @staticmethod
    def from_jsonable(jsonable):
        """Inverse of to_jsonable, with explode_json_string_values=False.

        This can be used to import objects from serialized JSON. This JSON should come from BaseType.to_jsonable(explode_json_string_values=False, include+type=True)

        Examples
        --------
        >>> with open('question_list.json') as fd:
        ...    questions = json.loads(fd.read())
        ...    # is a list of serialized questions
        ...    question_objects = BaseType.from_jsonable(questions)
        ...    # will return a list of api.Question

        """
        if type(jsonable) == list:
            return [BaseType.from_jsonable(item for item in list)]
        elif type(jsonable) == dict:
            if not jsonable.get('_type'):
                raise Exception('JSON must contain _type to be deserialized')
            from object_list_types import OBJECT_LIST_TYPES
            if jsonable['_type'] not in OBJECT_LIST_TYPES:
                raise Exception('Unknown type {}'.format(jsonable['_type']))
            result = OBJECT_LIST_TYPES[jsonable['_type']]._from_json(jsonable)
            return result
        else:
            raise Exception('Expected list or dict to deserialize')

    @staticmethod  # noqa
    def write_csv(fd, val, explode_json_string_values=False, **kwargs):
        """Write 'val' to CSV. val can be a BaseType instance or a list of
        BaseType

        This does a two-pass, calling to_flat_dict for each object, then
        finding the union of all headers,
        then writing out the value of each column for each object
        sorted by header name

        explode_json_string_values attempts to see if any of the str values
        are parseable by json.loads, and if so treat each property as a column
        value

        fd is a file-like object
        """
        def sort_headers(headers, **kwargs):
            '''returns a list of sorted headers (Column names)
            If kwargs has 'header_sort':
              if header_sort == False, do no sorting
              if header_sort == [] or True, do sorted(headers)
              if header_sort == ['col1', 'col2'], do sorted(headers), then
                put those headers first in order if they exist
            '''
            header_sort = kwargs.get('header_sort', [])

            if header_sort is False:
                return headers
            elif header_sort is True:
                pass
            elif not type(header_sort) in [list, tuple]:
                raise Exception("header_sort must be a list!")

            headers = sorted(headers)

            if header_sort is True or not header_sort:
                return headers

            custom_sorted_headers = []
            for hs in header_sort:
                for hidx, h in enumerate(headers):
                    if h.lower() == hs.lower():
                        custom_sorted_headers.append(headers.pop(hidx))

            # append the rest of the sorted_headers that didn't
            # match header_sort
            custom_sorted_headers += headers
            return custom_sorted_headers

        def fix_newlines(val):
            if type(val) == str:
                # turn \n into \r\n
                val = re.sub(r"([^\r])\n", r"\1\r\n", val)
            return val

        base_type_list = [val] if isinstance(val, BaseType) else val
        headers = set()
        for base_type in base_type_list:
            row = base_type.to_flat_dict(explode_json_string_values=explode_json_string_values)
            for col in row:
                headers.add(col)

        writer = csv.writer(fd)

        headers_sorted = sort_headers(list(headers), **kwargs)
        writer.writerow(headers_sorted)

        for base_type in base_type_list:
            row = base_type.to_flat_dict(explode_json_string_values=explode_json_string_values)
            writer.writerow(
                [fix_newlines(row.get(col, '')) for col in headers_sorted]
            )
