# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
"""Math module for for :mod:`pytan`"""


def get_percent(base, amount):
    """Utility method for getting percentage of base out of amount

    Parameters
    ----------
    base: int, float
    amount: int, float

    Returns
    -------
    percent : the percentage of base out of amount
    """
    if 0 in [base, amount]:
        percent = float(0)
    else:
        percent = (100 * (float(base) / float(amount)))
    return percent


def get_base(percent, amount):
    """Utility method for getting base for percentage of amount

    Parameters
    ----------
    percent: int, float
    amount: int, float

    Returns
    -------
    base : the base from percentage of amount
    """
    base = int((percent * amount) / 100.0)
    return base
