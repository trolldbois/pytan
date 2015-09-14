
Deploy Action Simple Against Windows Computers
==========================================================================================

Deploy an action using the package 'Distribute Tanium Standard Utilities' to all computers that pass the filter Operating System, that contains Windows, wait for result data to be complete, and then get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.077209
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.017385
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "19289", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a package for inclusion in an action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.040225
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "581", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 4 - Issue a GetObject to get the full object of a sensor for inclusion in a Group for an Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.015061
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "568", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 5 - Issue an AddObject to add a list of SavedActions (6.5 logic)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.046774
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1625", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 6 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.047805
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1523", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 7 - Issue a GetObject to get the last action created for a SavedAction
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.039913
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_7_response.xml>`_

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
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 8 - Issue a GetObject to get the package for an Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.224671
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_8_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "625", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 9 - Issue a GetResultInfo on an Action to have the Server create a question that tracks the results for a Deployed Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.009453
* `Step 9 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_9_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "551", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 10 - Issue a GetObject on the package for an action to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.034797
* `Step 10 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_10_request.xml>`_
* `Step 10 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_10_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "625", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 11 - Issue a GetObject on the target_group for an action to get the full Group object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.021211
* `Step 11 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_11_request.xml>`_
* `Step 11 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_11_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "506", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 12 - ID 81: Issuing an AddObject of a Question object with no Selects and the same Group used by the Action object. The number of systems that should successfully run the Action will be taken from result_info.passed_count for the Question asked when all answers for the question have reported in.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.045384
* `Step 12 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_12_request.xml>`_
* `Step 12 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_12_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1144", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "766", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 13 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.015932
* `Step 13 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_13_request.xml>`_
* `Step 13 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_13_response.xml>`_

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
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 14 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.026569
* `Step 14 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_14_request.xml>`_
* `Step 14 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_14_response.xml>`_

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
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 15 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.110539
* `Step 15 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_15_request.xml>`_
* `Step 15 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_15_response.xml>`_

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
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 16 - Issue a GetResultInfo for a Question to check the current progress of answers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.184619
* `Step 16 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_16_request.xml>`_
* `Step 16 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_16_response.xml>`_

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
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 17 - Issue a GetObject for an Action in order to have access to the latest values for stopped_flag and status
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005867
* `Step 17 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_17_request.xml>`_
* `Step 17 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_17_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1459", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 18 - Issue a GetResultInfo for an Action to ensure fresh data is available for a GetResultData call
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.008785
* `Step 18 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_18_request.xml>`_
* `Step 18 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_18_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "551", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 19 - Issue a GetResultData with the aggregate option set to True.This will return row counts of machines that have answered instead of all the data
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.013333
* `Step 19 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_19_request.xml>`_
* `Step 19 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_19_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "625", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 20 - Issue a GetObject for an Action in order to have access to the latest values for stopped_flag and status
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.200528
* `Step 20 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_20_request.xml>`_
* `Step 20 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_20_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1459", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 21 - Issue a GetResultInfo for an Action to ensure fresh data is available for a GetResultData call
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.039954
* `Step 21 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_21_request.xml>`_
* `Step 21 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_21_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "551", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 22 - Issue a GetResultData with the aggregate option set to True.This will return row counts of machines that have answered instead of all the data
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.043147
* `Step 22 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_22_request.xml>`_
* `Step 22 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_22_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "625", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 23 - Issue a GetObject for an Action in order to have access to the latest values for stopped_flag and status
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005525
* `Step 23 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_23_request.xml>`_
* `Step 23 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_23_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1459", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 24 - Issue a GetResultInfo for an Action to ensure fresh data is available for a GetResultData call
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.065215
* `Step 24 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_24_request.xml>`_
* `Step 24 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_24_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "551", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 25 - Issue a GetResultData for an Action with the aggregate option set to False. This will return all of the Action Statuses for each computer that have run this Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.029920
* `Step 25 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_25_request.xml>`_
* `Step 25 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_25_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "579", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 26 - Issue a GetObject for an Action in order to have access to the latest values for stopped_flag and status
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.050392
* `Step 26 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_26_request.xml>`_
* `Step 26 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_26_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1459", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 27 - Issue a GetResultInfo for an Action to ensure fresh data is available for a GetResultData call
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004834
* `Step 27 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_27_request.xml>`_
* `Step 27 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_27_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "551", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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


Step 28 - Issue a GetResultData for an Action with the aggregate option set to False. This will return all of the Action Statuses for each computer that have run this Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.006135
* `Step 28 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_28_request.xml>`_
* `Step 28 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_against_windows_computers_step_28_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "579", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-622-6eb3cc08a054104d45ce22051218b6125b034ddf0b2ff434de00794bde0e9da84c187596a64635b64fd54cf79b9bc279adfc3e6206a24f7e9a5d6fd86bc6c31a"
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
