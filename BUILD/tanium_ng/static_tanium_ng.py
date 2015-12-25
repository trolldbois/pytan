import sys

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str  # noqa
else:
    text_type = unicode  # noqa


class TaniumNextGenException(Exception):
    pass


class IncorrectTypeException(TaniumNextGenException):
    """Raised when a property is not of the expected type"""
    def __init__(self, obj, name, value, expected):
        self.name = name
        self.expected = expected
        self.value = value
        err = "Object {!r} attribute '{}' expected type '{}', got '{}' (value: '{}')"
        err = err.format(obj, name, expected.__name__, type(value).__name__, value)
        TaniumNextGenException.__init__(self, err)


def get_obj_type(tag):
    """Maps Tanium XML soap tags to the Tanium NG Python BaseType object"""
    if tag not in BASE_TYPES:  # noqa
        err = 'Unknown type {}'
        err = err.format(tag)
        raise TaniumNextGenException(err)
    result = BASE_TYPES[tag]  # noqa
    return result


class BaseType(object):
    """Base Python Type used for all Tanium XML SOAP Objects"""

    _SOAP_TAG = None
    """str of XML tag that Tanium SOAP API Uses to define this object"""

    _INIT_VALUES = {}
    """dict that stores optional argument values={} for setting values after initialization"""

    _INITIALIZED = False
    """bool to check if the BaseType has finished initiailizing or not"""

    _SIMPLE_PROPS = {}
    """dict that stores the simple properties for this object (str, int)"""

    _COMPLEX_PROPS = {}
    """dict that stores the complex properties for this object (other BaseTypes)"""

    _LIST_PROPS = {}
    """dict that stores the complex properties for this object (other BaseTypes, str, int)"""

    _IS_LIST = False
    """bool indicating if this is a single list object or not"""

    _LIST_ATTR = ''
    """str that stores the name of the list attribute for this object if it is a single list"""

    _LIST_TYPE = None
    """stores the type of the list objects for this object if it is a single list"""

    _ATTRS = []
    """list that stores a preferentially sorted list of non-list attributes for this object"""

    def __init__(self, simple_properties, complex_properties, list_properties, **kwargs):
        self._INITIALIZED = False

        # TODO: dont want to raise exception, but do want to log! (maybe Warning class like req?)
        try:
            from . import tickle_ng
            self._TICKLE_NG = tickle_ng
        except:
            print("WARNING: UNABLE TO LOAD TICKLE_NG!!!")
            self._TICKLE_NG = None

        self._INIT_VALUES = kwargs.get('values', {}) or {}

        self._SIMPLE_PROPS = simple_properties
        self._COMPLEX_PROPS = complex_properties
        self._LIST_PROPS = list_properties

        self._IS_LIST = len(list_properties) == 1
        if self._IS_LIST:
            self._LIST_ATTR, self._LIST_TYPE = list(list_properties.items())[0]

        self._ATTRS = list(self._SIMPLE_PROPS.keys()) + list(self._COMPLEX_PROPS.keys())
        self._ATTRS = sorted(self._ATTRS)
        for f in ['name', 'id']:
            if f in self._ATTRS:
                self._ATTRS.remove(f)
                self._ATTRS.insert(0, f)

        self._ALL_PROPS = {}
        self._ALL_PROPS.update(self._SIMPLE_PROPS)
        self._ALL_PROPS.update(self._COMPLEX_PROPS)
        self._ALL_PROPS.update(self._LIST_PROPS)

        self._INITIALIZED = True

    def _list_only_method(self):
        """Exception to throw on methods that are only supported for single list types"""
        if not self._IS_LIST:
            err = 'Not a list type with a single list property!'
            raise TaniumNextGenException(err)

    def __getitem__(self, idx):
        """Support a[n] for single list types."""
        self._list_only_method()
        result = getattr(self, self._LIST_ATTR).__getitem__(idx)
        return result

    def append(self, value):
        """Support .append() for single list types."""
        self._list_only_method()
        if not isinstance(value, self._LIST_TYPE):
            raise IncorrectTypeException(self, self._LIST_ATTR, value, self._LIST_TYPE)
        getattr(self, self._LIST_ATTR).append(value)

    def __add__(self, value):
        """Support + operand for single list types.

        >>> a = SensorList()
        >>> b = SensorList()
        >>> c = Sensor()
        >>> b.append(c)
        >>> d = a + b
        """
        self._list_only_method()
        mylist = getattr(self, self._LIST_ATTR)
        valuelist = getattr(value, value._LIST_ATTR)
        newlist = mylist + valuelist
        newobj = self.__class__()
        setattr(newobj, newobj._LIST_ATTR, newlist)
        return newobj

    def __iadd__(self, value):
        """Support += operand for list types.

        >>> a = SensorList()
        >>> b = SensorList()
        >>> c = Sensor()
        >>> b.append(c)
        >>> a += b
        """
        self._list_only_method()
        mylist = getattr(self, self._LIST_ATTR)
        mylist += getattr(value, value._LIST_ATTR)
        return self

    def __len__(self):
        """Return length of list attribute if this object is a list, elsewise
        return the number of attributes that are not None.
        """
        if self._IS_LIST:
            result = len(getattr(self, self._LIST_ATTR))
        else:
            result = sum([1 for k in self._ATTRS if getattr(self, k, None) is not None])
        return result

    def __repr__(self):
        """If this is a list item, return class name, list, and all attributes.
        If this is not a list item, return class name and all attributes.
        """
        class_name = self.__class__
        vals = []
        if self._IS_LIST:
            val = '{} items'.format(len(self))
            name = 'LIST:{!r}:{!r}'.format(self._LIST_ATTR, self._LIST_TYPE)
            vals.append([name, val])

        for k in self._ATTRS:
            val = getattr(self, k, None)
            name = '{} ({})'.format(k, self._ALL_PROPS[k])
            if isinstance(val, list):
                val = "{}".format(len(val))
            else:
                val = "{!r}".format(val)
            vals.append([name, val])

        vals = ', '.join(["{}.{}={}".format(class_name, *p) for p in vals])
        result = '{}: {}'.format(class_name, vals)
        return result

    def __str__(self):
        """If this is a list item, return class name, list length, and all attributes that are set.
        If this is not a list item, return class name and all attributes that are set.
        """
        class_name = self.__class__.__name__
        vals = []
        if self._IS_LIST:
            name = 'length'
            val = len(self)
            vals.append([name, val])

        for k in self._ATTRS:
            if getattr(self, k, None) in [None, []]:
                continue
            name = k
            val = getattr(self, k, None)
            if isinstance(val, list):
                val = "{} items".format(len(val))
            else:
                val = str(val).replace('\n', '')
            vals.append([name, val])

        if vals:
            vals = ', '.join(["{}.{}={}".format(class_name, *p) for p in vals])
        else:
            vals = "No attributes assigned yet!"

        result = '{}: {}'.format(class_name, vals)
        return result

    def __setattr__(self, name, value):
        """Enforce type of attribute assignments"""
        val_not_none = value is not None
        is_init = name != '_INITIALIZED' and getattr(self, '_INITIALIZED', False)
        if all([val_not_none, is_init]):
            if name in getattr(self, '_LIST_PROPS', {}):
                value = self._check_list(name, value)
            elif name in getattr(self, '_COMPLEX_PROPS', {}):
                value = self._check_complex(name, value)
            elif name in getattr(self, '_SIMPLE_PROPS', {}):
                value = self._check_simple(name, value)
        super(BaseType, self).__setattr__(name, value)

    def _set_init_values(self):
        for k, v in self._INIT_VALUES.items():
            setattr(self, k, v)

    def _check_complex(self, name, value):
        if not isinstance(value, self._COMPLEX_PROPS[name]):
            raise IncorrectTypeException(self, name, value, self._COMPLEX_PROPS[name])
        return value

    def _check_simple(self, name, value):
        if not isinstance(value, self._SIMPLE_PROPS[name]):
            if self._SIMPLE_PROPS[name] == int:
                try:
                    value = self._SIMPLE_PROPS[name](value)
                except:
                    raise IncorrectTypeException(self, name, value, self._SIMPLE_PROPS[name])
            else:
                raise IncorrectTypeException(self, name, value, self._SIMPLE_PROPS[name])
        return value

    def _check_list(self, name, value):
        if not isinstance(value, list):
            raise IncorrectTypeException(self, name, value, self._LIST_PROPS[name])
        for i in value:
            if not isinstance(i, self._LIST_PROPS[name]):
                raise IncorrectTypeException(self, name, i, self._LIST_PROPS[name])
        return value

    def to_xml(self, **kwargs):
        """Deserialize self ``obj`` into an XML body, relies on tickle_ng"""
        tickle_val = self._TICKLE_NG.ObjectToXML(self, **kwargs)
        result = tickle_val.XML
        return result


class ColumnList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``cs``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'cs'
    _OVERRIDE_XPATH = {
        'columns': './c',
    }

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={},
            complex_properties={},
            list_properties={'columns': Column},
            **kwargs
        )
        self.columns = []
        self._set_init_values()


class Column(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``c``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'c'
    _OVERRIDE_XPATH = {
        'what_hash': './wh',
        'display_name': './dn',
        'result_type': './rt',
        'values': './v',
    }

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'what_hash': int,
                'display_name': text_type,
                'result_type': int},
            complex_properties={},
            list_properties={'values': text_type},
            **kwargs
        )
        self.what_hash = None
        self.display_name = None
        self.result_type = None
        self.values = []
        self._set_init_values()


class RowList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``rs``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'rs'
    _OVERRIDE_XPATH = {
        'rows': './r',
    }

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={},
            complex_properties={},
            list_properties={'rows': Row},
            **kwargs
        )
        self.rows = []
        self._set_init_values()


class Row(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``r``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'r'
    _OVERRIDE_XPATH = {
        'columns': './c',
    }
    """Override the xpath used to find these elements"""

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={'id': int, 'cid': int},
            complex_properties={},
            list_properties={'columns': Column},
            **kwargs
        )
        self.id = None
        self.cid = None
        self.columns = []
        self._set_init_values()


class ResultInfoList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``result_infos``.

    This is the return from GetResultInfo, and it is not defined in console.wsdl,
    so it is statically defined.

    result_info could technically be a list, but the Tanium SOAP API only ever returns one, so
    we have it defined as a complex property instead of a list property.
    """

    _SOAP_TAG = 'result_infos'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={'now': text_type},
            complex_properties={'result_info': ResultInfo},
            list_properties={},
            **kwargs
        )
        self.now = None
        self.result_info = None
        self._set_init_values()


class ResultInfo(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``result_info``.

    This is the return from GetResultInfo, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'result_info'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'id': int,
                'age': int,
                'report_count': int,
                'saved_question_id': int,
                'question_id': int,
                'archived_question_id': int,
                'seconds_since_issued': int,
                'issue_seconds': int,
                'expire_seconds': int,
                'tested': int,
                'passed': int,
                'mr_tested': int,
                'mr_passed': int,
                'estimated_total': int,
                'select_count': int,
                'row_count': int,
                'error_count': int,
                'no_results_count': int,
                'row_count_machines': int,
                'row_count_flag': int,
            },
            complex_properties={},
            list_properties={},
            **kwargs
        )
        self.id = None
        self.age = None
        self.report_count = None
        self.saved_question_id = None
        self.question_id = None
        self.archived_question_id = None
        self.seconds_since_issued = None
        self.issue_seconds = None
        self.expire_seconds = None
        self.tested = None
        self.passed = None
        self.mr_tested = None
        self.mr_passed = None
        self.estimated_total = None
        self.select_count = None
        self.row_count = None
        self.error_count = None
        self.no_results_count = None
        self.row_count_machines = None
        self.row_count_flag = None
        self._set_init_values()


class ResultSetList(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``result_sets``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.

    result_set could technically be a list, but the Tanium SOAP API only ever returns one, so
    we have it defined as a complex property instead of a list property.
    """

    _SOAP_TAG = 'result_sets'

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={'now': text_type},
            complex_properties={'result_set': ResultSet},
            list_properties={},
            **kwargs
        )
        self.now = None
        self.result_set = None
        self._set_init_values()


class ResultSet(BaseType):
    """Python Object representation for Tanium SOAP XML tag: ``result_set``.

    This is the return from GetResultData, and it is not defined in console.wsdl,
    so it is statically defined.
    """

    _SOAP_TAG = 'result_set'
    _OVERRIDE_XPATH = {
        'rows': './rs',
        'columns': './cs',
    }
    """Override the xpath used to find these elements"""

    def __init__(self, **kwargs):
        BaseType.__init__(
            self,
            simple_properties={
                'age': int,
                'report_count': int,
                'saved_question_id': int,
                'question_id': int,
                'archived_question_id': int,
                'seconds_since_issued': int,
                'issue_seconds': int,
                'expire_seconds': int,
                'tested': int,
                'passed': int,
                'mr_tested': int,
                'mr_passed': int,
                'estimated_total': int,
                'select_count': int,
                'row_count': int,
                'row_count_machines': int,
                'filtered_row_count': int,
                'filtered_row_count_machines': int,
                'item_count': int,
            },
            complex_properties={'rows': RowList, 'columns': ColumnList},
            list_properties={},
            **kwargs
        )

        self.now = None
        self.age = None
        self.report_count = None
        self.saved_question_id = None
        self.question_id = None
        self.archived_question_id = None
        self.seconds_since_issued = None
        self.issue_seconds = None
        self.expire_seconds = None
        self.tested = None
        self.passed = None
        self.mr_tested = None
        self.mr_passed = None
        self.estimated_total = None
        self.select_count = None
        self.row_count = None
        self.row_count_machines = None
        self.filtered_row_count = None
        self.filtered_row_count_machines = None
        self.item_count = None
        self.rows = None
        self.columns = None
        self._set_init_values()
