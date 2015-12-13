# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Exceptions for :mod:`pytan`"""


class ValidationError(Exception):
    """Exception thrown for errors while validating definitions"""
    pass


class PytanHelp(Exception):
    """Exception thrown when printing out help"""
    pass


class PytanError(Exception):
    """Exception thrown for errors in :mod:`pytan`"""
    pass


class NetworkError(Exception):
    """Exception thrown for errors in :mod:`pytan`"""
    pass


class UnsupportedVersionError(Exception):
    """Exception thrown for version checks in :mod:`pytan.handler`"""
    pass


# not val'd below


class RunError(Exception):
    """Exception thrown when run=False from :func:`pytan.handler.Handler.deploy_action`"""
    pass


class PollingError(Exception):
    """Exception thrown for errors in :mod:`pytan.polling`"""
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


class ServerSideExportError(Exception):
    """Exception thrown for server side export errors in :mod:`pytan.handler`"""
    pass


class VersionParseError(Exception):
    """Exception thrown for server version parsing errors in :mod:`pytan.handler`"""
    pass


class ServerParseError(Exception):
    """Exception thrown for server parsing errors in :mod:`pytan.handler`"""
    pass


class PickerError(Exception):
    """Exception thrown for picker errors in :mod:`pytan.handler`"""
    pass
