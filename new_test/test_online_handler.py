import pytan
from pytan import handler, session, store, tanium_ng

import pytest


def test_valid_creds(valid_handler):
    assert isinstance(valid_handler, handler.Handler)
    assert isinstance(valid_handler.HANDLER_ARGS, store.ArgStore)
    assert isinstance(valid_handler.user_obj, tanium_ng.User)
    assert isinstance(valid_handler.session_id, pytan.string_types)
    assert isinstance(valid_handler.session_user_id, pytan.integer_types)


def test_valid_version(valid_handler):
    result = valid_handler.get_server_version()
    assert not valid_handler.SESSION._invalid_server_version()
    assert result


def test_get_hash(valid_handler, hash_string_args):
    result = valid_handler.get_hash(hash_string_args['str'])
    assert result == hash_string_args['hash']


def test_get_string(valid_handler, hash_string_args):
    result = valid_handler.get_string(hash_string_args['hash'])
    assert result == hash_string_args['str']


def test_valid_creds_bad_session_id(valid_args):
    myargs = {}
    myargs.update(valid_args)
    myargs['session_id'] = 'INVALID_CREDENTIALS'
    myargs['ignore_config_file'] = True
    valid_handler = handler.Handler(**myargs)
    assert isinstance(valid_handler, handler.Handler)
    assert isinstance(valid_handler.HANDLER_ARGS, store.ArgStore)
    assert isinstance(valid_handler.user_obj, tanium_ng.User)
    assert isinstance(valid_handler.session_id, pytan.string_types)
    assert isinstance(valid_handler.session_user_id, pytan.integer_types)


def test_invalid_password(valid_args):
    myargs = {}
    myargs.update(valid_args)
    myargs['password'] = 'INVALID_CREDENTIALS'
    myargs['ignore_config_file'] = True

    exc = session.AuthorizationError
    with pytest.raises(exc):
        handler.Handler(**myargs)


def test_invalid_username(valid_args):
    myargs = {}
    myargs.update(valid_args)
    myargs['username'] = 'INVALID_CREDENTIALS'
    myargs['ignore_config_file'] = True

    exc = session.AuthorizationError
    with pytest.raises(exc):
        handler.Handler(**myargs)


def test_invalid_session_id(valid_args):
    myargs = {}
    myargs['session_id'] = 'INVALID_CREDENTIALS'
    myargs['host'] = valid_args['host']
    myargs['port'] = valid_args['port']
    myargs['ignore_config_file'] = True
    exc = session.AuthorizationError
    with pytest.raises(exc):
        handler.Handler(**myargs)


def test_proxy(valid_args, https_proxy_args):
    myargs = {}
    myargs.update(valid_args)
    myargs.update(https_proxy_args)
    valid_session = handler.Handler(**myargs)
    assert isinstance(valid_session, handler.Handler)
    assert isinstance(valid_session._CREDS, session.CredStore)
    assert isinstance(valid_session._CREDS.user_obj, tanium_ng.User)


GET_METHODS = [
    'get_sensors',
    'get_packages',
    'get_actions',
    'get_clients',
    'get_groups',
    'get_questions',
    'get_saved_actions',
    'get_saved_questions',
    'get_settings',
    'get_users',
    'get_user_roles',
    'get_whitelisted_urls',
]


@pytest.fixture(params=GET_METHODS, scope="module")
def all_objects(valid_handler, request):
    handler_method = getattr(valid_handler, request.param)
    result = handler_method()
    result.handler_method = handler_method
    return result


@pytest.fixture(scope="module")
def single_object(all_objects):
    if not all_objects:
        t = all_objects._LIST_TYPE.__name__
        m = "single_object(): no objects of type {} available to test single object get on!"
        m = m.format(t)
        pytest.skip(m)

    result = all_objects[0]
    result.handler_method = all_objects.handler_method
    return result


def test_get_all_objects(all_objects):
    assert isinstance(all_objects, tanium_ng.BaseType)


def test_get_single_object_by_name_str(single_object):
    if not hasattr(single_object, 'name') or not single_object.name:
        t = single_object.__class__.__name__
        m = "test_get_single_object_by_name_str() object type {} does not have a name attribute"
        m = m.format(t)
        pytest.skip(m)

    spec = "{}".format(single_object.name)
    result = single_object.handler_method(spec)
    assert isinstance(result, tanium_ng.BaseType)


'''
handler.get_sensors('Computer Name') == 1
'''
