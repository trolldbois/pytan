
Ask Saved Question By Name Sse
==========================================================================================

Get the Saved Question object for Installed Applications then get the latest result data available using Server Side Export for that Saved Question


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.031615
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.048952
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "21408", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find saved question objects
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.019343
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "527", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
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


Step 4 - Issue a GetObject to get the full object of the last question asked by a saved question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.097412
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "21692", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
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


Step 5 - Issue a GetResultData to start a Server Side Export and get an export_id
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.008340
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "556", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "874", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 6 - Perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/495576890344.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.004215
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_6_request.txt>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_6_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "12", 
      "content-type": "application/octet-stream"
    }


Step 7 - Perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/495576890344.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.012210
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_7_request.txt>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_7_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "30", 
      "content-type": "application/octet-stream"
    }


Step 8 - Perform an HTTP get to retrieve the data of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/495576890344.xml.gz
* HTTP Method: GET
* Elapsed Time: 0:00:00.009353
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_8_request.txt>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_saved_question_by_name_sse_step_8_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-701-29b97782e68278725322ab84aafb73c07c061edb94c7a92b4c41f6242974fd25eec5231da64b31a04f26258e8da040f8e2e3c5f92ca633c1f59a88126ff7ae85"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-encoding": "gzip", 
      "content-length": "26799", 
      "content-type": "application/octet-stream"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
