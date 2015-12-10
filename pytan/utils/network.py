#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Network module for :mod:`pytan`"""

import logging
import socket
from . import exceptions

mylog = logging.getLogger(__name__)


def port_check(address, port, timeout=5):
    """Check if `address`:`port` can be reached within `timeout`

    Parameters
    ----------
    address : str
        * hostname/ip address to check `port` on
    port : int
        * port to check on `address`
    timeout : int, optional
        * timeout after N seconds of not being able to connect

    Returns
    -------
    :mod:`socket` or False :
        * if connection succeeds, the socket object is returned, else False is returned
    """
    try:
        return socket.create_connection((address, port), timeout)
    except socket.error:
        return False


def test_app_port(host, port):
    """Validates that `host`:`port` can be reached using :func:`port_check`

    Parameters
    ----------
    host : str
        * hostname/ip address to check `port` on
    port : int
        * port to check on `host`

    Raises
    ------
    exceptions.HandlerError : :exc:`exceptions.HandlerError`
        * if `host`:`port` can not be reached
    """
    chk_tpl = "Port test to {}:{} {}".format
    if port_check(host, port):
        mylog.debug(chk_tpl(host, port, "SUCCESS"))
    else:
        raise exceptions.NetworkError(chk_tpl(host, port, "FAILURE"))
