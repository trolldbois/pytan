
taniumpy.session module
***********************

Session handler for Tanium API

**exception taniumpy.session.AuthorizationError**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

**exception taniumpy.session.BadResponseError**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

**class taniumpy.session.DynamicFormatter**

   Bases: `string.Formatter
   <http://docs.python.org/2.7/library/string.html#string.Formatter>`_

   **get_value(key, args, kwargs)**

**exception taniumpy.session.HttpError**

   Bases: `exceptions.Exception
   <http://docs.python.org/2.7/library/exceptions.html#exceptions.Exception>`_

**class taniumpy.session.Session(server, port=443)**

   Bases: `object
   <http://docs.python.org/2.7/library/functions.html#object>`_

   ``ADD_OBJECT = 'AddObject'``

   ``AUTH_RES = '/auth'``

   ``DELETE_OBJECT = 'DeleteObject'``

   **FORMATTER(format_string, *args, **kwargs)**

   ``GET_OBJECT = 'GetObject'``

   ``GET_RESULT_DATA = 'GetResultData'``

   ``GET_RESULT_INFO = 'GetResultInfo'``

   ``INFO_RES = '/info.json'``

   ``REQUEST_BODY = u'<SOAP-ENV:Envelope ... </SOAP-ENV:Envelope>\n'``

   ``SOAP_PORT = 444``

   ``SOAP_RES = '/soap'``

   ``UPDATE_OBJECT = 'UpdateObject'``

   **add(obj, **kwargs)**

   **authenticate(username=None, password=None)**

   **delete(obj, **kwargs)**

   **find(object_type, **kwargs)**

   **getResultData(obj, **kwargs)**

   **getResultInfo(obj, **kwargs)**

   **get_server_info()**

   ``is_auth``

   **save(obj, **kwargs)**

   ``server_version``

   ``session_id``

**taniumpy.session.http_post(host, port, url, body=None, headers=None,
timeout=5)**

**taniumpy.session.load_file(filename)**
