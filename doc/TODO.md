<!-- MarkdownTOC -->

- [DOC](#doc)
- [EVERYWHERE](#everywhere)
- [TANIUMNG](#taniumng)
- [TESTS](#tests)
- [TICKLE](#tickle)
- [SESSION](#session)
- [HANDLER](#handler)
- [UTILS](#utils)
- [PLATFORM BUGS](#platform-bugs)
- [BUILD TOOLS](#build-tools)
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
* turn on pep257 in flake8 project settings

## EVERYWHERE
* ensure all exceptions are re-raised if not a specific Tanium/PyTan type
* clean up prints!!!:
grep 'print(' * -r|grep -v pyreadline|grep -v 'requests/'
* redo logging to use MYLOG.pytan_levels

## TANIUMNG
* TODO ADD DOCSTR TO BUILDER HEADER
* rebuild taniumpy with latest wsdl (LAST)
* document static props for things like what_hash and so on?? (LATER)

## TESTS
* ADD TESTS FOR HANDLER.get_* **NOW**
* add expected for tickle tests
* test against 6.6 (auth changes??)
* add approve action to pytan (need doc update and test update)
* add tests for dashboard stuffs
* cache_results test: If you are adding tests for that mechanism you could make tests that verify it returns an error if you specify a cache that has expired and make sure that the results that come back don’t change.
* test verify checks work against package with verification (unable to do) (UNKNOWN)
* test against all the different levels of user privs (UNKNOWN)

## TICKLE
* add delimiter opt

## SESSION
* add permission checking from user_obj
* move stats threading into it's own class LAST
* figure out cert based auth/plugin based auth? (HUGE)
 
## HANDLER
* ask_manual:
  * add prompting to createparams?
* ask_parsed:
  * parser doesnt work with params! catch [] in parser and throw exception? or do what console does and strip them out and re-add them back in (pull them out index correlated and add them back in index correlated, use CreateParams)
  * change parser to v3 with no failback
* handler_logs:
  * add gmt log back in
* GRD:
  * add auto paging/caching to normal GRD
  * add secondary loop for if any data == current result unavail/etc (MEDIUM)
* OTHER:
  * Add method to get question progress (MEDIUM)
  * add print_user bin script (SMALL)
  * ~~ Will store value as global in TSAT
  * bundle workflow capture into handler?
  * look into update object methods (UNKNOWN)
  * add caching (HUGE)
  * figure out how to get last N of an obj
  >>> v=handler.get_questions({'value': secs_from_now(secs=-(60 * 2)), 'type': 'Date', 'field': 'expiration', 'operator': 'Greater'})
  * add other operator types (last 5 seconds/minutes/days)
* EXPORT:
  * add export_obj option for csv to split columns longer than 32k
  * email out (MEDIUM)
* deploy_action:
  * work on deploy action & start_seconds_from_now (a new action gets created at actual start time)
  * automatically handle approved action workflow

## UTILS
* TODO figure out pyreadline later
* add "advanced" options capability to shellparser (custom action, custom formatter, custom format_help on shellparser)
* Add pytan log output to TSAT

## PLATFORM BUGS
* open enhancement for console.wsdl to contain platform version
* open enhancement for more fields at login
* open enhancement for better/split up logging
* SOAP Parse XML not printing out XML bodies from requests via pytan
* headers['SOAPAction'] = '"urn:TaniumSOAPAction"' NEEDED IN session.soap_request?
* Does timediff work for cachefilters?
* groups don't show not in front of query text for all sub groups when not_flag is 1 for parent group
* getobject for package_specs does not work, must do it via package_spec (should allow singular or multi form for all objects)
* cache filters do not work for: groups (by id), users, user_roles, whitelisted_urls
* cache filter Date not working against modification_time/creation_time?

## BUILD TOOLS
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

