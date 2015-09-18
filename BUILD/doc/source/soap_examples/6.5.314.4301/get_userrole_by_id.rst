
Get Userrole By Id
==========================================================================================

Get a user role object by id.


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.059940
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/get_userrole_by_id_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/get_userrole_by_id_step_1_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "password": "VGFuaXVtMjAxNSE=", 
      "username": "QWRtaW5pc3RyYXRvcg=="
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "134", 
      "content-type": "text/plain; charset=us-ascii"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.041443
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/get_userrole_by_id_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/get_userrole_by_id_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-654-a156c034e05efd22905e6c61ac55959bb7ae58f4c8f9a35c1962e1ee47a504a22b978c667a021812874096ad7841ef8a8f3c7f19cbc5b8a70dcc139a60e2ecab"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "20905", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.054283
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/get_userrole_by_id_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/get_userrole_by_id_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "468", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-654-a156c034e05efd22905e6c61ac55959bb7ae58f4c8f9a35c1962e1ee47a504a22b978c667a021812874096ad7841ef8a8f3c7f19cbc5b8a70dcc139a60e2ecab"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-encoding": "gzip", 
      "content-type": "text/xml;charset=UTF-8", 
      "transfer-encoding": "chunked"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
