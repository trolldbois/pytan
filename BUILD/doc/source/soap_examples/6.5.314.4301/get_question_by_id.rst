
Get Question By Id
==========================================================================================

Get a question object by id


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.006206
* `Step 1 Request Body <../_static/soap_outputs/get_question_by_id_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/get_question_by_id_step_1_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "password": "VGFuaXVtMjAxNSE=", 
      "username": "QWRtaW5pc3RyYXRvcg=="
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "135", 
      "content-type": "text/plain; charset=us-ascii"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.006814
* `Step 2 Request Body <../_static/soap_outputs/get_question_by_id_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/get_question_by_id_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6956-97b438be2639ca6835344f0549d2f56bc4b585b29e59202a1eb3bc747a211ccd44d4964486c2b797e2b20e01e30a1667e6917ced9dde839bbec98f9fe4760e5f"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "87505", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004008
* `Step 3 Request Body <../_static/soap_outputs/get_question_by_id_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/get_question_by_id_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "490", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6956-97b438be2639ca6835344f0549d2f56bc4b585b29e59202a1eb3bc747a211ccd44d4964486c2b797e2b20e01e30a1667e6917ced9dde839bbec98f9fe4760e5f"
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
