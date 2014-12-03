pytan.handler module
====================

.. automodule:: pytan.handler

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
.. automethod:: pytan.handler.Handler.ask_manual_human

Deploy an Action
***************************************************************

.. automethod:: pytan.handler.Handler.deploy_action
.. automethod:: pytan.handler.Handler.deploy_action_human
.. automethod:: pytan.handler.Handler.deploy_action_asker

Stopping an Action
***************************************************************

.. automethod:: pytan.handler.Handler.stop_action

------------


Handler Methods: Exporting/Importing Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Import an API Object from JSON
***************************************************************

.. automethod:: pytan.handler.Handler.create_from_json

Load a Python Object from JSON
***************************************************************

.. automethod:: pytan.handler.Handler.load_api_from_json

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

------------


Handler Methods: Deleting Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Delete an Object
***************************************************************

.. automethod:: pytan.handler.Handler.delete


------------


Handler Methods: Getting Objects
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Get Single or Multiple Objects of a type
***************************************************************

.. automethod:: pytan.handler.Handler.get

Get All Objects of a type
***************************************************************

.. automethod:: pytan.handler.Handler.get_all


------------


Handler Methods: Private Methods
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. automethod:: pytan.handler.Handler._find
.. automethod:: pytan.handler.Handler._get_multi
.. automethod:: pytan.handler.Handler._get_single
.. automethod:: pytan.handler.Handler._single_find
.. automethod:: pytan.handler.Handler._get_sensor_defs
.. automethod:: pytan.handler.Handler._get_package_def
.. automethod:: pytan.handler.Handler._export_class_BaseType
.. automethod:: pytan.handler.Handler._export_class_ResultSet
.. automethod:: pytan.handler.Handler._export_format_csv
.. automethod:: pytan.handler.Handler._export_format_json
.. automethod:: pytan.handler.Handler._export_format_xml
