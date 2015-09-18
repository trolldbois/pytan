
Create Whitelisted Url
==========================================================================================

Create a whitelisted url


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.047244
* `Step 1 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_1_request.txt>`_
* `Step 1 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.013061
* `Step 2 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_2_request.txt>`_
* `Step 2 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-611-275a13394bf5c20daa898559d19e2388ea12601e887e9f31e516a3e864e5d709eb5fe87b933fd000df313bd00fe750fa208c49fbcde3bf7ce6304a99b938c562"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "19289", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003514
* `Step 3 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_3_request.xml>`_
* `Step 3 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_3_response.xml>`_

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
      "session": "1-611-275a13394bf5c20daa898559d19e2388ea12601e887e9f31e516a3e864e5d709eb5fe87b933fd000df313bd00fe750fa208c49fbcde3bf7ce6304a99b938c562"
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


Step 4 - Issue an AddObject to add a WhitelistedURL object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.279121
* `Step 4 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_4_request.xml>`_
* `Step 4 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_4_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "698", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-611-275a13394bf5c20daa898559d19e2388ea12601e887e9f31e516a3e864e5d709eb5fe87b933fd000df313bd00fe750fa208c49fbcde3bf7ce6304a99b938c562"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "1016", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 5 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.005018
* `Step 5 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_5_request.xml>`_
* `Step 5 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "735", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-611-275a13394bf5c20daa898559d19e2388ea12601e887e9f31e516a3e864e5d709eb5fe87b933fd000df313bd00fe750fa208c49fbcde3bf7ce6304a99b938c562"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "987", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 6 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003609
* `Step 6 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_6_request.xml>`_
* `Step 6 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_6_response.xml>`_

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
      "session": "1-611-275a13394bf5c20daa898559d19e2388ea12601e887e9f31e516a3e864e5d709eb5fe87b933fd000df313bd00fe750fa208c49fbcde3bf7ce6304a99b938c562"
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


Step 7 - Issue a DeleteObject to delete an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.033705
* `Step 7 Request Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_7_request.xml>`_
* `Step 7 Response Body <../../_static/soap_outputs/6.5.314.4301/create_whitelisted_url_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "684", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.7.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-611-275a13394bf5c20daa898559d19e2388ea12601e887e9f31e516a3e864e5d709eb5fe87b933fd000df313bd00fe750fa208c49fbcde3bf7ce6304a99b938c562"
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
