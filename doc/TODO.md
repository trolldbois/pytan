<!-- MarkdownTOC -->

- [DOC](#doc)
  - [TANIUMNG](#taniumng)
  - [TESTS](#tests)
  - [SESSION](#session)
  - [HUMAN PARSING](#human-parsing)
  - [HANDLER/MAIN](#handlermain)
  - [UTILS](#utils)
- [TODO figure out pyreadline later](#todo-figure-out-pyreadline-later)
  - [TEST](#test)
  - [PLATFORM](#platform)
  - [LOW](#low)
  - [LIBXML](#libxml)

<!-- /MarkdownTOC -->

## DOC
* examples for tsat.py
* add more examples for sse everywhere
* go through SOAP doc and verify everything looks sane
* re-make dev workflow doc
* add timing doc for various GRD methods
* fix mddoctest for http://tanium.github.io/pytan/_static/bin_doc/write_pytan_user_config.html
* add note to pytan_test_steps about Administrator user having to exist
* add documentation note about PyTan only being fully tested with Administrator role 
* add windows install doc tip re: 2.7 only
* write history
* ensure all exceptions are re-raised if not a specific Tanium/PyTan type
* turn on pep257 in flake8 project settings
* document static props for things like what_hash and so on??
* clean up prints!!!:
grep 'print(' * -r|grep -v pyreadline|grep -v 'requests/'

## TANIUMNG
* TODO: ADD parameter_definition_dict TO BUILDER
* TODO ADD DOCSTR TO BUILDER HEADER
* rebuild taniumpy with latest wsdl (LAST)

## TESTS
* add expected for tickle tests

## SESSION
* add permission checking from user_obj
* move stats threading into it's own class LAST
 
## HUMAN PARSING
* argparse for specs/left/right/etc

## HANDLER/MAIN
* re-do logging yet again, add support for {0: -1, 11: 20, 12: 30, 14: 50} (pytan level: logging level) ==> NEXT
* also make log printer better (add a generic one that prints log levels in human friendly format, need map)
* create_parent_group_obj broken, fix it and add debug logging!
* add logger to tanium_ng and tickle_ng
* increase loglevel range to 50
* keep loglevels 1-10 reserved for shell scripts
* keep loglevels 10-30 reserved for info logs
* keep loglevels 30-50 reserved for debug logs
* 2.1.7: ask_saved: 
  * add log for get_result_info in refresh_data path
  * add check to see if question for re-fetched sq is not different from old sq, if so throw warning. 
* fix sse
* add auto paging/caching to normal GRD
* add secondary loop for if any data == current result unavail/etc (MEDIUM)
* Add method to get question progress (MEDIUM)
* add print_user bin script (SMALL)
* question filters get params too?? (UNKNOWN)
* add export_obj option for csv to split columns longer than 32k
* work on deploy action & start_seconds_from_now (a new action gets created at actual start time)
* ~~ Will store value as global in TSAT
* bundle workflow capture into handler?
* look into update object methods (UNKNOWN)
* email out (MEDIUM)
* add caching (HUGE)
* figure out how to get last N of an obj
>>> v=handler.get_questions({'value': secs_from_now(secs=-(60 * 2)), 'type': 'Date', 'field': 'expiration', 'operator': 'Greater'})

* test against 6.6 (auth changes??)


## UTILS
# TODO figure out pyreadline later
* add "advanced" options capability to shellparser (custom action, custom formatter, custom format_help on shellparser)

## TEST
* add approve action to pytan (need doc update and test update)
* add tests for dashboard stuffs
* cache_results test: If you are adding tests for that mechanism you could make tests that verify it returns an error if you specify a cache that has expired and make sure that the results that come back don’t change.
* test verify checks work against package with verification (unable to do) (UNKNOWN)
* test against all the different levels of user privs (UNKNOWN)

## PLATFORM
* open enhancement for console.wsdl to contain platform version

## LOW
* figure out cert based auth/plugin based auth? (HUGE)
* add RST output support to mdtester?

## LIBXML
* libxml
  - py3: sudo CPATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/libxml2 CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip3 install lxml
  - py2: sudo CPATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/libxml2 CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip2 install lxml

* timing for xml -- looks like celementtree is fastest for getting all questions, but for large result sets lxml may win over, need to test later
* should add xmltodict into mix
* need to create faux large result data sets (>50MB) (>100MB) (>500MB) and a faux large question list (>100,000)
* may need to change RowList/Row for speed!

  * lxml:
    >>> eval_timing("handler.get_questions()")
    Timing info for handler.get_questions() -- START: 2015-12-24 21:00:42.098527, END: 2015-12-24 21:00:51.189905, ELAPSED: 0:00:09.091378, RESPONSE LEN: 9915

  * celementtree:
    >>> eval_timing("handler.get_questions()")
    Timing info for handler.get_questions() -- START: 2015-12-24 21:02:00.768571, END: 2015-12-24 21:02:08.545939, ELAPSED: 0:00:07.777368, RESPONSE LEN: 9915

  * elementtree:
    >>> eval_timing("handler.get_questions()")
    Timing info for handler.get_questions() -- START: 2015-12-24 21:03:01.757966, END: 2015-12-24 21:03:09.961130, ELAPSED: 0:00:08.203164, RESPONSE LEN: 9915

