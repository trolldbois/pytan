# Using PyTan to test a Tanium install

## Download PyTan

  1. Clone the github repository from https://github.com/tanium/pytan

 .. or ..

  1. Go to https://github.com/tanium/pytan
  2. Click the "Download ZIP" button
  3. Extract the ZIP to somewhere on your system (i.e. C:\pytan)

## Install Python

  1. Not needed for Linux or Mac systems.
  2. On Windows, download the latest Python 2.7 version from https://www.python.org/downloads/  
  3. Install to the default path, all default options

## Edit test/API_INFO.py

  1. Open the file C:\pytan\pytan-master\test\API-INFO.py for editing
  2. Change username, password, and host to match your Tanium install

## Run test/test_pytan_valid_server_tests.py
  1. On Mac or Linux, just cd to where you extracted pytan to, and run test/test_pytan_valid_server_tests.py
  2. On Windows, you will need to run the test_pytan_valid_server_tests.py with the python binary, like so:
  ```
C:\Python27\python.exe c:\pytan\pytan-master\test\test_pytan_valid_server_tests.py
  ```
  3. Any non-zero exit code indicates failure
