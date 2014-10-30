#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.


class AuthorizationError(Exception):
    pass


class HttpError(Exception):
    pass


class BadRequestError(Exception):
    pass


class UnknownCommandError(Exception):
    pass


class InnerReturnError(Exception):
    pass


class OuterReturnError(Exception):
    pass


class BadResponseError(Exception):
    pass


class AppError(Exception):
    pass


class PickerError(Exception):
    pass
