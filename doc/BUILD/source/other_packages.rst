Other Packages
==================================

PyTan relies on a number of python packages to function properly. All dependencies are bundled with PyTan in order to make it easier for the user to start using PyTan right away.

requests Package
----------------

PyTan uses requests for all HTTP requests in order to get automatic keep alive support, session tracking, and a host of other things. requests is an open source package maintained at: https://github.com/kennethreitz/requests

.. automodule:: requests
    :show-inheritance:
    :members:
    :undoc-members:
    :private-members:

threaded_http Package
---------------------

PyTan uses threaded_http to create a fake HTTP server on localhost for the invalid server functional tests (see: :mod:`pytan.test_pytan_invalid_server_tests`). threaded_http is developed and maintained by Tanium.

.. automodule:: threaded_http
    :show-inheritance:
    :members:
    :undoc-members:
    :private-members:

xmltodict Package
-----------------

PyTan uses xmltodict for pretty printing XML documents (see: :func:`pytan.utils.xml_pretty`). xmltodict is an open source package maintained at: https://github.com/martinblech/xmltodict

.. automodule:: xmltodict
    :show-inheritance:
    :members:

ddt Package
-----------

PyTan uses ddt for creating automatically generating test cases from JSON files (see: :mod:`pytan.test_pytan_valid_server_tests`). ddt is an open source package maintained at: https://github.com/txels/ddt

.. automodule:: ddt
    :show-inheritance:
    :members:
    :undoc-members:
    :private-members:

pyreadline Package
------------------

PyTan uses pyreadline for providing tab completion within pytan_shell.py/.bat on Windows (see: :class:`pytan.binsupport.HistoryConsole`). pyreadline is stored in winlb/ instead of lib/ since it should only be imported on Windows. pyreadline is an open source package maintained at: https://pypi.python.org/pypi/pyreadline/2.0

