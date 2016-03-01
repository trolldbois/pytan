import logging

from pytan.builders import ObjectBuildError, log_result
from pytan.builders.params import build_params
from pytan.builders.filters import build_filter
from pytan.builders.constants import GROUP_DEFAULTS
from pytan.tanium_ng import Sensor, FilterList, Group, GroupList

MYLOG = logging.getLogger(__name__)


class BuildRightGroup(object):

    def __init__(self, handler, right_spec, **kwargs):
        self.SPEC = right_spec
        self.HANDLER = handler
        self.KWARGS = kwargs

        if not isinstance(self.SPEC, dict):
            err = 'spec must be a dict, you supplied type {}: {}'
            err = err.format(type(self.SPEC).__name__, self.SPEC)
            raise ObjectBuildError(err)

        if 'search_spec' not in self.SPEC:
            err = 'spec dict must have a "search_spec" key, you supplied: {}'
            err = err.format(self.SPEC)
            raise ObjectBuildError(err)

        self.GROUP_SPEC = self.SPEC.get('group_spec', {})
        self.LOT = self.GROUP_SPEC.get('lot', '1')
        self.KIND = self.GROUP_SPEC.get('kind', '')
        if self.KIND == 'group':
            self.get_group_obj()
        else:
            if 'filter_spec' not in self.SPEC:
                err = 'spec dict must have a "filter_spec" key, you supplied: {}'
                err = err.format(self.SPEC)
                raise ObjectBuildError(err)
            self.build_group_obj()

    def get_group_obj(self):
        self.RESULT = self.HANDLER.get_groups(limit_exact=1, search=self.SPEC['search_spec'])
        self.RESULT.lot = self.LOT

    def build_group_obj(self):
        self.SENSOR_OBJ = self.get_sensor_obj()
        self.SENSOR_PARAMS = self.build_sensor_params()
        self.FILTER_SENSOR = self.build_filter_sensor()
        self.FILTER = self.build_filter()
        self.FILTERLIST = self.build_filterlist()
        self.RESULT = self.build_filtergroup()
        self.RESULT.lot = self.LOT

    def build_sensor_params(self):
        pargs = {}
        pargs.update(self.KWARGS)
        pargs['named_param_spec'] = self.SPEC.get('named_param_spec', {})
        pargs['unnamed_param_spec'] = self.SPEC.get('unnamed_param_spec', [])
        pargs['obj'] = self.SENSOR_OBJ
        result = build_params(**pargs)
        return result

    def get_sensor_obj(self):
        result = self.HANDLER.get_sensors(limit_exact=1, search=self.SPEC['search_spec'])
        return result

    def build_filter_sensor(self):
        result = Sensor()
        if self.SENSOR_PARAMS:
            result.source_hash = self.SENSOR_OBJ.hash
            result.parameters = self.SENSOR_PARAMS
        else:
            result.hash = self.SENSOR_OBJ.hash
        log_result('BuildRightGroup.build_filter_sensor', result, locals())
        return result

    def build_filter(self):
        result = build_filter(self.FILTER_SENSOR, self.SPEC['filter_spec'])
        log_result('BuildRightGroup.build_filter', result, locals())
        return result

    def build_filterlist(self):
        result = FilterList(filter=[self.FILTER])
        log_result('BuildRightGroup.build_filterlist', result, locals())
        return result

    def build_filtergroup(self):
        result = Group(filters=self.FILTERLIST)
        log_result('BuildRightGroup.build_filtergroup', result, locals())
        return result


def build_right_group(handler, right_spec, **kwargs):
    builder = BuildRightGroup(handler, right_spec, **kwargs)
    result = builder.RESULT
    return result


def build_group(lot_spec, sub_groups):
    oargs = {k: lot_spec.get(k, v) for k, v in GROUP_DEFAULTS.items()}
    oargs['sub_groups'] = GroupList(group=sub_groups)
    result = Group(**oargs)
    return result


def build_parent_subgroup(right_items, lot, **kwargs):
    lot_specs = kwargs.get('lot_specs', {})
    lot_spec = lot_specs.get(lot, {})
    sub_groups = [x for x in right_items if get_lot(x) == lot]
    result = build_group(lot_spec, sub_groups)
    result.lot = lot
    log_result('lot #{}: build_parent_subgroup'.format(lot), result, locals())
    return result


def get_lot(group):
    result = getattr(group, 'lot', '1')
    return result


def build_parent_group(handler, **kwargs):
    right_specs = kwargs.get('right_specs', [])
    lot_specs = kwargs.get('lot_specs', {})
    right_items = [build_right_group(handler, s, **kwargs) for s in right_specs]
    if right_items:
        all_lots = list(set([get_lot(x) for x in right_items if get_lot(x) != '0']))
        parent_sub_groups = [
            build_parent_subgroup(right_items, l, **kwargs) for l in all_lots
        ]
        parent_sub_groups += [x for x in right_items if get_lot(x) == '0']
        parent_lot_spec = lot_specs.get('0', {})
        result = build_group(parent_lot_spec, parent_sub_groups)
        result.lot = '0'
    else:
        result = None
    log_result('lot #0: build_parent_group', result, locals())
    return result
