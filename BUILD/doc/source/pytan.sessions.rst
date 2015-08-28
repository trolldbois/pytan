pytan.sessions module
=====================

.. automodule:: pytan.sessions
    :show-inheritance:

Session Class
-------------

.. autoclass:: pytan.sessions.Session
    :show-inheritance:


Example: Create a Session object
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Setup a Session() object::

    >>> import sys
    >>> sys.path.append('/path/to/pytan/')
    >>> import pytan
    >>> session = pytan.sessions.Session('host')


Authenticate with the Session() object::

    >>> session.authenticate('username', 'password')



------------

Session Attributes
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
.. autoattribute:: pytan.sessions.Session.REQ_SESSION
.. autoattribute:: pytan.sessions.Session.XMLNS
.. autoattribute:: pytan.sessions.Session.REQUEST_BODY_BASE
.. autoattribute:: pytan.sessions.Session.REQUEST_BODY_TEMPLATE
.. autoattribute:: pytan.sessions.Session.AUTH_RES
.. autoattribute:: pytan.sessions.Session.SOAP_RES
.. autoattribute:: pytan.sessions.Session.INFO_RES
.. autoattribute:: pytan.sessions.Session.AUTH_CONNECT_TIMEOUT_SEC
.. autoattribute:: pytan.sessions.Session.AUTH_RESPONSE_TIMEOUT_SEC
.. autoattribute:: pytan.sessions.Session.INFO_CONNECT_TIMEOUT_SEC
.. autoattribute:: pytan.sessions.Session.INFO_RESPONSE_TIMEOUT_SEC
.. autoattribute:: pytan.sessions.Session.SOAP_CONNECT_TIMEOUT_SEC
.. autoattribute:: pytan.sessions.Session.SOAP_RESPONSE_TIMEOUT_SEC
.. autoattribute:: pytan.sessions.Session.SOAP_REQUEST_HEADERS
.. autoattribute:: pytan.sessions.Session.ELEMENT_RE_TXT
.. autoattribute:: pytan.sessions.Session.HTTP_DEBUG
.. autoattribute:: pytan.sessions.Session.HTTP_RETRY_COUNT
.. autoattribute:: pytan.sessions.Session.HTTP_AUTH_RETRY
.. autoattribute:: pytan.sessions.Session.STATS_LOOP_ENABLED
.. autoattribute:: pytan.sessions.Session.STATS_LOOP_SLEEP_SEC
.. autoattribute:: pytan.sessions.Session.STATS_LOOP_TARGETS
.. autoattribute:: pytan.sessions.Session.RECORD_ALL_REQUESTS
.. autoattribute:: pytan.sessions.Session.ALL_REQUESTS_RESPONSES
.. autoattribute:: pytan.sessions.Session.LAST_REQUESTS_RESPONSE
.. autoattribute:: pytan.sessions.Session.LAST_RESPONSE_INFO
.. autoattribute:: pytan.sessions.Session.BAD_RESPONSE_CMD_PRUNES
.. autoattribute:: pytan.sessions.Session.server
.. autoattribute:: pytan.sessions.Session.port
.. autoattribute:: pytan.sessions.Session.server_version

Session Methods
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Authentication
***************************************************************

.. automethod:: pytan.sessions.Session.authenticate
.. automethod:: pytan.sessions.Session.logout
.. autoattribute:: pytan.sessions.Session.is_auth
.. autoattribute:: pytan.sessions.Session.session_id

SOAP API Wrappers
***************************************************************

.. automethod:: pytan.sessions.Session.find
.. automethod:: pytan.sessions.Session.save
.. automethod:: pytan.sessions.Session.add
.. automethod:: pytan.sessions.Session.delete
.. automethod:: pytan.sessions.Session.run_plugin
.. automethod:: pytan.sessions.Session.get_result_info
.. automethod:: pytan.sessions.Session.get_result_data
.. automethod:: pytan.sessions.Session.get_result_data_sse

Server Info / Version / Stats
***************************************************************

.. automethod:: pytan.sessions.Session.get_server_info
.. automethod:: pytan.sessions.Session.get_server_version
.. automethod:: pytan.sessions.Session.get_server_stats
.. automethod:: pytan.sessions.Session.enable_stats_loop
.. automethod:: pytan.sessions.Session.disable_stats_loop

HTTP GET / POST
***************************************************************

.. automethod:: pytan.sessions.Session.http_get
.. automethod:: pytan.sessions.Session._http_get
.. automethod:: pytan.sessions.Session.http_post
.. automethod:: pytan.sessions.Session._http_post

Utility Methods
***************************************************************

.. automethod:: pytan.sessions.Session._replace_auth
.. automethod:: pytan.sessions.Session._full_url
.. automethod:: pytan.sessions.Session._clean_headers
.. automethod:: pytan.sessions.Session._start_stats_thread
.. automethod:: pytan.sessions.Session._stats_loop
.. automethod:: pytan.sessions.Session._flatten_server_info
.. automethod:: pytan.sessions.Session._get_percentage
.. automethod:: pytan.sessions.Session._find_stat_target
.. automethod:: pytan.sessions.Session._resolve_stat_target
.. automethod:: pytan.sessions.Session._build_body
.. automethod:: pytan.sessions.Session._create_run_plugin_object_body
.. automethod:: pytan.sessions.Session._create_add_object_body
.. automethod:: pytan.sessions.Session._create_delete_object_body
.. automethod:: pytan.sessions.Session._create_get_result_info_body
.. automethod:: pytan.sessions.Session._create_get_result_data_body
.. automethod:: pytan.sessions.Session._create_get_object_body
.. automethod:: pytan.sessions.Session._create_update_object_body
.. automethod:: pytan.sessions.Session._check_auth
.. automethod:: pytan.sessions.Session._regex_body_for_element
.. automethod:: pytan.sessions.Session._extract_cdata_el
.. automethod:: pytan.sessions.Session._get_response
