from pytan import text_type

LF = '\n'
CR = '\r'
CRLF = CR + LF


class ResultToRows(object):
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

    # constants
    _ROW_NAME = '{0.display_name}'
    _ROW_SHASH = 'From Sensor Hash: {0.what_hash}'
    # _ROW_SNAME = 'From Sensor Name: {0.sensor_name}'  # NEXTVER
    _ROW_TYPE = 'Result Type: {0.result_type}'

    _FLAT_ROW_IDX_FAIL = "NO INDEX CORRELATED VALUE FOR COLUMN NAME: {} INDEX: {}"
    _FLAT_ROW_ENEMY = "UNRELATED TO SENSOR HASH: {}"
    _FLAT_ROW_ELSE = "UNEXPECTED SCENARIO WITH SENSOR HASH: {}"

    def __init__(self, obj, **kwargs):
        self.ADD_TYPE = kwargs.get('add_type', True)  # TODO constant
        self.ADD_SENSOR = kwargs.get('add_sensor', True)  # TODO constant
        self.FLAT = kwargs.get('flat', False)  # TODO constant

        if self.FLAT:
            self.RESULT = self.get_flat_rows(obj, **kwargs)
        else:
            self.RESULT = self.get_normal_rows(obj, **kwargs)

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
                for val_idx in range(0, value_max):
                    result.append(dict([self.get_flat_row_val(col, wh, val_idx) for col in row]))
        return result

    def get_row_colname(self, c):
        results = []
        colname = self._ROW_NAME.format(c)
        results.append(colname)

        if self.ADD_TYPE:
            coltype = self._ROW_TYPE.format(c)
            results.append(coltype)

        if self.ADD_SENSOR:
            colsensor = self._ROW_SHASH.format(c)
            results.append(colsensor)

        result = self.join(results)
        return result

    def join(self, c):
        result = CRLF.join([text_type(v) for v in c])
        return result

    def get_flat_row_val(self, col, wh, val_idx):
        # see if this columns what hash matches our current what hash
        if col.what_hash == wh:
            # try to get the index correlated value from this row's column
            try:
                colval = col[val_idx]
            except:
                colval = self._FLAT_ROW_IDX_FAIL.format(col.display_name, val_idx)

        # if this col is not related, and just has one item, use that as the value
        elif col.what_hash != wh and len(col) == 1:
            colval = col[0]

        # if this col is not related and has more than one value, set as unrelated
        elif col.what_hash != wh and len(col) > 1:
            colval = self._FLAT_ROW_ENEMY.format(wh)

        # this shouldn't happen
        else:
            colval = self._FLAT_ROW_ELSE.format(wh)

        # return a dictionary with the key as the column name and the value as derived colval
        row_val = (self.get_row_colname(col), colval)
        return row_val

    '''
    NEXTVER: FIGURE OUT SENSOR HASH -> SENSOR NAME
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
