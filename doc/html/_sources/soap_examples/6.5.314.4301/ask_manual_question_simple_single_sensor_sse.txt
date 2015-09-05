
Ask Manual Question Simple Single Sensor Sse
==========================================================================================

Ask the question 'Get Computer Name from all machines', wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.015166
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_1_response.txt>`_

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
      "content-length": "135", 
      "content-type": "text/plain; charset=us-ascii"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.015534
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "113371", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003905
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "565", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
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


Step 4 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.009822
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "639", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "769", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 5 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.015708
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "494", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
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
* Elapsed Time: 0:00:00.002169
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
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
* Elapsed Time: 0:00:00.003279
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
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


Step 8 - Issue a GetResultData to start a Server Side Export and get an export_id
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003297
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "558", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "877", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 9 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494746930877.xml.status
* HTTP Method: GET
* Elapsed Time: 0:00:00.002575
* `Step 9 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_9_request.txt>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_9_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "27", 
      "content-type": "application/octet-stream"
    }


Step 10 - perform an HTTP get to retrieve the status of a server side export
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/export/1/494746930877.xml.gz
* HTTP Method: GET
* Elapsed Time: 0:00:00.002984
* `Step 10 Request Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_10_request.txt>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.5.314.4301/ask_manual_question_simple_single_sensor_sse_step_10_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-8123-bc10deab6ff38bb19ae2f1de584d2b661a1a94091d873c58f98168842d9a4bd9c8f44de946b485015cbf15bd964577a81bd6017c9e01eebf7ebdd1482d5727af"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-encoding": "gzip", 
      "content-length": "187", 
      "content-type": "application/octet-stream"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
