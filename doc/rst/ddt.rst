
ddt module
**********

**ddt.data(*values)**

   Method decorator to add to your test methods.

   Should be added to methods of instances of ``unittest.TestCase``.

**ddt.ddt(cls)**

   Class decorator for subclasses of ``unittest.TestCase``.

   Apply this decorator to the test case class, and then decorate test
   methods with ``@data``.

   For each method decorated with ``@data``, this will effectively
   create as many methods as data items are passed as parameters to
   ``@data``.

   The names of the test methods follow the pattern
   ``original_test_name_{ordinal}_{data}``. ``ordinal`` is the
   position of the data argument, starting with 1.

   For data we use a string representation of the data value converted
   into a valid python identifier.  If ``data.__name__`` exists, we
   use that instead.

   For each method decorated with ``@file_data('test_data.json')``,
   the decorator will try to load the test_data.json file located
   relative to the python file containing the method that is
   decorated. It will, for each ``test_name`` key create as many
   methods in the list of values from the ``data`` key.

**ddt.file_data(value)**

   Method decorator to add to your test methods.

   Should be added to methods of instances of ``unittest.TestCase``.

   ``value`` should be a path relative to the directory of the file
   containing the decorated ``unittest.TestCase``. The file should
   contain JSON encoded data, that can either be a list or a dict.

   In case of a list, each value in the list will correspond to one
   test case, and the value will be concatenated to the test method
   name.

   In case of a dict, keys will be used as suffixes to the name of the
   test case, and values will be fed as test data.

**ddt.is_hash_randomized()**

**ddt.mk_test_name(name, value, index=0)**

   Generate a new name for a test case.

   It will take the original test name and append an ordinal index and
   a string representation of the value, and convert the result into a
   valid python identifier by replacing extraneous characters with
   ``_``.

   If hash randomization is enabled (a feature available since
   2.7.3/3.2.3 and enabled by default since 3.3) and a "non-trivial"
   value is passed this will omit the name argument by default. Set
   *PYTHONHASHSEED* to a fixed value before running tests in these
   cases to get the names back consistently or use the *__name__*
   attribute on data values.

   A "trivial" value is a plain scalar, or a tuple or list consisting
   only of trivial values.

**ddt.unpack(func)**

   Method decorator to add unpack feature.
