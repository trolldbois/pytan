#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""SoapResponse Transformation methods"""
import os
import sys
import csv
import StringIO
import logging
import re

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
path_adds = [my_dir]

for x in path_adds:
    if x not in sys.path:
        sys.path.insert(0, x)

import SoapUtil
import SoapConstants


class SoapTransform(object):

    def __init__(self):
        self.logger = logging.getLogger("SoapWrap.transform")
        self.DLOG = self.logger.debug
        self.ILOG = self.logger.info
        self.WLOG = self.logger.warn
        self.ELOG = self.logger.error

    def get_rows(self, response, **kwargs):
        """transforms response.inner_return into a list of lists or dicts"""
        if response.command == 'GetObject':
            rows = self.parse_result_object(response, **kwargs)
        elif response.command == 'GetResultData':
            rows = self.parse_resultxml(response, **kwargs)

        # utf cleanup
        for row in rows:
            for k in row:
                row[k] = SoapUtil.utf_clean(row[k])

        return rows

    ## result_object
    def flatten_obj(self, fullobj, prefix=None):
        flat = {}
        # print fullobj, prefix
        if SoapUtil.is_dict(fullobj):
            for k, v in fullobj.iteritems():
                if prefix:
                    k = ('{}.{}').format(prefix, k)
                if SoapUtil.is_dict(v):
                    # print 'dict found: ', k, v
                    flat.update(self.flatten_obj(v, k))
                elif SoapUtil.is_list(v):
                    # print 'list found: ', k, v
                    for idx, item in enumerate(v):
                        itempre = ('{}{}').format(k, idx)
                        flat.update(self.flatten_obj(item, itempre))
                else:
                    # print 'other found: ', k, v
                    if v and SoapUtil.is_str(v):
                        v = v.replace('\n', '\r\n')
                    flat[k] = v
        elif SoapUtil.is_list(fullobj):
            flat[prefix] = ", ".join(fullobj)
        else:
            flat[prefix] = fullobj
        return flat

    ## result_object
    def parse_result_object(self, response, **kwargs):
        """
        example breakdown of result_object for GetObject on sensor:

        single sensor return:
        dict:result_object:
            dict:sensor:
                dict:sensor_details:

        multiple sensors return:
        dict:result_object:
            list:sensor:
                dict:sensor_details:

        all sensors return:
        dict:result_object:
            dict:sensors:
                list:sensor:
                    dict:sensor_details:
        """
        ERR1 = (
            "Unexpected error when parsing inner return: {}"
        ).format
        ERR2 = (
            "inner return contains neither a list or dictionary "
            "unable to parse out result object(s): {}"
        ).format

        try:
            return_items = response.inner_return.items()[0]
            prefix = return_items[0]
            results = return_items[1]
        except Exception as e:
            raise Exception(ERR1(e))

        # handle "all" responses
        if SoapUtil.is_dict(results):
            single_prefix = prefix[:-1]
            if single_prefix in results.keys():
                prefix = single_prefix
                results = results[prefix]

        if SoapUtil.is_list(results):
            rows = [self.flatten_obj(x, prefix) for x in results]
        elif SoapUtil.is_dict(results):
            rows = [self.flatten_obj(results, prefix)]
        else:
            raise Exception(ERR2(response.inner_return))

        return rows

    ## ResultXML
    def parse_resultxml(self, response, **kwargs):
        """
        breakdown of ResultXML for GetResultData:

        dict:result_sets:
            dict:result_set:
                dict:cs:
                    list:c: # column data
                        dict:
                            str:dn # column name
                            int:wh # column grouping
                            int:rt # result type (see RESULT_TYPE_MAP{})
                dict:rs:
                    list:r: # row data
                        dict:
                            list:c: # one entry per column for this row
                                dict:
                                    str/list:v # value for this row&column
        """
        inner_return = response.inner_return
        sensors = getattr(response, 'sensors', [])
        if not SoapUtil.is_list(sensors):
            sensors = [sensors]

        my_args = {
            'ADD_TYPE_TO_HEADERS': False,
            'ADD_SENSOR_TO_HEADERS': True,
            'EXPAND_GROUPED_COLUMNS': True,
            'HIDE_COUNT_COLUMN': True,
        }

        kwargs = {k: kwargs.get(k, v) for k, v in my_args.iteritems()}

        headers = self.get_headers(inner_return)

        if kwargs['ADD_TYPE_TO_HEADERS']:
            headers = self.add_type_to_headers(headers)

        if kwargs['ADD_SENSOR_TO_HEADERS']:
            headers = self.add_sensor_to_headers(headers, sensors)

        rows = self.get_resultxml_rows(inner_return, headers)

        if kwargs['HIDE_COUNT_COLUMN']:
            rows, headers = self.remove_count_column(rows, headers)

        if kwargs['EXPAND_GROUPED_COLUMNS']:
            rows = self.expand_grouped_columns(rows, headers)
        else:
            rows = self.flatten_grouped_columns(rows)
        return rows

    ## ResultXML
    def get_headers(self, inner_return):
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        header_list = result_set['cs']
        header_list = header_list['c']
        headers = []
        for header_dict in header_list:
            header_name = SoapUtil.utf_clean(header_dict['dn'])
            header_type = SoapConstants.RESULT_TYPE_MAP.get(
                header_dict['rt'], 'Unknown',
            )
            header_wh = header_dict['wh']
            headers.append({
                'name': header_name,
                'wh': header_wh,
                'type': header_type,
            })
        return headers

    ## ResultXML
    def add_type_to_headers(self, headers):
        for x in headers:
            x['name'] = "%s (%s)" % (x['name'], x['type'])
        return headers

    ## ResultXML
    def add_sensor_to_headers(self, headers, sensors):
        for h in headers:
            sensor = [x for x in sensors if x['hash'] == h['wh']]
            if sensor:
                sensor = sensor[0]
            else:
                sensor = {}
            if not sensor:
                continue
            h['name'] = "%s: %s" % (sensor.get('name'), h['name'])
        return headers

    ## ResultXML
    def remove_count_column(self, rows, headers):
        COUNT_HEADERS = ['Count (NumericDecimal)', 'Count']
        rows = [
            {k: v for k, v in row.iteritems() if k not in COUNT_HEADERS}
            for row in rows
        ]
        headers = [x for x in headers if x['name'] not in COUNT_HEADERS]
        return rows, headers

    ## ResultXML
    def get_resultxml_rows(self, inner_return, headers):
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        row_lists = result_set['rs']
        row_lists = row_lists['r']
        row_lists = [x['c'] for x in row_lists]
        row_lists = [
            [SoapUtil.utf_clean(y['v']) for y in x] for x in row_lists
        ]
        rows = []
        for row_list in row_lists:
            row_entry = {}
            for col_idx, col_data in enumerate(row_list):
                header = headers[col_idx]['name']
                row_entry[header] = col_data
            rows.append(row_entry)
        return rows

    ## ResultXML
    def flatten_grouped_columns(self, rows):
        rows = [
            {k: self.excel_list(v) for k, v in row.iteritems()}
            for row in rows
        ]
        return rows

    ## ResultXML
    def excel_list(self, l):
        if SoapUtil.is_list(l):
            l = [str(SoapUtil.utf_clean(x)) for x in l]
            l = '\r\n'.join(l)
        return l

    ## ResultXML
    def expand_grouped_columns(self, rows, headers):
        new_rows = []
        for row in rows:
            values_with_list = [SoapUtil.is_list(v) for v in row.values()]
            if not any(values_with_list):
                new_rows.append(row)
                continue
            for k in row:
                if not SoapUtil.is_list(row[k]):
                    continue
                header = [x for x in headers if x['name'] == k][0]
                wh_friends = [x for x in headers if x['wh'] == header['wh']]
                for v_idx, v in enumerate(row[k]):
                    new_rows.append(self.build_new_row(
                        row, wh_friends, v_idx, headers
                    ))
        return new_rows

    ## ResultXML
    def build_new_row(self, row, wh_friends, v_idx, headers):
        new_row = {}
        for h in headers:
            if h not in wh_friends:
                # if this column is not correlated to the column we are
                # working on and it is a multi line return, set it to empty
                if SoapUtil.is_list(row[h['name']]):
                    new_row[h['name']] = ""
                # if this column is not correlated to the column we are working
                # on and it's a single line return, set it to the same value
                else:
                    new_row[h['name']] = row[h['name']]
            else:
                # if this column is correlated to the column we are working on
                # set the value to the indexed value of this value
                new_row[h['name']] = row[h['name']][v_idx]
        return new_row

    ## CSV
    def get_all_headers(self, rows_list):
        headers = []
        for row_dict in rows_list:
            [headers.append(h) for h in row_dict.keys() if h not in headers]
        return headers

    ## CSV
    def sort_headers(self, headers, **kwargs):
        header_sort_priority = kwargs.get('HEADER_SORT_PRIORITY', [])
        if header_sort_priority is False:
            return headers
        sorted_headers = sorted(headers)
        if header_sort_priority:
            p_headers = []
            for kp in header_sort_priority:
                for kidx, k in enumerate(sorted_headers):
                    if k.endswith(kp):
                        p_headers.append(sorted_headers.pop(kidx))
            p_headers += sorted_headers
            sorted_headers = p_headers
        return sorted_headers

    ## CSV
    def csvlistwriter(self, rows_list):
        '''unused'''
        csv_io = StringIO.StringIO()
        headers = rows_list.pop(0)
        writer = csv.writer(csv_io, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        writer.writerows(rows_list)
        csv_str = csv_io.getvalue()
        return csv_str

    ## CSV
    def csvdictwriter(self, rows_list, **kwargs):
        """returns the rows_list (list of dicts) as a CSV string"""
        csv_io = StringIO.StringIO()
        headers = self.get_all_headers(rows_list)
        headers = self.sort_headers(headers, **kwargs)
        writer = csv.DictWriter(
            csv_io, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writerow(dict((h, h) for h in headers))
        writer.writerows(rows_list)
        csv_str = csv_io.getvalue()
        return csv_str

    def get_fn(self, response, format):
        max_len = 80
        s = str(response.request.objects_dict)
        s = re.sub(r'[^\w,:]', '', s)
        s = s.replace(':', '_')
        s = s.replace(',', '+')
        s = s[0:max_len]

        base_fn = []
        base_fn.append(response.request.caller_method)
        base_fn.append(s)
        base_fn.append(SoapUtil.get_now())
        base_fn = '__'.join(base_fn)
        fn = ("{}.{}").format(base_fn, format)
        return fn

    def write_response(self, response, fname=None, fdir=None, format='csv',
                       **kwargs):
        # kwargs passthrus:
        # HEADER_SORT_PRIORITY
        # ADD_TYPE_TO_HEADERS
        # ADD_SENSOR_TO_HEADERS
        # EXPAND_GROUPED_COLUMNS
        # HIDE_COUNT_COLUMN

        WRITE_TPL = ("Writing response to file: {}").format

        objtype = response.request.object_type

        HEADER_SORT_PRIORITY = [
            'name',
            'id',
            'description',
            'hash',
            'value_type',
        ]

        HEADER_SORT_PRIORITY = [
            '%s.%s' % (objtype, x) for x in HEADER_SORT_PRIORITY
        ]

        if response.command == 'GetObject':
            if 'HEADER_SORT_PRIORITY' not in kwargs:
                kwargs['HEADER_SORT_PRIORITY'] = HEADER_SORT_PRIORITY

        if fname is None:
            fname = self.get_fn(response, format)

        if 'fprefix' in kwargs:
            fname = ("{}_{}").format(kwargs['fprefix'], fname)

        if fdir is None:
            fdir = os.path.curdir

        fpath = os.path.join(fdir, fname)

        # formats = ['csv', 'xls', 'json', 'xml', 'full.xml', 'http_response']
        if format == 'csv':
            rows_list = self.get_rows(response, **kwargs)
            fout = self.csvdictwriter(rows_list, **kwargs)

        self.ILOG(WRITE_TPL(fpath))

        x = open(fpath, 'w+')
        x.write(fout)
        x.close()
        return fpath
