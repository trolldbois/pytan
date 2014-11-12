Problems:

get all actions fail with Action:

>>> handler.session.find(pytan.api.Action())
2014-11-12 01:38:14,910 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:666, status:200 OK
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/jolsen/gh/pytan/pytan/api/session.py", line 119, in find
    self.response_body = self._getResponse(self.request_body)
  File "/Users/jolsen/gh/pytan/pytan/api/session.py", line 216, in _getResponse
    raise BadResponseError(response_command)
pytan.api.session.BadResponseError: ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class ActionNotFound


get an action by id works:

>>> a=pytan.api.Action()
>>> a.id=1
>>> handler.session.find(a)
2014-11-12 01:38:36,242 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:2845, status:200 OK
2014-11-12 01:38:36,243 DEBUG    api.session: Session ID updated to: 1-4791-3178b34fc07a8dae134044d7f586a36545f06f72aebf0a14c890af9c2a9ecbea8eef1b9bff6d0103d656251bcd537c55787e8c8f2bb0bb1566515a9cbdee2b72
<pytan.api.object_types.action.Action object at 0x102325150>

need to get all actions via ActionList:

>>> handler.session.find(pytan.api.ActionList())
2014-11-12 01:38:58,971 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:847025, status:200 OK
2014-11-12 01:38:59,195 DEBUG    api.session: Session ID updated to: 1-4791-3178b34fc07a8dae134044d7f586a36545f06f72aebf0a14c890af9c2a9ecbea8eef1b9bff6d0103d656251bcd537c55787e8c8f2bb0bb1566515a9cbdee2b72
<pytan.api.object_types.action_list.ActionList object at 0x1024cfa10>

can't get action by name:

>>> r.name
'Unmanaged Asset Tracking - Run Scan'
>>> a=pytan.api.Action()
>>> a.name = r.name
>>> r=handler.session.find(a)
2014-11-12 01:41:04,853 DEBUG    api.session: HTTP response from 'https://172.16.31.128:443//soap' len:666, status:200 OK
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/jolsen/gh/pytan/pytan/api/session.py", line 119, in find
    self.response_body = self._getResponse(self.request_body)
  File "/Users/jolsen/gh/pytan/pytan/api/session.py", line 216, in _getResponse
    raise BadResponseError(response_command)
pytan.api.session.BadResponseError: ERROR: 400 Bad Request

XML Parse Error: SOAPProcessing Exception: class ActionNotFound
