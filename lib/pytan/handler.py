# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""The main :mod:`pytan` module that provides methods for programmatic use."""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import logging
import io
import threading

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import taniumpy
import pytan


class Handler(object):
    """Creates a connection to a Tanium SOAP Server on host:port

    Parameters
    ----------
    username : str
        `username` to connect to `host` with
    password : str
        `password` to connect to `host` with
    host : str
        hostname or ip of Tanium SOAP Server
    port : int, optional
        port of Tanium SOAP Server on `host`
    get_version : bool, optional
        get the version of the server from Tanium after authenticating, default to True
    gmt_log : bool, optional
        True use GMT timezone for log output, False use local time for log output
    loglevel : int, optional
        0 should not print anything, 1 and higher will print more
    debugformat : bool, optional
        False use one line logformat, True use two lines

    Notes
    -----
      * for 6.2: port 444 is the default SOAP port, port 443 forwards /soap/ URLs to the SOAP port,
        Use port 444 if you have direct access to it. However, port 444 is the only port that
        exposes the /info page in 6.2
      * for 6.5: port 443 is the default SOAP port, there is no port 444

    See Also
    --------
    :data:`pytan.constants.LOG_LEVEL_MAPS` : maps a given `loglevel` to respective logger names and their logger levels
    :data:`pytan.constants.INFO_FORMAT` : debugformat=False
    :data:`pytan.constants.DEBUG_FORMAT` : debugformat=True
    """

    def __init__(self, username, password, host, port="443", loglevel=0,
                 debugformat=False, get_version=True, gmt_log=True, **kwargs):
        super(Handler, self).__init__()

        self.mylog = logging.getLogger("pytan.handler")

        # setup the console logging handler
        pytan.utils.setup_console_logging(gmt_log)
        # create all the loggers and set their levels based on loglevel
        pytan.utils.set_log_levels(loglevel)
        # change the format of console logging handler if need be
        pytan.utils.change_console_format(debugformat)

        self.loglevel = loglevel

        if not username:
            raise pytan.exceptions.HandlerError("Must supply username!")
        if not password:
            raise pytan.exceptions.HandlerError("Must supply password!")
        if not host:
            raise pytan.exceptions.HandlerError("Must supply host!")
        if not port:
            raise pytan.exceptions.HandlerError("Must supply port!")
        try:
            port = int(port)
        except ValueError:
            raise pytan.exceptions.HandlerError("port must be an integer!")

        pytan.utils.test_app_port(host, port)
        self.session = pytan.sessions.Session(host, port)
        self.session.authenticate(username, password)
        if get_version:
            self.server_version = "Not yet determined!"
            thread = threading.Thread(target=self._derive_server_version, args=())
            thread.daemon = True
            thread.start()
        else:
            self.server_version = "get_version is False!"

    def __str__(self):
        str_tpl = "Handler for {}, Version: {}".format
        ret = str_tpl(self.session, getattr(self, 'server_version', 'Version Unavailable'))
        return ret

    # Questions
    def ask(self, **kwargs):
        """Ask a type of question and get the results back

        Parameters
        ----------
        qtype : str, optional
            type of question to ask: saved, manual, or _manual, defaults to manual

        Returns
        -------
        result : dict, containing:
            * `question_object` : one of the following depending on `qtype`: :class:`taniumpy.object_types.question.Question` or :class:`taniumpy.object_types.saved_question.SavedQuestion`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        See Also
        --------
        :data:`pytan.constants.Q_OBJ_MAP` : maps qtype to a method in Handler()
        """
        qtype = kwargs.get('qtype', 'manual')
        q_obj_map = pytan.utils.get_q_obj_map(qtype)
        kwargs.pop('qtype')
        result = getattr(self, q_obj_map['handler'])(**kwargs)
        return result

    @pytan.utils.func_timing
    def ask_saved(self, refresh_data=False, **kwargs):
        """Ask a saved question and get the results back

        Parameters
        ----------
        id : int, list of int, optional
            id of saved question to ask
        name : str, list of str
            name of saved question
        refresh_data: bool, optional
            False: do not perform a getResultInfo before issuing a getResultData
            True: perform a getResultInfo before issuing a getResultData

        Returns
        -------
        ret : dict, containing
            * `question_object` : :class:`taniumpy.object_types.saved_question.SavedQuestion`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        Notes
        -----
        id or name must be supplied
        """
        # get the saved_question object the user passed in
        sq_objs = self.get('saved_question', **kwargs)

        if len(sq_objs) != 1:
            err = (
                "Multiple saved questions returned, can only ask one "
                "saved question!\nArgs: {}\nReturned saved questions:\n\t{}"
            ).format
            sq_obj_str = '\n\t'.join([str(x) for x in sq_objs])
            raise pytan.exceptions.HandlerError(err(kwargs, sq_obj_str))

        sq_obj = sq_objs[0]

        q_obj = self._find(sq_obj.question)
        poller = None
        poller_success = None

        if refresh_data:
            # if GetResultInfo is issued on a saved question, Tanium will issue a new question
            # to fetch new/updated results
            self.get_result_info(sq_obj, **kwargs)

            # re-fetch the saved question object to get the newly asked question info
            sq_obj = self._find(pytan.utils.shrink_obj(sq_obj))

            q_obj = self._find(sq_obj.question)

            m = "Question Added, ID: {}, query text: {!r}, expires: {}".format
            self.mylog.debug(m(q_obj.id, q_obj.query_text, q_obj.expiration))

            # poll the new question for this saved question to wait for results
            poller = pytan.pollers.QuestionPoller(self, q_obj, **kwargs)
            poller_success = poller.run(**kwargs)

        # get the results for the questionf or this saved question
        result = self.get_result_data(q_obj, **kwargs)

        # add the sensors from this question to the ResultSet object
        # for reporting
        result.sensors = [x.sensor for x in q_obj.selects]

        ret = {
            'saved_question_object': sq_obj,
            'poller_object': poller,
            'poller_success': poller_success,
            'question_object': q_obj,
            'question_results': result,
        }

        return ret

    def ask_manual(self, **kwargs):
        """Ask a manual question using human strings and get the results back

        This method takes a string or list of strings and parses them into
        their corresponding definitions needed by :func:`_ask_manual`

        Parameters
        ----------
        sensors : str, list of str
            sensors (columns) to include in question
        question_filters : str, list of str, optional
            filters that apply to the whole question
        question_options : str, list of str, optional
            options that apply to the whole question
        get_results : bool, optional
            * True: wait for result completion after asking question
            * False: just ask the question and return it in result
        sensors_help : bool, optional
            * False: do not print the help string for sensors
            * True: print the help string for sensors and exit
        filters_help : bool, optional
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * False: do not print the help string for options
            * True: print the help string for options and exit

        Returns
        -------
        result : dict, containing:
            * `question_object` : :class:`taniumpy.object_types.question.Question`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        Examples
        --------
        >>> # example of str for `sensors`
        >>> sensors = 'Sensor1'

        >>> # example of str for `sensors` with params
        >>> sensors = 'Sensor1{key:value}'

        >>> # example of str for `sensors` with params and filter
        >>> sensors = 'Sensor1{key:value}, that contains:example text'

        >>> # example of str for `sensors` with params and filter and options
        >>> sensors = (
        ...     'Sensor1{key:value}, that contains:example text,'
        ...     'opt:ignore_case, opt:max_data_age:60'
        ... )

        >>> # example of str for question_filters
        >>> question_filters = 'Sensor2, that contains:example test'

        >>> # example of list of str for question_options
        >>> question_options = ['max_data_age:3600', 'and']

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`pytan.constants.OPTION_MAPS` : valid option dictionaries for options
        """

        if kwargs.get('sensors_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_sensors())

        if kwargs.get('filters_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_filters())

        if kwargs.get('options_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_options())

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

        clean_kw = ['sensor_defs', 'question_filter_defs', 'question_option_defs']
        [kwargs.pop(x) for x in clean_kw if x in kwargs]

        sensor_defs = pytan.utils.dehumanize_sensors(sensors)
        q_filter_defs = pytan.utils.dehumanize_question_filters(q_filters)
        q_option_defs = pytan.utils.dehumanize_question_options(q_options)

        result = self._ask_manual(
            sensor_defs=sensor_defs,
            question_filter_defs=q_filter_defs,
            question_option_defs=q_option_defs,
            **kwargs
        )
        return result

    # Actions
    def deploy_action(self, **kwargs):
        """Deploy an action and get the results back

        This method takes a string or list of strings and parses them into
        their corresponding definitions needed by :func:`_deploy_action`

        Parameters
        ----------
        package : str
            each string must describe a package
        action_filters : str, list of str, optional
            each string must describe a sensor and a filter which limits which computers the action will deploy `package` to
        action_options : str, list of str, optional
            options to apply to `action_filters`
        start_seconds_from_now : int, optional
            start action N seconds from now
        expire_seconds : int, optional
            expire action N seconds from now, will be derived from package if not supplied
        run : bool, optional
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise pytan.exceptions.RunFalse -- does not deploy the action
            * True: actually deploy the action
        get_results : bool, optional
            * True: wait for result completion after deploying action
            * False: just deploy the action and return the object in `ret`
        package_help : bool, optional
            * False: do not print the help string for package
            * True: print the help string for package and exit
        filters_help : bool, optional
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * False: do not print the help string for options
            * True: print the help string for options and exit

        Returns
        -------
        ret : dict, containing:
            * `action_object` : :class:`taniumpy.object_types.action.Action`
            * `action_results` : :class:`taniumpy.object_types.result_set.ResultSet`
            * `action_progress_human` : str, progress map in human form
            * `action_progress_map` : dict, progress map in dictionary form
            * `pre_action_question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        Examples
        --------
        >>> # example of str for `package`
        >>> package = 'Package1'

        >>> # example of str for `package` with params
        >>> package = 'Package1{key:value}'

        >>> # example of str for `action_filters` with params and filter for sensors
        >>> action_filters = 'Sensor1{key:value}, that contains:example text'

        >>> # example of list of str for `action_options`
        >>> action_options = ['max_data_age:3600', 'and']

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`pytan.constants.OPTION_MAPS` : valid option dictionaries for options
        """

        if kwargs.get('package_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_package())

        if kwargs.get('filters_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_filters())

        if kwargs.get('options_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_options())

        # the human string describing the sensors/filter that user wants
        # to deploy the action against
        action_filters = kwargs.get('action_filters', [])

        # the question options to use on the pre-action question and on the
        # group for the action filters
        action_options = kwargs.get('action_options', [])

        # name of package to deploy with params as {key=value1,key2=value2}
        package = kwargs.get('package', '')

        clean_kw = ['package_def', 'action_filter_defs', 'action_option_defs']
        [kwargs.pop(x) for x in clean_kw if x in kwargs]

        action_filter_defs = pytan.utils.dehumanize_sensors(action_filters, 'action_filters', True)
        action_option_defs = pytan.utils.dehumanize_question_options(action_options)
        package_def = pytan.utils.dehumanize_package(package)

        deploy_result = self._deploy_action(
            action_filter_defs=action_filter_defs,
            action_option_defs=action_option_defs,
            package_def=package_def,
            **kwargs
        )
        return deploy_result

    def stop_action(self, id, **kwargs):
        """Stop an action

        Parameters
        ----------
        id : int
            id of action to stop

        Returns
        -------
        action_stop_obj : :class:`taniumpy.object_types.action_stop.ActionStop`
            The object containing the ID of the action stop job
        """
        action_obj = self.get('action', id=id)[0]
        add_action_stop_obj = taniumpy.ActionStop()
        add_action_stop_obj.action = action_obj
        action_stop_obj = self._add(add_action_stop_obj)
        m = (
            'Action stopped successfully, ID of action stop: {}'
        ).format
        self.mylog.debug(m(action_stop_obj.id))
        return action_stop_obj

    # Result Data / Result Info
    @pytan.utils.func_timing
    def get_result_data(self, obj, aggregate=False, shrink=True, **kwargs):
        """Get the result data for a python API object

        This method issues a GetResultData command to the SOAP api for `obj`. GetResultData returns the columns and rows that are currently available for `obj`.

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            object to get result data for
        aggregate : bool, optional
            * False: get all the data
            * True: get just the aggregate data (row counts of matches)
        shrink : bool, optional
            * True: Shrink the object down to just id/name/hash attributes (for smaller request)
            * False: Use the full object as is

        Returns
        -------
        rd : :class:`taniumpy.object_types.result_set.ResultSet`
            The return of GetResultData for `obj`
        """

        """ note #1 from jwk:
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
        """
        if shrink:
            shrunk_obj = pytan.utils.shrink_obj(obj)
        else:
            shrunk_obj = obj

        if 'suppress_object_list' not in kwargs:
            kwargs['suppress_object_list'] = 1

        # do a getresultdata
        if aggregate:
            rd = self.session.get_result_data(shrunk_obj, row_counts_only_flag=1, **kwargs)
        else:
            rd = self.session.get_result_data(shrunk_obj, **kwargs)
        return rd

    @pytan.utils.func_timing
    def get_result_info(self, obj, shrink=True, **kwargs):
        """Get the result info for a python API object

        This method issues a GetResultInfo command to the SOAP api for `obj`. GetResultInfo returns information about how many servers have passed the `obj`, total number of servers, and so on.

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            object to get result data for
        shrink : bool, optional
            * True: Shrink the object down to just id/name/hash attributes (for smaller request)
            * False: Use the full object as is

        Returns
        -------
        ri : :class:`taniumpy.object_types.result_info.ResultInfo`
            The return of GetResultData for `obj`
        """
        if shrink:
            shrunk_obj = pytan.utils.shrink_obj(obj)
        else:
            shrunk_obj = obj

        if 'suppress_object_list' not in kwargs:
            kwargs['suppress_object_list'] = 1

        ri = self.session.get_result_info(shrunk_obj, **kwargs)
        # pytan.utils.log_session_communication(self)
        self.mylog.debug(ri)
        return ri

    # Objects
    def create_from_json(self, objtype, json_file):
        """Creates a new object using the SOAP api from a json file

        Parameters
        ----------
        objtype : str
            Type of object described in `json_file`
        json_file : str
            path to JSON file that describes an API object

        Returns
        -------
        ret : :class:`taniumpy.object_types.base.BaseType`
            TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`pytan.constants.GET_OBJ_MAP` : maps objtype to supported 'create_json' types
        """
        obj_map = pytan.utils.get_obj_map(objtype)
        create_json_ok = obj_map['create_json']
        if not create_json_ok:
            json_createable = ', '.join([
                x for x, y in pytan.constants.GET_OBJ_MAP.items() if y['create_json']
            ])
            m = (
                "{} is not a json createable object! Supported objects: {}"
            ).format
            raise pytan.exceptions.HandlerError(m(objtype, json_createable))

        add_obj = pytan.utils.load_taniumpy_from_json(json_file)

        if getattr(add_obj, '_list_properties', ''):
            obj_list = [x for x in add_obj]
        else:
            obj_list = [add_obj]

        del_keys = ['id', 'hash']
        [
            setattr(y, x, None)
            for y in obj_list for x in del_keys
            if hasattr(y, x)
        ]

        if obj_map.get('allfix'):
            ret = pytan.utils.get_taniumpy_obj(obj_map['allfix'])()
        else:
            ret = pytan.utils.get_taniumpy_obj(obj_map['all'])()

        for x in obj_list:
            try:
                list_obj = self._add(x)
            except Exception as e:
                m = (
                    "Failure while importing {}: {}\nJSON Dump of object: {}"
                ).format
                raise pytan.exceptions.HandlerError(m(x, e, x.to_json(x)))

            m = "New {} (ID: {}) created successfully!".format
            self.mylog.info(m(list_obj, getattr(list_obj, 'id', 'Unknown')))

            ret.append(list_obj)
        return ret

    def run_plugin(self, plugin):
        # run the plugin
        plugin_result = self.session.run_plugin(plugin)

        # zip up the sql results into a list of python dictionaries
        sql_zipped = pytan.utils.plugin_zip(plugin_result)

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def create_dashboard(self, name, text='', group='', public_flag=True):

        # get the ID for the group if a name was passed in
        if group:
            group_id = self.get('group', name=group)[0].id
        else:
            group_id = 0

        if public_flag:
            public_flag = 1
        else:
            public_flag = 0

        # create the plugin parent
        plugin = taniumpy.Plugin()
        plugin.name = 'CreateDashboard'
        plugin.bundle = 'Dashboards'

        # create the plugin arguments
        plugin.arguments = taniumpy.PluginArgumentList()

        arg1 = taniumpy.PluginArgument()
        arg1.name = 'dash_name'
        arg1.type = 'String'
        arg1.value = name
        plugin.arguments.append(arg1)

        arg2 = taniumpy.PluginArgument()
        arg2.name = 'dash_text'
        arg2.type = 'String'
        arg2.value = text
        plugin.arguments.append(arg2)

        arg3 = taniumpy.PluginArgument()
        arg3.name = 'group_id'
        arg3.type = 'Number'
        arg3.value = group_id
        plugin.arguments.append(arg3)

        arg4 = taniumpy.PluginArgument()
        arg4.name = 'public_flag'
        arg4.type = 'Number'
        arg4.value = public_flag
        plugin.arguments.append(arg4)

        arg5 = taniumpy.PluginArgument()
        arg5.name = 'sqid_xml'
        arg5.type = 'String'
        arg5.value = ''
        plugin.arguments.append(arg5)

        # run the plugin
        plugin_result, sql_zipped = self.run_plugin(plugin)

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def delete_dashboard(self, name):
        dashboards_to_del = self.get_dashboards(name)[1]

        # create the plugin parent
        plugin = taniumpy.Plugin()
        plugin.name = 'DeleteDashboards'
        plugin.bundle = 'Dashboards'

        # create the plugin arguments
        plugin.arguments = taniumpy.PluginArgumentList()

        arg1 = taniumpy.PluginArgument()
        arg1.name = 'dashboard_ids'
        arg1.type = 'Number_Set'
        arg1.value = ','.join([x['id'] for x in dashboards_to_del])
        plugin.arguments.append(arg1)

        # run the plugin
        plugin_result, sql_zipped = self.run_plugin(plugin)

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def get_dashboards(self, name=''):

        # create the plugin parent
        plugin = taniumpy.Plugin()
        plugin.name = 'GetDashboards'
        plugin.bundle = 'Dashboards'

        # run the plugin
        plugin_result, sql_zipped = self.run_plugin(plugin)

        # if name specified, filter the list of dicts for matching name
        if name:
            sql_zipped = [x for x in sql_zipped if x['name'] == name]
            if not sql_zipped:
                m = "No dashboards found that match name: {!r}".format
                raise pytan.exceptions.NotFoundError(m(name))

        # return the plugin result and the python dictionary of results
        return plugin_result, sql_zipped

    def create_sensor(self):
        """Create a sensor object

        Warnings
        --------
        Not currently supported, too complicated to add.
        Use :func:`create_from_json` instead for this object type!

        Raises
        ------
        pytan.exceptions.HandlerError : :exc:`pytan.utils.pytan.exceptions.HandlerError`
        """
        m = (
            "Sensor creation not supported via PyTan as of yet, too complex\n"
            "Use create_sensor_from_json() instead!"
        )
        raise pytan.exceptions.HandlerError(m)

    def create_package(
            self,
            name,
            command,
            display_name='',
            file_urls=[],
            command_timeout_seconds=600,
            expire_seconds=600,
            parameters_json_file='',
            verify_filters=[],
            verify_filter_options=[],
            verify_expire_seconds=600,
            **kwargs):
        """Create a package object

        Parameters
        ----------
        name : str
            name of package to create
        command : str
            command to execute
        display_name : str, optional
            display name of package
        file_urls : list of strings, optional
            * URL of file to add to package
            * can optionally define download_seconds by using SECONDS::URL
            * can optionally define file name by using FILENAME||URL
            * can combine optionals by using SECONDS::FILENAME||URL
            * FILENAME will be extracted from basename of URL if not provided
        command_timeout_seconds : int, optional
            timeout for command execution in seconds
        parameters_json_file : str, optional
            path to json file describing parameters for package
        expire_seconds : int, optional
            timeout for action expiry in seconds
        verify_filters : str or list of str, optional
            each string must describe a filter to be used to verify the package
        verify_filter_options : str or list of str, optional
            each string must describe an option for `verify_filters`
        verify_expire_seconds : int, optional
            timeout for verify action expiry in seconds
        filters_help : bool, optional
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * False: do not print the help string for options
            * True: print the help string for options and exit
        metadata: list of list of strs, optional
            * each list must be a 2 item list:
            * list item 1 property name
            * list item 2 property value

        Returns
        -------
        package_obj : :class:`taniumpy.object_types.package_spec.PackageSpec`
            TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filters for verify_filters
        :data:`pytan.constants.OPTION_MAPS` : valid options for verify_filter_options
        """

        if kwargs.get('filters_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_filters())

        if kwargs.get('options_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_options())

        metadata = kwargs.get('metadata', [])
        metadatalist_obj = pytan.utils.build_metadatalist_obj(metadata)

        # bare minimum arguments for new package: name, command
        add_package_obj = taniumpy.PackageSpec()
        add_package_obj.name = name
        if display_name:
            add_package_obj.display_name = display_name
        add_package_obj.command = command
        add_package_obj.command_timeout = command_timeout_seconds
        add_package_obj.expire_seconds = expire_seconds
        add_package_obj.metadata = metadatalist_obj

        # VERIFY FILTERS
        if verify_filters:
            verify_filter_defs = pytan.utils.dehumanize_question_filters(
                verify_filters
            )
            verify_option_defs = pytan.utils.dehumanize_question_options(
                verify_filter_options
            )
            verify_filter_defs = self._get_sensor_defs(verify_filter_defs)
            add_verify_group = pytan.utils.build_group_obj(
                verify_filter_defs, verify_option_defs
            )
            verify_group = self._add(add_verify_group)
            # this didn't work:
            # add_package_obj.verify_group = verify_group
            add_package_obj.verify_group_id = verify_group.id
            add_package_obj.verify_expire_seconds = verify_expire_seconds

        # PARAMETERS
        if parameters_json_file:
            # issue #6
            add_package_obj.parameter_definition = pytan.utils.load_param_json_file(parameters_json_file)

        # FILES
        if file_urls:
            filelist_obj = taniumpy.PackageFileList()
            for file_url in file_urls:
                # if :: is in file_url, split on it and use 0 as
                # download_seconds
                if '::' in file_url:
                    download_seconds, file_url = file_url.split('::')
                else:
                    download_seconds = 0
                # if || is in file_url, split on it and use 0 as file name
                # else wise get file name from basename of URL
                if '||' in file_url:
                    filename, file_url = file_url.split('||')
                else:
                    filename = os.path.basename(file_url)
                file_obj = taniumpy.PackageFile()
                file_obj.name = filename
                file_obj.source = file_url
                file_obj.download_seconds = download_seconds
                filelist_obj.append(file_obj)
            add_package_obj.files = filelist_obj

        package_obj = self._add(add_package_obj)
        m = "New package {!r} created with ID {!r}, command: {!r}".format
        self.mylog.info(m(package_obj.name, package_obj.id, package_obj.command))
        return package_obj

    def create_group(self, groupname, filters=[], filter_options=[], **kwargs):
        """Create a group object

        Parameters
        ----------
        groupname : str
            name of group to create
        filters : str or list of str, optional
            each string must describe a filter
        filter_options : str or list of str, optional
            each string must describe an option for `filters`
        filters_help : bool, optional
            * False: do not print the help string for filters
            * True: print the help string for filters and exit
        options_help : bool, optional
            * False: do not print the help string for options
            * True: print the help string for options and exit

        Returns
        -------
        group_obj : :class:`taniumpy.object_types.group.Group`
            TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filters for filters
        :data:`pytan.constants.OPTION_MAPS` : valid options for filter_options
        """

        if kwargs.get('filters_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_filters())

        if kwargs.get('options_help', False):
            raise pytan.exceptions.PytanHelp(pytan.help.help_options())

        filter_defs = pytan.utils.dehumanize_question_filters(filters)
        filter_defs = self._get_sensor_defs(filter_defs)
        option_defs = pytan.utils.dehumanize_question_options(filter_options)
        add_group_obj = pytan.utils.build_group_obj(filter_defs, option_defs)
        add_group_obj.name = groupname
        group_obj = self._add(add_group_obj)
        m = "New group {!r} created with ID {!r}, filter text: {!r}".format
        self.mylog.info(m(group_obj.name, group_obj.id, group_obj.text))
        return group_obj

    def create_user(self, username, rolename=[], roleid=[], properties=[]):
        """Create a user object

        Parameters
        ----------
        username : str
            name of user to create
        rolename : str or list of str, optional
            name(s) of roles to add to user
        roleid : int or list of int, optional
            id(s) of roles to add to user
        properties: list of list of strs, optional
            * each list must be a 2 item list:
            * list item 1 property name
            * list item 2 property value

        Returns
        -------
        user_obj : :class:`taniumpy.object_types.user.User`
            TaniumPy object added to Tanium SOAP Server
        """
        if roleid or rolename:
            rolelist_obj = self.get('userrole', id=roleid, name=rolename)
        else:
            rolelist_obj = taniumpy.RoleList()
        metadatalist_obj = pytan.utils.build_metadatalist_obj(
            properties, 'TConsole.User.Property',
        )
        add_user_obj = taniumpy.User()
        add_user_obj.name = username
        add_user_obj.roles = rolelist_obj
        add_user_obj.metadata = metadatalist_obj
        user_obj = self._add(add_user_obj)
        m = "New user {!r} created with ID {!r}, roles: {!r}".format
        self.mylog.info(m(
            user_obj.name, user_obj.id, [x.name for x in rolelist_obj]
        ))
        return user_obj

    def create_whitelisted_url(
            self,
            url,
            regex=False,
            download_seconds=86400,
            properties=[]):
        """Create a whitelisted url object

        Parameters
        ----------
        url : str
            text of new url
        regex : bool, optional
            * True: `url` is a regex pattern
            * False: `url` is not a regex pattern
        download_seconds : int, optional
            how often to re-download `url`
        properties: list of list of strs, optional
            * each list must be a 2 item list:
            * list item 1 property name
            * list item 2 property value

        Returns
        -------
        url_obj : :class:`taniumpy.object_types.white_listed_url.WhiteListedUrl`
            TaniumPy object added to Tanium SOAP Server
        """
        if regex:
            url = 'regex:' + url

        metadatalist_obj = pytan.utils.build_metadatalist_obj(
            properties, 'TConsole.WhitelistedURL',
        )
        add_url_obj = taniumpy.WhiteListedUrl()
        add_url_obj.url_regex = url
        add_url_obj.download_seconds = download_seconds
        add_url_obj.metadata = metadatalist_obj
        url_obj = self._add(add_url_obj)
        m = "New Whitelisted URL {!r} created with ID {!r}".format
        self.mylog.info(m(url_obj.url_regex, url_obj.id))
        return url_obj

    def delete(self, objtype, **kwargs):
        """Delete an object type

        Parameters
        ----------
        objtype : string
            type of object to delete
        id/name/hash : int or string, list of int or string
            search attributes of object to delete, must supply at least one valid search attr

        Returns
        -------
        ret : dict
            dict containing deploy action object and results from deploy action

        See Also
        --------
        :data:`pytan.constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        """
        obj_map = pytan.utils.get_obj_map(objtype)
        delete_ok = obj_map['delete']
        if not delete_ok:
            deletable = ', '.join([
                x for x, y in pytan.constants.GET_OBJ_MAP.items() if y['delete']
            ])
            m = "{} is not a deletable object! Deletable objects: {}".format
            raise pytan.exceptions.HandlerError(m(objtype, deletable))
        objs_to_del = self.get(objtype, **kwargs)
        deleted_objects = []
        for obj_to_del in objs_to_del:
            del_obj = self.session.delete(obj_to_del)
            deleted_objects.append(del_obj)
            m = "Deleted {!r}".format
            self.mylog.info(m(str(del_obj)))
        return deleted_objects

    @pytan.utils.func_timing
    def export_obj(self, obj, export_format='csv', **kwargs):
        """Exports a python API object to a given export format

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            TaniumPy object to export
        export_format : str, optional
            the format to export `obj` to, can be one of: csv, xml, json
        header_sort : list of str, bool, optional
            * for `export_format` csv and `obj` types :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            * True: sort the headers automatically
            * False: do not sort the headers at all
            * list of str: sort the headers returned by priority based on provided list
        header_add_sensor : bool, optional
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not prefix the headers with the associated sensor name for each column
            * True: prefix the headers with the associated sensor name for each column
        header_add_type : bool, optional
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not postfix the headers with the result type for each column
            * True: postfix the headers with the result type for each column
        expand_grouped_columns : bool, optional
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not expand multiline row entries into their own rows
            * True: expand multiline row entries into their own rows
        explode_json_string_values : bool, optional
            * for `export_format` json or csv and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: do not explode JSON strings in object attributes into their own object attributes
            * True: explode JSON strings in object attributes into their own object attributes
        minimal : bool, optional
            * for `export_format` xml and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: include empty attributes in XML output
            * True: do not include empty attributes in XML output

        Returns
        -------
        result : str
            the contents of exporting `export_format`

        See Also
        --------
        :data:`pytan.constants.EXPORT_MAPS` : maps the type `obj` to `export_format` and the optional args supported for each
        """
        objtype = type(obj)
        try:
            objclassname = objtype.__name__
        except:
            objclassname = 'Unknown'

        export_maps = pytan.constants.EXPORT_MAPS

        # build a list of supported object types
        supp_types = ', '.join(export_maps.keys())

        # see if supplied obj is a supported object type
        type_match = [
            x for x in export_maps if isinstance(obj, getattr(taniumpy, x))
        ]

        if not type_match:
            err = (
                "{} not a supported object to export, must be one of: {}"
            ).format
            raise pytan.exceptions.HandlerError(err(objtype, supp_types))

        # get the export formats for this obj type
        export_formats = export_maps.get(type_match[0], '')
        if export_format not in export_formats:
            err = (
                "{!r} not a supported export format for {}, must be one of: {}"
            ).format(export_format, objclassname, ', '.join(export_formats))
            raise pytan.exceptions.HandlerError(err)

        # perform validation on optional kwargs, if they exist
        opt_keys = export_formats.get(export_format, [])
        for opt_key in opt_keys:
            check_args = dict(opt_key.items() + {'d': kwargs}.items())
            pytan.utils.check_dictkey(**check_args)

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
            raise pytan.exceptions.HandlerError(err(objclassname))
        return result

    def export_to_report_file(self, obj, export_format='csv', **kwargs):
        """Exports a python API object to a file

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            TaniumPy object to export
        export_format : str
            the format to export `obj` to, can be one of: csv, xml, json
        header_sort : list of str, bool, optional
            * for `export_format` csv and `obj` types :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            * True: sort the headers automatically
            * False: do not sort the headers at all
            * list of str: sort the headers returned by priority based on provided list
        header_add_sensor : bool, optional
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not prefix the headers with the associated sensor name for each column
            * True: prefix the headers with the associated sensor name for each column
        header_add_type : bool, optional
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not postfix the headers with the result type for each column
            * True: postfix the headers with the result type for each column
        expand_grouped_columns : bool, optional
            * for `export_format` csv and `obj` type :class:`taniumpy.object_types.result_set.ResultSet`
            * False: do not expand multiline row entries into their own rows
            * True: expand multiline row entries into their own rows
        explode_json_string_values : bool, optional
            * for `export_format` json or csv and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: do not explode JSON strings in object attributes into their own object attributes
            * True: explode JSON strings in object attributes into their own object attributes
        minimal : bool, optional
            * for `export_format` xml and `obj` type :class:`taniumpy.object_types.base.BaseType`
            * False: include empty attributes in XML output
            * True: do not include empty attributes in XML output
        report_file: str, optional
            filename to save report as, will be automatically generated if not supplied
        report_dir: str, optional
            directory to save report in, if not supplied, will be extracted from `report_file`. if no directory in `report_file` or `report_file` not specified, will use current working directory.
        prefix: str, optional
            prefix to add to `report_file`
        postfix: str, optional
            postfix to add to `report_file`

        Returns
        -------
        report_path : str
            the full path to the file created with contents of `result`
        result : str
            the str of `export_format`
        """
        report_file = kwargs.get('report_file', None)

        if not report_file:
            report_file = "{}_{}.{}".format(
                type(obj).__name__, pytan.utils.get_now(), export_format,
            )
            m = "No report file name supplied, generated name: {!r}".format
            self.mylog.debug(m(report_file))

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

        with open(report_path, 'wb') as fd:
            fd.write(result)

        m = "Report file {!r} written with {} bytes".format
        self.mylog.info(m(report_path, len(result)))
        return report_path, result

    @pytan.utils.func_timing
    def get(self, objtype, **kwargs):
        """Get an object type

        Parameters
        ----------
        objtype : string
            type of object to get
        id/name/hash : int or string, list of int or string
            search attributes of object to get, must supply at least one valid search attr

        See Also
        --------
        :data:`pytan.constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        """
        obj_map = pytan.utils.get_obj_map(objtype)
        manual_search = obj_map['manual']
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]

        # if the api doesn't support filtering for this object,
        # or if the user didn't supply any api_kwattrs and manual_search
        # is true, get all objects of this type and manually filter
        if not api_attrs or (not any(api_kwattrs) and manual_search):
            all_objs = self.get_all(objtype, **kwargs)
            return_objs = getattr(taniumpy, all_objs.__class__.__name__)()
            for k, v in kwargs.iteritems():
                if not hasattr(all_objs[0], k):
                    continue
                if not pytan.utils.is_list(v):
                    v = [v]
                for aobj in all_objs:
                    if not getattr(aobj, k) in v:
                        continue
                    return_objs.append(aobj)
            if not return_objs:
                err = "No results found searching for {} with {}!!".format
                raise pytan.exceptions.HandlerError(err(objtype, kwargs))
            return return_objs

        # if api supports filtering for this object,
        # but no filters supplied in kwargs, raise
        if not any(api_kwattrs):
            err = "Getting a {} requires at least one filter: {}".format
            raise pytan.exceptions.HandlerError(err(objtype, api_attrs))

        # if there is a multi in obj_map, that means we can pass a list
        # type to the taniumpy. the list will have an entry for each api_kw
        if obj_map['multi']:
            return self._get_multi(obj_map, **kwargs)

        # if there is a single in obj_map but not multi, that means
        # we have to find each object individually
        elif obj_map['single']:
            return self._get_single(obj_map, **kwargs)

        err = "No single or multi search defined for {}".format
        raise pytan.exceptions.HandlerError(err(objtype))

    @pytan.utils.func_timing
    def get_all(self, objtype, **kwargs):
        """Get all objects of a type

        Parameters
        ----------
        objtype : string
            type of object to get

        See Also
        --------
        :data:`pytan.constants.GET_OBJ_MAP` : maps objtype to supported 'search' keys
        """
        obj_map = pytan.utils.get_obj_map(objtype)
        api_obj_all = pytan.utils.get_taniumpy_obj(obj_map['all'])()
        found = self._find(api_obj_all, **kwargs)
        return found

    # BEGIN PRIVATE METHODS
    @pytan.utils.func_timing
    def _add(self, api_object, **kwargs):
        """Wrapper for interfacing with :func:`taniumpy.session.Session.add`"""
        try:
            search_str = '; '.join([str(x) for x in api_object])
        except:
            search_str = api_object
        self.mylog.debug("Adding object {}".format(search_str))

        if 'suppress_object_list' not in kwargs:
            kwargs['suppress_object_list'] = 1

        try:
            added_obj = self.session.add(api_object, **kwargs)
        except Exception as e:
            self.mylog.error(e)
            err = "Error while trying to add object {}!!".format
            raise pytan.exceptions.HandlerError(err(search_str))

        pytan.utils.log_session_communication(self)

        try:
            added_obj = self._find(added_obj)
        except Exception as e:
            self.mylog.error(e)
            err = "Error while trying to find recently added object {}!!".format
            raise pytan.exceptions.HandlerError(err(search_str))

        self.mylog.debug("Added object {}".format(added_obj))
        return added_obj

    @pytan.utils.func_timing
    def _find(self, api_object, **kwargs):
        """Wrapper for interfacing with :func:`taniumpy.session.Session.find`"""
        try:
            search_str = '; '.join([str(x) for x in api_object])
        except:
            search_str = api_object
        self.mylog.debug("Searching for {}".format(search_str))

        if 'suppress_object_list' not in kwargs:
            kwargs['suppress_object_list'] = 1

        try:
            found = self.session.find(api_object, **kwargs)
        except Exception as e:
            self.mylog.error(e)
            err = "No results found searching for {}!!".format
            raise pytan.exceptions.HandlerError(err(search_str))

        if pytan.utils.empty_obj(found):
            err = "No results found searching for {}!!".format
            raise pytan.exceptions.HandlerError(err(search_str))

        self.mylog.debug("Found {}".format(found))
        return found

    def _get_multi(self, obj_map, **kwargs):
        """Find multiple item wrapper using :func:`_find`"""
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # create a list object to append our searches to
        api_obj_multi = pytan.utils.get_taniumpy_obj(obj_map['multi'])()

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if pytan.utils.is_list(v):
                for i in v:
                    api_obj_single = pytan.utils.get_taniumpy_obj(obj_map['single'])()
                    setattr(api_obj_single, k, i)
                    api_obj_multi.append(api_obj_single)
            else:
                api_obj_single = pytan.utils.get_taniumpy_obj(obj_map['single'])()
                setattr(api_obj_single, k, v)
                api_obj_multi.append(api_obj_single)

        # find the multi list object
        found = self._find(api_obj_multi, **kwargs)
        return found

    def _get_single(self, obj_map, **kwargs):
        """Find single item wrapper using :func:`_find`"""
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # we create a list object to append our single item searches to
        if obj_map.get('allfix', ''):
            found = pytan.utils.get_taniumpy_obj(obj_map['allfix'])()
        else:
            found = pytan.utils.get_taniumpy_obj(obj_map['all'])()

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if pytan.utils.is_list(v):
                for i in v:
                    for x in self._single_find(obj_map, k, i, **kwargs):
                        found.append(x)
            else:
                for x in self._single_find(obj_map, k, v, **kwargs):
                    found.append(x)

        return found

    def _single_find(self, obj_map, k, v, **kwargs):
        """Wrapper for single item searches interfacing with :func:`taniumpy.session.Session.find`"""
        found = []
        api_obj_single = pytan.utils.get_taniumpy_obj(obj_map['single'])()
        setattr(api_obj_single, k, v)
        obj_ret = self._find(api_obj_single, **kwargs)
        if getattr(obj_ret, '_list_properties', ''):
            for i in obj_ret:
                found.append(i)
        else:
            found.append(obj_ret)
        return found

    def _get_sensor_defs(self, defs):
        """Uses :func:`get` to update a definition with a sensor object"""
        s_obj_map = pytan.constants.GET_OBJ_MAP['sensor']
        search_keys = s_obj_map['search']

        for d in defs:
            def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

            # get the sensor object
            if 'sensor_obj' not in d:
                d['sensor_obj'] = self.get('sensor', **def_search)[0]
        return defs

    def _get_package_def(self, d):
        """Uses :func:`get` to update a definition with a package object"""
        s_obj_map = pytan.constants.GET_OBJ_MAP['package']
        search_keys = s_obj_map['search']

        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        # get the package object
        if 'package_obj' not in d:
            d['package_obj'] = self.get('package', **def_search)[0]
        return d

    def _export_class_BaseType(self, obj, export_format, **kwargs): # noqa
        """Handles exporting :class:`taniumpy.object_types.base.BaseType`"""
        # run the handler that is specific to this export_format, if it exists
        format_method_str = '_export_format_' + export_format
        format_handler = getattr(self, format_method_str, '')
        if format_handler:
            result = format_handler(obj, **kwargs)
        else:
            err = "{!r} not coded for in Handler!".format
            raise pytan.exceptions.HandlerError(err(export_format))
        return result

    def _export_class_ResultSet(self, obj, export_format, **kwargs): # noqa
        """Handles exporting :class:`taniumpy.object_types.result_set.ResultSet`"""
        """
        ensure kwargs[sensors] has all the sensors that correlate
        to the what_hash of each column, but only if header_add_sensor=True
        needed for: ResultSet.write_csv(header_add_sensor=True)
        """
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
            raise pytan.exceptions.HandlerError(err(export_format))
        return result

    def _export_format_csv(self, obj, **kwargs):
        """Handles exporting format: CSV"""
        if not hasattr(obj, 'write_csv'):
            err = "{!r} has no write_csv() method!".format
            raise pytan.exceptions.HandlerError(err(obj))
        out = io.BytesIO()
        if getattr(obj, '_list_properties', ''):
            result = obj.write_csv(out, list(obj), **kwargs)
        else:
            result = obj.write_csv(out, obj, **kwargs)
        result = out.getvalue()
        return result

    def _export_format_json(self, obj, **kwargs):
        """Handles exporting format: JSON"""
        if not hasattr(obj, 'to_json'):
            err = "{!r} has no to_json() method!".format
            raise pytan.exceptions.HandlerError(err(obj))
        result = obj.to_json(jsonable=obj, **kwargs)
        return result

    def _export_format_xml(self, obj, **kwargs):
        """Handles exporting format: XML"""
        if not hasattr(obj, 'toSOAPBody'):
            err = "{!r} has no toSOAPBody() method!".format
            raise pytan.exceptions.HandlerError(err(obj))
        result = obj.toSOAPBody(**kwargs)
        return result

    def _derive_server_version(self):
        self.server_version = self.session.get_server_version()

    @pytan.utils.func_timing
    def _deploy_action(self, run=False, get_results=True, **kwargs):
        """Deploy an action and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API, and as such is not meant for human consumption. Use :func:`deploy_action` instead.

        Parameters
        ----------
        package_def : dict
            definition that describes a package
        action_filter_defs : str, dict, list of str or dict, optional
            action filter definitions
        action_option_defs : dict, list of dict, optional
            action filter option definitions
        start_seconds_from_now : int, optional
            start action N seconds from now
        expire_seconds : int, optional
            expire action N seconds from now, will be derived from package if not supplied
        run : bool, optional
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise pytan.exceptions.RunFalse -- does not deploy the action
            * True: actually deploy the action
        get_results : bool, optional
            * True: wait for result completion after deploying action
            * False: just deploy the action and return the object in `ret`

        Returns
        -------
        ret : dict, containing:
            * `action_object` : :class:`taniumpy.object_types.action.Action`
            * `action_results` : :class:`taniumpy.object_types.result_set.ResultSet`
            * `action_progress_human` : str, progress map in human form
            * `action_progress_map` : dict, progress map in dictionary form
            * `pre_action_question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        Examples
        --------
        >>> # example of dict for `package_def`
        >>> package_def = {'name': 'PackageName1', 'params':{'param1': 'value1'}}

        >>> # example of str for `action_filter_defs`
        >>> action_filter_defs = 'Sensor1'

        >>> # example of dict for `action_filter_defs`
        >>> action_filter_defs = {
        ... 'name': 'Sensor1',
        ...     'filter': {
        ...         'operator': 'RegexMatch',
        ...         'not_flag': 0,
        ...         'value': '.*'
        ...     },
        ...     'options': {'and_flag': 1}
        ... }

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`pytan.constants.OPTION_MAPS` : valid option dictionaries for options
        """

        # ARGUMENT PROCESSING!
        action_filter_defs = pytan.utils.parse_defs(
            defname='action_filter_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=True,
            **kwargs
        )

        action_option_defs = pytan.utils.parse_defs(
            defname='action_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )

        package_def = pytan.utils.parse_defs(
            defname='package_def',
            deftypes=['dict()'],
            empty_ok=False,
            **kwargs
        )

        start_seconds_from_now = pytan.utils.get_kwargs_int(
            'start_seconds_from_now', 0, **kwargs
        )

        expire_seconds = pytan.utils.get_kwargs_int('expire_seconds', **kwargs)

        comment_default = 'Created by PyTan v{}'.format(pytan.__version__)
        issue_seconds_default = 0
        distribute_seconds_default = 0

        comment = kwargs.get('comment', comment_default)
        issue_seconds = kwargs.get('issue_seconds', issue_seconds_default)
        distribute_seconds = kwargs.get('distribute_seconds', distribute_seconds_default)

        # do basic validation of our defs
        pytan.utils.val_sensor_defs(action_filter_defs)
        pytan.utils.val_package_def(package_def)

        # get the objects that are in our defs and add them as
        # d['sensor_obj'] / d['package_obj']
        action_filter_defs = self._get_sensor_defs(action_filter_defs)
        package_def = self._get_package_def(package_def)

        """
        ask the question that pertains to the action filter, save the result as CSV,
        and raise a RunFalse exception

        this will be used to get a count for how many servers should be seen
        in the deploy action resultdata as 'completed'

        We supply Computer Name and Online = True as the sensors if run is
        False, then exit out after asking the question to allow the user
        to verify the results by looking at the CSV file

        The action filter for the deploy action is used as the question
        filter

        note from jwk: passed_count == the number of machines that pass the filter and
        therefore the number that should take the action
        """
        if not run:
            pre_action_sensors = ['Computer Name', 'Online, that =:True']
            pre_action_sensor_defs = pytan.utils.dehumanize_sensors(pre_action_sensors)
            pre_action_question = self._ask_manual(
                sensor_defs=pre_action_sensor_defs,
                question_filter_defs=action_filter_defs,
                question_option_defs=action_option_defs,
                hide_no_results_flag=1,
            )

            passed_count = pre_action_question['question_results'].passed
            m = (
                "Number of systems that match action filter (passed_count): {}"
            ).format
            self.mylog.debug(m(passed_count))

            if passed_count == 0:
                m = "Number of systems that match the action filters provided is zero!"
                raise pytan.exceptions.HandlerError(m)

            report_path, result = self.export_to_report_file(
                pre_action_question['question_results'],
                'csv',
                prefix='VERIFY_BEFORE_DEPLOY_ACTION_',
                **kwargs
            )

            m = (
                "'Run' is not True!!\n"
                "View and verify the contents of {} (length: {} bytes)\n"
                "Re-run this deploy action with run=True after verifying"
            ).format
            raise pytan.exceptions.RunFalse(m(report_path, len(result)))

        # BUILD THE OBJECT TO BE ADDED
        param_objlist = pytan.utils.build_param_objlist(
            obj=package_def['package_obj'],
            user_params=package_def['params'],
            delim='',
            derive_def=False,
            empty_ok=False,
        )

        '''Branch out logic for 6.2 vs 6.5 here:

         * For 6.2:
           * we need to add an Action object
           * do not encapsulate it in a list object
           * force a start time to be specified, if none is specified the action shows up as expired

         * For 6.5:
           * we need to add a SavedAction object
           * the server creates the actual Action object for us
           * to emulate what the console does, encapsulate the SavedAction in a SavedActionList
           * start time does not need to be specified
        '''
        # if server_version is None / "Not yet determined!" try to fetch the version
        if not self.server_version or self.server_version == "Not yet determined!":
            self.server_version = self.session.get_server_version()

        if self.server_version.startswith('6.2'):
            objtype = taniumpy.Action
            objlisttype = None
            force_start_time = True
        elif self.server_version.startswith('6.5'):
            objtype = taniumpy.SavedAction
            objlisttype = taniumpy.SavedActionList
            force_start_time = False
        # we will assume 6.2 if server_version is "Unable to determine"
        elif self.server_version == "Unable to determine":
            objtype = taniumpy.Action
            objlisttype = None
            force_start_time = True
        # default to 6.5 logic for all unknowns
        else:
            objtype = taniumpy.SavedAction
            objlisttype = taniumpy.SavedActionList
            force_start_time = False

        m = "DEPLOY_ACTION objtype: {}, objlisttype: {}, force_start_time: {}, version: {}".format
        self.mylog.debug(m(objtype, objlisttype, force_start_time, self.server_version))

        add_obj = objtype()
        add_obj.package_spec = taniumpy.PackageSpec()
        add_obj.id = -1
        add_obj.name = "API Deploy {}".format(package_def['package_obj'].name)
        add_obj.issue_seconds = issue_seconds
        add_obj.distribute_seconds = distribute_seconds
        add_obj.comment = comment
        add_obj.status = 0
        add_obj.start_time = ''
        add_obj.end_time = ''
        add_obj.public_flag = 0
        add_obj.policy_flag = 0
        add_obj.approved_flag = 0
        add_obj.issue_count = 0

        if param_objlist:
            add_obj.package_spec.source_id = package_def['package_obj'].id
            add_obj.package_spec.parameters = param_objlist
        else:
            add_obj.package_spec.id = package_def['package_obj'].id
            add_obj.package_spec.name = package_def['package_obj'].name

        if action_filter_defs or action_option_defs:
            targetgroup_obj = pytan.utils.build_group_obj(action_filter_defs, action_option_defs)
            add_obj.target_group = targetgroup_obj
        else:
            targetgroup_obj = None

        if 'start_seconds_from_now' in kwargs:
            if kwargs.get('start_seconds_from_now', 0) not in [None, 0]:
                add_obj.start_time = pytan.utils.seconds_from_now(start_seconds_from_now)

        if force_start_time and not add_obj.start_time:
            if start_seconds_from_now in [None, 0]:
                start_seconds_from_now = 1
            add_obj.start_time = pytan.utils.seconds_from_now(start_seconds_from_now)

        if package_def['package_obj'].expire_seconds:
            add_obj.expire_seconds = package_def['package_obj'].expire_seconds

        if expire_seconds:
            add_obj.expire_seconds = expire_seconds

        if objlisttype:
            add_objs = objlisttype()
            add_objs.append(add_obj)
            added_objs = self._add(add_objs)
            added_obj = added_objs[0]

            m = "DEPLOY_ACTION ADDED: {}, ID: {}".format
            self.mylog.debug(m(added_obj.__class__.__name__, added_obj.id))

            action_obj = self.get('action', id=added_obj.last_action.id)[0]
        else:
            added_obj = None
            action_obj = self._add(add_obj)

        m = "DEPLOY_ACTION ADDED: {}, ID: {}".format
        self.mylog.debug(m(action_obj.__class__.__name__, action_obj.id))

        action_info = self.get_result_info(action_obj)

        m = "DEPLOY_ACTION ADDED: Question for Action Results, ID: {}".format
        self.mylog.debug(m(action_info.question_id))

        ret = {
            'saved_action_object': added_obj,
            'action_object': action_obj,
            'package_object': package_def['package_obj'],
            'group_object': targetgroup_obj,
            'action_info': action_info,
            'poller_object': pytan.pollers.ActionPoller(self, action_obj, **kwargs),
            'action_results': None,
            'action_result_map': None,
            'poller_success': None,
        }

        if get_results:
            ret['poller_success'] = ret['poller_object'].run(**kwargs)
            ret['action_results'] = ret['poller_object'].result_data
            ret['action_result_map'] = ret['poller_object'].result_map

        return ret

    @pytan.utils.func_timing
    def _ask_manual(self, get_results=True, **kwargs):
        """Ask a manual question using definitions and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API,
        and as such is not meant for human consumption. Use :func:`ask_manual` instead.

        Parameters
        ----------
        sensor_defs : str, dict, list of str or dict
            sensor definitions
        question_filter_defs : dict, list of dict, optional
            question filter definitions
        question_option_defs : dict, list of dict, optional
            question option definitions
        get_results : bool, optional
            * True: wait for result completion after asking question
            * False: just ask the question and return it in `ret`

        Returns
        -------
        ret : dict, containing:
            * `question_object` : :class:`taniumpy.object_types.question.Question`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        Examples
        --------
        >>> # example of str for sensor_defs
        >>> sensor_defs = 'Sensor1'

        >>> # example of dict for sensor_defs
        >>> sensor_defs = {
        ... 'name': 'Sensor1',
        ...     'filter': {
        ...         'operator': 'RegexMatch',
        ...         'not_flag': 0,
        ...         'value': '.*'
        ...     },
        ...     'params': {'key': 'value'},
        ...     'options': {'and_flag': 1}
        ... }

        >>> # example of dict for question_filter_defs
        >>> question_filter_defs = {
        ...     'operator': 'RegexMatch',
        ...     'not_flag': 0,
        ...     'value': '.*'
        ... }

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`pytan.constants.OPTION_MAPS` : valid option dictionaries for options
        """

        # get our defs from kwargs and churn them into what we want
        sensor_defs = pytan.utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=True,
            **kwargs
        )

        q_filter_defs = pytan.utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )

        q_option_defs = pytan.utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )

        max_age_seconds = int(kwargs.get('max_age_seconds', 600))

        # do basic validation of our defs
        pytan.utils.val_sensor_defs(sensor_defs)
        pytan.utils.val_q_filter_defs(q_filter_defs)

        # get the sensor objects that are in our defs and add them as
        # d['sensor_obj']
        sensor_defs = self._get_sensor_defs(sensor_defs)
        q_filter_defs = self._get_sensor_defs(q_filter_defs)

        # build a SelectList object from our sensor_defs
        selectlist_obj = pytan.utils.build_selectlist_obj(sensor_defs)

        # build a Group object from our question filters/options
        group_obj = pytan.utils.build_group_obj(q_filter_defs, q_option_defs)

        # build a Question object from selectlist_obj and group_obj
        add_obj = pytan.utils.build_manual_q(selectlist_obj, group_obj)

        add_obj.max_age_seconds = max_age_seconds

        # add our Question and get a Question ID back
        added_obj = self._add(add_obj)

        m = "Question Added, ID: {}, query text: {!r}, expires: {}".format
        self.mylog.debug(m(added_obj.id, added_obj.query_text, added_obj.expiration))

        ret = {
            'question_object': added_obj,
            'poller_object': pytan.pollers.QuestionPoller(self, added_obj, **kwargs),
            'question_results': None,
            'poller_success': None,
        }

        if get_results:
            # poll the Question ID returned above to wait for results
            ret['poller_success'] = ret['poller_object'].run(**kwargs)

            # get the results
            ret['question_results'] = self.get_result_data(added_obj, **kwargs)

            # add the sensors from this question to the ResultSet object for reporting
            ret['question_results'].sensors = [x['sensor_obj'] for x in sensor_defs]

        return ret
