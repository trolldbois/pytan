import copy
import logging

from pytan.parsers import spec

mylog = logging.getLogger(__name__)


class FilterObject(spec.Spec):

    def post_init(self, spec, **kwargs):
        """pass."""
        self.single_class = self.tanium_ng.Filter()
        self.single_name = self.single_class.__name__
        self.single_obj = self.single_class()
        self.props = self.single_obj._simple_properties
        self.props_txt = ', '.join(self.props)
        self.me = "{}() for object {!r}"
        self.me = self.me.format(self.__class__.__name__, self.single_class.__name__)
        self.meerr = "{}.{}".format(__name__, self.me)

        # check that spec is a dict
        self.chk_dict_key('spec', {'spec': spec}, (dict,))

        # make a copy of spec into result
        self.original_spec = spec
        self.parsed_spec = copy.deepcopy(self.original_spec)

        # check that field key exists and is valid
        self.parsed_spec = self.chk_field(self.parsed_spec)

        # check that value key exists and is valid
        self.parsed_spec = self.chk_value(self.parsed_spec)

        # if operator key exists, parse & validate
        if 'operator' in self.parsed_spec:
            self.parsed_spec = self.chk_operator(self.parsed_spec)

        if 'not_flag' in self.parsed_spec:
            self.parsed_spec = self.chk_not_flag(self.parsed_spec)

        if 'field_type' in self.parsed_spec:
            self.parsed_spec = self.chk_field_type(self.parsed_spec)

        # if changed, log the change
        if self.original_spec != self.parsed_spec:
            m = "{} parsed from {!r} into {!r}"
            m = m.format(self.me, self.original_spec, self.parsed_spec)
            mylog.info(m)
        else:
            m = "{} parsed without change {!r}"
            m = m.format(self.me, self.parsed_spec)
            mylog.info(m)
