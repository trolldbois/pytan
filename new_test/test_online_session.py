import sys

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)

import time
import pytest

from pytan import session
from pytan import store
from pytan import tanium_ng

slow_test = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)


def test_valid_creds(valid_session):
    assert isinstance(valid_session, session.Session)
    assert isinstance(valid_session._CREDS, store.CredStore)
    assert isinstance(valid_session._CREDS.user_obj, tanium_ng.User)
    assert isinstance(valid_session.session_id, pytan.string_types)
    assert isinstance(valid_session.session_user_id, pytan.integer_types)


def test_valid_version(valid_session):
    result = valid_session.get_server_version()
    assert not valid_session._invalid_server_version()
    assert result


def test_get_hash(valid_session, hash_string_args):
    result = valid_session.get_hash(hash_string_args['str'])
    assert result == hash_string_args['hash']


def test_get_string(valid_session, hash_string_args):
    result = valid_session.get_string(hash_string_args['hash'])
    assert result == hash_string_args['str']


def test_invalid_find(valid_session):
    obj = tanium_ng.User(id=999999999)
    with pytest.raises(session.BadResponseError):
        valid_session.find(obj)


def test_valid_find(valid_session):
    obj = tanium_ng.User(id=valid_session.session_user_id)
    result = valid_session.find(obj)
    assert isinstance(result, tanium_ng.User)
    assert isinstance(result.name, pytan.string_types)


def test_valid_add_find_modify(valid_session):
    userlist = valid_session.find(tanium_ng.UserList())
    test_user_found = [x for x in userlist if x.name == 'pytest user']
    if test_user_found:
        valid_session.delete(test_user_found[0])

    admin_role = tanium_ng.UserRole(name='Administrator')
    sensor_role = tanium_ng.UserRole(name='Sensor Author')

    obj = tanium_ng.User()
    obj.name = 'pytest user'
    obj.roles = tanium_ng.UserRoleList()
    obj.roles.role = [admin_role]

    added_obj = valid_session.add(obj)
    assert isinstance(added_obj, tanium_ng.User)
    assert isinstance(added_obj.name, pytan.string_types)
    added_roles = [x.name for x in added_obj.roles]
    assert added_roles == ['Administrator']

    with pytest.raises(session.BadResponseError):
        valid_session.add(obj)

    found_obj = valid_session.find(added_obj)
    assert isinstance(found_obj, tanium_ng.User)
    assert isinstance(found_obj.name, pytan.string_types)

    found_obj.roles.role = [sensor_role]

    modified_obj = valid_session.save(found_obj)
    assert isinstance(modified_obj, tanium_ng.User)
    assert isinstance(modified_obj.name, pytan.string_types)
    modified_roles = [x.name for x in modified_obj.roles]
    assert modified_roles == ['Sensor Author']

    deleted_obj = valid_session.delete(modified_obj)
    assert deleted_obj.deleted_flag == 1
    assert isinstance(deleted_obj, tanium_ng.User)


def test_valid_creds_bad_session_id(valid_args):
    valid_args['session_id'] = 'INVALID_CREDENTIALS'
    valid_session = session.Session(**valid_args)
    assert isinstance(valid_session, session.Session)
    assert isinstance(valid_session._CREDS, session.CredStore)
    assert isinstance(valid_session._CREDS.user_obj, tanium_ng.User)


def test_session_id(valid_args):
    valid_session_1 = session.Session(**valid_args)
    session_id1 = valid_session_1.session_id

    session2_args = {}
    session2_args['host'] = valid_args['host']
    session2_args['port'] = valid_args['port']
    session2_args['session_id'] = session_id1

    valid_session_2 = session.Session(**session2_args)
    session_id2 = valid_session_2.session_id
    assert isinstance(valid_session_2, session.Session)
    assert isinstance(valid_session_2._CREDS, session.CredStore)
    assert isinstance(valid_session_2._CREDS.user_obj, tanium_ng.User)
    assert session_id1 == session_id2


def test_logout_single(valid_args):
    valid_session = session.Session(**valid_args)
    session_id1 = valid_session.session_id
    valid_session.logout()

    myargs = {}
    myargs['host'] = valid_args['host']
    myargs['port'] = valid_args['port']
    myargs['session_id'] = session_id1

    with pytest.raises(session.AuthorizationError):
        session.Session(**myargs)


def test_logout_all(valid_args):
    valid_session_1 = session.Session(**valid_args)
    session_id1 = valid_session_1.session_id

    valid_session_2 = session.Session(**valid_args)
    session_id2 = valid_session_2.session_id
    assert session_id1 != session_id2

    valid_session_2.logout(all_sessions=True)

    myargs = {}
    myargs['host'] = valid_args['host']
    myargs['port'] = valid_args['port']
    myargs['session_id'] = session_id1

    with pytest.raises(session.AuthorizationError):
        session.Session(**myargs)

    myargs['session_id'] = session_id2

    with pytest.raises(session.AuthorizationError):
        session.Session(**myargs)


def test_invalid_password(valid_args):
    myargs = {}
    myargs.update(valid_args)
    myargs['password'] = 'INVALID_CREDENTIALS'

    exc = session.AuthorizationError
    with pytest.raises(exc):
        session.Session(**myargs)


def test_invalid_username(valid_args):
    myargs = {}
    myargs.update(valid_args)
    myargs['username'] = 'INVALID_CREDENTIALS'

    exc = session.AuthorizationError
    with pytest.raises(exc):
        session.Session(**myargs)


def test_invalid_session_id(valid_args):
    myargs = {}
    myargs['session_id'] = 'INVALID_CREDENTIALS'
    myargs['host'] = valid_args['host']
    myargs['port'] = valid_args['port']

    exc = session.AuthorizationError
    with pytest.raises(exc):
        session.Session(**myargs)


def test_proxy(valid_args, https_proxy_args):
    myargs = {}
    myargs.update(valid_args)
    myargs.update(https_proxy_args)
    valid_session = session.Session(**myargs)
    assert isinstance(valid_session, session.Session)
    assert isinstance(valid_session._CREDS, session.CredStore)
    assert isinstance(valid_session._CREDS.user_obj, tanium_ng.User)


def test_re_auth_fast(valid_args):
    valid_session = session.Session(**valid_args)
    version1 = valid_session.get_server_info()
    session_id1 = valid_session.session_id
    assert version1
    assert session_id1

    # fake the fact that 5 minutes have passed by setting the session ID to a bad value
    valid_session._CREDS.session_id = 'INVALID_CREDENTIALS'

    version2 = valid_session.get_server_info()
    session_id2 = valid_session.session_id
    assert version2
    assert session_id2
    assert session_id1 != session_id2


@slow_test
def test_re_auth_slow(valid_args):
    valid_session = session.Session(**valid_args)
    version1 = valid_session.get_server_info()
    session_id1 = valid_session.session_id
    assert version1
    assert session_id1

    time.sleep(5 * 60)

    version2 = valid_session.get_server_info()
    session_id2 = valid_session.session_id
    assert version2
    assert session_id2
    assert session_id1 != session_id2


@slow_test
def test_persistent_slow(valid_args):
    valid_args['persistent'] = True

    valid_session = session.Session(**valid_args)
    version1 = valid_session.get_server_info()
    session_id1 = valid_session.session_id
    assert version1
    assert session_id1

    time.sleep(10 * 60)

    version2 = valid_session.get_server_info()
    session_id2 = valid_session.session_id
    assert version2
    assert session_id2
    assert session_id1 == session_id2
