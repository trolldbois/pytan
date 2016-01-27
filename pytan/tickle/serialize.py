import json
import logging

from pytan import PytanError, text_type, encoding
from pytan.constants import SUPER_VERBOSE
from pytan.tickle import ET
from pytan.tanium_ng import BaseType, ResultSetList, ResultSet
from pytan.excelwriter import ExcelWriter
from pytan.tickle.tools import jsonify
from pytan.tickle.constants import (
    TAG_NAME, LIST_NAME, EXPLODE_NAME, FLAT_WARN, FLAT_SEP, INCLUDE_EMPTY, SKIPS, FIRSTS, LASTS,
    RESULTSET_ARGS, RESULTSET_STRS
)

MYLOG = logging.getLogger(__name__)

LF = '\n'
CR = '\r'
CRLF = CR + LF


class XmlSerializeError(PytanError):
    pass


class DictSerializeError(PytanError):
    pass


class ToTree(object):
    """Convert a tanium_ng BaseType object into an ElementTree object.

    x = ToTree(obj)

    Get RESULT:
    x.RESULT
    """

    OBJ = None
    """tanium_ng object to convert to ElementTree object RESULT"""

    RESULT = None
    """ElementTree object created from OBJ"""

    def __init__(self, obj, **kwargs):
        self.KWARGS = kwargs
        self.INCLUDE_EMPTY = kwargs.get('include_empty', INCLUDE_EMPTY)
        self.OBJ = obj

        if not isinstance(obj, BaseType):
            err = "obj must be a tanium_ng.BaseType object, supplied type: {!r}, obj: {}"
            err = err.format(type(obj).__name__, obj)
            MYLOG.error(err)
            raise XmlSerializeError(err)

        self.RESULT = ET.Element(obj._SOAP_TAG)
        self.base_simple()
        self.base_complex()
        self.base_list()

        if SUPER_VERBOSE:
            m = "Converted tanium_ng object {!r} into tree:: {}"
            m = m.format(type(self.OBJ), self.RESULT)
            MYLOG.debug(m)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.INCLUDE_EMPTY:
                continue
            self.add_simple_el(prop, val)

    def add_simple_el(self, prop, val):
        val = text_type(val) if val is not None else None
        el = ET.Element(prop)
        el.text = val
        self.RESULT.append(el)

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.INCLUDE_EMPTY:
                continue

            if isinstance(val, BaseType):
                el = ET.Element(prop)
                child_val = to_tree(val, **self.KWARGS)
                [el.append(c) for c in list(child_val)]
                self.RESULT.append(el)
            else:
                self.add_simple_el(prop, val)

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = getattr(self.OBJ, prop)
            if not vals:
                continue

            if issubclass(prop_type, BaseType):
                for val in vals:
                    child_val = to_tree(val, **self.KWARGS)
                    self.RESULT.append(child_val)
            else:
                for val in vals:
                    if val is None and not self.INCLUDE_EMPTY:
                        continue
                    self.add_simple_el(prop, val)


class ToDict(object):
    """Convert either a single or list of tanium_ng BaseType objects into a python
    dict object

    x = ToDict(obj)
     ..or..
    x = ToDict([obj])

    Get RESULT:
    x.RESULT
    """

    FLAT = False
    """
    bool that controls if all nested objects of OBJ will be flattened out when creating RESULT
    """

    OBJ = None
    """tanium_ng object to convert to RESULT"""

    RESULT = {}
    """dict created from OBJ"""

    _PROP_PRE = ''
    """str that holds FLAT_PRE + _FLAT_SEP IF FLAT=True"""

    _PARENT = True
    """bool to indicate if this is the first spawn of this object"""

    _FLAT_PRE = ''
    """str to prefix property names if FLAT=True"""

    def __init__(self, obj, **kwargs):
        self.KWARGS = kwargs
        self.OBJ = obj

        self.INCLUDE_EMPTY = kwargs.get('include_empty', INCLUDE_EMPTY)
        self.FLAT = kwargs.get('flat', False)
        self.FLAT_PRE = kwargs.get('flat_pre', '')
        self.FLAT_SEP = kwargs.get('flat_sep', FLAT_SEP)
        self.PARENT = kwargs.get('parent', True)

        if self.FLAT and self.FLAT_PRE and not self.PARENT:
            self._PROP_PRE = '{}{}'.format(self.FLAT_PRE, self.FLAT_SEP)
        else:
            self._PROP_PRE = ''

        self.RESULT = {}

        if isinstance(self.OBJ, list):
            self.do_list()
        elif isinstance(self.OBJ, BaseType):
            if self.OBJ._IS_LIST and self.FLAT and self.PARENT:
                self.do_list()
            else:
                self.do_obj()
        else:
            err = "obj is type {!r}, must be a tanium_ng.BaseType object or a list"
            err = err.format(type(obj).__name__)
            raise DictSerializeError(err)

    def do_obj(self):
        if self.FLAT:
            self.RESULT.update(FLAT_WARN)
        self.RESULT[TAG_NAME] = self.OBJ._SOAP_TAG
        self.base_simple()
        self.base_complex()
        self.base_list()
        self.RESULT[TAG_NAME] = self.OBJ._SOAP_TAG

        m = "Converted tanium_ng object {!r} into dict with keys:: {}"
        m = m.format(type(self.OBJ), ', '.join(self.RESULT.keys()))
        MYLOG.debug(m)

    def do_list(self):
        if self.FLAT:
            self.RESULT.update(FLAT_WARN)

        try:
            self.RESULT[TAG_NAME] = self.OBJ._SOAP_TAG
        except:
            pass

        self.RESULT[LIST_NAME] = []
        for val in self.OBJ:
            child_args = self.get_child_args()
            child_val = to_dict(val, **child_args)
            self.RESULT[LIST_NAME].append(child_val)

        m = "Converted list of {} Tanium NG objects into a dict with keys:: {}"
        m = m.format(len(self.OBJ), ', '.join(self.RESULT.keys()))
        MYLOG.debug(m)

    def base_simple(self):
        """Process the simple properties from the tanium_ng object"""
        for prop in self.OBJ._SIMPLE_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.INCLUDE_EMPTY:
                continue

            prop_name = '{}{}'.format(self._PROP_PRE, prop)

            val_json = explode_json(val)
            if val_json:
                if self.FLAT:
                    val = flatten_pyobj(val_json, prefix=prop_name, sep=self.FLAT_SEP)
                    self.RESULT.update(val)
                else:
                    self.RESULT[EXPLODE_NAME] = val_json
            else:
                self.RESULT[prop_name] = val

    def base_complex(self):
        """Process the complex properties from the tanium_ng object"""
        for prop in self.OBJ._COMPLEX_PROPS:
            val = getattr(self.OBJ, prop)
            if val is None and not self.INCLUDE_EMPTY:
                continue

            prop_name = '{}{}'.format(self._PROP_PRE, prop)

            if val is not None:
                child_args = self.get_child_args(flat_pre=prop_name)
                child_val = to_dict(val, **child_args)
                if self.FLAT:
                    self.RESULT.update(child_val)
                else:
                    self.RESULT[prop_name] = child_val
            else:
                self.RESULT[prop_name] = val

    def base_list(self):
        """Process the list properties from the tanium_ng object"""
        for prop, prop_type in self.OBJ._LIST_PROPS.items():
            vals = getattr(self.OBJ, prop)
            if not vals and not self.INCLUDE_EMPTY:
                continue

            new_vals = []
            for idx, val in enumerate(vals):
                prop_name = '{}{}{}{}'.format(self._PROP_PRE, prop, self.FLAT_SEP, idx)

                if issubclass(prop_type, BaseType):
                    child_args = self.get_child_args(flat_pre=prop_name)
                    child_val = to_dict(val, **child_args)
                    new_vals.append(child_val)
                else:
                    if self.FLAT:
                        new_vals.append({prop_name: val})
                    else:
                        new_vals.append(val)

            if self.FLAT and not self.PARENT:
                [self.RESULT.update(v) for v in new_vals]
            else:
                self.RESULT[prop] = new_vals

    def get_child_args(self, **kwargs):
        child_args = {}
        child_args.update(self.KWARGS)
        child_args.update(kwargs)
        child_args['parent'] = False
        return child_args


class ToDictResultSet(object):
    '''
    normal rows xaxis::
    Computer Name || IP Address ||Count
    TPT1 || 1.1.1.1\n2.2.2.2 || 1
    auth || 1.1.1.1\n2.2.2.2 || 1
    WIN || 1.1.1.1\n2.2.2.2 || 1

    flat rows xaxis::
    Computer Name || IP Address ||Count
    TPT1 || 1.1.1.1 || 1
    TPT1 || 2.2.2.2 || 1
    auth || 1.1.1.1 || 1
    auth || 2.2.2.2 || 1
    WIN || 1.1.1.1 || 1
    WIN || 2.2.2.2 || 1

    normal rows yaxis::
    COLUMN NAME || row 1 vals || row 2 vals || row 3 vals
    Computer Name || TPT1 || auth || WIN
    IP Address || 1.1.1.1\n2.2.2.2 || 1.1.1.1\n2.2.2.2 || 1.1.1.1\n2.2.2.2
    Count || 1 || 1 || 1

    flat rows yaxis::
    COLUMN NAME || value 001 || value 002 || value 003

    Computer Name || TPT1 || TPT1
    IP Address || 1.1.1.1 || 2.2.2.2
    Count || 1 || 1

    Computer Name || auth || auth
    IP Address || 1.1.1.1 || 2.2.2.2
    Count || 1 || 1

    Computer Name || WIN || WIN
    IP Address || 1.1.1.1 || 2.2.2.2
    Count || 1 || 1
    '''

    def __init__(self, obj, **kwargs):
        for k, v in RESULTSET_ARGS.items():
            kwargs[k] = kwargs.get(k, v)

        if isinstance(obj, ResultSet):
            rows = obj.rows
            columns = obj.columns
        elif isinstance(obj, ResultSetList):
            rows = obj.result_set.rows
            columns = obj.result_set.columns
        else:
            err = "object must be either ResultSetList or ResultSet, supplied type: {} ({})"
            err = err.format(type(obj), obj)
            raise DictSerializeError(err)

        if not rows:
            err = "No rows found, can not proccess {}"
            err = err.format(obj)
            raise DictSerializeError(err)

        if not columns:
            err = "No columns found, can not proccess {}"
            err = err.format(obj)
            raise DictSerializeError(err)

        if kwargs.get('yaxis', False):
            if kwargs.get('flatten', False):
                result = self.do_flat_yaxis(rows, columns, **kwargs)
            else:
                result = self.do_normal_yaxis(rows, columns, **kwargs)
        else:
            if kwargs.get('flatten', False):
                result = self.do_flat_xaxis(rows, columns, **kwargs)
            else:
                result = self.do_normal_xaxis(rows, columns, **kwargs)

        kwargs['obj'] = obj
        kwargs['rowlen'] = len(rows)
        kwargs['collen'] = len(columns)
        kwargs['resultlen'] = len(result)

        m = RESULTSET_STRS['finished'].format(**kwargs)
        MYLOG.info(m)
        self.RESULT = result

    def new_yaxis_row(self, c, **kwargs):
        result = {}
        result['Column Name'] = c.display_name
        if kwargs.get('add_type', False):
            result['Result Type'] = c.result_type
        if kwargs.get('add_sensor', False):
            result['Sensor Name'] = c.sensor_nameorhash
        return result

    def do_normal_yaxis(self, rows, columns, **kwargs):
        result = []
        for ci, c in enumerate(columns):
            new_row = self.new_yaxis_row(c, **kwargs)
            for ri, r in enumerate(rows):
                header = RESULTSET_STRS['yaxis_row_vals'].format(ri=ri + 1)
                new_row[header] = join(r[ci].values)
            result.append(new_row)
        return result

    def do_normal_xaxis(self, rows, columns, **kwargs):
        result = []
        for r in rows:
            new_row = {}
            for c in r:
                header = self.colname(c, **kwargs)
                new_row[header] = join(c)
            result.append(new_row)
        return result

    def do_flat_xaxis(self, rows, columns, **kwargs):
        # get all of the unique names or hashes for each column in the current result set
        sensors = list(set([c.sensor_nameorhash for c in columns]))
        result = []
        # for each name/hash found, loop over all the rows and create a new set of rows
        # for this name/hash that have index correlated values
        for s in sensors:
            for r in rows:
                # get the highest value length from all of this what hashes friends
                value_max = max([len(c) for c in r if c.sensor_nameorhash == s])
                # if the maximum number of values for this column in this row is 1, skip it
                if value_max == 1:
                    continue
                # lets create a new row for each set of values that can exist
                for idx in range(0, value_max):
                    new_row = {}
                    for c in r:
                        header = self.colname(c, **kwargs)
                        new_row[header] = self.flatx_val(c, s, idx)
                    result.append(new_row)
        # if no rows created, then all rows are value_max == 1, so just do a normal xaxis
        if not result:
            result = self.do_normal_xaxis(rows, columns, **kwargs)
        return result

    def do_flat_yaxis(self, rows, columns, **kwargs):
        sensors = list(set([c.sensor_nameorhash for c in columns]))
        result = []
        for s in sensors:
            for ri, r in enumerate(rows):
                value_max = max([len(c) for c in r if c.sensor_nameorhash == s])
                # if the maximum number of values for this column in this row is 1, skip it
                if value_max == 1:
                    continue
                # lets create a new row for each set of values that can exist
                result.append({})
                for ci, c in enumerate(r):
                    new_row = self.flaty_row(c, s, ri, value_max, **kwargs)
                    if new_row:
                        result.append(new_row)
        if not result:
            result = self.do_normal_xaxis(rows, columns, **kwargs)
        return result

    def flaty_row(self, c, s, ri, value_max, **kwargs):
        result = {}
        for idx in range(0, value_max):
            header = RESULTSET_STRS['yaxis_flat_vals'].format(c=c, ri=ri + 1, idx=idx + 1)
            if c.sensor_nameorhash == s:
                try:
                    result[header] = c[idx]
                except:
                    result[header] = RESULTSET_STRS['flat_idx_fail'].format(c=c, idx=idx + 1, s=s)
            elif c.sensor_nameorhash != s and len(c) == 1:
                result[header] = c[0]
        if result:
            result.update(self.new_yaxis_row(c, **kwargs))
        return result

    def flatx_val(self, c, s, idx):
        # see if this columns what hash matches our current what hash
        if c.sensor_nameorhash == s:
            # try to get the index correlated value from this row's column
            try:
                result = c[idx]
            except:
                result = RESULTSET_STRS['flat_idx_fail'].format(c=c, idx=idx, s=s)
        # if this c is not related, and just has one item, use that as the value
        elif c.sensor_nameorhash != s and len(c) == 1:
            result = c[0]
        # if this c is not related and has more than one value, set as unrelated
        elif c.sensor_nameorhash != s and len(c) > 1:
            result = RESULTSET_STRS['flat_row_unrelated'].format(c=c, idx=idx, s=s)
        # this shouldn't happen
        else:
            result = RESULTSET_STRS['flow_row_unexpected'].format(c=c, idx=idx, s=s)
        return result

    def colname(self, c, **kwargs):
        results = []
        colname = RESULTSET_STRS['row_column_name'].format(c=c)
        results.append(colname)
        if kwargs.get('add_type', False):
            coltype = RESULTSET_STRS['sensor_type'].format(c=c)
            results.append(coltype)
        if kwargs.get('add_sensor', False):
            colsensor = RESULTSET_STRS['sensor'].format(c=c)
            results.append(colsensor)
        result = join(results)
        return result


def join(c):
    result = CRLF.join([text_type(v) for v in c])
    return result


def to_dict_resultset(obj, **kwargs):
    converter = ToDictResultSet(obj, **kwargs)
    result = converter.RESULT
    return result


def to_json_resultset(obj, **kwargs):
    rows = to_dict_resultset(obj, **kwargs)
    result = jsonify(rows, **kwargs)
    return result


def to_csv_resultset(obj, **kwargs):
    rows = to_dict_resultset(obj, **kwargs)
    writer = ExcelWriter()
    result = writer.run(rows, **kwargs)
    return result


def explode_json(val):
    """pass."""
    try:
        result = json.loads(val)
        # only explode non str/int types
        if not isinstance(result, (list, tuple, dict)):
            result = None
    except:
        result = None
    return result


def flatten_pyobj(pyobj, prefix='', sep='_'):
    """pass."""
    result = {}
    if isinstance(pyobj, (list, tuple)):
        for idx, val in enumerate(pyobj):
            mypre = '{}{}{}'.format(prefix, sep, idx)
            result.update(flatten_pyobj(val, mypre, sep))
    elif isinstance(pyobj, dict):
        for k, v in pyobj.items():
            mypre = '{}{}{}'.format(prefix, sep, k)
            result.update(flatten_pyobj(v, mypre, sep))
    else:
        if not prefix:
            prefix = type(pyobj).__name__
        result[prefix] = pyobj
    return result


def to_dict(obj, **kwargs):
    converter = ToDict(obj, **kwargs)
    result = converter.RESULT
    return result


def to_json(obj, **kwargs):
    obj_dict = to_dict(obj, **kwargs)
    result = jsonify(obj_dict, **kwargs)
    return result


def to_csv(obj, **kwargs):
    kwargs['flat'] = kwargs.get('flat', True)  # TODO CONSTANT
    obj_dict = to_dict(obj, **kwargs)

    if LIST_NAME in obj_dict:
        kwargs['rows'] = obj_dict[LIST_NAME]
    else:
        kwargs['rows'] = [obj_dict]

    kwargs['skips'] = kwargs.get('skips', []) + SKIPS
    kwargs['firsts'] = kwargs.get('firsts', []) + FIRSTS
    kwargs['lasts'] = kwargs.get('lasts', []) + LASTS

    writer = ExcelWriter()
    result = writer.run(**kwargs)
    return result


def to_tree(obj, **kwargs):
    converter = ToTree(obj, **kwargs)
    result = converter.RESULT
    return result


def to_xml(obj, **kwargs):
    tree = to_tree(obj, **kwargs)
    result = ET.tostring(tree, encoding=encoding)
    return result
