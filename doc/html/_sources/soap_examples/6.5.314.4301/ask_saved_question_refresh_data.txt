
Ask Saved Question Refresh Data
==========================================================================================

Get the Saved Question object for Installed Applications, ask the server to refresh the data vailable, wait for the new question spawned to complete results, then get the latest result data available for that Saved Question


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.006322
* `Step 1 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.014431
* `Step 2 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "88325", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find saved question objects
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.013249
* `Step 3 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "527", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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
* Elapsed Time: 0:00:00.003820
* `Step 4 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "21616", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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


Step 5 - Issue a GetResultInfo for a saved question in order to issue a new question, which refreshes the data for that saved question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.006532
* `Step 5 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "542", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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


Step 6 - Issue a GetObject for the saved question in order get the ID of the newly asked question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005835
* `Step 6 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_6_request.xml>`_
* `Step 6 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "538", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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


Step 7 - Issue a GetObject to get the full object of the last question asked by a saved question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002829
* `Step 7 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_7_request.xml>`_
* `Step 7 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "942", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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
* Elapsed Time: 0:00:00.001634
* `Step 8 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_8_request.xml>`_
* `Step 8 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_8_response.xml>`_

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
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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
* Elapsed Time: 0:00:00.002004
* `Step 9 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_9_request.xml>`_
* `Step 9 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_9_response.xml>`_

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
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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
* Elapsed Time: 0:00:00.002525
* `Step 10 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_10_request.xml>`_
* `Step 10 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_10_response.xml>`_

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
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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


Step 11 - Issue a GetResultData to get the answers for the last asked question of this saved question
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004172
* `Step 11 Request Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_11_request.xml>`_
* `Step 11 Response Body <../_static/soap_outputs/ask_saved_question_refresh_data_step_11_response.xml>`_

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
      "session": "1-7000-0b3a77745c282aea1f47fc9b35ea6d94e18e7f95336eb79657a3b449756d4ce45f272fff7ec4e30a8b8e4e86b07c39ed8122c70a7695dc18afbc0603d9c885c8"
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
