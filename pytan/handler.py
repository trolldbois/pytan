# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""PyTan: A wrapper around Tanium's SOAP API in Python

Like saran wrap. But not.

This requires Python 2.7
"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import logging
import io
import time
from . import utils
from . import constants
from . import api
from .utils import HandlerError
from .utils import RunFalse

mylog = logging.getLogger("handler")
actionlog = logging.getLogger("action_progress")


class Handler(object):

    def __init__(self, username, password, host, port="444", loglevel=0,
                 debugformat=False, **kwargs):
        super(Handler, self).__init__()

        # use port 444 if you have direct access to it,
        # port 444 is direct access to API
        # port 443 uses apache forwarder which then goes to port 444

        # setup the console logging handler
        utils.setup_console_logging()
        # create all the loggers and set their levels based on loglevel
        utils.set_log_levels(loglevel)
        # change the format of console logging handler if need be
        utils.change_console_format(debugformat)

        self.loglevel = loglevel

        if not username:
            raise HandlerError("Must supply username!")
        if not password:
            raise HandlerError("Must supply password!")
        if not host:
            raise HandlerError("Must supply host!")
        if not port:
            raise HandlerError("Must supply port!")
        try:
            port = int(port)
        except ValueError:
            raise HandlerError("port must be an integer!")

        utils.test_app_port(host, port)
        self.session = api.Session(host, port)
        self.session.authenticate(username, password)

    def __str__(self):
        str_tpl = "Handler for {}".format
        ret = str_tpl(self.session)
        return ret

    def ask(self, **kwargs):
        qtype = kwargs.get('qtype', '')
        if not qtype:
            err = (
                "Must supply question type as 'qtype'! Valid choices: {}"
            ).format
            raise HandlerError(err(', '.join(constants.Q_OBJ_MAP)))
        q_obj_map = utils.get_q_obj_map(qtype)
        kwargs.pop('qtype')
        result = getattr(self, q_obj_map['handler'])(**kwargs)
        return result

    def ask_saved(self, **kwargs):

        # get the saved_question object the user passed in
        q_objs = self.get('saved_question', **kwargs)

        if len(q_objs) != 1:
            err = (
                "Multiple saved questions returned, can only ask one "
                "saved question!\nArgs: {}\nReturned saved questions:\n\t{}"
            ).format
            q_obj_str = '\n\t'.join([str(x) for x in q_objs])
            raise HandlerError(err(kwargs, q_obj_str))

        q_obj = q_objs[0]

        # poll the Saved Question ID returned above to wait for results
        ask_kwargs = utils.get_ask_kwargs(**kwargs)
        asker = api.QuestionAsker(self.session, q_obj, **ask_kwargs)
        asker.run({'ProgressChanged': utils.question_progress})

        # get the results
        req_kwargs = utils.get_req_kwargs(**kwargs)
        result = self.session.getResultData(q_obj, **req_kwargs)

        # add the sensors from this question to the ResultSet object
        # for reporting
        result.sensors = [x.sensor for x in q_obj.question.selects]
        ret = {
            'question_object': q_obj,
            'question_results': result,
        }

        return ret

    def ask_manual(self, get_results=True, **kwargs):
        '''Parses a set of python objects into a Question object,
        adds the Question object, and returns the results for the Question ID
        of the added Question object
        '''

        # get our defs from kwargs and churn them into what we want
        sensor_defs = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )

        q_filter_defs = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )

        q_option_defs = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )

        # do basic validation of our defs
        utils.val_sensor_defs(sensor_defs)
        utils.val_q_filter_defs(q_filter_defs)

        # get the sensor objects that are in our defs and add them as
        # d['sensor_obj']
        sensor_defs = self._get_sensor_defs(sensor_defs)
        q_filter_defs = self._get_sensor_defs(q_filter_defs)

        # build a SelectList object from our sensor_defs
        selectlist_obj = utils.build_selectlist_obj(sensor_defs)

        # build a Group object from our question filters/options
        group_obj = utils.build_group_obj(q_filter_defs, q_option_defs)

        # build a Question object from selectlist_obj and group_obj
        add_q_obj = utils.build_manual_q(selectlist_obj, group_obj)

        # add our Question and get a Question ID back
        q_obj = self.session.add(add_q_obj)

        # refetch the full object of the question so that we have access
        # to everything (especially query_text)
        q_obj = self.get('question', id=q_obj.id)[0]

        ret = {
            'question_object': q_obj,
            'question_results': None,
        }

        if get_results:
            # poll the Question ID returned above to wait for results
            ask_kwargs = utils.get_ask_kwargs(**kwargs)
            asker = api.QuestionAsker(self.session, q_obj, **ask_kwargs)
            asker.run({'ProgressChanged': utils.question_progress})

            # get the results
            req_kwargs = utils.get_req_kwargs(**kwargs)
            result = self.session.getResultData(q_obj, **req_kwargs)

            # add the sensors from this question to the ResultSet object
            # for reporting
            result.sensors = [x['sensor_obj'] for x in sensor_defs]
            ret['question_results'] = result

        return ret

    def ask_manual_human(self, **kwargs):
        '''Parses a set of "human" strings into python objects usable
        by ask_manual()
        '''

        if 'sensors' in kwargs:
            sensors = kwargs.pop('sensors')
        else:
            sensors = []

        if 'question_filters' in kwargs:
            q_filters = kwargs.pop('question_filters')
        else:
            q_filters = []

        if 'question_options' in kwargs:
            q_options = kwargs.pop('question_options')
        else:
            q_options = []

        sensor_defs = utils.dehumanize_sensors(sensors)
        q_filter_defs = utils.dehumanize_question_filters(q_filters)
        q_option_defs = utils.dehumanize_question_options(q_options)

        result = self.ask_manual(
            sensor_defs=sensor_defs,
            question_filter_defs=q_filter_defs,
            question_option_defs=q_option_defs,
            **kwargs
        )
        return result

    def deploy_action(self, run=False, get_results=True, **kwargs):

        # get our defs from kwargs and churn them into what we want
        action_filter_defs = utils.parse_defs(
            defname='action_filter_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )

        action_option_defs = utils.parse_defs(
            defname='action_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )

        package_def = utils.parse_defs(
            defname='package_def',
            deftypes=['dict()'],
            empty_ok=False,
            **kwargs
        )

        start_seconds_from_now = utils.get_kwargs_int(
            'start_seconds_from_now', 1, **kwargs
        )

        expire_seconds = utils.get_kwargs_int('expire_seconds', **kwargs)

        # do basic validation of our defs
        utils.val_sensor_defs(action_filter_defs)
        utils.val_package_def(package_def)

        # get the objects that are in our defs and add them as
        # d['sensor_obj'] / d['package_obj']
        action_filter_defs = self._get_sensor_defs(action_filter_defs)
        package_def = self._get_package_def(package_def)

        '''
        ask the question that pertains to the action filter
        this will be used to get a count for how many servers should be seen
        in the deploy action resultdata as 'completed'

        We supply Computer Name and Online = True as the sensors if run is
        False, then exit out after asking the question to allow the user
        to verify the contents

        If run is True we just use Online = True for the sensor

        The action filter for the deploy action is used as the question
        filter in both cases
        '''
        if not run:
            pre_action_sensors = ['Computer Name', 'Online, that = True']
        else:
            pre_action_sensors = ['Online, that = True']

        pre_action_sensor_defs = utils.dehumanize_sensors(pre_action_sensors)
        pre_action_result_ret = self.ask_manual(
            sensor_defs=pre_action_sensor_defs,
            question_filter_defs=action_filter_defs,
            question_option_defs=action_option_defs,
            hide_no_results_flag=1,
        )
        pre_action_result = pre_action_result_ret['question_results']

        if not run:
            report_path, result = self.export_to_report_file(
                pre_action_result, 'csv',
                prefix='VERIFY_BEFORE_DEPLOY_ACTION_', **kwargs
            )
            m = (
                "'Run' is not True!!\n"
                "View and verify the contents of {} (length: {} bytes)\n"
                "Re-run this deploy action with run=True after verifying"
            ).format
            raise RunFalse(m(report_path, len(result)))

        ''' note from jwk:
        passed_count == the number of machines that pass the filter and
        therefore the number that should take the action
        '''
        passed_count = pre_action_result.passed
        m = (
            "Number of systems that match action filter (passed_count): {}"
        ).format
        mylog.debug(m(passed_count))

        targetgroup_obj = utils.build_group_obj(
            action_filter_defs, action_option_defs
        )

        package_obj = package_def['package_obj']
        user_params = package_def['params']
        param_objlist = utils.build_param_objlist(
            obj=package_obj,
            user_params=user_params,
            delim='',
            derive_def=False,
            empty_ok=False,
        )

        a_package_obj = api.PackageSpec()
        if param_objlist:
            a_package_obj.source_id = package_obj.id
            a_package_obj.parameters = param_objlist
        else:
            a_package_obj.name = package_obj.name

        add_action_obj = api.Action()
        add_action_obj.name = "API Deploy {}".format(package_obj.name)
        add_action_obj.package_spec = a_package_obj
        add_action_obj.target_group = targetgroup_obj
        add_action_obj.start_time = utils.seconds_from_now(
            start_seconds_from_now
        )

        if expire_seconds is not None:
            add_action_obj.expire_seconds = expire_seconds

        action_obj = self.session.add(add_action_obj)

        m = "Deploy Action Added, ID: {}".format
        mylog.debug(m(action_obj.id))

        action_obj = self.get('action', id=action_obj.id)[0]

        ret = {
            'action_object': action_obj,
            'action_results': None,
            'action_progress_human': None,
            'action_progress_map': None,
            'pre_action_question_results': pre_action_result_ret,
        }

        if get_results:
            deploy_results = self.deploy_action_asker(
                action_obj.id, passed_count
            )
            ret.update(deploy_results)
            m = "Deploy Action Completed {}".format
            mylog.debug(m(utils.seconds_from_now(0, '')))

        return ret

    def deploy_action_human(self, **kwargs):
        # the human string describing the sensors/filter that user wants
        # to deploy the action against
        if 'action_filters' in kwargs:
            action_filters = kwargs.pop('action_filters')
        else:
            action_filters = []

        # the question options to use on the pre-action question and on the
        # group for the action filters
        if 'action_options' in kwargs:
            action_options = kwargs.pop('action_options')
        else:
            action_options = []

        # name of package to deploy with params as {key=value1,key2=value2}
        if 'package' in kwargs:
            package = kwargs.pop('package')
        else:
            package = ''

        action_filter_defs = utils.dehumanize_sensors(action_filters)
        action_option_defs = utils.dehumanize_question_options(action_options)
        package_def = utils.dehumanize_package(package)

        deploy_result = self.deploy_action(
            action_filter_defs=action_filter_defs,
            action_option_defs=action_option_defs,
            package_def=package_def,
            **kwargs
        )
        return deploy_result

    def deploy_action_asker(self, action_id, passed_count=0):
        action_obj = self.get('action', id=action_id)[0]
        ps = action_obj.package_spec
        '''
        A package_spec has to have a verify_group defined on it in order
        for deploy action verification to trigger. That can be only done
        at package_spec create or update time
        '''
        if ps.verify_group or ps.verify_group_id:
            m = "Setting up 'finished' for verify"
            finished_keys = ['done', 'verify_done']
            success_keys = ['verify_done']
            running_keys = ['running', 'verify_running']
            failed_keys = ['failed']
        else:
            m = "Setting up 'finished' for no_verify"
            finished_keys = ['done', 'no_verify_done']
            success_keys = ['no_verify_done']
            running_keys = ['running']
            failed_keys = ['failed']

        mylog.debug(m)
        ARS = constants.ACTION_RESULT_STATUS
        finished_keys = utils.get_dict_list_items(ARS, finished_keys)
        success_keys = utils.get_dict_list_items(ARS, success_keys)
        running_keys = utils.get_dict_list_items(ARS, running_keys)
        failed_keys = utils.get_dict_list_items(ARS, failed_keys)

        passed_count_reached = False
        finished = False
        while not passed_count_reached or not finished:
            m = "Deploy Action Asker loop for {!r}: {}".format
            mylog.debug(m(action_obj.name, utils.seconds_from_now(0, '')))

            if not passed_count_reached:
                # get the aggregate resultdata
                rd = self.get_result_data(action_obj, True)

                current_passed = sum([int(x['Count'][0]) for x in rd.rows])
                passed_pct = current_passed * (100.0 / float(passed_count))

                m = (
                    "Deploy Action {} Current Passed: {}, Expected Passed: {}"
                ).format
                mylog.debug(m(action_obj.name, current_passed, passed_count))

                m = "Action Results Passed: {1:.0f}% ({0})".format
                actionlog.info(m(action_obj.name, passed_pct))

                # if current_passed matches passed_count, then set
                # passed_count_reached = True
                if current_passed >= passed_count:
                    passed_count_reached = True

                if not passed_count_reached:
                    time.sleep(1)
                    continue

            # if passed_count was reached (the sum of Count from all rows from
            # the aggregate getresultdata is the same or greater as the number
            # of servers that matched the pre-action question), determine
            # if all servers have "finished"

            # get the full resultdata
            rd = self.get_result_data(action_obj, False)

            # create a dictionary to hold action statuses and the
            # computer names for each action status
            as_map = {}

            for row in rd.rows:
                computer_name = row['Computer Name'][0]
                action_status = row['Action Statuses'][0]
                action_status = action_status.split(':')[1]
                if not action_status in as_map:
                    as_map[action_status] = []
                as_map[action_status].append(computer_name)

            total_count = utils.get_dict_list_len(as_map)
            finished_count = utils.get_dict_list_len(as_map, finished_keys)
            success_count = utils.get_dict_list_len(as_map, success_keys)
            running_count = utils.get_dict_list_len(as_map, running_keys)
            failed_count = utils.get_dict_list_len(as_map, failed_keys)
            unknown_count = utils.get_dict_list_len(as_map, ARS, True)

            finished_pct = finished_count * (100.0 / float(passed_count))

            m = "Action Results Completed: {1:.0f}% ({0})".format
            actionlog.info(m(action_obj.name, finished_pct))

            progress = (
                "{} Result Counts:\n"
                "\tRunning Count: {}\n"
                "\tSuccess Count: {}\n"
                "\tFailed Count: {}\n"
                "\tUnknown Count: {}\n"
                "\tFinished Count: {}\n"
                "\tTotal Count: {}\n"
                "\tFinished Count must equal: {}"
            ).format(
                action_obj.name,
                running_count,
                success_count,
                failed_count,
                unknown_count,
                finished_count,
                total_count,
                passed_count,
            )

            if finished_count >= passed_count:
                actionlog.info(progress)
                finished = True
                break

            mylog.debug(progress)
            time.sleep(1)

        ret = {
            'action_object': action_obj,
            'action_results': rd,
            'action_progress_human': progress,
            'action_progress_map': as_map,
        }

        return ret

    def export_obj(self, obj, export_format, **kwargs):
        objtype = type(obj)
        try:
            objclassname = objtype.__name__
        except:
            objclassname = 'Unknown'

        export_maps = constants.EXPORT_MAPS

        # build a list of supported object types
        supp_types = ', '.join(export_maps.keys())

        # see if supplied obj is a supported object type
        type_match = [
            x for x in export_maps if isinstance(obj, getattr(api, x))
        ]

        if not type_match:
            err = (
                "{} not a supported object to export, must be one of: {}"
            ).format
            raise HandlerError(err(objtype, supp_types))

        # get the export formats for this obj type
        export_formats = export_maps.get(type_match[0], '')
        if export_format not in export_formats:
            err = (
                "{!r} not a supported export format for {}, must be one of: {}"
            ).format(export_format, objclassname, ', '.join(export_formats))
            raise HandlerError(err)

        # perform validation on optional kwargs, if they exist
        opt_keys = export_formats.get(export_format, [])
        for opt_key in opt_keys:
            check_args = dict(opt_key.items() + {'d': kwargs}.items())
            utils.check_dictkey(**check_args)

        # filter out the kwargs that are specific to this obj type and
        # format type
        format_kwargs = {
            k: v for k, v in kwargs.iteritems()
            if k in [a['key'] for a in opt_keys]
        }

        # run the handler that is specific to this objtype, if it exists
        class_method_str = '_export_class_' + type_match[0]
        class_handler = getattr(self, class_method_str, '')
        if class_handler:
            result = class_handler(obj, export_format, **format_kwargs)
        else:
            err = "{!r} not supported by Handler!".format
            raise HandlerError(err(objclassname))
        return result

    def export_to_report_file(self, obj, export_format, **kwargs):

        report_file = kwargs.get('report_file', None)

        if not report_file:
            report_file = "{}_{}.{}".format(
                type(obj).__name__, utils.get_now(), export_format,
            )
            m = "No report file name supplied, generated name: {!r}".format
            mylog.debug(m(report_file))

        # try to get report_dir from the report_file
        report_dir = os.path.dirname(report_file)

        # try to get report_dir from kwargs
        if not report_dir:
            report_dir = kwargs.get('report_dir', None)

        # just use current working dir
        if not report_dir:
            report_dir = os.getcwd()

        # make report_dir if it doesnt exist
        if not os.path.isdir(report_dir):
            os.makedirs(report_dir)

        # remove any path from report_file
        report_file = os.path.basename(report_file)

        # if prefix/postfix, add to report_file
        prefix = kwargs.get('prefix', '')
        postfix = kwargs.get('postfix', '')
        report_file, report_ext = os.path.splitext(report_file)
        report_file = '{}{}{}{}'.format(
            prefix, report_file, postfix, report_ext
        )

        # join the report_dir and report_file to come up with report_path
        report_path = os.path.join(report_dir, report_file)

        # get the results of exporting the object
        result = self.export_obj(obj, export_format, **kwargs)

        with open(report_path, 'w') as fd:
            fd.write(result)

        m = "Report file {!r} written with {} bytes".format
        mylog.info(m(report_path, len(result)))
        return report_path, result

    def get(self, obj, **kwargs):
        obj_map = utils.get_obj_map(obj)
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]

        # if the api doesn't support filtering for this object,
        # get all objects of this type and manually filter
        if not api_attrs:
            all_objs = self.get_all(obj, **kwargs)
            return_objs = getattr(api, all_objs.__class__.__name__)()
            for k, v in kwargs.iteritems():
                if not hasattr(all_objs[0], k):
                    continue
                if not utils.is_list(v):
                    v = [v]
                for obj in all_objs:
                    if not getattr(obj, k) in v:
                        continue
                    return_objs.append(obj)
            if not return_objs:
                err = "No results found searching for {}!!".format
                raise HandlerError(err(kwargs))
            return return_objs

        # if api supports filtering for this object,
        # but no filters supplied in kwargs, raise
        if not any(api_kwattrs):
            err = "Getting a {} requires at least one filter: {}".format
            raise HandlerError(err(obj, api_attrs))

        # if there is a multi in obj_map, that means we can pass a list
        # type to the api. the list will an entry for each api_kw
        if obj_map['multi']:
            return self._get_multi(obj_map, **kwargs)

        # if there is a single in obj_map but not multi, that means
        # we have to find each object individually
        if obj_map['single']:
            return self._get_single(obj_map, **kwargs)

        err = "No single or multi search defined for {}".format
        raise HandlerError(err(obj))

    def get_all(self, obj, **kwargs):
        obj_map = utils.get_obj_map(obj)
        api_obj_all = getattr(api, obj_map['all'])()
        found = self._find(api_obj_all, **kwargs)
        return found

    def get_result_data(self, obj, aggregate=False, **kwargs):
        ''' note #1 from jwk:
        For Action GetResultData:
        You have to make a ResultInfo request at least once every 2 minutes.
        The server gathers the result data by asking a saved question.
        It won't re-issue the saved question unless you make a GetResultInfo
        request. When you make a GetResultInfo request, if there is no
        question that is less than 2 minutes old, the server will automatically
        reissue a new question instance to make sure fresh data is available.

        note #2 from jwk:
         To get the aggregate data (without computer names),
         set row_counts_only_flag = 1. To get the computer names,
         use row_counts_only_flag = 0 (default).
        '''

        # do a getresultinfo to ensure fresh data is available for
        # getresultdata
        self.get_result_info(obj, **kwargs)

        # do a getresultdata
        if aggregate:
            rd = self.session.getResultData(
                obj, row_counts_only_flag=1, **kwargs
            )
        else:
            rd = self.session.getResultData(obj, **kwargs)
        return rd

    def get_result_info(self, obj, **kwargs):
        ri = self.session.getResultInfo(obj, **kwargs)
        return ri

    def stop_action(self, id, **kwargs):
        action_obj = self.get('action', id=id)[0]
        add_action_stop_obj = api.ActionStop()
        add_action_stop_obj.action = action_obj
        action_stop_obj = self.session.add(add_action_stop_obj)
        m = (
            'Action stopped successfully, ID of action stop: {}'
        ).format
        mylog.debug(m(action_stop_obj.id))
        return action_stop_obj

    # BEGIN PRIVATE METHODS
    def _find(self, api_object, **kwargs):
        req_kwargs = utils.get_req_kwargs(**kwargs)
        try:
            search_str = '; '.join([str(x) for x in api_object])
        except:
            search_str = api_object
        mylog.debug("Searching for {}".format(search_str))
        try:
            found = self.session.find(api_object, **req_kwargs)
        except Exception as e:
            mylog.error(e)
            err = "No results found searching for {}!!".format
            raise HandlerError(err(search_str))

        if utils.empty_obj(found):
            err = "No results found searching for {}!!".format
            raise HandlerError(err(search_str))

        mylog.debug("Found {}".format(found))
        return found

    def _get_multi(self, obj_map, **kwargs):
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # create a list object to append our searches to
        api_obj_multi = getattr(api, obj_map['multi'])()
        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    api_obj_single = getattr(api, obj_map['single'])()
                    setattr(api_obj_single, k, i)
                    api_obj_multi.append(api_obj_single)
            else:
                api_obj_single = getattr(api, obj_map['single'])()
                setattr(api_obj_single, k, v)
                api_obj_multi.append(api_obj_single)

        # find the multi list object
        found = self._find(api_obj_multi, **kwargs)
        return found

    def _get_single(self, obj_map, **kwargs):
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # we create a list object to append our single item searches to
        if obj_map.get('allfix', ''):
            found = getattr(api, obj_map['allfix'])()
        else:
            found = getattr(api, obj_map['all'])()

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    api_obj_single = getattr(api, obj_map['single'])()
                    setattr(api_obj_single, k, i)
                    found.append(self._find(api_obj_single, **kwargs))
            else:
                api_obj_single = getattr(api, obj_map['single'])()
                setattr(api_obj_single, k, v)
                found.append(self._find(api_obj_single, **kwargs))

        return found

    def _get_sensor_defs(self, defs):
        s_obj_map = constants.GET_OBJ_MAP['sensor']
        search_keys = s_obj_map['search']

        for d in defs:
            def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

            # get the sensor object
            if not 'sensor_obj' in d:
                d['sensor_obj'] = self.get('sensor', **def_search)[0]
        return defs

    def _get_package_def(self, d):
        s_obj_map = constants.GET_OBJ_MAP['package']
        search_keys = s_obj_map['search']

        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        # get the package object
        if not 'package_obj' in d:
            d['package_obj'] = self.get('package', **def_search)[0]
        return d

    def _export_class_BaseType(self, obj, export_format, **kwargs):
        # run the handler that is specific to this export_format, if it exists
        format_method_str = '_export_format_' + export_format
        format_handler = getattr(self, format_method_str, '')
        if format_handler:
            result = format_handler(obj, **kwargs)
        else:
            err = "{!r} not coded for in Handler!".format
            raise HandlerError(err(export_format))
        return result

    def _export_class_ResultSet(self, obj, export_format, **kwargs):
        '''
        ensure kwargs[sensors] has all the sensors that correlate
        to the what_hash of each column, but only if header_add_sensor=True
        needed for: ResultSet.write_csv(header_add_sensor=True)
        '''
        header_add_sensor = kwargs.get('header_add_sensor', False)
        sensors = kwargs.get('sensors', []) or getattr(obj, 'sensors', [])

        if header_add_sensor:
            kwargs['sensors'] = sensors
            sensor_hashes = [x.hash for x in sensors]
            column_hashes = [x.what_hash for x in obj.columns]
            missing_hashes = [
                x for x in column_hashes if x not in sensor_hashes and x > 1
            ]
            if missing_hashes:
                missing_sensors = self.get('sensor', hash=missing_hashes)
                kwargs['sensors'] += list(missing_sensors)

        # run the handler that is specific to this export_format, if it exists
        format_method_str = '_export_format_' + export_format
        format_handler = getattr(self, format_method_str, '')
        if format_handler:
            result = format_handler(obj, **kwargs)
        else:
            err = "{!r} not coded for in Handler!".format
            raise HandlerError(err(export_format))
        return result

    def _export_format_csv(self, obj, **kwargs):
        if not hasattr(obj, 'write_csv'):
            err = "{!r} has no write_csv() method!".format
            raise HandlerError(err(obj))
        out = io.BytesIO()
        if getattr(obj, '_list_properties', ''):
            result = obj.write_csv(out, list(obj), **kwargs)
        else:
            result = obj.write_csv(out, obj, **kwargs)
        result = out.getvalue()
        return result

    def _export_format_json(self, obj, **kwargs):
        if not hasattr(obj, 'to_json'):
            err = "{!r} has no to_json() method!".format
            raise HandlerError(err(obj))
        result = obj.to_json(jsonable=obj, **kwargs)
        return result

    def _export_format_xml(self, obj, **kwargs):
        if not hasattr(obj, 'toSOAPBody'):
            err = "{!r} has no toSOAPBody() method!".format
            raise HandlerError(err(obj))
        result = obj.toSOAPBody(**kwargs)
        return result
