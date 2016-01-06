import sys

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)

import time
import pytest

from pytan import threaded_http
from pytan import session
from pytan import tanium_ng

pytan.handler.add_override_log(loglevel=50)

# OPTS:
RUN_SLOW = True
HOST = '10.0.1.240'
USERNAME = 'Administrator'
PASSWORD = 'Tanium2015!'
PORT = 443
HTTPS_PROXY = "http://localhost:8080"

# INTERNALS
BAD = 'INVALID_CREDENTIALS'
BAD_PORT = 5000
HTTPD_HOST = 'localhost'
HTTPD_PORT = 4433
HASH_TEST = '3409330187'
STRING_TEST = 'Computer Name'

VALID_ARGS = {"username": USERNAME, "password": PASSWORD, "host": HOST, "port": PORT}
HTTPD_ARGS = {'host': HTTPD_HOST, 'port': HTTPD_PORT, 'verbosity': 2}
INVALID_ARGS = [
    {
        "username": USERNAME,
        "password": BAD,
        "host": HOST,
        "port": PORT,
        "err": session.AuthorizationError,
    },
    {
        "username": BAD,
        "password": PASSWORD,
        "host": HOST,
        "port": PORT,
        "err": session.AuthorizationError,
    },
    {
        "session_id": BAD,
        "host": HOST,
        "port": PORT,
        "err": session.AuthorizationError,
    },
    {
        "username": USERNAME,
        "password": PASSWORD,
        "host": HTTPD_HOST,
        "port": HTTPD_PORT,
        "err": session.HttpError,
    },
    {
        "username": USERNAME,
        "password": PASSWORD,
        "host": HOST,
        "port": BAD_PORT,
        "err": session.NetworkError,
    },
]


slow_test = pytest.mark.skipif(not RUN_SLOW, reason="slow tests disabled")
proxy_test = pytest.mark.skipif(not HTTPS_PROXY, reason="no proxy defined")
invalid_params = pytest.mark.parametrize("invalid_credentials", INVALID_ARGS)


@pytest.fixture(scope="module", params=[HTTPD_ARGS])
def httpd(request):
    return threaded_http.threaded_http(**request.param)


@pytest.fixture(scope="module", params=[VALID_ARGS])
def validsession(request):
    return session.Session(**request.param)


def test_valid_creds(validsession):
    s = validsession
    assert isinstance(s, session.Session)
    assert isinstance(s._CREDS, session.CredStore)
    assert isinstance(s._CREDS.user_obj, tanium_ng.User)
    assert isinstance(s.session_id, pytan.string_types)
    assert isinstance(s.session_user_id, pytan.integer_types)


def test_valid_version(validsession):
    s = validsession
    v = s.get_server_version()
    assert not s._invalid_server_version()
    assert v


def test_get_hash(validsession):
    s = validsession
    result = s.get_hash(STRING_TEST)
    assert result == HASH_TEST


def test_get_string(validsession):
    s = validsession
    result = s.get_string(HASH_TEST)
    assert result == STRING_TEST


def test_invalid_find(validsession):
    s = validsession
    obj = tanium_ng.User(values={'id': 99999})
    with pytest.raises(session.BadResponseError):
        s.find(obj)


def test_valid_find(validsession):
    s = validsession
    obj = tanium_ng.User(values={'id': s.session_user_id})
    result = s.find(obj)
    assert isinstance(result, tanium_ng.User)
    assert isinstance(result.name, pytan.string_types)


def test_valid_add_find_modify(validsession):
    s = validsession
    userlist = s.find(tanium_ng.UserList())
    test_user_found = [x for x in userlist if x.name == 'pytest user']
    if test_user_found:
        s.delete(test_user_found[0])

    admin_role = tanium_ng.UserRole(values={'name': 'Administrator'})
    sensor_role = tanium_ng.UserRole(values={'name': 'Sensor Author'})

    obj = tanium_ng.User()
    obj.name = 'pytest user'
    obj.roles = tanium_ng.UserRoleList()
    obj.roles.role = [admin_role]

    added_obj = s.add(obj)
    assert isinstance(added_obj, tanium_ng.User)
    assert isinstance(added_obj.name, pytan.string_types)
    added_roles = [x.name for x in added_obj.roles]
    assert added_roles == ['Administrator']

    with pytest.raises(session.BadResponseError):
        s.add(obj)

    found_obj = s.find(added_obj)
    assert isinstance(found_obj, tanium_ng.User)
    assert isinstance(found_obj.name, pytan.string_types)

    found_obj.roles.role = [sensor_role]

    modified_obj = s.save(found_obj)
    assert isinstance(modified_obj, tanium_ng.User)
    assert isinstance(modified_obj.name, pytan.string_types)
    modified_roles = [x.name for x in modified_obj.roles]
    assert modified_roles == ['Sensor Author']

    deleted_obj = s.delete(modified_obj)
    assert deleted_obj.deleted_flag == 1
    assert isinstance(deleted_obj, tanium_ng.User)


def test_valid_creds_bad_session_id():
    s = session.Session(session_id=BAD, **VALID_ARGS)
    assert isinstance(s, session.Session)
    assert isinstance(s._CREDS, session.CredStore)
    assert isinstance(s._CREDS.user_obj, tanium_ng.User)


def test_session_id():
    s1 = session.Session(**VALID_ARGS)
    session1 = s1.session_id
    s2 = session.Session(host=HOST, port=PORT, session_id=session1)
    session2 = s2.session_id
    assert isinstance(s2, session.Session)
    assert isinstance(s2._CREDS, session.CredStore)
    assert isinstance(s2._CREDS.user_obj, tanium_ng.User)
    assert session1 == session2


def test_re_auth_fakeout():
    s = session.Session(**VALID_ARGS)
    si = s.get_server_info()
    assert si
    session1 = s.session_id
    # fake the fact that 5 minutes have passed by setting the session ID to a bad value
    s._CREDS.session_id = BAD
    si = s.get_server_info()
    assert si
    session2 = s.session_id
    assert session1 != session2


def test_logout_single():
    s = session.Session(**VALID_ARGS)
    session1 = s.session_id
    s.logout()
    with pytest.raises(session.AuthorizationError):
        session.Session(host=HOST, port=PORT, session_id=session1)


def test_logout_all():
    s1 = session.Session(**VALID_ARGS)
    session1 = s1.session_id

    s2 = session.Session(**VALID_ARGS)
    session2 = s2.session_id
    assert session1 != session2

    s2.logout(all_sessions=True)
    with pytest.raises(session.AuthorizationError):
        session.Session(host=HOST, port=PORT, session_id=session1)

    with pytest.raises(session.AuthorizationError):
        session.Session(host=HOST, port=PORT, session_id=session2)


@invalid_params
def test_invalid_creds(httpd, invalid_credentials):
    exc = invalid_credentials.pop('err')
    with pytest.raises(exc):
        session.Session(**invalid_credentials)


@proxy_test
def test_proxy():
    s = session.Session(https_proxy=HTTPS_PROXY, **VALID_ARGS)
    assert isinstance(s, session.Session)
    assert isinstance(s._CREDS, session.CredStore)
    assert isinstance(s._CREDS.user_obj, tanium_ng.User)


@slow_test
def test_re_auth_slow():
    s = session.Session(**VALID_ARGS)
    si = s.get_server_info()
    assert si
    session1 = s.session_id
    time.sleep(5 * 60)
    si = s.get_server_info()
    assert si
    session2 = s.session_id
    assert session1 != session2


@slow_test
def test_persistent_slow():
    s = session.Session(persistent=True, **VALID_ARGS)
    si = s.get_server_info()
    assert si
    session1 = s.session_id
    time.sleep(10 * 60)
    si = s.get_server_info()
    assert si
    session2 = s.session_id
    assert session1 == session2
