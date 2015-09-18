
Ask Manual Question Sensor With Parameters And Filter
==========================================================================================

Ask the question 'Get Folder Name Search with RegEx Match[Program Files, , No, No, Microsoft.*] containing "Shared" from all machines', wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.026226
* `Step 1 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_1_response.txt>`_

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
      "content-length": "111", 
      "content-type": "text/plain; charset=us-ascii", 
      "date": "Sat, 05 Sep 2015 05:42:31 GMT", 
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
* Elapsed Time: 0:00:00.000996
* `Step 2 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_2_response.txt>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-length": "207", 
      "content-type": "text/html; charset=iso-8859-1", 
      "date": "Sat, 05 Sep 2015 05:42:31 GMT", 
      "keep-alive": "timeout=5, max=99", 
      "server": "Apache", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 3 - Get the server version via /info.json
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:444/info.json
* HTTP Method: POST
* Elapsed Time: 0:00:00.012990
* `Step 3 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_3_request.txt>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_3_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "Content-Length": "0", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "content-length": "11245", 
      "content-type": "application/json"
    }


Step 4 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004739
* `Step 4 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "587", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5243", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:31 GMT", 
      "keep-alive": "timeout=5, max=98", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 5 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.016234
* `Step 5 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1081", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "669", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:31 GMT", 
      "keep-alive": "timeout=5, max=97", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 6 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.032395
* `Step 6 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_6_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "5528", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:31 GMT", 
      "keep-alive": "timeout=5, max=96", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 7 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003087
* `Step 7 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_7_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "703", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:31 GMT", 
      "keep-alive": "timeout=5, max=95", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 8 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004357
* `Step 8 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_8_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "703", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:36 GMT", 
      "keep-alive": "timeout=5, max=94", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 9 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004188
* `Step 9 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_9_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:41 GMT", 
      "keep-alive": "timeout=5, max=93", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 10 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003386
* `Step 10 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_10_request.xml>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_10_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:46 GMT", 
      "keep-alive": "timeout=5, max=92", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 11 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003846
* `Step 11 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_11_request.xml>`_
* `Step 11 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_11_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:51 GMT", 
      "keep-alive": "timeout=5, max=91", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 12 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003976
* `Step 12 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_12_request.xml>`_
* `Step 12 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_12_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:42:56 GMT", 
      "keep-alive": "timeout=5, max=90", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 13 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003742
* `Step 13 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_13_request.xml>`_
* `Step 13 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_13_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:01 GMT", 
      "keep-alive": "timeout=5, max=89", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 14 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003744
* `Step 14 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_14_request.xml>`_
* `Step 14 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_14_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:06 GMT", 
      "keep-alive": "timeout=5, max=88", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 15 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003480
* `Step 15 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_15_request.xml>`_
* `Step 15 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_15_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:11 GMT", 
      "keep-alive": "timeout=5, max=87", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 16 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003659
* `Step 16 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_16_request.xml>`_
* `Step 16 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_16_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:16 GMT", 
      "keep-alive": "timeout=5, max=86", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 17 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003424
* `Step 17 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_17_request.xml>`_
* `Step 17 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_17_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:21 GMT", 
      "keep-alive": "timeout=5, max=85", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 18 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004960
* `Step 18 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_18_request.xml>`_
* `Step 18 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_18_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:26 GMT", 
      "keep-alive": "timeout=5, max=84", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 19 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004205
* `Step 19 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_19_request.xml>`_
* `Step 19 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_19_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:31 GMT", 
      "keep-alive": "timeout=5, max=83", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 20 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003853
* `Step 20 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_20_request.xml>`_
* `Step 20 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_20_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "706", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:36 GMT", 
      "keep-alive": "timeout=5, max=82", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 21 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003312
* `Step 21 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_21_request.xml>`_
* `Step 21 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_21_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:41 GMT", 
      "keep-alive": "timeout=5, max=81", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 22 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003503
* `Step 22 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_22_request.xml>`_
* `Step 22 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_22_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:46 GMT", 
      "keep-alive": "timeout=5, max=80", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 23 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003567
* `Step 23 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_23_request.xml>`_
* `Step 23 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_23_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:51 GMT", 
      "keep-alive": "timeout=5, max=79", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 24 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003462
* `Step 24 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_24_request.xml>`_
* `Step 24 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_24_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "707", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:43:56 GMT", 
      "keep-alive": "timeout=5, max=78", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 25 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003819
* `Step 25 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_25_request.xml>`_
* `Step 25 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_25_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "716", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:44:01 GMT", 
      "keep-alive": "timeout=5, max=77", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 26 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003773
* `Step 26 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_26_request.xml>`_
* `Step 26 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_26_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "718", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:44:06 GMT", 
      "keep-alive": "timeout=5, max=76", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 27 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003905
* `Step 27 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_27_request.xml>`_
* `Step 27 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_27_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "721", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:44:11 GMT", 
      "keep-alive": "timeout=5, max=75", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


Step 28 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://172.16.31.128:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004016
* `Step 28 Request Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_28_request.xml>`_
* `Step 28 Response Body <../../_static/soap_outputs/6.2.314.3321/ask_manual_question_sensor_with_parameters_and_filter_step_28_response.xml>`_

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
      "session": "25-1654-94a80067fafd857c77fb770837506f0f3cbc30649785e6556cf513e0d92b0fcf532eac20784d05b48ec6c8cbf0f58d2d6a2b1b58e6c4bce23e71c8fa88ec166e"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "Keep-Alive", 
      "content-encoding": "gzip", 
      "content-length": "2491", 
      "content-type": "text/xml;charset=UTF-8", 
      "date": "Sat, 05 Sep 2015 05:44:11 GMT", 
      "keep-alive": "timeout=5, max=74", 
      "server": "Apache", 
      "strict-transport-security": "max-age=15768000", 
      "x-frame-options": "SAMEORIGIN"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
