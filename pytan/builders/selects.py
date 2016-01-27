import logging

from pytan.builders import ObjectBuildError, log_result
from pytan.builders.params import build_params
from pytan.builders.filters import build_filter
from pytan.tanium_ng import Sensor, Select, SelectList

MYLOG = logging.getLogger(__name__)


class BuildLeftSelect(object):

    def __init__(self, handler, spec, **kwargs):
        self.SPEC = spec
        self.HANDLER = handler
        self.KWARGS = kwargs

        if not isinstance(spec, dict):
            err = 'spec must be a dict, you supplied type {}: {}'
            err = err.format(type(spec).__name__, spec)
            MYLOG.error(err)
            raise ObjectBuildError(err)

        if 'search_spec' not in spec:
            err = 'spec dict must have a "search_spec" key, you supplied: {}'
            err = err.format(spec)
            MYLOG.error(err)
            raise ObjectBuildError(err)

        self.SENSOR_OBJ = self.get_sensor_obj()
        self.SENSOR_PARAMS = self.build_sensor_params()
        self.SELECT_SENSOR = self.build_select_sensor()
        self.SELECT_FILTER = self.build_select_filter()
        self.RESULT = self.build_select()

    def build_sensor_params(self):
        pargs = {}
        pargs.update(self.KWARGS)
        pargs['named_param_spec'] = self.SPEC.get('named_param_spec', {})
        pargs['unnamed_param_spec'] = self.SPEC.get('unnamed_param_spec', [])
        pargs['obj'] = self.SENSOR_OBJ
        result = build_params(**pargs)
        return result

    def build_select(self):
        result = Select()
        result.sensor = self.SELECT_SENSOR
        result.filter = self.SELECT_FILTER
        log_result('BuildLeftSelect.build_select', result, locals())
        return result

    def get_sensor_obj(self):
        result = self.HANDLER.get_sensors(limit_exact=1, search=self.SPEC['search_spec'])
        return result

    def build_select_sensor(self):
        result = Sensor()
        if self.SENSOR_PARAMS:
            result.source_hash = self.SENSOR_OBJ.hash
            result.parameters = self.SENSOR_PARAMS
        else:
            result.hash = self.SENSOR_OBJ.hash
        log_result('BuildLeftSelect.build_select_sensor', result, locals())
        return result

    def build_select_filter(self):
        filter_spec = self.SPEC.get('filter_spec', {})
        sensor = Sensor(hash=self.SENSOR_OBJ.hash)
        result = build_filter(sensor, filter_spec)
        log_result('BuildLeftSelect.build_select_filter', result, locals())
        return result


def build_left_select(handler, spec, **kwargs):
    builder = BuildLeftSelect(handler, spec, **kwargs)
    result = builder.RESULT
    return result


def build_selectlist(handler, **kwargs):
    left_specs = kwargs.get('left_specs', [])
    selects = [build_left_select(handler, s, **kwargs) for s in left_specs]
    result = SelectList(select=selects)
    log_result('build_selectlist', result, locals())
    return result
