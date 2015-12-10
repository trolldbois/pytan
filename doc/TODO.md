<!-- MarkdownTOC -->

- [DOC](#doc)
- [BUG](#bug)
- [GEN](#gen)
- [TEST](#test)
- [PLATFORM](#platform)
- [LOW](#low)

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

## BUG
* work on deploy action & start_seconds_from_now (a new action gets created at actual start time)
* on 6.2, block info.json (block 444), fix _regex_for_body_element when _get_response tries to parse for server_version but it doesn't exist
* param with \ at end breaks parameter parser regex
* ~~ Will store value as global in TSAT

## GEN
* fix filename of datetime stamp in win
* bring new session scripts into build system
* 2.1.7: ask_saved: 
  * add log for get_result_info in refresh_data path
  * add check to see if question for re-fetched sq is not different from old sq, if so throw warning. 
* re-figure out py2exe
* add auto paging/caching to normal GRD
* rewrite write_csv
* add secondary loop for if any data == current result unavail/etc (MEDIUM)
* Add method to get question progress (MEDIUM)
* add print_user bin script (SMALL)
* change get logic to use cache_filters instead of objectlist for object selection (HUGE)
* fix search attrs for cmdline scripts (HUGE/CORRELATIVE)
* add non id/name/hash search support to get_$object.py (HUGE/CORRELATIVE)
* question filters get params too?? (UNKNOWN)
* add json source for parameters in TSAT
* add export_obj option for csv to split columns longer than 32k
* refactor utils/binsupport (3.x)

## TEST
* add approve action to pytan (need doc update and test update)
* add tests for dashboard stuffs
* add unit tests for logout()
* add unit tests for auth with session
* rebuild zip_dists, and test on win (or expire ZIP builds for now, no one using?)
* cache_results test: If you are adding tests for that mechanism you could make tests that verify it returns an error if you specify a cache that has expired and make sure that the results that come back don’t change.
* test verify checks work against package with verification (unable to do) (UNKNOWN)
* test against all the different levels of user privs (UNKNOWN)

## PLATFORM
* open enhancement for console.wsdl to contain platform version
* await update on cs values in SSE XML

## LOW
* bundle workflow capture into handler?
* fix build bin doc to run on windows (figure out later)
* look into update object methods (UNKNOWN)
* logfile support (MEDIUM)
* email out (MEDIUM)
* add caching (HUGE)
* figure out cert based auth/plugin based auth? (HUGE)
* add RST output support to mdtester?
