
pytan.handler module
********************

The main `pytan <pytan#module-pytan>`_ module that provides methods
for programmatic use.


Handler Class
=============

**class pytan.handler.Handler(username, password, host, port='444',
loglevel=0, debugformat=False, **kwargs)**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   Creates a connection to a Tanium SOAP Server on host:port

   :Parameters:
      **username** : str

      ..

         *username* to connect to *host* with

      **password** : str

      ..

         *password* to connect to *host* with

      **host** : str

      ..

         hostname or ip of Tanium SOAP Server

      **port** : int, optional

      ..

         port of Tanium SOAP Server on *host*

      **loglevel** : int, optional

      ..

         0 should not print anything, 1 and higher will print more

      **debugformat** : bool, optional

      ..

         False use one line logformat, True use two lines

   `pytan.constants.LOG_LEVEL_MAPS
      <pytan.constants#pytan.constants.LOG_LEVEL_MAPS>`_
         maps a given *loglevel* to respective logger names and their
         logger levels

      `pytan.constants.INFO_FORMAT
      <pytan.constants#pytan.constants.INFO_FORMAT>`_
         debugformat=False

      `pytan.constants.DEBUG_FORMAT
      <pytan.constants#pytan.constants.DEBUG_FORMAT>`_
         debugformat=True

   -[ Notes ]-

   * port 444 is the default SOAP port

   * port 443 forwards /soap/ URLs to the SOAP port

   * Use port 444 if you have direct access to it


Example: Create a Handler object
--------------------------------

Setup a Handler() object:

::

   >>> import sys
   >>> sys.path.append('/path/to/pytan/')
   >>> import pytan
   >>> handler = pytan.Handler('username', 'password', 'host')

======================================================================


Handler Methods: Questions and Actions
--------------------------------------


Ask a Question
~~~~~~~~~~~~~~

**Handler.ask(**kwargs)**

   Ask a type of question and get the results back

   :Parameters:
      **qtype** : str

      ..

         type of question to ask: saved_question, manual, or
         manual_human

   :Returns:
      **result** : dict, containing:

      ..

         * *question_object* : one of the following depending on
           *qtype*: `taniumpy.object_types.question.Question
           <taniumpy.object_types#taniumpy.object_types.question.Question>`_
           or `taniumpy.object_types.saved_question.SavedQuestion
           <taniumpy.object_types#taniumpy.object_types.saved_question.SavedQuestion>`_

         * *question_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

   `pytan.constants.Q_OBJ_MAP
      <pytan.constants#pytan.constants.Q_OBJ_MAP>`_
         maps qtype to a method in Handler()


Ask a Saved Question
~~~~~~~~~~~~~~~~~~~~

**Handler.ask_saved(**kwargs)**

   Ask a saved question and get the results back

   :Parameters:
      **id** : int, list of int, optional

      ..

         id of saved question to ask

      **name** : str, list of str

      ..

         name of saved question

   :Returns:
      **ret** : dict, containing

      ..

         * *question_object* :
           `taniumpy.object_types.saved_question.SavedQuestion
           <taniumpy.object_types#taniumpy.object_types.saved_question.SavedQuestion>`_

         * *question_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

   `pytan.constants.ASK_KWARGS
      <pytan.constants#pytan.constants.ASK_KWARGS>`_
         list of kwargs that can be passed to
         `taniumpy.question_asker.QuestionAsker
         <taniumpy.question_asker#taniumpy.question_asker.QuestionAsker>`_

   -[ Notes ]-

   id or name must be supplied


Asking a Manual Question
~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.ask_manual(get_results=True, **kwargs)**

   Ask a manual question using definitions and get the results back

   This method requires in-depth knowledge of how filters and options
   are created in the API, and as such is not meant for human
   consumption. Use ``ask_manual_human()`` instead.

   :Parameters:
      **sensor_defs** : str, dict, list of str or dict

      ..

         sensor definitions

      **question_filter_defs** : dict, list of dict, optional

      ..

         question filter definitions

      **question_option_defs** : dict, list of dict, optional

      ..

         question option definitions

      **get_results** : bool, optional

      ..

         * True: wait for result completion after asking question

         * False: just ask the question and return it in *ret*

   :Returns:
      **ret** : dict, containing:

      ..

         * *question_object* :
           `taniumpy.object_types.question.Question
           <taniumpy.object_types#taniumpy.object_types.question.Question>`_

         * *question_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

   `pytan.constants.FILTER_MAPS
      <pytan.constants#pytan.constants.FILTER_MAPS>`_
         valid filter dictionaries for filters

      `pytan.constants.OPTION_MAPS
      <pytan.constants#pytan.constants.OPTION_MAPS>`_
         valid option dictionaries for options

      `pytan.constants.ASK_KWARGS
      <pytan.constants#pytan.constants.ASK_KWARGS>`_
         list of kwargs that can be passed to
         `taniumpy.question_asker.QuestionAsker
         <taniumpy.question_asker#taniumpy.question_asker.QuestionAsker>`_

   -[ Examples ]-

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

**Handler.ask_manual_human(**kwargs)**

   Ask a manual question using human strings and get the results back

   This method takes a string or list of strings and parses them into
   their corresponding definitions needed by ``ask_manual()``

   :Parameters:
      **sensors** : str, list of str

      ..

         sensors (columns) to include in question

      **question_filters** : str, list of str, optional

      ..

         filters that apply to the whole question

      **question_options** : str, list of str, optional

      ..

         options that apply to the whole question

      **get_results** : bool, optional

      ..

         True: wait for result completion after asking question False:
         just ask the question and return it in result

   :Returns:
      **result** : dict, containing:

      ..

         * *question_object* :
           `taniumpy.object_types.question.Question
           <taniumpy.object_types#taniumpy.object_types.question.Question>`_

         * *question_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

   `pytan.constants.FILTER_MAPS
      <pytan.constants#pytan.constants.FILTER_MAPS>`_
         valid filter dictionaries for filters

      `pytan.constants.OPTION_MAPS
      <pytan.constants#pytan.constants.OPTION_MAPS>`_
         valid option dictionaries for options

      `pytan.constants.ASK_KWARGS
      <pytan.constants#pytan.constants.ASK_KWARGS>`_
         list of kwargs that can be passed to
         `taniumpy.question_asker.QuestionAsker
         <taniumpy.question_asker#taniumpy.question_asker.QuestionAsker>`_

   -[ Examples ]-

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


Deploy an Action
~~~~~~~~~~~~~~~~

**Handler.deploy_action(run=False, get_results=True, **kwargs)**

   Deploy an action and get the results back

   This method requires in-depth knowledge of how filters and options
   are created in the API, and as such is not meant for human
   consumption. Use ``deploy_action_human()`` instead.

   :Parameters:
      **package_def** : dict

      ..

         definition that describes a package

      **action_filter_defs** : str, dict, list of str or dict,
      optional

      ..

         action filter definitions

      **action_option_defs** : dict, list of dict, optional

      ..

         action filter option definitions

      **start_seconds_from_now** : int, optional

      ..

         start action N seconds from now

      **expire_seconds** : int, optional

      ..

         expire action N seconds from now, will be derived from
         package if not supplied

      **run** : bool, optional

      ..

         * False: just ask the question that pertains to verify
           action, export the results to CSV, and raise RunFalse --
           does not deploy the action

         * True: actually deploy the action

      **get_results** : bool, optional

      ..

         * True: wait for result completion after deploying action

         * False: just deploy the action and return the object in
           *ret*

   :Returns:
      **ret** : dict, containing:

      ..

         * *action_object* : `taniumpy.object_types.action.Action
           <taniumpy.object_types#taniumpy.object_types.action.Action>`_

         * *action_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * *action_progress_human* : str, progress map in human form

         * *action_progress_map* : dict, progress map in dictionary
           form

         * *pre_action_question_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

   `pytan.constants.FILTER_MAPS
      <pytan.constants#pytan.constants.FILTER_MAPS>`_
         valid filter dictionaries for filters

      `pytan.constants.OPTION_MAPS
      <pytan.constants#pytan.constants.OPTION_MAPS>`_
         valid option dictionaries for options

   -[ Examples ]-

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

**Handler.deploy_action_human(**kwargs)**

   Deploy an action and get the results back

   This method takes a string or list of strings and parses them into
   their corresponding definitions needed by ``deploy_action()``

   :Parameters:
      **package** : str

      ..

         each string must describe a package

      **action_filters** : str, list of str, optional

      ..

         each string must describe a sensor and a filter which limits
         which computers the action will deploy *package* to

      **action_options** : str, list of str, optional

      ..

         options to apply to *action_filters*

      **start_seconds_from_now** : int, optional

      ..

         start action N seconds from now

      **expire_seconds** : int, optional

      ..

         expire action N seconds from now, will be derived from
         package if not supplied

      **run** : bool, optional

      ..

         * False: just ask the question that pertains to verify
           action, export the results to CSV, and raise RunFalse --
           does not deploy the action

         * True: actually deploy the action

      **get_results** : bool, optional

      ..

         * True: wait for result completion after deploying action

         * False: just deploy the action and return the object in
           *ret*

   :Returns:
      **ret** : dict, containing:

      ..

         * *action_object* : `taniumpy.object_types.action.Action
           <taniumpy.object_types#taniumpy.object_types.action.Action>`_

         * *action_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * *action_progress_human* : str, progress map in human form

         * *action_progress_map* : dict, progress map in dictionary
           form

         * *pre_action_question_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

   `pytan.constants.FILTER_MAPS
      <pytan.constants#pytan.constants.FILTER_MAPS>`_
         valid filter dictionaries for filters

      `pytan.constants.OPTION_MAPS
      <pytan.constants#pytan.constants.OPTION_MAPS>`_
         valid option dictionaries for options

   -[ Examples ]-

   >>> # example of str for `package`
   >>> package = 'Package1'

   >>> # example of str for `package` with params
   >>> package = 'Package1{key:value}'

   >>> # example of str for `action_filters` with params and filter for sensors
   >>> action_filters = 'Sensor1{key:value}, that contains example text'

   >>> # example of list of str for `action_options`
   >>> action_options = ['max_data_age:3600', 'and']

**Handler.deploy_action_asker(action_id, passed_count=0)**

   Checks the results of a deploy action job and waits for completion

   :Parameters:
      **action_id** : int

      ..

         id of deploy action to get results for and wait on completion

      **passed_count** : int, optional

      ..

         the number of servers that must equate "completed" in order
         for deploy action to be recognized as completed

   :Returns:
      **ret** : dict, containing:

      ..

         * *action_object* : `taniumpy.object_types.action.Action
           <taniumpy.object_types#taniumpy.object_types.action.Action>`_

         * *action_results* :
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * *action_progress_human* : str, progress map in human form

         * *action_progress_map* : dict, progress map in dictionary
           form

   `pytan.constants.ACTION_RESULT_STATUS
      <pytan.constants#pytan.constants.ACTION_RESULT_STATUS>`_
         maps the values in *Action Statuses* columns to
         success/completed/failed/etc


Stopping an Action
~~~~~~~~~~~~~~~~~~

**Handler.stop_action(id, **kwargs)**

   Stop an action

   :Parameters:
      **id** : int

      ..

         id of action to stop

   :Returns:
      **action_stop_obj** :
      `taniumpy.object_types.action_stop.ActionStop
      <taniumpy.object_types#taniumpy.object_types.action_stop.ActionStop>`_

      ..

         The object containing the ID of the action stop job

======================================================================


Handler Methods: Exporting/Importing Objects
--------------------------------------------


Import an API Object from JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.create_from_json(objtype, json_file)**

   Creates a new object using the SOAP api from a json file

   :Parameters:
      **objtype** : str

      ..

         Type of object described in *json_file*

      **json_file** : str

      ..

         path to JSON file that describes an API object

   :Returns:
      **ret** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         TaniumPy object added to Tanium SOAP Server

   `pytan.constants.GET_OBJ_MAP
      <pytan.constants#pytan.constants.GET_OBJ_MAP>`_
         maps objtype to supported 'create_json' types


Load a Python Object from JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.load_taniumpy_from_json(json_file)**

   Opens a json file and parses it into an taniumpy object

   :Parameters:
      **json_file** : str

      ..

         path to JSON file that describes an API object

   :Returns:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         TaniumPy object converted from json file


Export Object
~~~~~~~~~~~~~

**Handler.export_obj(obj, export_format, **kwargs)**

   Exports a python API object to a given export format

   :Parameters:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_ or
      `taniumpy.object_types.result_set.ResultSet
      <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

      ..

         TaniumPy object to export

      **export_format** : str

      ..

         the number of servers that must equate "completed" in order
         for deploy action to be recognized as completed

      **header_sort** : list of str, bool, optional

      ..

         * for *export_format* csv and *obj* types
           `taniumpy.object_types.base.BaseType
           <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_
           or `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * True: sort the headers automatically

         * False: do not sort the headers at all

         * list of str: sort the headers returned by priority based on
           provided list

      **header_add_sensor** : bool, optional

      ..

         * for *export_format* csv and *obj* type
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * False: do not prefix the headers with the associated sensor
           name for each column

         * True: prefix the headers with the associated sensor name
           for each column

      **header_add_type** : bool, optional

      ..

         * for *export_format* csv and *obj* type
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * False: do not postfix the headers with the result type for
           each column

         * True: postfix the headers with the result type for each
           column

      **expand_grouped_columns** : bool, optional

      ..

         * for *export_format* csv and *obj* type
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * False: do not expand multiline row entries into their own
           rows

         * True: expand multiline row entries into their own rows

      **explode_json_string_values** : bool, optional

      ..

         * for *export_format* json or csv and *obj* type
           `taniumpy.object_types.base.BaseType
           <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

         * False: do not explode JSON strings in object attributes
           into their own object attributes

         * True: explode JSON strings in object attributes into their
           own object attributes

      **minimal** : bool, optional

      ..

         * for *export_format* xml and *obj* type
           `taniumpy.object_types.base.BaseType
           <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

         * False: include empty attributes in XML output

         * True: do not include empty attributes in XML output

   :Returns:
      **result** : str

      ..

         the contents of exporting *export_format*

   `pytan.constants.EXPORT_MAPS
      <pytan.constants#pytan.constants.EXPORT_MAPS>`_
         maps the type *obj* to *export_format* and the optional args
         supported for each


Export Object to Report File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.export_to_report_file(obj, export_format, **kwargs)**

   Exports a python API object to a file

   :Parameters:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_ or
      `taniumpy.object_types.result_set.ResultSet
      <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

      ..

         TaniumPy object to export

      **export_format** : str

      ..

         the number of servers that must equate "completed" in order
         for deploy action to be recognized as completed

      **header_sort** : list of str, bool, optional

      ..

         * for *export_format* csv and *obj* types
           `taniumpy.object_types.base.BaseType
           <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_
           or `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * True: sort the headers automatically

         * False: do not sort the headers at all

         * list of str: sort the headers returned by priority based on
           provided list

      **header_add_sensor** : bool, optional

      ..

         * for *export_format* csv and *obj* type
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * False: do not prefix the headers with the associated sensor
           name for each column

         * True: prefix the headers with the associated sensor name
           for each column

      **header_add_type** : bool, optional

      ..

         * for *export_format* csv and *obj* type
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * False: do not postfix the headers with the result type for
           each column

         * True: postfix the headers with the result type for each
           column

      **expand_grouped_columns** : bool, optional

      ..

         * for *export_format* csv and *obj* type
           `taniumpy.object_types.result_set.ResultSet
           <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

         * False: do not expand multiline row entries into their own
           rows

         * True: expand multiline row entries into their own rows

      **explode_json_string_values** : bool, optional

      ..

         * for *export_format* json or csv and *obj* type
           `taniumpy.object_types.base.BaseType
           <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

         * False: do not explode JSON strings in object attributes
           into their own object attributes

         * True: explode JSON strings in object attributes into their
           own object attributes

      **minimal** : bool, optional

      ..

         * for *export_format* xml and *obj* type
           `taniumpy.object_types.base.BaseType
           <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

         * False: include empty attributes in XML output

         * True: do not include empty attributes in XML output

      **report_file: str, optional**

      ..

         filename to save report as, will be automatically generated
         if not supplied

      **report_dir: str, optional**

      ..

         directory to save report in, if not supplied, will be
         extracted from *report_file*. if no directory in
         *report_file* or *report_file* not specified, will use
         current working directory.

      **prefix: str, optional**

      ..

         prefix to add to *report_file*

      **postfix: str, optional**

      ..

         postfix to add to *report_file*

   :Returns:
      **report_path** : str

      ..

         the full path to the file created with contents of *result*

      **result** : str

      ..

         the str of *export_format*

======================================================================


Handler Methods: Creating Objects
---------------------------------


Create a Group
~~~~~~~~~~~~~~

**Handler.create_group(groupname, filters=[], filter_options=[])**

   Create a group object

   :Parameters:
      **groupname** : str

      ..

         name of group to create

      **filters** : str or list of str, optional

      ..

         each string must describe a filter

      **filter_options** : str or list of str, optional

      ..

         each string must describe an option for *filters*

   :Returns:
      **group_obj** : `taniumpy.object_types.group.Group
      <taniumpy.object_types#taniumpy.object_types.group.Group>`_

      ..

         TaniumPy object added to Tanium SOAP Server

   `pytan.constants.FILTER_MAPS
      <pytan.constants#pytan.constants.FILTER_MAPS>`_
         valid filters for filters

      `pytan.constants.OPTION_MAPS
      <pytan.constants#pytan.constants.OPTION_MAPS>`_
         valid options for filter_options


Create a Package
~~~~~~~~~~~~~~~~

**Handler.create_package(name, command, display_name='', file_urls=[],
command_timeout_seconds=600, expire_seconds=600,
parameters_json_file='', verify_filters=[], verify_filter_options=[],
verify_expire_seconds=600)**

   Create a package object

   :Parameters:
      **name** : str

      ..

         name of package to create

      **command** : str

      ..

         command to execute

      **display_name** : str, optional

      ..

         display name of package

      **file_urls** : list of strings, optional

      ..

         * URL of file to add to package

         * can optionally define download_seconds by using
           SECONDS::URL

         * can optionally define file name by using FILENAME||URL

         * can combine optionals by using SECONDS::FILENAME||URL

         * FILENAME will be extracted from basename of URL if not
           provided

      **command_timeout_seconds** : int, optional

      ..

         timeout for command execution in seconds

      **parameters_json_file** : str, optional

      ..

         path to json file describing parameters for package

      **expire_seconds** : int, optional

      ..

         timeout for action expiry in seconds

      **verify_filters** : str or list of str, optional

      ..

         each string must describe a filter to be used to verify the
         package

      **verify_filter_options** : str or list of str, optional

      ..

         each string must describe an option for *verify_filters*

      **verify_expire_seconds** : int, optional

      ..

         timeout for verify action expiry in seconds

   :Returns:
      **package_obj** :
      `taniumpy.object_types.package_spec.PackageSpec
      <taniumpy.object_types#taniumpy.object_types.package_spec.PackageSpec>`_

      ..

         TaniumPy object added to Tanium SOAP Server

   `pytan.constants.FILTER_MAPS
      <pytan.constants#pytan.constants.FILTER_MAPS>`_
         valid filters for verify_filters

      `pytan.constants.OPTION_MAPS
      <pytan.constants#pytan.constants.OPTION_MAPS>`_
         valid options for verify_filter_options


Create a Sensor
~~~~~~~~~~~~~~~

**Handler.create_sensor()**

   Create a sensor object

   :Raises:
      **HandlerError** : `pytan.utils.HandlerError
      <pytan.utils#pytan.utils.HandlerError>`_

   Warning: Not currently supported, too complicated to add. Use
     ``create_from_json()`` instead for this object type!


Create a User
~~~~~~~~~~~~~

**Handler.create_user(username, rolename=[], roleid=[],
properties=[])**

   Create a user object

   :Parameters:
      **username** : str

      ..

         name of user to create

      **rolename** : str or list of str, optional

      ..

         name(s) of roles to add to user

      **roleid** : int or list of int, optional

      ..

         id(s) of roles to add to user

      **properties: list of list of strs, optional**

      ..

         * each list must be a 2 item list:

         * list item 1 property name

         * list item 2 property value

   :Returns:
      **user_obj** : `taniumpy.object_types.user.User
      <taniumpy.object_types#taniumpy.object_types.user.User>`_

      ..

         TaniumPy object added to Tanium SOAP Server


Create a Whitelisted URL
~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.create_whitelisted_url(url, regex=False,
download_seconds=86400, properties=[])**

   Create a whitelisted url object

   :Parameters:
      **url** : str

      ..

         text of new url

      **regex** : bool, optional

      ..

         * True: *url* is a regex pattern

         * False: *url* is not a regex pattern

      **download_seconds** : int, optional

      ..

         how often to re-download *url*

      **properties: list of list of strs, optional**

      ..

         * each list must be a 2 item list:

         * list item 1 property name

         * list item 2 property value

   :Returns:
      **url_obj** :
      `taniumpy.object_types.white_listed_url.WhiteListedUrl
      <taniumpy.object_types#taniumpy.object_types.white_listed_url.WhiteListedUrl>`_

      ..

         TaniumPy object added to Tanium SOAP Server

======================================================================


Handler Methods: Deleting Objects
---------------------------------


Delete an Object
~~~~~~~~~~~~~~~~

**Handler.delete(objtype, **kwargs)**

   Delete an object type

   :Parameters:
      **objtype** : string

      ..

         type of object to delete

      **id/name/hash** : int or string, list of int or string

      ..

         search attributes of object to delete, must supply at least
         one valid search attr

   :Returns:
      **ret** : dict

      ..

         dict containing deploy action object and results from deploy
         action

   `pytan.constants.GET_OBJ_MAP
      <pytan.constants#pytan.constants.GET_OBJ_MAP>`_
         maps objtype to supported 'search' keys

======================================================================


Handler Methods: Getting Objects
--------------------------------


Get Single or Multiple Objects of a type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.get(objtype, **kwargs)**

   Get an object type

   :Parameters:
      **objtype** : string

      ..

         type of object to get

      **id/name/hash** : int or string, list of int or string

      ..

         search attributes of object to get, must supply at least one
         valid search attr

   `pytan.constants.GET_OBJ_MAP
      <pytan.constants#pytan.constants.GET_OBJ_MAP>`_
         maps objtype to supported 'search' keys


Get All Objects of a type
~~~~~~~~~~~~~~~~~~~~~~~~~

**Handler.get_all(objtype, **kwargs)**

   Get all objects of a type

   :Parameters:
      **objtype** : string

      ..

         type of object to get

   `pytan.constants.GET_OBJ_MAP
      <pytan.constants#pytan.constants.GET_OBJ_MAP>`_
         maps objtype to supported 'search' keys


Handler Methods: Getting Result Data / Result Info
--------------------------------------------------

**Handler.get_result_data(obj, aggregate=False, **kwargs)**

   Get the result data for a python API object

   This method issues a GetResultData command to the SOAP api for
   *obj*. GetResultData returns the columns and rows that are
   currently available for *obj*.

   :Parameters:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         object to get result data for

      **aggregate** : bool, optional

      ..

         * False: get all the data

         * True: get just the aggregate data (row counts of matches)

   :Returns:
      **rd** : `taniumpy.object_types.result_set.ResultSet
      <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

      ..

         The return of GetResultData for *obj*

**Handler.get_result_info(obj, **kwargs)**

   Get the result info for a python API object

   This method issues a GetResultInfo command to the SOAP api for
   *obj*. GetResultInfo returns information about how many servers
   have passed the *obj*, total number of servers, and so on.

   :Parameters:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         object to get result data for

   :Returns:
      **ri** : `taniumpy.object_types.result_info.ResultInfo
      <taniumpy.object_types#taniumpy.object_types.result_info.ResultInfo>`_

      ..

         The return of GetResultData for *obj*

======================================================================


Handler Methods: Private Methods
--------------------------------

**Handler._find(api_object, **kwargs)**

   Wrapper for interfacing with `taniumpy.session.Session.find()
   <taniumpy.session#taniumpy.session.Session.find>`_

**Handler._get_multi(obj_map, **kwargs)**

   Find multiple item wrapper using ``_find()``

**Handler._get_single(obj_map, **kwargs)**

   Find single item wrapper using ``_find()``

**Handler._single_find(obj_map, k, v, **kwargs)**

   Wrapper for single item searches interfacing with
   `taniumpy.session.Session.find()
   <taniumpy.session#taniumpy.session.Session.find>`_

**Handler._get_sensor_defs(defs)**

   Uses ``get()`` to update a definition with a sensor object

**Handler._get_package_def(d)**

   Uses ``get()`` to update a definition with a package object

**Handler._export_class_BaseType(obj, export_format, **kwargs)**

   Handles exporting `taniumpy.object_types.base.BaseType
   <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

**Handler._export_class_ResultSet(obj, export_format, **kwargs)**

   Handles exporting `taniumpy.object_types.result_set.ResultSet
   <taniumpy.object_types#taniumpy.object_types.result_set.ResultSet>`_

**Handler._export_format_csv(obj, **kwargs)**

   Handles exporting format: CSV

**Handler._export_format_json(obj, **kwargs)**

   Handles exporting format: JSON

**Handler._export_format_xml(obj, **kwargs)**

   Handles exporting format: XML
