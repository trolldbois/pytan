"""Exceptions for :mod:`pytan`"""


class PytanException(Exception):
    """Exception thrown for errors while validating definitions"""
    pass


class ValidationError(PytanException):
    """Exception thrown for errors while validating definitions"""
    pass


class PytanHelp(PytanException):
    """Exception thrown when printing out help"""
    pass


class PytanError(PytanException):
    """Exception thrown for errors in :mod:`pytan`"""
    pass


class NetworkError(PytanException):
    """Exception thrown for errors in :mod:`pytan`"""
    pass


class UnsupportedVersionError(PytanException):
    """Exception thrown for version checks in :mod:`pytan.handler`"""
    pass


# not val'd below


class RunError(PytanException):
    """Exception thrown when run=False from :func:`pytan.handler.Handler.deploy_action`"""
    pass


class PollingError(PytanException):
    """Exception thrown for errors in :mod:`pytan.polling`"""
    pass


class TimeoutException(PytanException):
    """Exception thrown for timeout errors in :mod:`pytan.polling`"""
    pass


class HttpError(PytanException):
    """Exception thrown for HTTP errors in :mod:`pytan.sessions`"""
    pass


class AuthorizationError(PytanException):
    """Exception thrown for authorization errors in :mod:`pytan.sessions`"""
    pass


class BadResponseError(PytanException):
    """Exception thrown for BadResponse messages from Tanium in :mod:`pytan.sessions`"""
    pass


class NotFoundError(PytanException):
    """Exception thrown for Not Found messages from Tanium in :mod:`pytan.handler`"""
    pass


class VersionMismatchError(PytanException):
    """Exception thrown for version_check in :mod:`pytan.utils`"""
    pass


class ServerSideExportError(PytanException):
    """Exception thrown for server side export errors in :mod:`pytan.handler`"""
    pass


class VersionParseError(PytanException):
    """Exception thrown for server version parsing errors in :mod:`pytan.handler`"""
    pass


class ServerParseError(PytanException):
    """Exception thrown for server parsing errors in :mod:`pytan.handler`"""
    pass


class PickerError(PytanException):
    """Exception thrown for picker errors in :mod:`pytan.handler`"""
    pass
