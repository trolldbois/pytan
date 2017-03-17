# This is not a runnable py file. This is essentially pseudocode. Delete file
# after it has been included in the main py file, replacing the 10 minute dump logic.

# the overarching goal, which is not really fully encapsulated by this code, is to
# run a question continually. When it is about to expire, re-run it. The question
# contains data from endpoints that will augment bro's conn.log. The trick here is
# to only send data that we haven't already seen to Bro via broker.
# The way to do this is to examine the row id in the question's result data. The
# row id will be a unique number for each answer line from endpoints.
# An obvious solution is to use a python 'set' as an O(1) lookup table for row IDs.
# There would be no need to keep the answer data corresponding to the row ID as the
# dictionary value, so a set is probably ideal.


# if the question is re-run because it expired, the question would have a new question
# ID and so the row ids are no longer going to be uniquely identifying data compared to
# the last run. In this case, clear the set and start filling anew.

# this is the pseudo-code as-is, given by Jim O, for streaming question data via
# use of the callback. Note that Jim's code would not work for a 'set' type, the code
# uses an .append method instead of an .add method of a set. Investigate whether
# it would make more sense to use set methods like 'update' to do the work in bulk,
# eliminating the need to check if it's in the set explicitly.

# - use a callback function that is custom written to take poller, pct, and kwargs
# - pass in as one of the kwargs to ask_parsed/manual/whatever a "set" of row-id's
#  already known by bro (fetch this somehow)
#- in the callback function, do something like this (pseudo code):

                def callback_to_add_bro_data(bro_info, row):
                    # bro_server/bro_host/bro_whatever??? or even a pre-existing bro connection??
                    # get that from bro_info

                    # whatever the call is on the bro_server to add the data here:
                    bro_server.add_data(row)


                def cb1(poller, pct, **kwargs):
                    # print pct
                    # print kwargs

                    known_result_ids = kwargs.get("known_result_ids", [])
                    bro_info = kwargs.get("bro_info", {})

                    rd = poller.get_result_data()

                    try:
                        print handler.export_obj(rd)
                    except Exception as e:
                        print e

                    for row in rd.rows:
                        if row.id in known_result_ids:
                            continue
                        known_result_ids.append(row.id)

                        callback_to_add_bro_data(row)


### Example usage

>>> def cb1(poller, pct, **kwargs):
...    rd = poller.get_result_data()
...    print handler.export_obj(rd)
...    print pct
...    print kwargs
...
>>>
>>> v = handler.ask_parsed("get computer name", picker=1, callbacks={"ProgressChanged": cb1}, test_kw="BOO")
[pytan.pollers.QuestionPoller] [run_callback] WARNING  Exception occurred in 'ProgressChanged' Callback: ResultSet for ID 38530, Columns: 0, Total Rows: None, Current Rows: 0, EstTotal: 1, Passed: 0, MrPassed: 0, Tested: 0, MrTested: 0 has no columns!
Computer Name
plat70.lab.com

100.0
{'sse_format': 'xml_obj', 'test_kw': 'BOO'}```
