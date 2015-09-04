
Ask Manual Question Complex Query2
==========================================================================================

Ask the question 'Get Computer Name and Last Logged In User and Installed Applications containing "Google (Search|Chrome)" from all machines with Installed Applications containing "Google (Search|Chrome)"' and set ignore_case_flag to 1 and or_flag to 1 on the Installed Applications sensors on the right hand side of the question, then wait for result data to be complete, and get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.007472
* `Step 1 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.014728
* `Step 2 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "88223", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002128
* `Step 3 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "565", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 4 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002414
* `Step 4 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "571", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 5 - Issue a GetObject to get the full object of a sensor for inclusion in a Select for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002335
* `Step 5 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "574", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 6 - Issue a GetObject to get the full object of a sensor for inclusion in a Group for a Question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002212
* `Step 6 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_6_request.xml>`_
* `Step 6 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "574", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 7 - Issue an AddObject to add a Question object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.012807
* `Step 7 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_7_request.xml>`_
* `Step 7 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1174", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "769", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 8 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.012531
* `Step 8 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_8_request.xml>`_
* `Step 8 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "494", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 9 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001716
* `Step 9 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_9_request.xml>`_
* `Step 9 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_9_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 10 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001635
* `Step 10 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_10_request.xml>`_
* `Step 10 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_10_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 11 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002136
* `Step 11 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_11_request.xml>`_
* `Step 11 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_11_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "498", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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


Step 12 - Issue a GetResultData to get answers for a question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001741
* `Step 12 Request Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_12_request.xml>`_
* `Step 12 Response Body <../_static/soap_outputs/ask_manual_question_complex_query2_step_12_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "526", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6998-ec9c0cc41fcb67257e819c5c8f1ff7f7dc5028d8ee80f6d3ccc0d53f196486a1ed62c4b1f4f045a506fa8ad916cae7ca570d010da49cdf908e14e68e2f2cb2b8"
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
