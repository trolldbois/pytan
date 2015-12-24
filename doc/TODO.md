<!-- MarkdownTOC -->

- [DOC](#doc)
- [TANIUMNG](#taniumng)
- [SESSION](#session)
- [HUMAN PARSING](#human-parsing)
- [HANDLER](#handler)
- [UTILS](#utils)
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
* write history

## TANIUMNG
* move serializers out => tickle NOW
  * MAKE RESULTINFO A BASETYPE! ==> NOW
  * MAKE RESULTSET A BASETYPE! ==> NOW
* timing for xml?
* rebuild taniumpy with latest wsdl
* get annotations from wsdl

## SESSION
* http/s proxy
* reauth broke
* move stats threading into it's own class
* i plan to extend that signature to add “domain” and “secondary” as part of my current pytan refactor, in order to support all 4 fields the /auth api supports
* on 6.2, block info.json (block 444), fix _regex_for_body_element when _get_response tries to parse for server_version but it doesn't exist

## HUMAN PARSING
* argparse for specs/left/right/etc

## HANDLER
* create_parent_group_obj broken, fix it and add debug logging!
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

## UTILS
* remove external deps from utils, move version into utils

## TEST
* add approve action to pytan (need doc update and test update)
* add tests for dashboard stuffs
* add unit tests for logout()
* add unit tests for auth with session
* cache_results test: If you are adding tests for that mechanism you could make tests that verify it returns an error if you specify a cache that has expired and make sure that the results that come back don’t change.
* test verify checks work against package with verification (unable to do) (UNKNOWN)
* test against all the different levels of user privs (UNKNOWN)

## PLATFORM
* open enhancement for console.wsdl to contain platform version
* await update on cs values in SSE XML

## LOW
* figure out cert based auth/plugin based auth? (HUGE)
* add RST output support to mdtester?
