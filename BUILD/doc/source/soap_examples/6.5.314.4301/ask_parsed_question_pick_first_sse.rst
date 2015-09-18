
Ask Parsed Question Pick First Sse
==========================================================================================

Ask the server to parse the question text 'computer name and ip route details' and add the question object that is returned in the first ParseResultGroup,  wait for result data to be complete, then use server side export to get the result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.050073
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.057523
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "20907", 
      "content-type": "application/json"
    }


Step 3 - Issue an AddObject to add a ParseJob for question_text and get back ParseResultGroups
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.276596
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_3_response.xml>`_

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
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
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


Step 4 - Issue an AddObject to add the Question object from the chosen ParseResultGroup
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.021862
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "713", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "766", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 5 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.055439
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "492", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
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


Step 6 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003493
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "496", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
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


Step 7 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.137176
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "496", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
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


Step 8 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.283579
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "496", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
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


Step 9 - Issue a GetResultData to start a Server Side Export and get an export_id
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.007293
* `Step 9 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_9_response.xml>`_

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
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "874", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 10 - Perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/495576641239.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.017539
* `Step 10 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_10_request.txt>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_10_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "27", 
      "content-type": "application/octet-stream"
    }


Step 11 - Perform an HTTP get to retrieve the data of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/495576641239.xml.gz
* HTTP Method: GET
* Elapsed Time: 0:00:00.023642
* `Step 11 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_11_request.txt>`_
* `Step 11 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_parsed_question_pick_first_sse_step_11_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-682-cf5be7a273cdd8f47e6946fc15781ccf6fedbc0e3dac4cd43075bb5b815e4f0a5323a5e2f84d6fce8d141a8e26c2b6467bc871845f47773ee19f275c1a244019"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-encoding": "gzip", 
      "content-length": "467", 
      "content-type": "application/octet-stream"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
