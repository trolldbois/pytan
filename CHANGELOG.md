<!-- MarkdownTOC -->

- [2.2.1](#221)
  - [bug fixes](#bug-fixes)
- [2.2.0](#220)
  - [bug fixes](#bug-fixes-1)
  - [enhancements](#enhancements)
- [2.1.9](#219)
- [2.1.8](#218)
  - [enhancements](#enhancements-1)
- [2.1.7](#217)
  - [enhancements](#enhancements-2)
  - [doc updates](#doc-updates)
  - [bug fixes](#bug-fixes-2)
  - [work in progress](#work-in-progress)
  - [notes](#notes)
- [2.1.6](#216)
  - [enhancements](#enhancements-3)
- [2.1.5](#215)
  - [bug fixes](#bug-fixes-3)
  - [enhancements](#enhancements-4)
- [2.1.4](#214)
  - [bug fixes](#bug-fixes-4)
  - [enhancements](#enhancements-5)
  - [doc updates](#doc-updates-1)
  - [test updates](#test-updates)
- [2.1.3](#213)
  - [enhancements](#enhancements-6)
- [2.1.2](#212)
  - [bug fixes](#bug-fixes-5)
- [2.1.1](#211)
  - [enhancements](#enhancements-7)
- [2.1.0](#210)
  - [bug fixes](#bug-fixes-6)
  - [enhancements](#enhancements-8)
  - [doc updates](#doc-updates-2)
- [2.0.3](#203)
- [2.0.2](#202)
- [2.0.1](#201)
- [2.0.0](#200)
- [1.6.0](#160)
- [1.0.4](#104)
- [1.0.3](#103)
- [1.0.2](#102)
- [1.0.1](#101)
- [1.0.0](#100)
- [0.6.0](#060)
- [0.5.0](#050)
- [0.0.0](#000)

<!-- /MarkdownTOC -->

# 2.2.1

[Released](https://github.com/tanium/pytan/releases/tag/2.2.1) on Jun 30 2017

## bug fixes

* Changing how CSV export of ResultSet objects worked to include Count column by default broke some validation tests
* Added remove_count=True to Valid Export ResultSet tests
* Also added remove_count as valid option to constants.EXPORT_MAPS so it can get funneled down properly to the underlying methods

# 2.2.0

[Released](https://github.com/tanium/pytan/releases/tag/2.2.0) on Jun 27 2017

## bug fixes

* lib directory updates:
  * requests and xmltodict now moved into lib/libs_external directory
  * lib/libs_external directory has support for multi-platform libraries, but not used as of yet - only "any" directory used
  * init.py in lib/pytan package now tries to import lib/libs_external directory before anything else
  * using requests[security] to overcome SSL oddities on OSX / other platforms
  * requests updated to latest version
  * xmltodict updated to latest version
  * ddt NOT updated to latest version, still lives in lib/ instead of lib/libs_external due to massive changes that break how pytan relies on ddt in testing suite

## enhancements

* PEP8/flake8 fixes:
  * lib/pytan/sessions.py
  * lib/pytan/handler.py
* Modified default behavior of lib/pytan/sessions.py:Session.platform_is_6_5():
  * No longer assume that platform is 6.2
  * Will now default to assuming platform is 6.5 or greater
  * force_server_version can still be used to force pytan behavior to 6.2
* Modified default behavior of lib/taniumpy/object_types/result_set.py:
  * 'Count' column will no longer be removed from CSV exports of Result Sets by default, need to supply remove_count=True as an argument to the CSV exporter in order to revert to old behavior
* Callback support added to pytan.handler.Handler:
  * ``handle_cb`` is the new method added to handle callbacks
    * takes 3 arguments itself:
      * obj: the object to pass into a callback function and return
      * cb: the name of the callback to fetch from the ``callbacks`` dict argument in kwargs
      * kwargs: the extra arguments passed to the calling method
    * If a callback named "cb" is found in the ``callbacks`` dict argument in kwargs, that callback will be run with 3 arguments:
      * handler: the instantiated object of the handler itself
      * obj: the object that the callback method should return after modifying
      * kwargs: the extra arguments passed to the calling method
    * If a callback function fails, it will throw an exception. This behavior can be over-ridden by passing callback_exception_failure=False
  * ``_deploy_action`` now supports the following callbacks:
    * PackageDefinition: allows you to change the package definition dict object
    * ActionFilterDefinitions: allows you to change the action filter definitions list object
    * ActionOptionDefinitions: allows you to change the action option definitions list object
    * VerifyActionQuestion: allows you to change the verification question arguments dictionary if run=False
    * PreAddAction: allows you to change the Action object before it gets added
  * ``_ask_manual`` now supports the following callbacks:
    * SensorDefinitions: allows you to change the sensor definitions list object
    * QuestionFilterDefinitions: allows you to change the question filter definitions list object
    * QuestionOptionDefinitions: allows you to change the question option definitions list object
    * PreAddQuestion: allows you to change the Question object before it gets added
  * ``_add`` now supports the following callbacks:
    * PreAddObject: allows you to change ANY object before it gets added
  * More callbacks can be added throughout Handler with ease, please advise if you see the need for one somewhere
  * added ``EXAMPLES\POC\deploy_action_computer_groups.py`` as a proof to show callback support, specifically in deploy_action. Utilizies a callback function named ``handle_cgs`` that is an example PreAddAction callback that modifies the target_group of an Action if computer group names are supplied.

# 2.1.9

[Development branch](https://github.com/tanium/pytan/tree/develop) on N/A

* Not released, major dev work stop-gapped for other reasons. Do not touch develop branch!

# 2.1.8

[Released](https://github.com/tanium/pytan/releases/tag/2.1.8) on Jan 19 2016

## enhancements
* TSAT logging improvement: add file log handler to ALL loggers, not just TSAT log
* added complete_pct arg for ask_manual to binsupport.py

# 2.1.7

[Released](https://github.com/tanium/pytan/releases/tag/2.1.7) on Dec 08 2015 

## enhancements
* added new POC example scripts: export_action_objects.py, find_content_matches.py, get_client_filter.py, sensor_cleanup.py, approved_action_workflow.py

## doc updates
* Fixed missing LICENSE file
* Updated README.md format
* Updated TODO.md format
* Updated CHANGLOG.md format

## bug fixes
* Bring tsat.py into alignment with 2.x series of PyTan, complete re-vamp
* Fix get_result_data() to handle kwargs properly
* fixed a bug in handler.py calling vig_decode in class init that caused failure with --session_id

## work in progress
* Fixing ask_parsed.py SSE option handling
* Added new bin scripts: close_session.py, get_session.py

## notes
* This release is an interim release meant to make the newly re-written tsat.py available ASAP. Another release will be published with full regression testing and re-built documentation as time allows.

# 2.1.6

[Released](https://github.com/tanium/pytan/releases/tag/2.1.6) on Oct 2 2015 

## enhancements
* adding force_server_version as a parameter to Handler & Session
* adding force_passed_done_count as a parameter to QuestionPoller

# 2.1.5

[Released](https://github.com/tanium/pytan/releases/tag/2.1.5) on Sep 15 2015 

## bug fixes
* pollers.QuestionPoller(): increase number of get_result_info retries from 2 to 10 and add one second delay between each retry in get_result_info(), add gri_retry_count to parameter docs everywhere
* sessions.Session(): missing statslog in setup_logging

## enhancements
* Added support for PyTan User Config for storing Handler arguments in JSON format
* handler.Handler(): add pytan_user_config parameter to init, add support for overriding init parameters with values from PyTan User Config as json file
* constants: add PYTAN_USER_CONFIG for default location of PyTan User Config as ~/.pytan_config.json
* binsupport.input_prompts(): no longer prompt for missing inputs if PyTan User Config is valid and has the parameters
* adding --pytan_user_config to all bin/ scripts for Handler Options
* handler.Handler(): added write_pytan_user_config() and read_pytan_user_config()
* added password obfuscation/de-obfuscation, write_pytan_user_config() will now obfsucate the password, init() will now always try to de-obfuscate the password if the password starts and ends with ::
* add examples for new write_pytan_user_config script
* re-built documentation for 2.1.5

# 2.1.4

[Released](https://github.com/tanium/pytan/releases/tag/2.1.4) on Sep 14 2015 

## bug fixes
* handler.Handler(): check for str version of found objects attribute in manual override/non api search
* pollers.QuestionPoller(): added a retry to GetResultInfo calls in pollers if estimated_total == 0 in order to overcome internal bug #5193 (random estimated_total == 0 returns from GRI, unable to reproduce on demand)

## enhancements
* added winlib/ directory
* added open source package pyreadline to winlib/ directory
* re-tooled pytan.binsupport.HistoryConsole to make it more error proof
* re-tooled pytan.binsupport.HistoryConsole to import winlib/ if on windows (for access to pyreadline)
* pytan_shell.py now has tab completion support on Windows (and a host of  keyboard shortcuts)
* new script: get_saved_question_history.py -- provides a method for seeing what questions asked for a saved question have data
* new script: approve_saved_question.py -- provides a way to approve an action when Global Setting "require_action_approval" is set to 1
* pollers.QuestionPoller(): added override_estimated_total parameter
* pollers.ActionPoller(): added override_passed_count parameter

## doc updates
* examples added for ask_parsed.py
* examples added for get_saved_question_history.py
* examples added for approve_saved_question.py
* examples updated for stop_action.py
* updated docstrings for Handler for deploy_action, ask_saved, ask_parsed, ask_manual to include Poller passthroughs
* fixed broken console.wsdl link
* added Command Line Help to left hand side bar
* added better descriptions for the SOAP examples, PyTan Command Line Help, and PyTan API Validation test sections

## test updates
* updating sensors used in tests due to change in Initial Content (sensor “Folder Name Search with RegEx Match” no longer available, switched to use “Folder Contents”)

# 2.1.3

[Released](https://github.com/tanium/pytan/releases/tag/2.1.3) on Sep 09 2015 

## enhancements
* change ask_saved.py to accept —no-refresh_data and —refresh_data, instead of just —refresh_data (to allow the user to be explicit). The default is still —no-refresh_data

# 2.1.2

[Released](https://github.com/tanium/pytan/releases/tag/2.1.2) on Sep 09 2015 

## bug fixes
* make --name work for get_user.py/delete_user.py

# 2.1.1

[Released](https://github.com/tanium/pytan/releases/tag/2.1.1) on Sep 08 2015 

## enhancements
* added group to pytan.handler.create_user()
* HTML docs now zipped up into doc/html/PyTan-$VERSION-HTML_DOC.zip
* re-built docs for new create_user option

# 2.1.0

[Released](https://github.com/tanium/pytan/releases/tag/2.1.0) on Sep 05 2015 

## bug fixes
* pytan.handler.Handler.deploy_action(): changed to return package object that was created for said action, not the package object that was sourced from
* pytan.handler.Handler._platform_is_6_2(): force a call to pytan.handler.Handler.get_server_version() if self.server_version_dict is not set yet
* pytan.handler.Handler.deploy_action(): fix packages created by Tanium SOAP API when adding an action so that they are hidden from the console. also ensure more of the attributes for the source package are copied into the new package for continuity.
* pytan.handler.Handler._get_package_def(): fix for pytan.handler.Handler.deploy_action() when searching for packages by name -- if using a package that has in the past existed, had actions deployed against it that created hidden packages, then the actual visible package was deleted and re-created with the same name, _get_package_def() would actually target one of the hidden packages. added include_hidden_flag=0 to GetObject call in _get_package_def() to fix this. also added to pytan.handler.Handler.sensor_def() to stem possible similar issues for pytan.handler.Handler.ask_manual()
* in pytan.handler.Handler._parse_versioning(): Added notes re: server_version states and added server_version_bad_states. both checks for server_version will check against server_version_bad_states.
* pytan.utils.log_session_communication(): Update to use LAST_REQUESTS_RESPONSE object instead of XML body variables

## enhancements
* pytan.handler has new methods: ask_parsed, parse_query, xml_to_result_set_obj, create_report_file
* massive refactor, bringing all code from bin scripts into pytan.binsupport
* massive refactor, moving all command line code from pytan.utils to pytan.binsupport
* massive refactor:
  * cleaned up all arguments everywhere 
  * ensured every method takes kwargs that needs to
  * changed all argument passing to explicit name/value pairs
* pytan.handler.Handler._export_format_xml(): Add support for ResultSet by checking for _RAW_XML on object, and also run XML through pytan.utils.xml_pretty()
* pytan.session.Session.get_server_info(): added better error handling
* pytan.binsupport.add_ask_report_argparser(): Add XML option for command line scripts that support export format options for asking reports
* pytan.binsupport.setup_parser(): Modify the argument parser used by all bin scripts to expose more handler options
* pytan.handler.Handler.deploy_action(): added action_name and action_comment options
* pytan.constants: add xml as supported format for ResultSet
* pytan.constants: add ask_parsed as supported question type
* pytan.sessions.Session(): massive refactor:
  * move response_prunes in _get_response() to self.BAD_RESPONSE_CMD_PRUNES
  * renamed self.last to self.LAST_RESPONSE_INFO, add initial null variable to Object level and doc
  * renamed self.REQ_RESPONSE to self.LAST_REQUESTS_RESPONSE, add initial null variable to Object level and doc
  * add self.RECORD_ALL_REQUESTS to Object level and doc, controls whether every Requests response object gets appended to self.ALL_REQUESTS_RESPONSES, add kwargs pass thru to init, add kwargs pass through to pytan.handler.Handler
  * add self.ALL_REQUESTS_RESPONSES to Object level and doc
  * add initial null variables to Object level and doc for: server, port, server_version
  * get rid of the *_CMD object variables, unnecessary
  * get rid of the *_RE object variables, replace with single ELEMENT_RE_TXT
  * rename _parse_response_for_regex() to _regex_body_for_element()
  * update _regex_body_for_element() to take element name to search for instead of regex, compile regex on the fly from self.ELEMENT_RE_TXT, log debug messages about regex results
  * rename _extract_cdata_el() to _extract_resultxml()
  * remove export_id element searching from _extract_resultxml()
  * change _extract_resultxml() to return the raw resultxml text instead of the ElementTree object
  * remove LAST_XML_REQUEST_BODY and LAST_XML_RESPONSE_BODY object variables from everywhere — these values can be retrieved from LAST_REQUESTS_RESPONSE.request.body and LAST_REQUESTS_RESPONSE.text respectively
  * remove _extract_export_id()
  * remove export_id handling code from get_result_data()
  * add get_result_data_sse(), which explicitly expects an export_id to exist in the XML response
* bin/ and winbin/: 
  * all new bin scripts
  * now every script is automatically generated and maintained by build system
  * ask_saved_question is now ask_saved
  * ask_manual_quesiton is now ask_manual
  * Tanium_Sensor_Analysis_Tool is now tsat
  * Tanium_Unmanaged_Asset_Tracker moved to EXAMPLES/POC for now, unmaintained
  * new script: ask_parsed
* pytan.sessions.Session.get_server_version(): change log level for version parse failures to debug instead of warning

## doc updates
* doc string updates all over the place
* pointers to KB/Tanium
* double quotes for windows
* console.wsdl ref link
* command line help has note about export format needing to be at end of command line now
* re-wrote BUILD/build_api_examples.py as a real process
* added auto build of SOAP API documentation
* added auto build of pytan validation tests documentation
* flattened, reformatted, and cleaned up doc structure
* made all documentation more automated, no more need to update RST files with new methods/removed methods

# 2.0.3

[Released](https://github.com/tanium/pytan/releases/tag/2.0.3) on Aug 26 2015 

* Added support for server side exports via pytan.handler.get_result_data_sse()
* Added server side export poller to pytan.pollers.SSEPoller
* Added server side export constants to pytan.constants
* Added server side export exceptions to pytan.exceptions
* Added server side export POC to EXAMPLES/poc/test_server_side_export.py
* Refactoring of pytan.sessions, pytan.handler, and pytan.pollers
* Refactored server version checking in pytan.handler
* Updated doc/console.wsdl to platform version 6.5.314.3400
* Re-generated pytan/lib/taniumpy from new doc/console.wsdl
* Added changelog and todo links to pytan readme
* Change functional tests to split invalid / valid server tests into individual files
* Made logging of threaded_http use stderr
* Made logging of threaded_http controllable
* Fixed up tags
* Added tag links to Changelog
* Re-org of TODO.md, relocate to root dir
* Re-org of CHANGELOG.md, added links to releases, old changes, etc
* Updated pytan_test_steps.md to reference new functional test script name
* Copied pytan_test_steps.md to static doc dir
* Incorporated console.wsdl in doc dir
* Added version of tanium server to console.wsdl
* Modified taniumpy build process, using doc/console.wsdl now
* Re-generated taniumpy from 6.5.314.4291 console.wsdl

# 2.0.2

[Released](https://github.com/tanium/pytan/releases/tag/2.0.2) on Aug 18 2015 

* Logging improvements
* Test verbosity cleanups

# 2.0.1

[Released](https://github.com/tanium/pytan/tree/release/2.0.1) on Aug 11 2015

* Added saved action support

# 2.0.0

[Released](https://github.com/tanium/pytan/tree/release/2.0.0) on Aug 7 2015

* 6.2 and 6.5 support
* Completely overhauled session support (we now use keep alive, gzip, and other fun things)
* Completely overhauled Question polling
* Completely overhauled Action polling
* New XML cleaning to remove illegal characters that sometimes slip into sensor data from non-US systems
* And a whole lot of improvements, bug fixes, and performance fixes for large result sets beyond that

# 1.6.0

[Released](https://github.com/tanium/pytan/tree/release/1.0.4) on Apr 15 2015

* Cleaned up open file handles
* Added not a windows script to platform filters (Last Login has it)
* Added retry support to http_post
* Added stats method to session
* Made deploy action work for 6.5 AND 6.2
* Made ActionPoller
* Fixed saved questions
* Added peer review changes from AP
* Added runplugin support
* Fixed invalid character xml issue
* Added saved questions json to api/doc gen

# 1.0.4

[Released](https://github.com/tanium/pytan/tree/release/1.0.4) on Mar 26 2015 

* Added better xml cleaning / invalid character handling to session.py
* Added xml_fix to BaseType.py 
* Added support for sensor driven data for deploying action/package (this was done by adding support for undefined parameters, and "works" in theory, but in execution has lots of issues due to percent encoded parameters)

# 1.0.3

[Released](https://github.com/tanium/pytan/tree/release/1.0.3) on Feb 11 2015 

* Fixed utf-8 issue in taniumpy
* Improvements in build process for STATICWINBUILD

# 1.0.2

[Released](https://github.com/tanium/pytan/releases/tag/1.0.2) on Feb 6 2015 

* Filter hidden sensors from print_sensors.py
* Added better param json decoding error handling in print_sensors.py
* Added support for static building via py2exe
* Built "ask all questions" workflow
* Renamed ask all questions to Tanium Sensor Analysis Tool
* Added username/password/host prompt to all py scripts
* Added config.bat, run.bat, readme.md for TSAT
* Added auto zipper for TSAT build

# 1.0.1

[Released](https://github.com/tanium/pytan/tree/1.0.1) on Dec 8 2014 

* Added question_asker args to get_ask_kwargs
* API documentation added via sphinx
* API examples added to sphinx
* Command line documentation added via mddoctest
* Restructured pytan dir into lib dir
  * pytan/api ->> lib/taniumpy
  * pytan ->> lib/pytan
  * pytan/xmltodict.py ->> lib/xmltodict
* Changed relative imports everywhere to explicit imports via PYTHONPATH (package issues during relative import)
* Convert all func tests to DDT
* Build API doc examples/API examples from ddt func test
* Added complicated query examples
* Added version to pdf
* Changed filters to use : between filter choice and value
* Update sensor help for ask_manual_question.py to describe params
* Added help to manual stuff
* Incorporated mdocbuild for bin scripts
* Built markdown docs for bin scripts
* Added usage to docs
* Updated readme

# 1.0.0

[Released](https://github.com/tanium/pytan/tree/1.0.0) on Dec 1 2014 

* Support sensors filters/options/params for manual questions
* Support whole question filters/options for manual questions
* Integrated auto wsdl generator
* Unit tests updated
* Added json for resultset
* Wrote unittests for dehumanize_* (and everything else)
* Updated all unit tests to work with new handler
* Integrated reporting into handler (export_*)
* Added unittests for export_obj
* Updated all bin/ scripts to work with new handler
* Added functests and unittest for deploy action
* Wrote bin script for deploy
* Added stop action and bin script
* Added get action results bin script
* Added delete support
* Added create_from_json for each create type
* Added unittests for create/delete
* Added whitelisted_urls to unittests for class setup
* Added bin scripts for delete
* Added bin scripts for create_from_json
* Added bin scripts for create

# 0.6.0

[Released](https://github.com/tanium/pytan/tree/0.6.0) on Nov 8 2014

* Re-worked unit tests to be more better-er (data driven)
* Re-worked COUNT column hiding 
* Marked parsed question as no params support (add check for [] and throw  error if found)
* Moved XML dict grabbing stuff from soapwrap into soapresponse
* Created print_sensors.py
* Changed get_objects into get_sensors.py/*
* Added tests for humanize_result_object on sensors single/mult/all
* Added support for parameters in manual questions, handle escaped commas
* Added script / method to return all sensor names for discovery of manual question builder

# 0.5.0 

[Released](https://github.com/tanium/pytan/tree/0.5.0) on Nov 5 2014

* Added better app_test
* Moved formatting/data transforms out
* Added json out
* Refactored unittests for write_response()
* Added xml out
* Added csv out
* Fixed get_question_object request to map to original request
* Added manual query
* Added tests for iwndows
* Added longer wait time for est_total to be nicer to API
* Added python wrapper scripts
* Added windows wrapper scripts
* Added unix example scripts
* Tested against 444 vs 443
* Generalized username/password in test cases

# 0.0.0

[Released](https://github.com/tanium/pytan/releases/tag/0.0.0) on Oct 10 2014

* Initial startup for PyTan
