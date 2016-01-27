import copy
import logging

from pytan import PytanError, string_types
from pytan.parsers.tokens import search_tokenize, left_tokenize, right_tokenize, lot_tokenize
from pytan.parsers.specs import search_specify, left_specify, right_specify, lot_specify

MYLOG = logging.getLogger(__name__)


class SpecInvalidError(PytanError):
    pass


class Coerce(object):

    def verify_specs(self, specs):
        if isinstance(specs, string_types):
            specs = [specs]
        elif isinstance(specs, dict):
            specs = [specs]
        elif isinstance(specs, (list, tuple)):
            specs = list(specs)
        else:
            err = "{}: specs must be a string, dict, or list, you supplied type {!r}, {!r}"
            err = err.format(self.me, type(specs).__name__, specs)
            MYLOG.error(err)
            raise SpecInvalidError(err)
        return specs

    @property
    def me(self):
        me = self.__class__.__name__
        result = "{}()"
        result = result.format(me)
        return result


class CoerceSearch(Coerce):

    SPEC_NAME = 'search_specs'

    def __init__(self, specs=[], add_subspecs=[], **kwargs):
        """specs should be one of the following:

        a string that should be parsed into a list of a list of dicts
        a list of strings that should each be parsed into a list of dicts then grouped in a list
        a dict that should be turned into a list of a list of dicts
        a list of dicts that should be turned into a list of a list of dicts
        """
        self.KWARGS = kwargs
        self.SPECS = copy.deepcopy(specs)

        if self.SPECS:
            self.SPECS = self.verify_specs(self.SPECS)

        self.ADD_SUBSPECS = add_subspecs
        append_subspecs = self.coerce_subspecs(add_subspecs)

        self.RESULT = [self.coerce_subspecs(s, append_subspecs) for s in self.SPECS]

        if not self.RESULT and append_subspecs:
            self.RESULT = [append_subspecs]

        m = "{}: Coerced specs {!r} into new specs {!r}"
        m = m.format(self.me, specs, self.RESULT)
        MYLOG.info(m)

    def coerce_subspecs(self, subspecs=[], append_subspecs=[]):
        """subspecs should be one of the following:

        a string that should be parsed into a list of dicts (subspecs) by search_tokenize()
        a list of dicts (subspecs)
        a dict (subspec)
        """
        if isinstance(subspecs, string_types):
            subspecs = self.my_tokenize()(subspecs)

        if isinstance(subspecs, dict):
            subspecs = [subspecs]
        elif isinstance(subspecs, (list, tuple)):
            subspecs = list(subspecs)
        else:
            err = "subspecs must be a string, dict, or list, you supplied type {!r}, {!r}"
            err = err.format(type(subspecs).__name__, subspecs)
            MYLOG.error(err)
            raise SpecInvalidError(err)

        result = [self.coerce_subspec(s) for s in subspecs]
        if append_subspecs:
            [result.append(s) for s in append_subspecs if s not in result]
        return result

    def coerce_subspec(self, subspec):
        if isinstance(subspec, dict):
            pargs = {}
            pargs.update(self.KWARGS)
            pargs[self.SPEC_NAME] = subspec
            result = self.my_specify()(**pargs)
        else:
            err = "subspec {} must be a dict! all specs: {}"
            err = err.format(subspec, self.SPECS)
            MYLOG.error(err)
            raise SpecInvalidError(err)
        return result

    def my_tokenize(self):
        return search_tokenize

    def my_specify(self):
        return search_specify


class CoerceLeft(Coerce):

    SPEC_NAME = 'left_spec'

    def __init__(self, specs=[], **kwargs):
        """specs should be one of the following:

        a string that should be parsed into a a list of dicts
        a list of strings that should each be parsed into a dicts then grouped in a list
        a dict that should be turned into a list of dicts
        a list of dicts that should be turned into a list of dicts
        """
        self.KWARGS = kwargs
        self.SPECS = copy.deepcopy(specs)

        if self.SPECS:
            self.SPECS = self.verify_specs(self.SPECS)

        self.RESULT = [self.coerce_subspec(s) for s in self.SPECS]

        m = "{}: Coerced specs {!r} into specs {!r}"
        m = m.format(self.me, specs, self.RESULT)
        MYLOG.info(m)

    def coerce_subspec(self, subspec):
        """subspec should be one of the following:

        a string that should be parsed into a dict (subspec) by TOKEN_PARSER()
        a dict (subspec) that should be validated by SPEC_PARSER
        """
        if isinstance(subspec, string_types):
            subspec = self.my_tokenize()(subspec)

        if isinstance(subspec, dict):
            pargs = {}
            pargs.update(self.KWARGS)
            pargs[self.SPEC_NAME] = subspec
            result = self.my_specify()(**pargs)
        else:
            err = "{}: subspec must be a string or dict, you supplied type {!r}, {!r}"
            err = err.format(self.me, type(subspec).__name__, subspec)
            MYLOG.error(err)
            raise SpecInvalidError(err)
        return result

    def my_tokenize(self):
        return left_tokenize

    def my_specify(self):
        return left_specify


class CoerceRight(CoerceLeft):

    SPEC_NAME = 'right_spec'

    def my_tokenize(self):
        return right_tokenize

    def my_specify(self):
        return right_specify


class CoerceLot(Coerce):

    SPEC_NAME = 'lot_spec'

    def __init__(self, specs=[], **kwargs):
        """specs should be one of the following:

        a string that should be parsed into a dict
        a list of strings that should each be parsed into dicts then grouped into one dict
        a dict that should be turned into a dict
        a list of dicts that should be turned into dicts then grouping into one dict
        """
        self.KWARGS = kwargs
        self.SPECS = copy.deepcopy(specs)

        if self.SPECS:
            self.SPECS = self.verify_specs(self.SPECS)

        self.RESULT = self.coerce_subspecs(self.SPECS)

        m = "{}: Coerced specs {!r} into specs {!r}"
        m = m.format(self.me, specs, self.RESULT)
        MYLOG.info(m)

    def coerce_subspecs(self, subspecs):
        subspecs = [self.coerce_subspec(s) for s in subspecs]
        result = {i['lot']: i for i in subspecs if i}
        return result

    def coerce_subspec(self, subspec):
        """subspec should be one of the following:

        a string that should be parsed into a dict (subspec) by TOKEN_PARSER()
        a dict (subspec) that should be validated by SPEC_PARSER
        """
        if isinstance(subspec, string_types):
            subspec = self.my_tokenize()(subspec)

        if isinstance(subspec, dict):
            pargs = {}
            pargs.update(self.KWARGS)
            pargs[self.SPEC_NAME] = subspec
            result = self.my_specify()(**pargs)
        else:
            err = "{}: subspec must be a string or dict, you supplied type {!r}, {!r}"
            err = err.format(self.me, type(subspec).__name__, subspec)
            MYLOG.error(err)
            raise SpecInvalidError(err)
        return result

    def my_tokenize(self):
        return lot_tokenize

    def my_specify(self):
        return lot_specify


def coerce_search(search, **kwargs):
    coercer = CoerceSearch(search, **kwargs)
    result = coercer.RESULT
    return result


def coerce_left(left, **kwargs):
    coercer = CoerceLeft(left, **kwargs)
    result = coercer.RESULT
    return result


def coerce_right(right, **kwargs):
    coercer = CoerceRight(right, **kwargs)
    result = coercer.RESULT
    return result


def coerce_lot(lot, **kwargs):
    coercer = CoerceLot(lot, **kwargs)
    result = coercer.RESULT
    return result
