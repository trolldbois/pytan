
Create Whitelisted Url From JSON
==========================================================================================

Get a whitelisted url object, add ' API TEST' to the url_regex of the whitelisted url object, delete any pre-existing whitelisted url with the new url_regex, then create a new whitelisted url object with the new url_regex


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.050520
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.013842
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-618-f573d43c4fa5f4dd8134a1c3f8cbd8c28e6e2be54428f252099a6b66fb7b88dc9de60c5b17a4e71f5aa5ab992931317756bf1af1497e607cd7b9406f15d7f56a"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "19291", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.327725
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "480", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-618-f573d43c4fa5f4dd8134a1c3f8cbd8c28e6e2be54428f252099a6b66fb7b88dc9de60c5b17a4e71f5aa5ab992931317756bf1af1497e607cd7b9406f15d7f56a"
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


Step 4 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.004698
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "480", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-618-f573d43c4fa5f4dd8134a1c3f8cbd8c28e6e2be54428f252099a6b66fb7b88dc9de60c5b17a4e71f5aa5ab992931317756bf1af1497e607cd7b9406f15d7f56a"
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


Step 5 - Issue a DeleteObject to delete an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.048635
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "535", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-618-f573d43c4fa5f4dd8134a1c3f8cbd8c28e6e2be54428f252099a6b66fb7b88dc9de60c5b17a4e71f5aa5ab992931317756bf1af1497e607cd7b9406f15d7f56a"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "950", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 6 - Issue an AddObject to add an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.009301
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "575", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-618-f573d43c4fa5f4dd8134a1c3f8cbd8c28e6e2be54428f252099a6b66fb7b88dc9de60c5b17a4e71f5aa5ab992931317756bf1af1497e607cd7b9406f15d7f56a"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "862", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 7 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003909
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_from_json_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "586", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-618-f573d43c4fa5f4dd8134a1c3f8cbd8c28e6e2be54428f252099a6b66fb7b88dc9de60c5b17a4e71f5aa5ab992931317756bf1af1497e607cd7b9406f15d7f56a"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "833", 
      "content-type": "text/xml;charset=UTF-8"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
