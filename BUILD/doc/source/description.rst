Description
=================

This is a set of packages and scripts that provides a simple way for programmatically interfacing with Tanium's SOAP API. It is comprised of four parts:

    * Tanium Server SOAP API: The SOAP server embedded into the Tanium server itself, listens on port 444 but is also available via port 443.
    * TaniumPy Python Package (:mod:`taniumpy`): A python package comprised of a set of python objects automatically generated from the WSDL file that describes the Tanium SOAP API. These python objects handle the serialization and deserialization of XML to and from the Tanium Server SOAP API. Located in ``lib/taniumpy``
    * PyTan Python Package: (:mod:`pytan`): A python package that provides a set of methods to make interfacing with TaniumPy more human friendly. Located in ``lib/pytan``
    * PyTan Command Line Scripts: A set of command line scripts that utilize the PyTan Package (:mod:`pytan`) to make it easy for non-programmers to create/get/delete/ask/deploy objects via the Tanium Server SOAP API.

Why it was created
=====================

This was created to solve for the following needs:

    - Create a python package (:mod:`pytan`) to provide a set of methods for making it easier to programmatically interface with Tanium via the SOAP API.
    - Create a set of command line scripts utilizing the :mod:`pytan` package that handle the argument parsing, thereby providing non-programmers with command line access to the functionality therein.
    - Provide a way to ask questions and get results via Python and/or the command line.
    - Provide a way to deploy actions and get results via Python and/or the command line.
    - Provide a way to export/import objects in JSON via Python and/or the command line.

Requirements
============
    -  Python 2.7: To date PyTan has only been qualified against 2.7.6 and 2.7.9 on Mac/Linux/Windows.
    -  A working install of Tanium Server 6.2: To date PyTan has only been qualified against 6.2.X versions of Tanium. It does not yet run against 6.5.X versions.

Installation
============

Windows Installation
    * Download Python 2.7 from https://www.python.org/downloads/windows/
    * Install Python 2.7 -- if you accept the default paths it will install to ``C:\Python27``
    * Copy PyTan from github to your local machine somewhere
    * If you did not accept the default install path for Python 2.7, edit ``pytan\winbin\CONFIG.bat`` to change the *PYTHON* variable to point to the full path of *python.exe*

OS X Installation
    * OS X 10.8 and higher come with Python 2.7 out of the box
    * Copy PyTan from github to your local machine somewhere

Linux Installation
    * Ensure Python 2.7 is installed
    * Ensure the first *python* binary in your path points to your Python 2.7 installation
    * Copy PyTan from github to your local machine somewhere

Usage
============

    * For command line usage, refer to `Command Line Help Index <_static/bin_doc/index.html>`_
    * For API Examples, refer to the :doc:`examples/pytan_examples`
    * For in depth API Documentation, refer to the :doc:`pytan`, especially the :doc:`pytan.handler`

Directory Layout
================

    * **EXAMPLES/ directory**: contains a set of example python files that show how to use the various methods exposed by (:mod:`pytan`)
    * **BUILD/ directory**: contains the scripts that build the HTML and PDF documentation in doc/, generate the (:mod:`taniumpy`), generate the python examples in EXAMPLES/, generate some of the command line scripts in bin/, and generate all of the documentation for the command line scripts in doc/_static/bin_doc
    * **bin/ directory**: contains all of the command line scripts that utilize the (:mod:`pytan`)
    * **doc/ directory**: contains the HTML and PDF documentation
    * **lib/ directory**: contains the python libraries (:mod:`pytan`) and (:mod:`taniumpy`), as well as other python libraries
    * **test/ directory**: contains the unit and functional tests for (:mod:`pytan`)
    * **winbin/ directory**: contains the Windows batch scripts which wrap around the python command line scripts in bin/
    * **ZIP_DIST/ directory**: contains standalone windows executables for certain tools, created by batch files in BUILD/STATICWINBUILD/
