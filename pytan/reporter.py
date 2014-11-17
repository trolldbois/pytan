# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import logging
import json
import StringIO
import csv
import re
from operator import itemgetter
from . import constants
from . import utils
# from .packages import xmltodict
from .exceptions import ReporterError

mylog = logging.getLogger("pytan.handler")

class Reporter(object):
    FORMATS = constants.TRANSFORM_FORMATS
    BOOL_KWARGS = constants.TRANSFORM_BOOL_KWARGS
    HEADER_SORT_PRIORITY = constants.TRANSFORM_HEADER_SORT_PRIORITY

    def __init__(self):
        super(Reporter, self).__init__()

        self.last_transform = {}

    def __str__(self):
        str_tpl = (
            "{} formats: {}"
        ).format
        ret = str_tpl(self.__class__.__name__, ', '.join(self.FORMATS))
        return ret

    def write_response(self, response, fname=None, fdir=None, ftype='csv',
                       fprefix=None, fpostfix=None, fext=None, **kwargs):
        write_tpl = "Writing response to file: {}".format
        badf_err = "Unsupported format: {!r}, must be one of {r}".format
        excf_err = 'Exception in {}.{}({}, {})'.format

        kwargs = {
            k: kwargs.get(k, v)
            for k, v in self.BOOL_KWARGS.iteritems()
        }

        hsp = 'HEADER_SORT_PRIORITY'
        otype = response.request.objtype

        # for GetObject command, prepend the object type so the header
        # sort priority works better
        if response.command == 'GetObject':
            kwargs[hsp] = kwargs.get(hsp, getattr(self, hsp))
            kwargs[hsp] = ['%s.%s' % (otype, x) for x in kwargs.get(hsp, [])]

        if fname is None:
            fname = self.get_fname(response)

        if fprefix is not None:
            fname = "{}.{}".format(fprefix, fname)

        if fpostfix is not None:
            fname = "{}.{}".format(fname, fpostfix)

        if fext is None:
            fext = ftype

        fname = "{}.{}".format(fname, fext)

        if fdir is None:
            fdir = os.path.curdir

        fpath = os.path.join(fdir, fname)

        if ftype in self.FORMATS:
            try:
                fout = getattr(self, self.FORMATS[ftype])(response, **kwargs)
            except:
                self.logger.critical(excf_err(
                    self.__class__.__name__,
                    self.FORMATS[ftype],
                    response,
                    kwargs,
                )
                )
                self.logger.critical(utils.jsonify(response.inner_return))
                raise
        else:
            raise ReporterError(badf_err(
                ftype, ', '.join(self.FORMATS.keys())
            ))

        self.ILOG(write_tpl(fpath))

        fout = fout.encode('utf-8')

        x = open(fpath, 'w+')
        x.write(fout)
        x.close()

        self.last_transform = {fpath: fout}

        return fpath

    @staticmethod
    def get_fname(response):
        base_fn = [
            response.request.__class__.__name__,
            response.request.objtype,
            utils.stringify_obj(response.request.query),
            utils.get_now()]
        base_fn = '__'.join(base_fn)
        return base_fn

    def get_rows(self, response, **kwargs):
        """transforms response.inner_return into a list of dicts"""
        rows = []
        if response.command == 'GetObject':
            rows = self.parse_result_object(response, **kwargs)
        elif response.command == 'GetResultData':
            rows = self.parse_resultxml(response, **kwargs)

        # utf cleanup
        for row in rows:
            for k in row:
                row[k] = utils.utf_clean(row[k])

        return rows

    # XML
    def get_xml(self, response, **kwargs):
        rows_list = self.get_rows(response, **kwargs)
        new_rows = []
        for row in rows_list:
            new_row = [{'n': n, 'v': v} for n, v in row.iteritems()]
            new_row = {'col': new_row}
            new_rows.append(new_row)

        new_rows = {'SoapTransform': {'row': new_rows}}
        fout = xmltodict.unparse(new_rows, pretty=True, indent="  ")
        return fout

    # RAW XML
    @staticmethod
    def get_rawxml(response, **kwargs):
        inner_return = {'raw_inner_xml': response.inner_return}
        fout = xmltodict.unparse(inner_return, pretty=True, indent="  ")
        return fout

    # RAW REQUEST
    @staticmethod
    def get_rawrequest(response, **kwargs):
        fout = response.request.xml_raw
        return fout

    # RAW RESPONSE
    @staticmethod
    def get_rawresponse(response, **kwargs):
        fout = response.page.text
        return fout

    ## JSON
    def get_json(self, response, **kwargs):
        rows_list = self.get_rows(response, **kwargs)
        fout = json.dumps(rows_list, sort_keys=True, indent=4)
        return fout

    ## CSV
    def get_csv(self, response, **kwargs):
        rows_list = self.get_rows(response, **kwargs)
        fout = self.csvdictwriter(rows_list, **kwargs)
        return fout

    ## CSV
    @staticmethod
    def get_all_headers(rows_list):
        headers = []
        for row_dict in rows_list:
            [headers.append(h) for h in row_dict.keys() if h not in headers]
        return headers

    ## CSV
    @staticmethod
    def sort_headers(headers, **kwargs):
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
    @staticmethod
    def csvlistwriter(rows_list):
        """unused"""
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

    ## result_object
    def flatten_obj(self, fullobj, prefix=None):
        flat = {}
        # print fullobj, prefix
        if utils.is_dict(fullobj):
            for k, v in fullobj.iteritems():
                if prefix:
                    k = '{}.{}'.format(prefix, k)
                if utils.is_dict(v):
                    # print 'dict found: ', k, v
                    flat.update(self.flatten_obj(v, k))
                elif utils.is_list(v):
                    # print 'list found: ', k, v
                    for idx, item in enumerate(v):
                        itempre = '{}{}'.format(k, idx)
                        flat.update(self.flatten_obj(item, itempre))
                else:
                    # print 'other found: ', k, v
                    if v and utils.is_str(v):
                        v = v.replace('\n', '\r\n')
                    flat[k] = v
        elif utils.is_list(fullobj):
            flat[prefix] = ", ".join(fullobj)
        else:
            flat[prefix] = fullobj
        return flat

    ## result_object
    def humanize_result_object(self, response, **kwargs):
        err1 = (
            "Unexpected error when parsing inner return: {}"
        ).format
        err3 = ("No print method available for object type {}").format

        try:
            return_items = response.inner_return.items()[0]
            prefix = return_items[0]
            results = return_items[1]
        except Exception as e:
            raise Exception(err1(e))

        # handle "all" responses
        if utils.is_dict(results):
            single_prefix = prefix[:-1]
            if single_prefix in results.keys():
                prefix = single_prefix
                results = results[prefix]

        if not utils.is_list(results):
            results = [results]

        if prefix == 'sensor':
            human_out = self.humanize_results_sensor(results, **kwargs)
        else:
            raise Exception(err3(prefix))

        if not human_out:
            human_out.append("No results returned...")
        human_out = '\n'.join(human_out)
        return human_out

    @staticmethod
    def humanize_results_sensor(results, **kwargs):
        '''
        kwargs:
          CATEGORIES(list): only show sensors for these categories
          PLATFORMS(list): only show sensors that match these platforms
          SENSOR_REGEXES(list): only show sensors that match these regexes
          HIDE_PARAMS(bool): do not show params in output
          PARAMS_ONLY(bool): show only sensors with params
          JSON_SENSOR(bool): just print out a json dump of the sensor
        '''
        sens_line = (
            "  Sensor Name: '{name}', Platforms: {platforms}, "
            "Category: {category}"
        ).format
        desc_line = "    Description: {description}".format
        param_line = "    Parameter {}:".format
        pval_line = "      {}: {}".format

        kw_categories = [x.lower() for x in kwargs.get('CATEGORIES', [])]
        kw_platforms = [x.lower() for x in kwargs.get('PLATFORMS', [])]
        kw_sensor_regexes = kwargs.get('SENSOR_REGEXES', [])
        kw_sensor_regexes = [re.compile(x) for x in kw_sensor_regexes]
        kw_hide_params = kwargs.get('HIDE_PARAMS', False)
        kw_params_only = kwargs.get('PARAMS_ONLY', False)
        kw_json_sensor = kwargs.get('JSON_SENSOR', False)

        human_out = []
        cat_groups = {}
        for r in results:
            rcat = str(r['category'])
            if kw_categories:
                if rcat.lower() not in kw_categories:
                    continue
            if rcat not in cat_groups:
                cat_groups[rcat] = []
            cat_groups[rcat].append(r)

        for cat_group in sorted(cat_groups):
            cat_items = sorted(cat_groups[cat_group], key=itemgetter('name'))
            for cat_item in cat_items:
                if kw_sensor_regexes:
                    name_match = [
                        x for x in kw_sensor_regexes
                        if x.search(cat_item['name'])
                    ]
                    if not name_match:
                        continue

                if kw_json_sensor:
                    human_out.append(utils.jsonify(cat_item, 2))
                    continue

                # clean up description
                item_desc = cat_item.get('description') or ''
                item_desc = item_desc.replace('\n', ' ').strip()
                cat_item['description'] = item_desc

                # figure out platforms for this item
                item_plats = []
                item_queries = cat_item.get('queries', {})
                item_queries = item_queries.get('query', [])

                if not utils.is_list(item_queries):
                    item_queries = [item_queries]

                for item_query in item_queries:
                    query_script = item_query.get('script')
                    if not query_script:
                        continue
                    if 'THIS IS A STUB' in query_script:
                        continue
                    if 'echo Windows Only' in query_script:
                        continue
                    item_plats.append(item_query['platform'])

                if item_plats:
                    item_plats = sorted(item_plats)
                else:
                    item_plats = ['None']

                if kw_platforms:
                    plat_match = [
                        x for x in item_plats if x.lower() in kw_platforms
                    ]
                    if not plat_match:
                        continue

                cat_item['platforms'] = ', '.join(item_plats)

                item_params = cat_item.get('parameter_definition') or {}
                item_params = item_params.get('parameters') or []

                if kw_params_only and not item_params:
                    continue

                poppers = [
                    'model',
                    'parameterType',
                    'snapInterval',
                    'validationExpressions',
                ]

                for p in poppers:
                    [i.pop(p) for i in item_params if p in i]

                human_out.append(sens_line(**cat_item))
                human_out.append(desc_line(**cat_item))

                if kw_hide_params:
                    continue

                for item_idx, item_param in enumerate(item_params):
                    human_out.append(param_line(item_idx + 1))
                    for k, v in sorted(item_param.iteritems()):
                        if not v:
                            continue
                        human_out.append(pval_line(k, v))

                human_out.append("")
        return human_out

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
        err1 = (
            "Unexpected error when parsing inner return: {}"
        ).format
        err2 = (
            "inner return contains neither a list or dictionary "
            "unable to parse out result object(s): {}"
        ).format

        try:
            return_items = response.inner_return.items()[0]
            prefix = return_items[0]
            results = return_items[1]
        except Exception as e:
            raise Exception(err1(e))

        # handle "all" responses
        if utils.is_dict(results):
            single_prefix = prefix[:-1]
            if single_prefix in results.keys():
                prefix = single_prefix
                results = results[prefix]

        if utils.is_list(results):
            rows = [self.flatten_obj(x, prefix) for x in results]
        elif utils.is_dict(results):
            rows = [self.flatten_obj(results, prefix)]
        else:
            raise Exception(err2(response.inner_return))

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
        if not utils.is_list(sensors):
            sensors = [sensors]

        headers = self.get_headers(inner_return)

        if kwargs.get('ADD_TYPE_TO_HEADERS', False):
            headers = self.add_type_to_headers(headers)

        if kwargs.get('ADD_SENSOR_TO_HEADERS', False):
            headers = self.add_sensor_to_headers(headers, sensors)

        rows = self.get_resultxml_rows(inner_return, headers)
        rows, headers = self.check_count_column(rows, headers)

        if kwargs.get('EXPAND_GROUPED_COLUMNS', False):
            rows = self.expand_grouped_columns(rows, headers)
        else:
            rows = self.flatten_grouped_columns(rows)
        return rows

    ## ResultXML
    @staticmethod
    def get_headers(inner_return):
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        header_list = result_set['cs']
        header_list = header_list['c']
        headers = []
        for header_dict in header_list:
            header_name = utils.utf_clean(header_dict['dn'])
            header_type = constants.RESULT_TYPE_MAP.get(
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
    @staticmethod
    def add_type_to_headers(headers):
        for x in headers:
            x['name'] = "%s (%s)" % (x['name'], x['type'])
        return headers

    ## ResultXML
    @staticmethod
    def add_sensor_to_headers(headers, sensors):
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
    def check_count_column(self, rows, headers):
        count_headers = ['Count (NumericDecimal)', 'Count']
        if not any([x.get(y, 0) > 1 for y in count_headers for x in rows]):
            self.DLOG("Removing count header from result, all = 1")
            rows = [
                {k: v for k, v in row.iteritems() if k not in count_headers}
                for row in rows
            ]
            headers = [x for x in headers if x['name'] not in count_headers]
        return rows, headers

    ## ResultXML
    @staticmethod
    def get_resultxml_rows(inner_return, headers):
        result_sets = inner_return['result_sets']
        result_set = result_sets['result_set']
        row_lists = result_set['rs']
        row_lists = row_lists['r']
        row_lists = [x['c'] for x in row_lists]
        row_lists = [
            [utils.utf_clean(y['v']) for y in x] for x in row_lists
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
    @staticmethod
    def excel_list(l):
        if utils.is_list(l):
            l = [str(utils.utf_clean(x)) for x in l]
            l = '\r\n'.join(l)
        return l

    ## ResultXML
    def expand_grouped_columns(self, rows, headers):
        new_rows = []
        for row in rows:
            values_with_list = [utils.is_list(v) for v in row.values()]
            if not any(values_with_list):
                new_rows.append(row)
                continue
            for k in row:
                if not utils.is_list(row[k]):
                    continue
                header = [x for x in headers if x['name'] == k][0]
                wh_friends = [x for x in headers if x['wh'] == header['wh']]
                for v_idx, v in enumerate(row[k]):
                    new_rows.append(self.build_new_row(
                        row, wh_friends, v_idx, headers
                    ))
        return new_rows

    ## ResultXML
    @staticmethod
    def build_new_row(row, wh_friends, v_idx, headers):
        new_row = {}
        for h in headers:
            if h not in wh_friends:
                # if this column is not correlated to the column we are
                # working on and it is a multi line return, set it to empty
                if utils.is_list(row[h['name']]):
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
