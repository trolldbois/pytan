  * add tests for SSE
  * fix doc strings for exceptions
  * add custom name to deploy_action
  * add more docstrings to sessions.py
  * open bug for console.wsdl to contain platform version
  * http_get() not correctly fixing on auth on expired session
  * remove xml_cleaner for http_get, perform only if export_format=1
  * change deploy_action to return package_object that was created for said action, not package_object that was used as template
  * add to cmd line help: export type & export options must be at end of cmd line
  * GRD with export_flag=1, write FLE on Handler
  * rebuild zip_dists, and test on win
  * add console.wsdl to documentation via build script
  * add approve action to pytan (need doc update and test update)
  * add unit tests for logout()
  * add unit tests for auth with session
  * add unit tests for sessions_lib
  * work on deploy action & start_seconds_from_now (a new action gets created at actual start time)
  * add doc note re excel limit for cell
  * re-work build API example scripts to be more better-er
  * update EXAMPLES to work with 2.0.0
  * winbin doc note re double quotes and using batch scripts instead of py scripts directly
  * add more doc notes/refs for dehumanize_*
  * add tests for dashboard stuffs
  * add approve action 
  * add dashboard wrappers
  * add secondary loop for if any data == current result unavail/etc (MEDIUM)
  * change get logic to use cache_filters instead of objectlist for object selection (HUGE)
  * cache_results test: If you are adding tests for that mechanism you could make tests that verify it returns an error if you specify a cache that has expired and make sure that the results that come back don’t change.
  * Add method to get question progress (MEDIUM)
  * explain get == select col data, from == select row data (SMALL/DOC)
  * add pointers to KB articles (SMALL/DOC)
  * add readme.md to examples (SMALL/DOC)
  * fix search attrs for cmdline scripts (HUGE/CORRELATIVE)
  * add non id/name/hash search support to get_$object.py (HUGE/CORRELATIVE)
  * question filters get params too?? (UNKNOWN)
  * add print_user bin script (SMALL)
  * test verify checks work against package with verification (unable to do) (UNKNOWN)
  * look into update object methods (UNKNOWN)
  * add method to calculate total time btwn request and response (UNKNOWN)
  * test against all the different levels of user privs (UNKNOWN)
  * logfile support (MEDIUM)
  * email out (MEDIUM)
  * test against demo tanium (MEDIUM)
  * add caching (HUGE)
  * figure out cert based auth/plugin based auth? (HUGE)
  * broken CR in folder name search regex match (SMALL) (limit in excel, 32k chars per cell)
  * add os env overrides!
  ```
    def __env_overrides(self):
        """looks for OS environment variables and overrides the corresponding
        attribute if they exist
        """
        or_tpl = "Overriding {!r} with OS environment variable {!r}".format

        for os_env_var, class_var in constants.OS_ENV_MAP.iteritems():
            if not os_env_var in os.environ.keys():
                continue

            if not os.environ[os_env_var]:
                continue

            self.DLOG(or_tpl(os.environ[os_env_var], os_env_var))
            setattr(self, class_var, os.environ[os_env_var])

# Used by SoapWrap.SoapWrap for environment variable override mappings
OS_ENV_MAP = {
    'SOAP_USERNAME': 'self.__username',
    'SOAP_PASSWORD': 'self.__password',
    'SOAP_HOSTNAME': 'self.__host',
    'SOAP_PORT': 'self.__port',
    'SOAP_PROTOCOL': 'self.__protocol',
    'SOAP_PATH': 'self.__soap_path',
}
  ```

