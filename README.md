# Table of Contents
 * [What is it](#what-is-it)
 * [How do I install it](#how-do-i-install-it)
  * [Windows Installation](#windows-installation)
  * [OS X Installation](#os-x-installation)
  * [Linux Installation](#linux-installation)
 * [How do I use it](#how-do-i-use-it)

# What is it

PyTan was created to solve for the following needs:
  1. Create a python library to provide an easy set of methods for programmatically interfacing with Tanium via the SOAP API
  2. Create a set of command line scripts that utilize the python library that handle the argument parsing, thereby providing non-python users with command line access to the functionality provided by the methods inside of the python library

[TOC](#table-of-contents)

# How do I install it

To date, this has only been tested on OS X 10.10 and Windows 2008 R2.

## Windows Installation
  * Download Python 2.7 from https://www.python.org/downloads/release/python-278/
  * Install Python 2.7 -- if you accept the default paths it will install to C:\Python27
  * Copy this distro to your local machine somewhere
  * If you did not accept the default install path for Python 2.7, edit ```pytan\winbin\CONFIG.bat``` to change the *PYTHON* variable to point to the full path of *python.exe*
  
## OS X Installation
  * OS X 10.8 and higher come with Python 2.7 out of the box
  * Copy this distro to your local machine somewhere

## Linux Installation
  * Ensure Python 2.7 is installed
  * Ensure the first *python* binary in your path points to your Python 2.7 installation
  * Copy this distro to your local machine somewhere

[TOC](#table-of-contents)

# How do I use it

[TOC](#table-of-contents)
