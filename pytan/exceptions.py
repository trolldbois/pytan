#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.


class HandlerError(Exception):
    pass


class PickerError(Exception):
    pass


class ReporterError(Exception):
    pass


class ManualParserError(Exception):
    pass
