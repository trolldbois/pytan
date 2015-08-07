pytan.handler module
====================

.. automodule:: pytan.handler

Handler Class
-------------

.. autoclass:: pytan.handler.Handler
    :show-inheritance:

Example: Create a Handler object
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Setup a Handler() object::

    >>> import sys
    >>> sys.path.append('/path/to/pytan/')
    >>> import pytan
    >>> handler = pytan.Handler('username', 'password', 'host')



------------


Handler Methods: Questions and Actions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Ask a Question
***************************************************************

.. automethod:: pytan.handler.Handler.ask

Ask a Saved Question
***************************************************************

.. automethod:: pytan.handler.Handler.ask_saved

Asking a Manual Question
***************************************************************

.. automethod:: pytan.handler.Handler.ask_manual

Deploy an Action
***************************************************************

.. automethod:: pytan.handler.Handler.deploy_action

Stopping an Action
***************************************************************

.. automethod:: pytan.handler.Handler.stop_action

------------


Handler Methods: Exporting/Importing Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Import an API Object from JSON
***************************************************************

.. automethod:: pytan.handler.Handler.create_from_json

Export Object
***************************************************************

.. automethod:: pytan.handler.Handler.export_obj

Export Object to Report File
***************************************************************

.. automethod:: pytan.handler.Handler.export_to_report_file

------------


Handler Methods: Creating Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Create a Group
***************************************************************

.. automethod:: pytan.handler.Handler.create_group

Create a Package
***************************************************************

.. automethod:: pytan.handler.Handler.create_package

Create a Sensor
***************************************************************

.. automethod:: pytan.handler.Handler.create_sensor

Create a User
***************************************************************

.. automethod:: pytan.handler.Handler.create_user

Create a Whitelisted URL
***************************************************************

.. automethod:: pytan.handler.Handler.create_whitelisted_url

Create a Dashboard
***************************************************************

.. automethod:: pytan.handler.Handler.create_dashboard


------------


Handler Methods: Deleting Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Delete an Object
***************************************************************

.. automethod:: pytan.handler.Handler.delete

Delete a Dashboard
***************************************************************

.. automethod:: pytan.handler.Handler.delete_dashboard


------------


Handler Methods: Getting Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Get Single or Multiple Objects of a type
***************************************************************

.. automethod:: pytan.handler.Handler.get

Get All Objects of a type
***************************************************************

.. automethod:: pytan.handler.Handler.get_all

Get Dashboards
***************************************************************

.. automethod:: pytan.handler.Handler.get_dashboards


------------


Handler Methods: Getting Result Data / Result Info
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. automethod:: pytan.handler.Handler.get_result_data
.. automethod:: pytan.handler.Handler.get_result_info


------------


Handler Methods: Plugins
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. automethod:: pytan.handler.Handler.run_plugin


Handler Methods: Private Methods
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. automethod:: pytan.handler.Handler._add
.. automethod:: pytan.handler.Handler._ask_manual
.. automethod:: pytan.handler.Handler._deploy_action
.. automethod:: pytan.handler.Handler._derive_server_version
.. automethod:: pytan.handler.Handler._export_class_BaseType
.. automethod:: pytan.handler.Handler._export_class_ResultSet
.. automethod:: pytan.handler.Handler._export_format_csv
.. automethod:: pytan.handler.Handler._export_format_json
.. automethod:: pytan.handler.Handler._export_format_xml
.. automethod:: pytan.handler.Handler._find
.. automethod:: pytan.handler.Handler._get_multi
.. automethod:: pytan.handler.Handler._get_package_def
.. automethod:: pytan.handler.Handler._get_sensor_defs
.. automethod:: pytan.handler.Handler._get_single
.. automethod:: pytan.handler.Handler._single_find

.. toctree::
