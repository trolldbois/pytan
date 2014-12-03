Welcome to PyTan's documentation!
=================================

PyTan is comprised of 3 parts:
  * Tanium Server SOAP API: The SOAP server embedded into the Tanium server itself, listens on port 444 but is also available via port 443.
  * TaniumPy (:mod:`api`): A python package comprised of a set of python objects automatically generated from the WSDL file that describes the Tanium SOAP API. These python objects handle the serialization and deserialization of XML to and from the Tanium Server SOAP API. Located in ``pytan/``
  * PyTan: (:mod:`pytan`): A python package that provides a set of methods to make interfacing with TaniumPy more human friendly. Located in ``pytan/api/``

Contents:

.. toctree::
   :maxdepth: 6
   :numbered:

   PyTan package: An API wrapper around TaniumPy, the api package. <pytan/pytan>
   TaniumPy - The api package: An XML serializer/deserializer for Taniums SOAP API <pytan/api/api>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

