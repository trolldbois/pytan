from pytan.handler_args import create_argstore
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


def pytest_configure(config):
    kwargs = config.__dict__['option'].__dict__
    argstore = create_argstore(**kwargs)
    handler_args = argstore.handler_args
    setup_log(**handler_args)
    config.handler_args = handler_args

    if not handler_args.username or not handler_args.password or not handler_args.host:
        print("""

     ** WARNING **

     Online tests will be skipped!! username, password, or host not supplied
""")
        config.skip_online = True
    else:
        config.skip_online = False

    # print(handler_args)
    # print(dir(config))
    # from pytan import historyconsole
    # historyconsole.HistoryConsole()
