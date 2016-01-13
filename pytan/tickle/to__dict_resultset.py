import logging

from pytan import PytanError, text_type
from pytan.tanium_ng import ResultSetList, ResultSet
from pytan.excelwriter import ExcelWriter
from pytan.tickle.tools import jsonify

from pytan.tickle.constants import RESULTSET_ARGS, RESULTSET_STRS

MYLOG = logging.getLogger(__name__)

LF = '\n'
CR = '\r'
CRLF = CR + LF


class DictSerializeError(PytanError):
    pass


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
    NAME || row 1 vals || row 2 vals || row 3 vals
    Computer Name || TPT1 || auth || WIN
    IP Address || 1.1.1.1\n2.2.2.2 || 1.1.1.1\n2.2.2.2 || 1.1.1.1\n2.2.2.2
    Count || 1 || 1 || 1

    flat rows yaxis::
    NAME || row 1 val 1 || row 1 val 2 || row 2 val 1 || row 2 val 2 || row 3 val 1 || row 3 val 2
    Computer Name || TPT1 || TPT1 || auth || auth || WIN || WIN
    IP Address || 1.1.1.1 || 2.2.2.2 || 1.1.1.1 || 2.2.2.2 || 1.1.1.1 || 2.2.2.2
    Count || 1 || 1 || 1 || 1 || 1 || 1

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
