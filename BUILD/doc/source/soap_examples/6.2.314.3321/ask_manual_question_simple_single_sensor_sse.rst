
Ask Manual Question Simple Single Sensor Sse
==========================================================================================

Ask the question 'Get Computer Name from all machines', wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.017374
* `Step 1 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_1_response.txt>`_

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
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "110", 
      "content-type": "text/plain; charset=us-ascii", 
      "date": "Sat, 05 Sep 2015 05:36:43 GMT", 
      "keep-alive": "timeout=5, max=100", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "vary": "Accept-Encoding", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 2 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/info.json
* HTTP Method: GET
* Elapsed Time: 0:00:00.001257
* `Step 2 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_2_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-length": "207", 
      "content-type": "text/html; charset=iso-8859-1", 
      "date": "Sat, 05 Sep 2015 05:36:43 GMT", 
      "keep-alive": "timeout=5, max=99", 
      "server": "Apache", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 3 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:444/info.json
* HTTP Method: POST
* Elapsed Time: 0:00:00.014372
* `Step 3 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_3_request.txt>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_3_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "Content-Length": "0", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "11011", 
      "content-type": "application/json"
    }


Step 4 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004925
* `Step 4 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_4_response.xml>`_

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
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "788", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:43 GMT", 
      "keep-alive": "timeout=5, max=98", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 5 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.011706
* `Step 5 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_5_response.xml>`_

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
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "494", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:43 GMT", 
      "keep-alive": "timeout=5, max=97", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "vary": "Accept-Encoding", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 6 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.012991
* `Step 6 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "493", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "1204", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:43 GMT", 
      "keep-alive": "timeout=5, max=96", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 7 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003373
* `Step 7 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "705", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:43 GMT", 
      "keep-alive": "timeout=5, max=95", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 8 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003404
* `Step 8 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "718", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:48 GMT", 
      "keep-alive": "timeout=5, max=94", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 9 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003535
* `Step 9 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_9_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "497", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "718", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:53 GMT", 
      "keep-alive": "timeout=5, max=93", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 10 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003386
* `Step 10 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_10_request.xml>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_simple_single_sensor_sse_step_10_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "525", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1647-2bc8b8ac45c72b79b674e7e181baba6fec6db84ab55ee4e68da61c924f0515e36f2a49d131042da365284b55e16b4398823f63c3a6bb22397312bd9ad40de887"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "864", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:36:53 GMT", 
      "keep-alive": "timeout=5, max=92", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
