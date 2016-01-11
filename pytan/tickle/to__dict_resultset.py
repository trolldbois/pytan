import logging

from pytan import PytanError, text_type
from pytan.tanium_ng import ResultSetList
from pytan.excelwriter import ExcelWriter
from pytan.tickle.tools import jsonify

from pytan.session import HASH_CACHE
from pytan.tickle.constants import (
    RESULTSET_ADD_TYPE, RESULTSET_ADD_SENSOR, RESULTSET_FLATTEN, RESULTSET_STRS
)

MYLOG = logging.getLogger(__name__)

LF = '\n'
CR = '\r'
CRLF = CR + LF


class DictSerializeError(PytanError):
    pass


class ToDictResultSet(object):
    '''
    normal rows::
    Computer Name || IP Address ||Count
    TPT1 || 1.1.1.1\n2.2.2.2 || 1
    auth || 1.1.1.1\n2.2.2.2 || 1
    WIN || 1.1.1.1\n2.2.2.2 || 1

    flat rows::
    Computer Name || IP Address ||Count
    TPT1 || 1.1.1.1 || 1
    TPT1 || 2.2.2.2 || 1
    auth || 1.1.1.1 || 1
    auth || 2.2.2.2 || 1
    WIN || 1.1.1.1 || 1
    WIN || 2.2.2.2 || 1
    '''

    def __init__(self, obj, **kwargs):
        self.ADD_TYPE = kwargs.get('add_type', RESULTSET_ADD_TYPE)
        self.ADD_SENSOR = kwargs.get('add_sensor', RESULTSET_ADD_SENSOR)
        self.FLATTEN = kwargs.get('flatten', RESULTSET_FLATTEN)

        if not isinstance(obj, ResultSetList):
            err = "obj is type {!r}, must be a tanium_ng.ResultSetList object"
            err = err.format(type(obj).__name__)
            raise DictSerializeError(err)

        if self.FLATTEN:
            self.RESULT = self.get_flat_rows(obj, **kwargs)
        else:
            self.RESULT = self.get_normal_rows(obj, **kwargs)

        m = (
            "Converted tanium_ng object {!r} with {} rows and {} columns into "
            "{} rows using flatten={}, add_type={}, add_sensor={}"
        )
        m = m.format(
            type(obj),
            len(obj.result_set.rows),
            len(obj.result_set.columns),
            len(self.RESULT),
            self.FLATTEN,
            self.ADD_TYPE,
            self.ADD_SENSOR,
        )
        MYLOG.info(m)

    def get_normal_rows(self, obj, **kwargs):
        rows = obj.result_set.rows
        result = [{self.get_row_colname(c): self.join(c) for c in r} for r in rows]
        return result

    def get_flat_rows(self, obj, **kwargs):
        rows = obj.result_set.rows
        columns = obj.result_set.columns
        # get all of the hashes for each column in the current result set
        what_hashes = list(set([c.what_hash for c in columns]))

        result = []
        for wh in what_hashes:
            for row in rows:
                # get the highest value length from all of this what hashes friends
                value_max = max([len(c) for c in row if c.what_hash == wh])
                # if the maximum number of values for this column in this row is 1, skip it
                if value_max == 1:
                    continue
                # lets create a new row for each set of values that can exist
                for idx in range(0, value_max):
                    flat_row_vals = [self.get_flat_row_val(c, wh, idx) for c in row]
                    result.append(dict(flat_row_vals))
        return result

    def get_flat_row_val(self, c, wh, idx):
        # see if this columns what hash matches our current what hash
        if c.what_hash == wh:
            # try to get the index correlated value from this row's column
            try:
                val = c[idx]
            except:
                val = RESULTSET_STRS['flat_idx_fail'].format(c=c, idx=idx)

        # if this c is not related, and just has one item, use that as the value
        elif c.what_hash != wh and len(c) == 1:
            val = c[0]

        # if this c is not related and has more than one value, set as unrelated
        elif c.what_hash != wh and len(c) > 1:
            val = RESULTSET_STRS['flat_row_unrelated'].format(c=c)

        # this shouldn't happen
        else:
            val = RESULTSET_STRS['flow_row_unexpected'].format(c=c)

        # return a dictionary with the key as the column name and the value as derived val
        row_val = (self.get_row_colname(c), val)
        return row_val

    def get_row_colname(self, c):
        results = []
        c.name_or_hash = self.get_name_or_hash(c)

        colname = RESULTSET_STRS['row_column_name'].format(c=c)
        results.append(colname)

        if self.ADD_TYPE:
            coltype = RESULTSET_STRS['sensor_type'].format(c=c)
            results.append(coltype)

        if self.ADD_SENSOR:
            colsensor = RESULTSET_STRS['sensor'].format(c=c)
            results.append(colsensor)

        result = self.join(results)
        return result

    def join(self, c):
        result = CRLF.join([text_type(v) for v in c])
        return result

    def get_name_or_hash(self, c):
        handler = getattr(self, '_HANDLER', None)
        wh = getattr(c, 'what_hash', '')
        sn = getattr(c, 'sensor_name', '')
        cache_result = HASH_CACHE.get(wh, '')
        if sn:
            result = sn
        elif cache_result:
            result = cache_result
        elif handler and wh:
            result = handler.SESSION.get_string(from_hash=wh)
        else:
            result = 'hash({})'.format(wh)
        return result

    '''
    NEXTVER: RE-DO Y AXIS
    NEXTVER: FIGURE OUT FLAT Y AXIS
    NEXTVER: FIGURE OUT PIVOT COLUMN

    straight column csv export::
    NAME: 1  || 2 || 3
    Computer Name: TPT1 || auth || WIN
    Count: 1 || 1 || 1

    self:
    _COL_ROW = 'Values in row: {}'
    _COL_NAME = 'Column Name'
    _COL_TYPE = "Result Type"
    _COL_SHASH = "From Sensor Hash"
    # _COL_SNAME = "From Sensor Name"  # NEXTVER

    init:
        # xaxis = kwargs.get('xaxis', True)  # TODO constant
        # yaxis = kwargs.get('yaxis', False)  # TODO constant

        # if yaxis:
            # run_method = self.run_yaxis
        # elif xaxis:
            # run_method = self.run_xaxis
        # else:

    def run_yaxis(self, rd, **kwargs):
        # for idx, col in enumerate(self.columns):
            # col.values = [row[idx].values for row in self.rows]
        columns = rd.result_set.columns
        result = [dict(self.get_col_colname(c) + self.get_col_vals(c)) for c in columns]
        return result

    def get_col_colname(self, c):
        result = []
        colname = [self._COL_NAME, text_type(c.display_name)]
        result.append(colname)

        if self.ADD_TYPE:
            coltype = [self._COL_TYPE, text_type(c.result_type)]
            result.append(coltype)

        if self.ADD_SENSOR:
            colsensor = [self._COL_SHASH, text_type(c.what_hash)]
            result.append(colsensor)
        return result

    def get_col_vals(self, c):
        result = [[self._COL_ROW.format(idx + 1), self.join(r)] for idx, r in enumerate(c)]
        return result
    '''


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
