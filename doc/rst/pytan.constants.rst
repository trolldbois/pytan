
pytan.constants module
**********************

PyTan Constants

This contains a number of constants that drive PyTan.

``pytan.constants.ACTION_RESULT_STATUS = {'Verified.': ['no_v ...
Running.': ['running']}``

   Maps a deploy action result status to it's respective end states.

``pytan.constants.ASK_KWARGS = ['timeout', 'polling_interval',
'pct_complete_threshold']``

   A list of arguments that will be passed on to the question
   asker/poller `taniumpy.question_asker.QuestionAsker
   <taniumpy.question_asker#taniumpy.question_asker.QuestionAsker>`_

``pytan.constants.DEBUG_FORMAT = '[%(lineno)-5d - %(f ... s %(name)s
%(message)s'``

   Logging format for debugformat=True

``pytan.constants.EXPORT_MAPS = {'ResultSet': {'json ... s': [<type
'bool'>]}]}}``

   Maps a given TaniumPy object to the list of supported export
   formats for each object type, and the valid optional arguments for
   each export format. Optional arguments construct:
      * key: the optional argument name itself

      * valid_types: the valid python types that are allowed to be
        passed as a value to *key*

      * valid_list_types: the valid python types in str format that
        are allowed to be passed in a list, if list is one of the
        *valid_types*

``pytan.constants.FILTER_MAPS = [{'operator': 'Less' ... ,
'regexmatch', 're']}]``

   Maps a given set of human strings into the various filter
   attributes used by the SOAP API. Also used to verify that a
   manually supplied filter via a definition is valid. Construct:
      * human: a list of human strings that can be used after '*,
        that*'. Ex: '*, that* ``contains`` ``value``'

      * operator: the filter operator used by the SOAP API when
        building a filter that matches *human*

      * not_flag: the value to set on *not_flag* when building a
        filter that matches *human*

      * pre_value: the prefix to add to the ``value`` when building a
        filter

      * post_value: the postfix to add to the ``value`` when building
        a filter

``pytan.constants.FILTER_RE = ',\\s*that'``

   The regex that is used to find filters in a string. Ex:
   *Sensor1*``, that`` *contains blah*

``pytan.constants.GET_OBJ_MAP = {'user': {'search':  ... alse,
'delete': False}}``

   Maps an object type from a human friendly string into various
   aspects:
      * single: The ``TaniumPy`` object used to find singular
        instances of this object type

      * multi: The ``TaniumPy`` object used to find multiple instances
        of this object type

      * all: The ``TaniumPy`` object used to find all instances of
        this object type

      * search: The list of attributes that can be used with the
        Tanium SOAP API for searches

      * manual: Whether or not this object type is allowed to do a
        manual search, that is -- allow the user to specify an
        attribute that is not in search, which will get ALL objects of
        that type then search for a match based on attribute values
        for EVERY key/value pair supplied

      * delete: Whether or not this object type can be deleted

      * create_json: Whether or not this object type can be created by
        importing from JSON

``pytan.constants.INFO_FORMAT = '%(asctime)s %(levelname)-8s %(name)s:
%(message)s'``

   Logging format for debugformat=False

``pytan.constants.LOG_LEVEL_MAPS = [(0, {'api.session.h ...
.http.body': 'DEBUG'})]``

   Map for loglevel(int) -> logger -> logger
   level(logging.INFO|WARN|DEBUG|...). Higher loglevels will include
   all levels up to and including that level. Contains a list of
   tuples, each tuple consisting of:
      * int, loglevel

      * dict, *{{logger_name: logger_level}}* for this loglevel

``pytan.constants.OPTION_MAPS = [{'destination': 'fi ... d_type':
<type 'int'>}]``

   Maps a given human string into the various options for filters used
   by the SOAP API. Also used to verify that a manually supplied
   option via a definition is valid. Construct:
      * human: the human string that can be used after '*opt:*'. Ex:
        '*opt*:``value_type``:``value``'

      * destination: the type of object this option can be applied to
        (filter or group)

      * attrs: the attributes and their values used by the SOAP API
        when building a filter with an option that matches *human*

      * attr: the attribute used by the SOAP API when building a
        filter with an option that matches *human*. ``value`` is
        pulled from after a *:* when only attr exists for an option
        map, and not attrs.

      * valid_values: if supplied, the list of valid values for this
        option

      * valid_type: performs type checking on the value supplied to
        verify it is correct

      * human_type: the human string for the value type if the option
        requires a value

``pytan.constants.OPTION_RE = ',\\s*opt:'``

   The regex that is used to find options in a string. Ex: *Sensor1,
   that contains blah*``, opt:``*ignore_case*``,
   opt:``*max_data_age:3600*

``pytan.constants.PARAM_DELIM = '||'``

   The string to surround a parameter with when passing parameters to
   the SOAP API for a sensor in a question. Ex:
   ``||``*parameter_key*``||``

``pytan.constants.PARAM_KEY_SPLIT = '='``

   The string that is used to split parameter key from parameter
   value. Ex: *key1*``=``*value1*

``pytan.constants.PARAM_RE = '\\{(.*?)\\}'``

   The regex that is used to parse parameters from a human string. Ex:
   ala {key1=value1}

``pytan.constants.PARAM_SPLIT_RE = '(?<!\\\\),'``

   The regex that is used to split multiple parameters. Ex:
   key1=value1, key2=value2

``pytan.constants.Q_OBJ_MAP = {'manual': {'handler ... ':
'ask_manual_human'}}``

   Maps a question type from a human friendly string into the handler
   method that supports each type

``pytan.constants.REQ_KWARGS = ['hide_errors_flag', ... ',
'json_pretty_print']``

   A list of arguments that will be pulled from any respective kwargs
   for most calls to `taniumpy.session.Session
   <taniumpy.session#taniumpy.session.Session>`_

``pytan.constants.SELECTORS = ['id', 'name', 'hash']``

   The search selectors that can be extracted from a string. Ex:
   ``name``:*Sensor1,* or ``id``:*1*, or ``hash``:*1111111*

``pytan.constants.SENSOR_TYPE_MAP = {0: 'Hash', 1: 'Stri ... 12:
'LastOperatorType'}``

   Maps a Result type from the Tanium SOAP API from an int to a string
