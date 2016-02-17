import pytest

from pytan import threaded_http
from pytan import handler
from pytan import session
from pytan.handler_args import build_argstore
from pytan.handler_logs import setup_log
from pytan.constants import OVERRIDE_LEVEL


def pytest_addoption(parser):
    parser.addoption(
        "--runslow",
        action="store_true", help="run slow tests", default=False,
    )
    parser.addoption(
        "--host",
        action="store", help="host to use in online tests",
    )
    parser.addoption(
        "--port",
        action="store", help="port to use in online tests",
    )
    parser.addoption(
        "--username",
        action="store", help="username to use in online tests",
    )
    parser.addoption(
        "--password",
        action="store", help="password to use in online tests",
    )
    parser.addoption(
        "--domain",
        action="store", help="domain to use in online tests",
    )
    parser.addoption(
        "--secondary",
        action="store", help="secondary to use in online tests",
    )
    parser.addoption(
        "--https_proxy",
        action="store", help="https proxy to use in online tests",
    )
    parser.addoption(
        "--loglevel",
        action="store", help="loglevel to configure pytan with", default=OVERRIDE_LEVEL, type=int,
    )
    parser.addoption(
        "--config_file",
        action="store", help="pytan user config to source values from",
    )
    parser.addoption(
        "--httpd_host",
        action="store", default="127.0.0.1", help="host to use for threaded HTTP server tests",
    )
    parser.addoption(
        "--httpd_port",
        action="store", default=4433, type=int, help="port to use for threaded HTTP server tests",
    )


def pytest_configure(config):
    kwargs = config.__dict__['option'].__dict__
    argstore = build_argstore(**kwargs)
    handler_args = argstore.handler_args
    setup_log(**handler_args)
    config.handler_args = handler_args

    if not handler_args.username or not handler_args.password or not handler_args.host:
        print("\n\n\t\t** WARNING **")
        print("\n\n\t\tOnline tests will be skipped!! username, password, or host not supplied")
        config.skip_online = True
    else:
        config.skip_online = False

    # print(handler_args)
    # print(dir(config))
    # from pytan import historyconsole
    # historyconsole.HistoryConsole()


def pytest_unconfigure(config):
    if hasattr(config, 'REPORT_TMPDIR'):
        print('Report directory for this session:\n"{}"'.format(config.REPORT_TMPDIR))
    # for i in config.REPORT_TMPDIR.listdir():
    #     print(' "{}"'.format(i))
    # print('Report directory for this session:\n"{}"'.format(config.REPORT_TMPDIR))


# def pytest_report_header(config):
#     return dir(config)


# @pytest.mark.hookwrapper
# def pytest_pyfunc_call(pyfuncitem):
#     yield
#     # print('pyfunc call after')
#     if 'report_tmpdir' in pyfuncitem.funcargs:
#         print(pyfuncitem.funcargs['report_tmpdir'])


@pytest.fixture(scope='session', autouse=True)
def report_tmpdir(tmpdir_factory, pytestconfig):
    d = tmpdir_factory.mktemp('report_tmpdir')
    pytestconfig.REPORT_TMPDIR = d
    return d


@pytest.fixture(scope="session", autouse=True)
def httpd(request):
    httpd_host = request.config.getoption('httpd_host')
    httpd_port = request.config.getoption('httpd_port')
    verbosity = request.config.getoption('loglevel')
    httpd_args = {'host': httpd_host, 'port': httpd_port, 'verbosity': verbosity}
    result = threaded_http.threaded_http(**httpd_args)
    return result


@pytest.fixture(scope="session")
def https_proxy_args(request):
    https_proxy = pytest.config.handler_args.https_proxy
    if https_proxy:
        result = {'https_proxy': https_proxy}
    else:
        pytest.skip("need --https_proxy to run")
    return result


@pytest.fixture(scope="session")
def valid_args(request):
    if request.config.skip_online:
        pytest.skip("need --username and --password and --host option to run")
    else:
        result = {
            "username": request.config.handler_args.username,
            "password": request.config.handler_args.password,
            "domain": request.config.handler_args.domain,
            "secondary": request.config.handler_args.secondary,
            "host": request.config.handler_args.host,
            "port": request.config.handler_args.port,
        }
    return result


@pytest.fixture(scope="session")
def hash_string_args():
    result = {}
    result['hash'] = 1551313314
    result['str'] = 'Test 123456789'
    return result


@pytest.fixture(scope="session")
def valid_session(request, valid_args):
    result = session.Session(**valid_args)
    return result


@pytest.fixture(scope="session")
def valid_handler(request):
    result = handler.Handler(parsed_handler_args=request.config.handler_args)
    return result
