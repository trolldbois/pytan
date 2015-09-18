
Deploy Action Simple Without Results
==========================================================================================

Deploy an action using the package 'Distribute Tanium Standard Utilities' to all computers and do not wait for result data to be complete and do not get result data


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.321828
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.035296
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "19290", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to get the full object of a package for inclusion in an action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.037010
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_3_response.xml>`_

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
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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


Step 4 - Issue an AddObject to add a list of SavedActions (6.5 logic)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.030735
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1443", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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


Step 5 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.025474
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "1521", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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


Step 6 - Issue a GetObject to get the last action created for a SavedAction
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005034
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_6_response.xml>`_

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
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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


Step 7 - Issue a GetObject to get the package for an Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.283089
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_7_response.xml>`_

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
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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


Step 8 - Issue a GetResultInfo on an Action to have the Server create a question that tracks the results for a Deployed Action
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.013982
* `Step 8 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_8_request.xml>`_
* `Step 8 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_8_response.xml>`_

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
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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


Step 9 - Issue a GetObject on the package for an action to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.040974
* `Step 9 Request Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_9_request.xml>`_
* `Step 9 Response Body <../../_static/soap_outputs/6.5.314.4301/deploy_action_simple_without_results_step_9_response.xml>`_

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
      "session": "1-621-afb1d46105ffaaab5496cad137052128d03cb870720f6c9bad352df1ecac743870c7fd897d5bef5363117902bcaced8b9277ada93fea0aa823585b53141797e6"
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
