
Basic API Authentication
==========================================================================================

This is an example for how to authenticate against the SOAP API


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.005930
* `Step 1 Request Body <../_static/soap_outputs/basic_api_authentication_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/basic_api_authentication_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.013502
* `Step 2 Request Body <../_static/soap_outputs/basic_api_authentication_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/basic_api_authentication_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6911-da6e5b707595c7b5e42d4738029d5c97256bb813fc843855cb9c675c54dacb06c8153557fb60ea17bb11354344f58e242fd776fe0a417ba7007d37328f41ba83"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "86180", 
      "content-type": "application/json"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
