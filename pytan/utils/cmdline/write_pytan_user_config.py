from . import base


class Worker(base.Base):
    DESCRIPTION = 'Creates a PyTan User Config file based on the current parameters'
    GROUP_NAME = 'Write PyTan User Config Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        puc_h = "PyTan User Config file to write for PyTan arguments (defaults to: {})"
        puc_h = puc_h.format(self.constants.PYTAN_USER_CONFIG)
        self.grp.add_argument(
            '--new_config',
            required=False, default=self.SUPPRESS, action='store', dest='new_config', help=puc_h
        )

    def get_response(self, kwargs):
        m = "++ Writing Pytan User Config with arguments:\n{}"
        print m.format(self.pf(kwargs))
        response = self.handler.write_pytan_user_config(**kwargs)
        m = "PyTan User config file successfully written: {}"
        print m.format(response)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
