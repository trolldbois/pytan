# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Provides exceptions for the :mod:`pytan` module."""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True


class HandlerError(Exception):
    """Exception thrown for most errors in :mod:`pytan.handler`"""
    pass


class HumanParserError(Exception):
    """Exception thrown for errors while parsing human strings from :mod:`pytan.handler`"""
    pass


class DefinitionParserError(Exception):
    """Exception thrown for errors while parsing definitions from :mod:`pytan.handler`"""
    pass


class RunFalse(Exception):
    """Exception thrown when run=False from :func:`pytan.handler.Handler.deploy_action`"""
    pass


class PytanHelp(Exception):
    """Exception thrown when printing out help"""
    pass


class PollingError(Exception):
    """Exception thrown for most errors in :mod:`pytan.polling`"""
    pass


class TimeoutException(Exception):
    """Exception thrown for timeout errors in :mod:`pytan.polling`"""
    pass


class HttpError(Exception):
    """Exception thrown for HTTP errors in :mod:`pytan.sessions`"""
    pass


class AuthorizationError(Exception):
    """Exception thrown for authorization errors in :mod:`pytan.sessions`"""
    pass


class BadResponseError(Exception):
    """Exception thrown for BadResponse messages from Tanium in :mod:`pytan.sessions`"""
    pass


class NotFoundError(Exception):
    """Exception thrown for Not Found messages from Tanium in :mod:`pytan.handler`"""
    pass


class VersionMismatchError(Exception):
    """Exception thrown for version_check in :mod:`pytan.utils`"""
    pass


class RunPluginError(Exception):
    """Exception thrown for run_plugin in :mod:`pytan.sessions`"""
    pass
