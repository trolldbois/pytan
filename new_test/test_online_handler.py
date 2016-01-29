import sys

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)

# import time
import pytest

from pytan import session
from pytan import store
from pytan import handler
from pytan import tanium_ng

# pytestmark = pytest.mark.skipif(
#     pytest.config.skip_online,
#     reason="need --username and --password and --host option to run"
# )


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


@pytest.mark.parametrize("get_method", GET_METHODS)
def get_method_all(valid_handler, get_method):
    m = getattr(valid_handler, get_method)
    result = m()
    assert isinstance(result, tanium_ng.BaseType)
    assert len(result) >= 1


'''
handler.get_sensors('Computer Name') == 1
'''
