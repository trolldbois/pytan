# TODO NOW
  * [X] broken CR in folder name search regex match (SMALL) (limit in excel, 32k chars per cell)
  * [ ] add secondary loop for if any data == current result unavail/etc (MEDIUM)
  * [ ] change get logic to use cache_filters instead of objectlist for object selection (HUGE)
  * [X] clean up open file handles
  * [ ] winbin doc note re double quotes and using batch scripts instead of py scripts directly
  * [X] add not a windows script to platform filters (Last Login has it)

# TODO LATER
  * [?] Add method to get question progress (MEDIUM)
  * [ ] explain get == select col data, from == select row data (SMALL/DOC)
  * [ ] add pointers to KB articles (SMALL/DOC)
  * [ ] add readme.md to examples (SMALL/DOC)
  * [ ] fix search attrs for cmdline scripts (HUGE/CORRELATIVE)
  * [ ] add non id/name/hash search support to get_$object.py (HUGE/CORRELATIVE)
  * [ ] question filters get params too?? (UNKNOWN)
  * [ ] add print_user bin script (SMALL)
  * [ ] test verify checks work against package with verification (unable to do) (UNKNOWN)
  * [ ] look into update object methods (UNKNOWN)
  * [ ] add method to calculate total time btwn request and response (UNKNOWN)
  * [ ] test against all the different levels of user privs (UNKNOWN)
  * [ ] logfile support (MEDIUM)
  * [ ] email out (MEDIUM)
  * [ ] test against demo tanium (MEDIUM)
  * [ ] add caching (HUGE)
  * [ ] figure out cert based auth/plugin based auth? (HUGE)

# DONE
  * 0.5.0
    * [X] better app_test
    * [X] move formatting/data transforms OUT (transforms.py?)
    * [X] REFACTOR TIME>>>>>
    * [X] json out
    * [X] refactor unittests for write_response()
    * [X] xml out
    * [X] csv out
    * [X] fix get_question_object request to map to original request
    * [X] manual query
    * [X] test on windoze
    * [X] ADD LONGER WAIT TIME FOR HIGHER est_total TO BE NICER TO API
    * [X] python wrapper scripts
    * [X] windows wrapper scripts
    * [X] unix example scripts
    * [X] test against 444 vs 443
    * [X] generalize username/password in test cases
  * 0.6.0
    * [X] re-work unit tests to be more better-er (data driven)
    * [X] re-work COUNT column hiding (need to expand testbed to have 2 or more  of one OS)
    * [X] mark parsed question as no params support (add check for [] and throw  excpetion if found)
    * [X] move XML dict grabbing stuff from soapwrap into soapresponse
    * [X] create print_sensors.py
    * [X] change get_objects into get_sensors.py/*
    * [X] test humanize_result_object on sensors single/mult/all
    * [X] support parameters in manual questions
      * [X] handle escaped commas
    * [X] add script / method to return all sensor names for discovery of manual question builder
  * 1.0.0
    * [X] support sensors filters/options/params for manual questions
    * [X] support whole question filters/options for manual questions
    * [X] auto wsdl generator
    * [X] ResultSet needs a write_csv
    * [X] figure out ask manual question
    * [X] UNIT TESTS UPDATE
    * [X] json for resultset
    * [X] write unittests for dehumanize_* (and everything else)
    * [X] update all unit tests to work with new handler
    * [X] ResultSet needs a to_json
    * [X] integrate reporting into handler (export_*)
    * [X] add unittests for export_obj
    * [X] update all bin/ scripts to work with new handler
    * [X] figure out deploy action
    * [X] functests and unittest for deploy action
    * [X] checkin api changes to taniumpy
    * [X] write bin script for deploy
    * [X] add stop action and bin script
    * [X] add get action results bin script
    * [X] add delete support
    * [X] figure out the "create" object for every type that i'm supporting for "get"
    * [X] add create_from_json for each create type
    * [X] create_from_json(): NEED TO TEST FOR REST OF create_json = True, sensor working
    * [X] unittests for create/delete
    * [X] add whitelisted_urls to unittests for class setup
    * [X] bin scripts for delete
    * [X] bin scripts for create_from_json
    * [X] bin scripts for create
  * 1.0.1
    * [X] add question_asker args to get_ask_kwargs
    * [X] API documentation added via sphinx
    * [X] API examples added to sphinx
    * [X] Command line documentation added via mddoctest
    * [X] restructured pytan dir into lib dir
      * [X] pytan/api ->> lib/taniumpy
      * [X] pytan ->> lib/pytan
      * [X] pytan/xmltodict.py ->> lib/xmltodict
    * [X] changed relative imports everywhere to explicit imports via PYTHONPATH (package issues during relative import)
    * [X] convert all func tests to DDT
    * [X] build API doc examples/API examples from ddt func test
    * [X] add complicated query examples
    * [X] add version to pdf
    * [X] change filters to use : between filter choice and value
    * [X] update sensor help for ask_manual_question.py to describe params
    * [X] add help to manual stuff
    * [X] incorporate mdocbuild for bin scripts
    * [X] build markdown docs for bin scripts
    * [X] add usage to docs
    * [X] update readme
  * 1.0.2
    * [X] filter hidden sensors from print_sensors.py
    * [X] add better param json decoding error handling in print_sensors.py
    * [X] Add support for static building via py2exe
    * [X] build "ask all questions" workflow
    * [X] rename ask all questions to Tanium Sensor Analysis Tool
    * [X] add username/password/host prompt to all py scripts
    * [X] add config.bat, run.bat, readme.md for TSAT
    * [X] add auto zipper for TSAT build
  * 1.0.3
    * [X] fix utf-8 issue in taniumpy
    * [X] improvements in build process for STATICWINBUILD
    * [X] rebuild doc dirs
  * 1.0.4
    * [X] add better xml cleaning / invalid character handling to session.py (MEDIUM)
    * [X] add xml_fix to BaseType.py (SMALL)
    * [X] add support for sensor driven data for deploying action/package (this was done by adding support for undefined parameters, and "works" in theory, but in execution has lots of issues due to percent encoded parameters) (SMALL)
