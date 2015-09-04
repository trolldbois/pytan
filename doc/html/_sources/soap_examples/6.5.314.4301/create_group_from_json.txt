
Create Group From JSON
==========================================================================================

Get a group object, add ' API TEST' to the name of the group object, delete any pre-existing group with the new name, then create a new group object with the new name


Step 1 - Authenticate to the SOAP API via /auth
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/auth
* HTTP Method: GET
* Elapsed Time: 0:00:00.008859
* `Step 1 Request Body <../_static/soap_outputs/create_group_from_json_step_1_request.txt>`_
* `Step 1 Response Body <../_static/soap_outputs/create_group_from_json_step_1_response.txt>`_

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
* Elapsed Time: 0:00:00.014108
* `Step 2 Request Body <../_static/soap_outputs/create_group_from_json_step_2_request.txt>`_
* `Step 2 Response Body <../_static/soap_outputs/create_group_from_json_step_2_response.json>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Connection": "keep-alive", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6923-1b5896b8960f90f883e294e107cd909333673f42fa0e820a1e58cd246a1e64db99db50b01c7aa28a04b509600b3196b17bcc668b8dd4062b8b0a7d8e6d1dd459"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "86180", 
      "content-type": "application/json"
    }


Step 3 - Issue a GetObject to find an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.003172
* `Step 3 Request Body <../_static/soap_outputs/create_group_from_json_step_3_request.xml>`_
* `Step 3 Response Body <../_static/soap_outputs/create_group_from_json_step_3_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "517", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6923-1b5896b8960f90f883e294e107cd909333673f42fa0e820a1e58cd246a1e64db99db50b01c7aa28a04b509600b3196b17bcc668b8dd4062b8b0a7d8e6d1dd459"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "941", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 4 - Issue a GetObject to find the object to be deleted
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.001771
* `Step 4 Request Body <../_static/soap_outputs/create_group_from_json_step_4_request.xml>`_
* `Step 4 Response Body <../_static/soap_outputs/create_group_from_json_step_4_response.xml>`_

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
      "session": "1-6923-1b5896b8960f90f883e294e107cd909333673f42fa0e820a1e58cd246a1e64db99db50b01c7aa28a04b509600b3196b17bcc668b8dd4062b8b0a7d8e6d1dd459"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "952", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 5 - Issue a DeleteObject to delete an object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.002377
* `Step 5 Request Body <../_static/soap_outputs/create_group_from_json_step_5_request.xml>`_
* `Step 5 Response Body <../_static/soap_outputs/create_group_from_json_step_5_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "620", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6923-1b5896b8960f90f883e294e107cd909333673f42fa0e820a1e58cd246a1e64db99db50b01c7aa28a04b509600b3196b17bcc668b8dd4062b8b0a7d8e6d1dd459"
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
* Elapsed Time: 0:00:00.003491
* `Step 6 Request Body <../_static/soap_outputs/create_group_from_json_step_6_request.xml>`_
* `Step 6 Response Body <../_static/soap_outputs/create_group_from_json_step_6_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "658", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6923-1b5896b8960f90f883e294e107cd909333673f42fa0e820a1e58cd246a1e64db99db50b01c7aa28a04b509600b3196b17bcc668b8dd4062b8b0a7d8e6d1dd459"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "762", 
      "content-type": "text/xml;charset=UTF-8"
    }


Step 7 - Issue a GetObject on the recently added object in order to get the full object
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

* URL: https://10.0.1.240:443/soap
* HTTP Method: POST
* Elapsed Time: 0:00:00.014759
* `Step 7 Request Body <../_static/soap_outputs/create_group_from_json_step_7_request.xml>`_
* `Step 7 Response Body <../_static/soap_outputs/create_group_from_json_step_7_response.xml>`_

* Request Headers:

.. code-block:: json
    :linenos:

    
    {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip", 
      "Connection": "keep-alive", 
      "Content-Length": "487", 
      "Content-Type": "text/xml; charset=utf-8", 
      "User-Agent": "python-requests/2.6.0 CPython/2.7.10 Darwin/14.5.0", 
      "session": "1-6923-1b5896b8960f90f883e294e107cd909333673f42fa0e820a1e58cd246a1e64db99db50b01c7aa28a04b509600b3196b17bcc668b8dd4062b8b0a7d8e6d1dd459"
    }

* Response Headers:

.. code-block:: json
    :linenos:

    
    {
      "connection": "keep-alive", 
      "content-length": "934", 
      "content-type": "text/xml;charset=UTF-8"
    }


.. rubric:: Footnotes

.. [#] this file automatically created by BUILD/build_api_examples.py
