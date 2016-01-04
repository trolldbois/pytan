#!/usr/bin/env python3 -ttB

# BEGIN BOOTSTRAP CODE

# statically defined path
PYTAN_PATH = "~/gh/pytan"

import os
import sys
sys.dont_write_bytecode = True

# list of paths to insert at beginning of PYTHONPATH
path_adds = []

# add PYTAN_PATH to path_adds
path_adds.append(PYTAN_PATH)

# get parent_dir and add to path_adds (allows scripts that live in bin/ to work automatically)
my_filepath = os.path.abspath(sys.argv[0])
my_file = os.path.basename(my_filepath)
my_name = os.path.splitext(my_file)[0]
my_dir = os.path.dirname(my_filepath)
parent_dir = os.path.dirname(my_dir)
path_adds.append(my_dir)
path_adds.append(parent_dir)

# if OS Environment "PYTAN_PATH" is set, add that to path_adds
if 'PYTAN_PATH' in os.environ:
    path_adds.append(os.environ['PYTAN_PATH'])

# expand user directories and get the absolute path of all path_adds
path_adds = [os.path.abspath(os.path.expanduser(aa)) for aa in path_adds]

# add the path_adds to beginning of PYTHONPATH
[sys.path.insert(0, aa) for aa in path_adds if aa not in sys.path]

import pytan  # noqa
# END BOOTSTRAP CODE

# from pytan import tanium_ng
import time  # noqa
import pytest
import threaded_http
from pytan import session

HOST = '10.0.1.240'
USERNAME = 'Administrator'
PASSWORD = 'Tanium2015!'
PORT = 443

BAD = 'INVALID_CREDENTIALS'
BAD_PORT = 5000

HTTPD_HOST = 'localhost'
HTTPD_PORT = 4433

VALID_ARGS = {"username": USERNAME, "password": PASSWORD, "host": HOST, "port": PORT}

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

HTTPD_ARGS = [{'host': HTTPD_HOST, 'port': HTTPD_PORT, 'verbosity': 2}]

pytan.handler.add_override_log(loglevel=50)


@pytest.fixture(scope="module", params=HTTPD_ARGS)
def httpd(request):
    return threaded_http.threaded_http(**request.param)


@pytest.fixture(scope="function", params=VALID_ARGS)
def validsession(request):
    return session.Session(**request.param)


def test_valid_creds():
    s = session.Session(**VALID_ARGS)
    assert isinstance(s, session.Session)
    assert isinstance(s._CREDS, session.CredStore)
    assert isinstance(s._CREDS.user_obj, pytan.tanium_ng.User)


def test_session_id():
    s1 = session.Session(**VALID_ARGS)
    session1 = s1.session_id
    s2 = session.Session(host=HOST, port=PORT, session_id=session1)
    assert isinstance(s2, session.Session)
    assert isinstance(s2._CREDS, session.CredStore)
    assert isinstance(s2._CREDS.user_obj, pytan.tanium_ng.User)


def test_valid_version():
    s = session.Session(**VALID_ARGS)
    v = s.get_server_version()
    assert not s._invalid_server_version()
    assert v


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


# def test_re_auth_slow(validsession):
#     validsession.get_server_info()
#     session1 = validsession.session_id
#     time.sleep(5 * 60)
#     validsession.get_server_info()
#     session2 = validsession.session_id
#     assert session1 != session2


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

    s2.logout(all_sessions=True)
    with pytest.raises(session.AuthorizationError):
        session.Session(host=HOST, port=PORT, session_id=session1)

    with pytest.raises(session.AuthorizationError):
        session.Session(host=HOST, port=PORT, session_id=session2)


@pytest.mark.parametrize("sargs", INVALID_ARGS)
def test_invalid_creds(httpd, sargs):
    exc = sargs.pop('err')
    with pytest.raises(exc):
        session.Session(**sargs)

if __name__ == '__main__':
    pytest.main()
