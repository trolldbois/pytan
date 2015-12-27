import copy
import logging

from pytan.parsers.spec import Spec
from pytan.parsers.getobject import GetObject

mylog = logging.getLogger(__name__)


class LeftSide(Spec):

    def post_init(self, specs, **kwargs):
        """pass."""
        self.me = "{}()".format(self.__class__.__name__)
        self.meerr = "{}.{}".format(__name__, self.me)

        self.chk_dict_key('specs', {'specs': specs}, (dict, list, tuple,))

        self.original_specs = specs

        if not isinstance(self.original_specs, (list, tuple)):
            self.original_specs = [self.original_specs]

        self.parsed_specs = [self.parse_spec(s) for s in self.original_specs]

    def parse_spec(self, spec):
        parsed_spec = copy.deepcopy(spec)
        # check that spec is a dict
        self.chk_dict_key('spec', {'spec': spec}, (dict,))

        # check that sensor key exists and is a dict
        self.has_dict_key('sensor', spec)
        self.chk_dict_key('sensor', spec, (dict,))

        # parse the sensor dict
        sensor_parser = GetObject(self.tanium_ng.SensorList, spec['sensor'])
        parsed_spec['sensor'] = sensor_parser.parsed_spec
        return parsed_spec
