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
import time
import json

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import taniumpy
from pytan import utils
from pytan import constants
from pytan.utils import HandlerError
from pytan.utils import RunFalse

mylog = logging.getLogger("handler")
actionlog = logging.getLogger("action_progress")


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
    loglevel : int, optional
        0 should not print anything, 1 and higher will print more
    debugformat : bool, optional
        False use one line logformat, True use two lines

    Notes
    -----
      * port 444 is the default SOAP port
      * port 443 forwards /soap/ URLs to the SOAP port
      * Use port 444 if you have direct access to it

    See Also
    --------
    :data:`pytan.constants.LOG_LEVEL_MAPS` : maps a given `loglevel` to respective logger names and their logger levels
    :data:`pytan.constants.INFO_FORMAT` : debugformat=False
    :data:`pytan.constants.DEBUG_FORMAT` : debugformat=True
    """

    def __init__(self, username, password, host, port="444", loglevel=0,
                 debugformat=False, **kwargs):
        super(Handler, self).__init__()

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
        self.session = taniumpy.Session(host, port)
        self.session.authenticate(username, password)

    def __str__(self):
        str_tpl = "Handler for {}".format
        ret = str_tpl(self.session)
        return ret

    def ask(self, **kwargs):
        """Ask a type of question and get the results back

        Parameters
        ----------
        qtype : str
            type of question to ask: saved_question, manual, or manual_human

        Returns
        -------
        result : dict, containing:
            * `question_object` : one of the following depending on `qtype`
                * :class:`taniumpy.object_types.question.Question`
                * :class:`taniumpy.object_types.saved_question.SavedQuestion`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        See Also
        --------
        :data:`pytan.constants.Q_OBJ_MAP` : maps qtype to a method in Handler()
        """
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
        """Ask a saved question and get the results back

        Parameters
        ----------
        id : int, list of int, optional
            id of saved question to ask
        name : str, list of str
            name of saved question

        Returns
        -------
        ret : dict, containing
            * `question_object` : :class:`taniumpy.object_types.saved_question.SavedQuestion`
            * `question_results` : :class:`taniumpy.object_types.result_set.ResultSet`

        Notes
        -----
        id or name must be supplied

        See Also
        --------
        :data:`pytan.constants.ASK_KWARGS`: list of kwargs that can be passed to :class:`taniumpy.question_asker.QuestionAsker`
        """
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
        asker = taniumpy.QuestionAsker(self.session, q_obj, **ask_kwargs)
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
        """Ask a manual question using definitions and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API,
        and as such is not meant for human consumption. Use :func:`ask_manual_human` instead.

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
        :data:`pytan.constants.ASK_KWARGS` : list of kwargs that can be passed to :class:`taniumpy.question_asker.QuestionAsker`
        """

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
            asker = taniumpy.QuestionAsker(self.session, q_obj, **ask_kwargs)
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
        """Ask a manual question using human strings and get the results back

        This method takes a string or list of strings and parses them into
        their corresponding definitions needed by :func:`ask_manual`

        Parameters
        ----------
        sensors : str, list of str
            sensors (columns) to include in question
        question_filters : str, list of str, optional
            filters that apply to the whole question
        question_options : str, list of str, optional
            options that apply to the whole question
        get_results : bool, optional
            True: wait for result completion after asking question
            False: just ask the question and return it in result

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
        >>> sensors = 'Sensor1{key:value}, that contains example text'

        >>> # example of str for `sensors` with params and filter and options
        >>> sensors = (
        ...     'Sensor1{key:value}, that contains example text,'
        ...     'opt:ignore_case, opt:max_data_age:60'
        ... )

        >>> # example of str for question_filters
        >>> question_filters = 'Sensor2, that contains example test'

        >>> # example of list of str for question_options
        >>> question_options = ['max_data_age:3600', 'and']

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`pytan.constants.OPTION_MAPS` : valid option dictionaries for options
        :data:`pytan.constants.ASK_KWARGS` : list of kwargs that can be passed to :class:`taniumpy.question_asker.QuestionAsker`
        """

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

    def load_taniumpy_from_json(self, json_file):
        """Opens a json file and parses it into an taniumpy object

        Parameters
        ----------
        json_file : str
            path to JSON file that describes an API object

        Returns
        -------
        obj : :class:`taniumpy.object_types.base.BaseType`
            TaniumPy object converted from json file
        """
        try:
            fh = open(json_file)
        except Exception as e:
            m = "Unable to open json_file {!r}, {}".format
            raise HandlerError(m(json_file, e))

        howto_m = (
            "Use get_${OBJECT_TYPE}.py with --include-type and "
            "--no-explode-json to export a valid JSON file that can be used "
            "for importing"
        )

        try:
            json_dict = json.load(fh)
        except:
            m = "Unable to parse json_file {!r}, {}\n{}".format
            raise HandlerError(m(json_file, e, howto_m))

        if '_type' not in json_dict:
            m = "Missing '_type' key in JSON loaded dictionary!\n{}".format
            raise HandlerError(m(howto_m))

        try:
            obj = taniumpy.BaseType.from_jsonable(json_dict)
        except Exception as e:
            m = (
                "Unable to parse json_file {!r} into an API {} object\n"
                "Exception from API.from_jsonable(): {}\n{}"
            ).format
            raise HandlerError(m(json_file, json_dict['_type'], e, howto_m))
        return obj

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
        obj_map = utils.get_obj_map(objtype)
        create_json_ok = obj_map['create_json']
        if not create_json_ok:
            json_createable = ', '.join([
                x for x, y in constants.GET_OBJ_MAP.items() if y['create_json']
            ])
            m = (
                "{} is not a json createable object! Supported objects: {}"
            ).format
            raise HandlerError(m(objtype, json_createable))

        add_obj = self.load_taniumpy_from_json(json_file)

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
            ret = getattr(taniumpy, obj_map['allfix'])()
        else:
            ret = getattr(taniumpy, obj_map['all'])()

        for x in obj_list:
            try:
                list_obj = self.session.add(x)
            except Exception as e:
                m = (
                    "Failure while importing {}: {}\nJSON Dump of object: {}"
                ).format
                raise HandlerError(m(x, e, x.to_json(x)))

            list_obj = self.session.find(list_obj)
            m = "New {} (ID: {}) created successfully!".format
            mylog.info(m(list_obj, getattr(list_obj, 'id', 'Unknown')))

            ret.append(list_obj)
        return ret

    def create_sensor(self):
        """Create a sensor object

        Warnings
        --------
        Not currently supported, too complicated to add.
        Use :func:`create_from_json` instead for this object type!

        Raises
        ------
        HandlerError : :exc:`pytan.utils.HandlerError`
        """
        m = (
            "Sensor creation not supported via PyTan as of yet, too complex\n"
            "Use create_sensor_from_json() instead!"
        )
        raise HandlerError(m)

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
            verify_expire_seconds=600):
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

        Returns
        -------
        package_obj : :class:`taniumpy.object_types.package_spec.PackageSpec`
            TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filters for verify_filters
        :data:`pytan.constants.OPTION_MAPS` : valid options for verify_filter_options
        """

        # bare minimum arguments for new package: name, command
        add_package_obj = taniumpy.PackageSpec()
        add_package_obj.name = name
        if display_name:
            add_package_obj.display_name = display_name
        add_package_obj.command = command
        add_package_obj.command_timeout = command_timeout_seconds
        add_package_obj.expire_seconds = expire_seconds

        # VERIFY FILTERS
        if verify_filters:
            verify_filter_defs = utils.dehumanize_question_filters(
                verify_filters
            )
            verify_option_defs = utils.dehumanize_question_options(
                verify_filter_options
            )
            verify_filter_defs = self._get_sensor_defs(verify_filter_defs)
            add_verify_group = utils.build_group_obj(
                verify_filter_defs, verify_option_defs
            )
            verify_group = self.session.add(add_verify_group)
            # this didn't work:
            # add_package_obj.verify_group = verify_group
            add_package_obj.verify_group_id = verify_group.id
            add_package_obj.verify_expire_seconds = verify_expire_seconds

        # PARAMETERS
        if parameters_json_file:
            try:
                pd = json.load(open(parameters_json_file))
            except Exception as e:
                m = (
                    "Failed to load JSON parameter file {!r}, error {!r}!!\n"
                    "Refer to doc/example_of_all_package_parameters.json "
                    "file for examples of each parameter type"
                ).format
                raise HandlerError(m(parameters_json_file, e))
            try:
                pd_params = pd['parameters']
            except:
                m = (
                    "JSON parameter file {!r} is missing a 'parameters' "
                    "list!!\n"
                    "Refer to doc/example_of_all_package_parameters.json "
                    "file for examples of each parameter type"
                ).format
                raise HandlerError(m(parameters_json_file))

            for pd_param in pd_params:
                try:
                    pd_key = pd_param['key']
                except:
                    m = (
                        "JSON parameter file {!r} is missing a 'key' "
                        "in the parameter {!r}!!\n"
                        "Refer to doc/example_of_all_package_parameters.json "
                        "file for examples of each parameter type"
                    ).format
                    raise HandlerError(m(parameters_json_file, pd_param))
                if pd_key not in command:
                    m = (
                        "command {!r} is missing the parameter key '{}' "
                        "referenced in the JSON parameter file {!r}!!\n"
                        "Ensure all parameters are referenced in the command"
                    ).format
                    raise HandlerError(m(
                        command, pd_key, parameters_json_file
                    ))

            add_package_obj.parameter_definition = json.dumps(pd)

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

        package_obj = self.session.add(add_package_obj)
        package_obj = self.session.find(package_obj)
        m = "New package {!r} created with ID {!r}, command: {!r}".format
        mylog.info(m(package_obj.name, package_obj.id, package_obj.command))
        return package_obj

    def create_group(self, groupname, filters=[], filter_options=[]):
        """Create a group object

        Parameters
        ----------
        groupname : str
            name of group to create
        filters : str or list of str, optional
            each string must describe a filter
        filter_options : str or list of str, optional
            each string must describe an option for `filters`

        Returns
        -------
        group_obj : :class:`taniumpy.object_types.group.Group`
            TaniumPy object added to Tanium SOAP Server

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filters for filters
        :data:`pytan.constants.OPTION_MAPS` : valid options for filter_options
        """

        filter_defs = utils.dehumanize_question_filters(filters)
        filter_defs = self._get_sensor_defs(filter_defs)
        option_defs = utils.dehumanize_question_options(filter_options)
        add_group_obj = utils.build_group_obj(filter_defs, option_defs)
        add_group_obj.name = groupname
        group_obj = self.session.add(add_group_obj)
        group_obj = self.session.find(group_obj)
        m = "New group {!r} created with ID {!r}, filter text: {!r}".format
        mylog.info(m(group_obj.name, group_obj.id, group_obj.text))
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
        metadatalist_obj = utils.build_metadatalist_obj(
            properties, 'TConsole.User.Property',
        )
        add_user_obj = taniumpy.User()
        add_user_obj.name = username
        add_user_obj.roles = rolelist_obj
        add_user_obj.metadata = metadatalist_obj
        user_obj = self.session.add(add_user_obj)
        m = "New user {!r} created with ID {!r}, roles: {!r}".format
        mylog.info(m(
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

        metadatalist_obj = utils.build_metadatalist_obj(
            properties, 'TConsole.WhitelistedURL',
        )
        add_url_obj = taniumpy.WhiteListedUrl()
        add_url_obj.url_regex = url
        add_url_obj.download_seconds = download_seconds
        add_url_obj.metadata = metadatalist_obj
        url_obj = self.session.add(add_url_obj)
        url_obj = self.session.find(url_obj)
        m = "New Whitelisted URL {!r} created with ID {!r}".format
        mylog.info(m(url_obj.url_regex, url_obj.id))
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
        obj_map = utils.get_obj_map(objtype)
        delete_ok = obj_map['delete']
        if not delete_ok:
            deletable = ', '.join([
                x for x, y in constants.GET_OBJ_MAP.items() if y['delete']
            ])
            m = "{} is not a deletable object! Deletable objects: {}".format
            raise HandlerError(m(objtype, deletable))
        objs_to_del = self.get(objtype, **kwargs)
        deleted_objects = []
        for obj_to_del in objs_to_del:
            del_obj = self.session.delete(obj_to_del)
            deleted_objects.append(del_obj)
            m = "Deleted {!r}".format
            mylog.info(m(str(del_obj)))
        return deleted_objects

    def deploy_action(self, run=False, get_results=True, **kwargs):
        """Deploy an action and get the results back

        This method requires in-depth knowledge of how filters and options are created in the API, and as such is not meant for human consumption. Use :func:`deploy_action_human` instead.

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
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise RunFalse -- does not deploy the action
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

        """
        ask the question that pertains to the action filter
        this will be used to get a count for how many servers should be seen
        in the deploy action resultdata as 'completed'

        We supply Computer Name and Online = True as the sensors if run is
        False, then exit out after asking the question to allow the user
        to verify the contents

        If run is True we just use Online = True for the sensor

        The action filter for the deploy action is used as the question
        filter in both cases
        """
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

        """ note from jwk:
        passed_count == the number of machines that pass the filter and
        therefore the number that should take the action
        """
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

        a_package_obj = taniumpy.PackageSpec()
        if param_objlist:
            a_package_obj.source_id = package_obj.id
            a_package_obj.parameters = param_objlist
        else:
            a_package_obj.name = package_obj.name

        add_action_obj = taniumpy.Action()
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
        """Deploy an action and get the results back

        This method takes a string or list of strings and parses them into
        their corresponding definitions needed by :func:`deploy_action`

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
            * False: just ask the question that pertains to verify action, export the results to CSV, and raise RunFalse -- does not deploy the action
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
        >>> # example of str for `package`
        >>> package = 'Package1'

        >>> # example of str for `package` with params
        >>> package = 'Package1{key:value}'

        >>> # example of str for `action_filters` with params and filter for sensors
        >>> action_filters = 'Sensor1{key:value}, that contains example text'

        >>> # example of list of str for `action_options`
        >>> action_options = ['max_data_age:3600', 'and']

        See Also
        --------
        :data:`pytan.constants.FILTER_MAPS` : valid filter dictionaries for filters
        :data:`pytan.constants.OPTION_MAPS` : valid option dictionaries for options
        """
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
        """Checks the results of a deploy action job and waits for completion

        Parameters
        ----------
        action_id : int
            id of deploy action to get results for and wait on completion
        passed_count : int, optional
            the number of servers that must equate "completed" in order for deploy action to be recognized as completed

        Returns
        -------
        ret : dict, containing:
            * `action_object` : :class:`taniumpy.object_types.action.Action`
            * `action_results` : :class:`taniumpy.object_types.result_set.ResultSet`
            * `action_progress_human` : str, progress map in human form
            * `action_progress_map` : dict, progress map in dictionary form

        See Also
        --------
        :data:`pytan.constants.ACTION_RESULT_STATUS` : maps the values in *Action Statuses* columns to success/completed/failed/etc
        """
        action_obj = self.get('action', id=action_id)[0]
        ps = action_obj.package_spec
        """
        A package_spec has to have a verify_group defined on it in order
        for deploy action verification to trigger. That can be only done
        at package_spec create or update time
        """
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
        """Exports a python API object to a given export format

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            TaniumPy object to export
        export_format : str
            the number of servers that must equate "completed" in order for deploy action to be recognized as completed
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

        export_maps = constants.EXPORT_MAPS

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
        """Exports a python API object to a file

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType` or :class:`taniumpy.object_types.result_set.ResultSet`
            TaniumPy object to export
        export_format : str
            the number of servers that must equate "completed" in order for deploy action to be recognized as completed
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
        obj_map = utils.get_obj_map(objtype)
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
                if not utils.is_list(v):
                    v = [v]
                for aobj in all_objs:
                    if not getattr(aobj, k) in v:
                        continue
                    return_objs.append(aobj)
            if not return_objs:
                err = "No results found searching for {} with {}!!".format
                raise HandlerError(err(objtype, kwargs))
            return return_objs

        # if api supports filtering for this object,
        # but no filters supplied in kwargs, raise
        if not any(api_kwattrs):
            err = "Getting a {} requires at least one filter: {}".format
            raise HandlerError(err(objtype, api_attrs))

        # if there is a multi in obj_map, that means we can pass a list
        # type to the taniumpy. the list will have an entry for each api_kw
        if obj_map['multi']:
            return self._get_multi(obj_map, **kwargs)

        # if there is a single in obj_map but not multi, that means
        # we have to find each object individually
        elif obj_map['single']:
            return self._get_single(obj_map, **kwargs)

        err = "No single or multi search defined for {}".format
        raise HandlerError(err(objtype))

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
        obj_map = utils.get_obj_map(objtype)
        api_obj_all = getattr(taniumpy, obj_map['all'])()
        found = self._find(api_obj_all, **kwargs)
        return found

    def get_result_data(self, obj, aggregate=False, **kwargs):
        """Get the result data for a python API object

        This method issues a GetResultData command to the SOAP api for `obj`. GetResultData returns the columns and rows that are currently available for `obj`.

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            object to get result data for
        aggregate : bool, optional
            * False: get all the data
            * True: get just the aggregate data (row counts of matches)

        Returns
        -------
        rd : :class:`taniumpy.object_types.result_set.ResultSet`
            The return of GetResultData for `obj`
        """
        # do a getresultinfo to ensure fresh data is available for
        # getresultdata
        self.get_result_info(obj, **kwargs)
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
        # do a getresultdata
        if aggregate:
            rd = self.session.getResultData(
                obj, row_counts_only_flag=1, **kwargs
            )
        else:
            rd = self.session.getResultData(obj, **kwargs)
        return rd

    def get_result_info(self, obj, **kwargs):
        """Get the result info for a python API object

        This method issues a GetResultInfo command to the SOAP api for `obj`. GetResultInfo returns information about how many servers have passed the `obj`, total number of servers, and so on.

        Parameters
        ----------
        obj : :class:`taniumpy.object_types.base.BaseType`
            object to get result data for

        Returns
        -------
        ri : :class:`taniumpy.object_types.result_info.ResultInfo`
            The return of GetResultData for `obj`
        """
        ri = self.session.getResultInfo(obj, **kwargs)
        return ri

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
        action_stop_obj = self.session.add(add_action_stop_obj)
        m = (
            'Action stopped successfully, ID of action stop: {}'
        ).format
        mylog.debug(m(action_stop_obj.id))
        return action_stop_obj

    # BEGIN PRIVATE METHODS
    def _find(self, api_object, **kwargs):
        """Wrapper for interfacing with :func:`taniumpy.session.Session.find`"""
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
        """Find multiple item wrapper using :func:`_find`"""
        api_attrs = obj_map['search']
        api_kwattrs = [kwargs.get(x, '') for x in api_attrs]
        api_kw = {k: v for k, v in zip(api_attrs, api_kwattrs)}

        # create a list object to append our searches to
        api_obj_multi = getattr(taniumpy, obj_map['multi'])()
        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
                for i in v:
                    api_obj_single = getattr(taniumpy, obj_map['single'])()
                    setattr(api_obj_single, k, i)
                    api_obj_multi.append(api_obj_single)
            else:
                api_obj_single = getattr(taniumpy, obj_map['single'])()
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
            found = getattr(taniumpy, obj_map['allfix'])()
        else:
            found = getattr(taniumpy, obj_map['all'])()

        for k, v in api_kw.iteritems():
            if v and k not in obj_map['search']:
                continue  # if we can't search for k, skip

            if not v:
                continue  # if v empty, skip

            if utils.is_list(v):
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
        api_obj_single = getattr(taniumpy, obj_map['single'])()
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
        s_obj_map = constants.GET_OBJ_MAP['sensor']
        search_keys = s_obj_map['search']

        for d in defs:
            def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

            # get the sensor object
            if not 'sensor_obj' in d:
                d['sensor_obj'] = self.get('sensor', **def_search)[0]
        return defs

    def _get_package_def(self, d):
        """Uses :func:`get` to update a definition with a package object"""
        s_obj_map = constants.GET_OBJ_MAP['package']
        search_keys = s_obj_map['search']

        def_search = {s: d.get(s, '') for s in search_keys if d.get(s, '')}

        # get the package object
        if not 'package_obj' in d:
            d['package_obj'] = self.get('package', **def_search)[0]
        return d

    def _export_class_BaseType(self, obj, export_format, **kwargs):
        """Handles exporting :class:`taniumpy.object_types.base.BaseType`"""
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
            raise HandlerError(err(export_format))
        return result

    def _export_format_csv(self, obj, **kwargs):
        """Handles exporting format: CSV"""
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
        """Handles exporting format: JSON"""
        if not hasattr(obj, 'to_json'):
            err = "{!r} has no to_json() method!".format
            raise HandlerError(err(obj))
        result = obj.to_json(jsonable=obj, **kwargs)
        return result

    def _export_format_xml(self, obj, **kwargs):
        """Handles exporting format: XML"""
        if not hasattr(obj, 'toSOAPBody'):
            err = "{!r} has no toSOAPBody() method!".format
            raise HandlerError(err(obj))
        result = obj.toSOAPBody(**kwargs)
        return result
