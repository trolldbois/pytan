import logging

from pytan.builders import ObjectBuildError, log_result
from pytan.tanium_ng import Filter, CacheFilter, CacheFilterList
from pytan.builders.constants import FILTER_DEFAULTS, CACHE_FILTER_DEFAULTS

MYLOG = logging.getLogger(__name__)


def build_filter(sensor, filter_spec, **kwargs):
    result = None
    if filter_spec:
        if not isinstance(filter_spec, dict):
            err = 'filter_spec must be a dict, you supplied type {}: {}'
            err = err.format(type(filter_spec).__name__, filter_spec)
            MYLOG.error(err)
            raise ObjectBuildError(err)

        if 'value' not in filter_spec:
            err = 'filter_spec dict must have a "value" key, you supplied: {}'
            err = err.format(filter_spec)
            MYLOG.error(err)
            raise ObjectBuildError(err)

        oargs = {k: filter_spec.get(k, v) for k, v in FILTER_DEFAULTS.items()}
        oargs['sensor'] = sensor
        result = Filter(**oargs)
    return result


def build_cachefilterlist(search_specs):
    """pass."""
    if not isinstance(search_specs, (list, tuple)):
        search_specs = [search_specs]
    filters = [build_cachefilter(s) for s in search_specs]
    result = CacheFilterList(filter=filters)
    log_result('build_cachefilterlist', result, locals())
    return result


def build_cachefilter(search_spec):
    """pass."""
    if not isinstance(search_spec, dict):
        err = 'search_spec must be a dict, you supplied type {}: {}'
        err = err.format(type(search_spec).__name__, search_spec)
        MYLOG.error(err)
        raise ObjectBuildError(err)

    if 'value' not in search_spec:
        err = 'search_spec dict must have a "value" key, you supplied: {}'
        err = err.format(search_spec)
        MYLOG.error(err)
        raise ObjectBuildError(err)

    oargs = {k: search_spec.get(k, v) for k, v in CACHE_FILTER_DEFAULTS.items()}
    result = CacheFilter(**oargs)
    log_result('build_cachefilter', result, locals())
    return result
