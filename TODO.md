  * DOC:
    * examples for ask_parsed.py
    * examples for tsat.py
    * add more examples for sse everywhere
    * go through SOAP doc and verify everything looks sane
    * zip up HTML doc in dev/master repo to save on sync craziness

  * BUG:
    * work on deploy action & start_seconds_from_now (a new action gets created at actual start time)

  * GEN:
    * move platform 6.5 checks into GRD_SSE, call normal GRD instead of throwing exception
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

  * TEST:
    * add approve action to pytan (need doc update and test update)
    * add tests for dashboard stuffs
    * add unit tests for logout()
    * add unit tests for auth with session
    * rebuild zip_dists, and test on win (or expire ZIP builds for now, no one using?)
    * cache_results test: If you are adding tests for that mechanism you could make tests that verify it returns an error if you specify a cache that has expired and make sure that the results that come back don’t change.
    * test verify checks work against package with verification (unable to do) (UNKNOWN)
    * test against all the different levels of user privs (UNKNOWN)

  * PLATFORM:
    * open enhancement for console.wsdl to contain platform version
    * await update on cs values in SSE XML

  * LOW:
    * bundle workflow capture into handler?
    * fix build bin doc to run on windows (figure out later)
    * write get_session_id.py (later)
    * update EXAMPLES to work with 2.0.0
    * look into update object methods (UNKNOWN)
    * logfile support (MEDIUM)
    * email out (MEDIUM)
    * add caching (HUGE)
    * figure out cert based auth/plugin based auth? (HUGE)
    * add RST output support to mdtester?
    * add os env overrides and/or add profile overrides
