only required arguments should be in function/method signature
use kwargs.get('right', []) for all optional arguments
keep kwargs.get() at top of function
line length limit = 100
fully pep8/flake compliant (with NO messages disabled)
doc string on everything
use .format for string formatting
use 3 lines to format a string: line 1: m = "text", line 2: m = m.format(), line 3: print m
use m for log message strings
use err for err message strings
avoid nested returns
