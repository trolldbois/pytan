
pytan.utils module
******************

Collection of exceptions, classes, and methods used throughout `pytan
<pytan#module-pytan>`_


Utility Classes: Exceptions
===========================

Exceptions used throughout `pytan <pytan#module-pytan>`_:

**exception pytan.utils.HandlerError**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

   Exception thrown for most errors in `pytan.handler
   <pytan.handler#module-pytan.handler>`_

**exception pytan.utils.HumanParserError**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

   Exception thrown for errors while parsing human strings from
   `pytan.handler <pytan.handler#module-pytan.handler>`_

**exception pytan.utils.DefinitionParserError**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

   Exception thrown for errors while parsing definitions from
   `pytan.handler <pytan.handler#module-pytan.handler>`_

**exception pytan.utils.RunFalse**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

   Exception thrown when run=False from
   `pytan.handler.Handler.deploy_action()
   <pytan.handler#pytan.handler.Handler.deploy_action>`_


Utility Classes: Logging handlers
=================================

**class pytan.utils.SplitStreamHandler**

   Bases: ``logging.Handler``

   Custom ``logging.Handler`` class that sends all messages that are
   logging.INFO and below to STDOUT, and all messages that are
   logging.WARNING and above to STDERR

   **emit(record)**


Utility Classes: Argument Parsers for Command Line Scripts
==========================================================

**class pytan.utils.CustomArgFormat(prog, indent_increment=2,
max_help_position=24, width=None)**

   Bases: `argparse.ArgumentDefaultsHelpFormatter
   <http://docs.python.org/2.7/library/argparse.html#argparse.ArgumentDefaultsHelpFormatter>`_,
   `argparse.RawDescriptionHelpFormatter
   <http://docs.python.org/2.7/library/argparse.html#argparse.RawDescriptionHelpFormatter>`_

   Multiple inheritance Formatter class for `argparse.ArgumentParser
   <http://docs.python.org/2.7/library/argparse.html#argparse.ArgumentParser>`_.

   If a `argparse.ArgumentParser
   <http://docs.python.org/2.7/library/argparse.html#argparse.ArgumentParser>`_
   class uses this as it's Formatter class, it will show the defaults
   for each argument in the *help* output

**class pytan.utils.CustomArgParse(*args, **kwargs)**

   Bases: `argparse.ArgumentParser
   <http://docs.python.org/2.7/library/argparse.html#argparse.ArgumentParser>`_

   Custom `argparse.ArgumentParser
   <http://docs.python.org/2.7/library/argparse.html#argparse.ArgumentParser>`_
   class which does a number of things:

   * Uses ``pytan.utils.CustomArgFormat`` as it's Formatter class, if
     none was passed in

   * Prints help if there is an error

   * Prints the help for any subparsers that exist

   **error(message)**

   **print_help(**kwargs)**


Utility Functions: Logging
==========================

**pytan.utils.change_console_format(debug=False)**

   Changes the logging format for console handler to
   `pytan.constants.DEBUG_FORMAT
   <pytan.constants#pytan.constants.DEBUG_FORMAT>`_ or
   `pytan.constants.INFO_FORMAT
   <pytan.constants#pytan.constants.INFO_FORMAT>`_

   :Parameters:
      **debug** : bool, optional

      ..

         * False : set logging format for console handler to
           `pytan.constants.INFO_FORMAT
           <pytan.constants#pytan.constants.INFO_FORMAT>`_

         * True :  set logging format for console handler to
           `pytan.constants.DEBUG_FORMAT
           <pytan.constants#pytan.constants.DEBUG_FORMAT>`_

**pytan.utils.remove_logging_handler(name)**

   Removes a logging handler

   :Parameters:
      **name** : str

      ..

         name of logging handler to remove. if name == 'all' then all
         logging handlers are removed

**pytan.utils.set_all_loglevels(level='DEBUG')**

   Sets all loggers that the logging system knows about to a given
   logger level

**pytan.utils.set_log_levels(loglevel=0)**

   Enables loggers based on loglevel and
   `pytan.constants.LOG_LEVEL_MAPS
   <pytan.constants#pytan.constants.LOG_LEVEL_MAPS>`_

   :Parameters:
      **loglevel** : int, optional

      ..

         loglevel to match against each item in
         `pytan.constants.LOG_LEVEL_MAPS
         <pytan.constants#pytan.constants.LOG_LEVEL_MAPS>`_ - each
         item that is greater than or equal to loglevel will have the
         according loggers set to their respective levels identified
         there-in.

**pytan.utils.setup_console_logging()**

   Creates a console logging handler using ``SplitStreamHandler``


Utility Functions: Type Checking
================================

**pytan.utils.is_dict(l)**

   returns True if *l* is a dictionary, False if not

**pytan.utils.is_list(l)**

   returns True if *l* is a list, False if not

**pytan.utils.is_num(l)**

   returns True if *l* is a number, False if not

**pytan.utils.is_str(l)**

   returns True if *l* is a string, False if not


Utility Functions: Misc
=======================

**pytan.utils.get_dict_list_items(d, i)**

   Gets keys from dict *d* if any item in list *i* is in the list
   value for each key

   :Parameters:
      **d** : dict of str

      ..

         dict to get strs from if list contains any item from *i*

      **i** : list of str

      ..

         list of strs to check if for existence in any lists in *d*

   :Returns:
      **list** : list of str

      ..

         list of strings from *d* that have *i* in their values

**pytan.utils.get_dict_list_len(d, keys=[], negate=False)**

   Gets the sum of each list in dict *d*

   :Parameters:
      **d** : dict of str

      ..

         dict to sums of

      **keys** : list of str

      ..

         list of keys to get sums of, if empty gets a sum of all keys

      **negate** : bool

      ..

         * only used if keys supplied

         * False : get the sums of *d* that do match keys

         * True : get the sums of *d* that do not match keys

   :Returns:
      **list_len** : int

      ..

         sum of lists in *d* that match keys

**pytan.utils.get_now()**

   Get current time in human friendly format

   :Returns:
      str :

      ..

         str of current time return from ``human_time()``

**pytan.utils.human_time(t, tformat='%Y_%m_%d-%H_%M_%S-%Z')**

   Get time in human friendly format

   :Parameters:
      **t** : int, float, time

      ..

         either a unix epoch or struct_time object to convert to
         string

      **tformat** : str, optional

      ..

         format of string to convert time to

   :Returns:
      str :

      ..

         *t* converted to str

**pytan.utils.jsonify(v, indent=2, sort_keys=True)**

   Turns python object *v* into a pretty printed JSON string

   :Parameters:
      **v** : object

      ..

         python object to convert to JSON

      **indent** : int, 2

      ..

         number of spaces to indent JSON string when pretty printing

      **sort_keys** : bool, True

      ..

         sort keys of JSON string when pretty printing

   :Returns:
      str :

      ..

         JSON pretty printed string

**pytan.utils.port_check(address, port, timeout=5)**

   Check if *address*:*port* can be reached within *timeout*

   :Parameters:
      **address** : str

      ..

         hostname/ip address to check *port* on

      **port** : int

      ..

         port to check on *address*

      **timeout** : int, optional

      ..

         timeout after N seconds of not being able to connect

   :Returns:
      `socket
      <http://docs.python.org/2.7/library/socket.html#module-socket>`_
      or False :

      ..

         if connection succeeds, the socket object is returned, else
         False is returned

**pytan.utils.seconds_from_now(secs=0, tz='utc')**

   Get time in Tanium SOAP API format *secs* from now

   :Parameters:
      **secs** : int

      ..

         seconds from now to get time str

      **tz** : str, optional

      ..

         time zone to return string in, default is 'utc' - supplying
         anything else will supply local time

   :Returns:
      str :

      ..

         time *secs* from now in Tanium SOAP API format

**pytan.utils.test_app_port(host, port)**

   Validates that *host*:*port* can be reached using ``port_check()``

   :Parameters:
      **host** : str

      ..

         hostname/ip address to check *port* on

      **port** : int

      ..

         port to check on *host*

   :Raises:
      **HandlerError** : ``pytan.utils.HandlerError``

      ..

         if *host*:*port* can not be reached

**pytan.utils.version_check(reqver)**

   Allows scripts using `pytan <pytan#module-pytan>`_ to validate the
   version of the script aginst the version of `pytan
   <pytan#module-pytan>`_

   :Parameters:
      **reqver** : str

      ..

         string containing version number to check against
         ``Exception``

   :Raises:
      **Exception** : ``Exception``

      ..

         if `pytan.__version__ <pytan#pytan.__version__>`_ is not
         greater or equal to *reqver*

**pytan.utils.xml_pretty(x)**

   Uses `xmltodict <xmltodict#module-xmltodict>`_ to pretty print an
   XML str *x*

   :Parameters:
      **x** : str

      ..

         XML string to pretty print

   :Returns:
      str :

      ..

         The pretty printed string of *x*

**pytan.utils.xml_pretty_resultobj(x)**

   Uses `xmltodict <xmltodict#module-xmltodict>`_ to pretty print an
   the result-object element in XML str *x*

   :Parameters:
      **x** : str

      ..

         XML string to pretty print

   :Returns:
      str :

      ..

         The pretty printed string of result-object in *x*

**pytan.utils.xml_pretty_resultxml(x)**

   Uses `xmltodict <xmltodict#module-xmltodict>`_ to pretty print an
   the ResultXML element in XML str *x*

   :Parameters:
      **x** : str

      ..

         XML string to pretty print

   :Returns:
      str :

      ..

         The pretty printed string of ResultXML in *x*


Utility Functions: Argument Parsers for Command Line Scripts
============================================================

**pytan.utils.setup_parser(desc, help=False)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts that use `pytan <pytan#module-pytan>`_. This
   establishes the basic arguments that are needed by all such
   scripts, such as:

   * --help

   * --username

   * --password

   * --host

   * --port

   * --loglevel

   * --debugformat (not shown in --help)

**pytan.utils.setup_get_object_argparser(obj, doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to get objects.

**pytan.utils.setup_create_json_object_argparser(obj, doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to create objects from json files.

**pytan.utils.setup_delete_object_argparser(obj, doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to delete objects.

**pytan.utils.setup_ask_saved_argparser(doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to ask saved questions.

**pytan.utils.setup_stop_action_argparser(doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to stop actions.

**pytan.utils.setup_deploy_action_argparser(doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to deploy actions.

**pytan.utils.setup_get_result_argparser(doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to get results for questions or actions.

**pytan.utils.setup_ask_manual_argparser(doc)**

   Method to setup the base ``pytan.utils.CustomArgParse`` class for
   command line scripts using ``pytan.utils.setup_parser()``, then add
   specific arguments for scripts that use `pytan
   <pytan#module-pytan>`_ to ask manual questions.

**pytan.utils.add_ask_report_argparser(parser)**

   Method to extend a ``pytan.utils.CustomArgParse`` class for command
   line scripts with arguments for scripts that need to supply export
   format subparsers for asking questions.

**pytan.utils.add_report_file_options(parser)**

   Method to extend a ``pytan.utils.CustomArgParse`` class for command
   line scripts with arguments for scripts that need to supply export
   file and directory options.

**pytan.utils.add_get_object_report_argparser(parser)**

   Method to extend a ``pytan.utils.CustomArgParse`` class for command
   line scripts with arguments for scripts that need to supply export
   format subparsers for getting objects.

**pytan.utils.get_grp_opts(parser, grp_names)**

   Used to get arguments in *parser* that match argument group names
   in *grp_names*

   :Parameters:
      **parser** : ``argparse.ArgParse``

      ..

         ArgParse object

      **grp_names** : list of str

      ..

         list of str of argument group names to get arguments for

   :Returns:
      **grp_opts** : list of str

      ..

         list of arguments gathered from argument group names in
         *grp_names*

**pytan.utils.process_create_json_object_args(parser, handler, obj,
all_args)**

   Process command line args supplied by user for create json object

   :Parameters:
      **parser** : ``argparse.ArgParse``

      ..

         ArgParse object used to parse *all_args*

      **handler** : `pytan.handler.Handler
      <pytan.handler#pytan.handler.Handler>`_

      ..

         Instance of Handler created from command line args

      **obj** : str

      ..

         Object type for create json object

      **all_args** : dict

      ..

         dict of args parsed from *parser*

   :Returns:
      **response** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         response from `pytan.handler.Handler.create_from_json()
         <pytan.handler#pytan.handler.Handler.create_from_json>`_

**pytan.utils.process_delete_object_args(parser, handler, obj,
all_args)**

   Process command line args supplied by user for delete object

   :Parameters:
      **parser** : ``argparse.ArgParse``

      ..

         ArgParse object used to parse *all_args*

      **handler** : `pytan.handler.Handler
      <pytan.handler#pytan.handler.Handler>`_

      ..

         Instance of Handler created from command line args

      **obj** : str

      ..

         Object type for delete object

      **all_args** : dict

      ..

         dict of args parsed from *parser*

   :Returns:
      **response** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         response from `pytan.handler.Handler.delete()
         <pytan.handler#pytan.handler.Handler.delete>`_

**pytan.utils.process_get_object_args(parser, handler, obj,
all_args)**

   Process command line args supplied by user for get object

   :Parameters:
      **parser** : ``argparse.ArgParse``

      ..

         ArgParse object used to parse *all_args*

      **handler** : `pytan.handler.Handler
      <pytan.handler#pytan.handler.Handler>`_

      ..

         Instance of Handler created from command line args

      **obj** : str

      ..

         Object type for get object

      **all_args** : dict

      ..

         dict of args parsed from *parser*

   :Returns:
      **response** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         response from `pytan.handler.Handler.get()
         <pytan.handler#pytan.handler.Handler.get>`_


Utility Functions: Dehumanize human strings
===========================================

**pytan.utils.dehumanize_package(package)**

   Turns a package str into a package definition

   :Parameters:
      **package** : str

      ..

         A str that describes a package and optionally a selector
         and/or parameters

   :Returns:
      **package_def** : dict

      ..

         dict parsed from *sensors*

**pytan.utils.dehumanize_question_filters(question_filters)**

   Turns a question_filters str or list of str into a question filter
   definition

   :Parameters:
      **question_filters** : str, list of str

      ..

         A str or list of str that describes a sensor for a question
         filter(s) and optionally a selector and/or filter

   :Returns:
      **question_filter_defs** : list of dict

      ..

         list of dict parsed from *question_filters*

**pytan.utils.dehumanize_question_options(question_options)**

   Turns a question_options str or list of str into a question option
   definition

   :Parameters:
      **question_options** : str, list of str

      ..

         A str or list of str that describes question options

   :Returns:
      **question_option_defs** : list of dict

      ..

         list of dict parsed from *question_options*

**pytan.utils.dehumanize_sensors(sensors, key='sensors',
empty_ok=False)**

   Turns a sensors str or list of str into a sensor definition

   :Parameters:
      **sensors** : str, list of str

      ..

         A str or list of str that describes a sensor(s) and
         optionally a selector, parameters, filter, and/or options

      **key** : str, optional

      ..

         Name of key that user should have provided *sensors* as

      **empty_ok** : bool, optional

      ..

         False: *sensors* is not allowed to be empty, throw
         ``HumanParserError`` if it is empty True: *sensors* is
         allowed to be empty

   :Returns:
      **sensor_defs** : list of dict

      ..

         list of dict parsed from *sensors*

**pytan.utils.extract_filter(s)**

   Extracts a filter from str *s*

   :Parameters:
      **s** : str

      ..

         A str that may or may not have a filter identified by ', that
         HUMAN VALUE'

   :Returns:
      **s** : str

      ..

         str *s* without the parsed_filter included

      **parsed_filter** : dict

      ..

         filter attributes mapped from filter from *s* if any found

**pytan.utils.extract_options(s)**

   Extracts options from str *s*

   :Parameters:
      **s** : str

      ..

         A str that may or may not have options identified by ',
         opt:name[:value]'

   :Returns:
      **s** : str

      ..

         str *s* without the parsed_options included

      **parsed_options** : list

      ..

         options extracted from *s* if any found

**pytan.utils.extract_params(s)**

   Extracts parameters from str *s*

   :Parameters:
      **s** : str

      ..

         A str that may or may not have parameters identified by
         {key=value}

   :Returns:
      **s** : str

      ..

         str *s* without the parsed_params included

      **parsed_params** : list

      ..

         parameters extracted from *s* if any found

**pytan.utils.extract_selector(s)**

   Extracts a selector from str *s*

   :Parameters:
      **s** : str

      ..

         A str that may or may not have a selector in the beginning in
         the form of id:, name:, or :hash -- if no selector found,
         name will be assumed as the default selector

   :Returns:
      **s** : str

      ..

         str *s* without the parsed_selector included

      **parsed_selector** : str

      ..

         selector extracted from *s*, or 'name' if none found

**pytan.utils.map_filter(filter_str)**

   Maps a filter str against ``constants.FILTER_MAPS``

   :Parameters:
      **filter_str** : str

      ..

         filter_str str that should be validated

   :Returns:
      **filter_attrs** : dict

      ..

         dict containing mapped filter attributes for SOAP API

**pytan.utils.map_option(opt, dest)**

   Maps an opt str against ``constants.OPTION_MAPS``

   :Parameters:
      **opt** : str

      ..

         option str that should be validated

      **dest** : list of str

      ..

         list of valid destinations (i.e. *filter* or *group*)

   :Returns:
      **opt_attrs** : dict

      ..

         dict containing mapped option attributes for SOAP API

**pytan.utils.map_options(options, dest)**

   Maps a list of options using ``map_option()``

   :Parameters:
      **options** : list of str

      ..

         list of str that should be validated

      **dest** : list of str

      ..

         list of valid destinations (i.e. *filter* or *group*)

   :Returns:
      **mapped_options** : dict

      ..

         dict of all mapped_options


Utility Functions: kwargs getters
=================================

**pytan.utils.get_ask_kwargs(**kwargs)**

   Gets QuestionAsker args from kwargs and returns a dict with just
   those matching args

   :Parameters:
      ****kwargs** : dict

      ..

         kwargs to get keys from

   :Returns:
      **ask_kwargs** : dict

      ..

         args from kwargs that are found in
         `pytan.constants.ASK_KWARGS
         <pytan.constants#pytan.constants.ASK_KWARGS>`_

**pytan.utils.get_kwargs_int(key, default=None, **kwargs)**

   Gets key from kwargs and validates it is an int

   :Parameters:
      **key** : str

      ..

         key to get from kwargs

      **default** : int, optional

      ..

         default value to use if key not found in kwargs

      ****kwargs** : dict

      ..

         kwargs to get key from

   :Returns:
      **val** : int

      ..

         value from key, or default if supplied

**pytan.utils.get_req_kwargs(**kwargs)**

   Gets SOAP API request args from kwargs and returns a dict with just
   those matching args

   :Parameters:
      ****kwargs** : dict

      ..

         kwargs to get keys from

   :Returns:
      **req_kwargs** : dict

      ..

         args from kwargs that are found in
         `pytan.constants.REQ_KWARGS
         <pytan.constants#pytan.constants.REQ_KWARGS>`_


Utility Functions: Object mappers
=================================

**pytan.utils.get_obj_map(objtype)**

   Gets an object map for *objtype*

   :Parameters:
      **objtype** : str

      ..

         object type to get object map from in
         `pytan.constants.GET_OBJ_MAP
         <pytan.constants#pytan.constants.GET_OBJ_MAP>`_

   :Returns:
      **obj_map** : dict

      ..

         matching object map for *objtype* from
         `pytan.constants.GET_OBJ_MAP
         <pytan.constants#pytan.constants.GET_OBJ_MAP>`_

**pytan.utils.get_q_obj_map(qtype)**

   Gets an object map for *qtype*

   :Parameters:
      **qtype** : str

      ..

         question type to get object map from in
         `pytan.constants.Q_OBJ_MAP
         <pytan.constants#pytan.constants.Q_OBJ_MAP>`_

   :Returns:
      **obj_map** : dict

      ..

         matching object map for *qtype* from
         `pytan.constants.Q_OBJ_MAP
         <pytan.constants#pytan.constants.Q_OBJ_MAP>`_


Utility Functions: TaniumPy objects
===================================

**pytan.utils.apply_options_obj(options, obj, dest)**

   Updates an object with options

   :Parameters:
      **options** : dict

      ..

         dict containing options definition

      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         TaniumPy object to apply *options* to

      **dest** : list of str

      ..

         list of valid destinations (i.e. *filter* or *group*)

   :Returns:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         TaniumPy object updated with attributes from *options*

**pytan.utils.build_group_obj(q_filter_defs, q_option_defs)**

   Creates a Group object from q_filter_defs and q_option_defs

   :Parameters:
      **q_filter_defs** : list of dict

      ..

         List of dict that are question filter definitions

      **q_option_defs** : dict

      ..

         dict of question filter options

   :Returns:
      **group_obj** : `taniumpy.object_types.group.Group
      <taniumpy.object_types#taniumpy.object_types.group.Group>`_

      ..

         Group object with list of
         `taniumpy.object_types.filter.Filter
         <taniumpy.object_types#taniumpy.object_types.filter.Filter>`_
         built from *q_filter_defs* and *q_option_defs*

**pytan.utils.build_manual_q(selectlist_obj, group_obj)**

   Creates a Question object from selectlist_obj and group_obj

   :Parameters:
      **selectlist_obj** :
      `taniumpy.object_types.select_list.SelectList
      <taniumpy.object_types#taniumpy.object_types.select_list.SelectList>`_

      ..

         SelectList object to add to Question object

      **group_obj** : `taniumpy.object_types.group.Group
      <taniumpy.object_types#taniumpy.object_types.group.Group>`_

      ..

         Group object to add to Question object

   :Returns:
      **add_q_obj** : `taniumpy.object_types.question.Question
      <taniumpy.object_types#taniumpy.object_types.question.Question>`_

      ..

         Question object built from selectlist_obj and group_obj

**pytan.utils.build_metadatalist_obj(properties, nameprefix)**

   Creates a MetadataList object from properties

   :Parameters:
      **properties** : list of list of strs

      ..

         list of lists, each list having two strs - str 1: property
         key, str2: property value

      **nameprefix** : str

      ..

         prefix to insert in front of property key when creating
         MetadataItem

   :Returns:
      **metadatalist_obj** :
      `taniumpy.object_types.metadata_list.MetadataList
      <taniumpy.object_types#taniumpy.object_types.metadata_list.MetadataList>`_

      ..

         MetadataList object with list of
         `taniumpy.object_types.metadata_item.MetadataItem
         <taniumpy.object_types#taniumpy.object_types.metadata_item.MetadataItem>`_
         built from *properties*

**pytan.utils.build_param_obj(key, val, delim='')**

   Creates a Parameter object from key and value, surrounding key with
   delim

   :Parameters:
      **key** : str

      ..

         key to use for parameter

      **value** : str

      ..

         value to use for parameter

      **delim** : str

      ..

         str to surround key with when adding to parameter object

   :Returns:
      **param_obj** : `taniumpy.object_types.parameter.Parameter
      <taniumpy.object_types#taniumpy.object_types.parameter.Parameter>`_

      ..

         Parameter object built from key and val

**pytan.utils.build_param_objlist(obj, user_params, delim='',
derive_def=False, empty_ok=False)**

   Creates a ParameterList object from user_params

   :Parameters:
      **obj** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         TaniumPy object to verify parameters against

      **user_params** : dict

      ..

         dict describing key and value of user supplied params

      **delim** : str

      ..

         str to surround key with when adding to parameter object

      **derive_def** : bool, optional

      ..

         * False: Do not derive default values, and throw a
           ``HandlerError`` if user did not supply a value for a given
           parameter

         * True: Try to derive a default value for each parameter if
           user did not supply one

      **empty_ok** : bool, optional

      ..

         * False: If user did not supply a value for a given
           parameter, throw a ``HandlerError``

         * True: If user did not supply a value for a given parameter,
           do not add the parameter to the ParameterList object

   :Returns:
      **param_objlist** :
      `taniumpy.object_types.parameter_list.ParameterList
      <taniumpy.object_types#taniumpy.object_types.parameter_list.ParameterList>`_

      ..

         ParameterList object with list of
         `taniumpy.object_types.parameter.Parameter
         <taniumpy.object_types#taniumpy.object_types.parameter.Parameter>`_
         built from user_params

**pytan.utils.build_selectlist_obj(sensor_defs)**

   Creates a SelectList object from sensor_defs

   :Parameters:
      **sensor_defs** : list of dict

      ..

         List of dict that are sensor definitions

   :Returns:
      **select_objlist** :
      `taniumpy.object_types.select_list.SelectList
      <taniumpy.object_types#taniumpy.object_types.select_list.SelectList>`_

      ..

         SelectList object with list of
         `taniumpy.object_types.select.Select
         <taniumpy.object_types#taniumpy.object_types.select.Select>`_
         built from *sensor_defs*

**pytan.utils.derive_param_default(obj_param)**

   Derive a parameter default

   :Parameters:
      **obj_param** : dict

      ..

         parameter dict from TaniumPy object

   :Returns:
      **def_val** : str

      ..

         default value derived from obj_param

**pytan.utils.empty_obj(taniumpy_object)**

   Validate that a given TaniumPy object is not empty

   :Parameters:
      **taniumpy_object** : `taniumpy.object_types.base.BaseType
      <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_

      ..

         object to check if empty

   :Returns:
      bool

      ..

         True if *taniumpy_object* is considered empty, False
         otherwise

**pytan.utils.get_filter_obj(sensor_def)**

   Creates a Filter object from sensor_def

   :Parameters:
      **sensor_def** : dict

      ..

         dict containing sensor definition

   :Returns:
      **filter_obj** : `taniumpy.object_types.filter.Filter
      <taniumpy.object_types#taniumpy.object_types.filter.Filter>`_

      ..

         Filter object created from *sensor_def*

**pytan.utils.get_obj_params(obj)**

   Get the parameters from a TaniumPy object and JSON load them

   obj : `taniumpy.object_types.base.BaseType
   <taniumpy.object_types#taniumpy.object_types.base.BaseType>`_
      TaniumPy object to get parameters from

   :Returns:
      **params** : dict

      ..

         JSON loaded dict of parameters from *obj*

**pytan.utils.question_progress(asker, pct)**

   Call back method for `taniumpy.question_asker.QuestionAsker.run()
   <taniumpy.question_asker#taniumpy.question_asker.QuestionAsker.run>`_
   to report progress while waiting for results from a question

   :Parameters:
      **asker** : `taniumpy.question_asker.QuestionAsker
      <taniumpy.question_asker#taniumpy.question_asker.QuestionAsker>`_

      ..

         QuestionAsker instance

      **pct** : float

      ..

         Percentage completion of question


Utility Functions: Definition objects
=====================================

**pytan.utils.check_dictkey(d, key, valid_types, valid_list_types)**

   Yet another method to check a dictionary for a key

   :Parameters:
      **d** : dict

      ..

         dictionary to check for key

      **key** : str

      ..

         key to check for in d

      **valid_types** : list of str

      ..

         list of str of valid types for key

      **valid_list_types** : list of str

      ..

         if key is a list, validate that all values of list are in
         valid_list_types

**pytan.utils.chk_def_key(def_dict, key, keytypes, keysubtypes=None,
req=False)**

   Checks that def_dict has key

   :Parameters:
      **def_dict** : dict

      ..

         Definition dictionary

      **key** : str

      ..

         key to check for in def_dict

      **keytypes** : list of str

      ..

         list of str of valid types for key

      **keysubtypes** : list of str

      ..

         if key is a dict or list, validate that all values of dict or
         list are in keysubtypes

      **req** : bool

      ..

         * False: key does not have to be in def_dict

         * True: key must be in def_dict, throw
           ``DefinitionParserError`` if not

**pytan.utils.parse_defs(defname, deftypes, strconv=None,
empty_ok=True, defs=None, **kwargs)**

   Parses and validates defs into new_defs

   :Parameters:
      **defname** : str

      ..

         Name of definition

      **deftypes** : list of str

      ..

         list of valid types that defs can be

      **strconv** : str

      ..

         if supplied, and defs is a str, turn defs into a dict with
         key = strconv, value = defs

      **empty_ok** : bool

      ..

         * True: defs is allowed to be empty

         * False: defs is not allowed to be empty

   :Returns:
      **new_defs** : list of dict

      ..

         parsed and validated defs

**pytan.utils.val_package_def(package_def)**

   Validates package definitions

   Ensures package definition has a selector, and if a package
   definition has a params key, that key is valid

   :Parameters:
      **package_def** : dict

      ..

         package definition

**pytan.utils.val_q_filter_defs(q_filter_defs)**

   Validates question filter definitions

   Ensures each question filter definition has a selector, and if a
   question filter definition has a filter key, that key is valid

   :Parameters:
      **q_filter_defs** : list of dict

      ..

         list of question filter definitions

**pytan.utils.val_sensor_defs(sensor_defs)**

   Validates sensor definitions

   Ensures each sensor definition has a selector, and if a sensor
   definition has a params, options, or filter key, that each key is
   valid

   :Parameters:
      **sensor_defs** : list of dict

      ..

         list of sensor definitions
