from . import base


class Worker(base.Base):
    DESCRIPTION = 'Stop an action by ID'
    GROUP_NAME = 'Stop Action Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-i', '--id',
            required=True, type=int, action='store', dest='id',
            help='ID of Action to stop',
        )

    def get_response(self, kwargs):
        m = "++ Stopping action with arguments:\n{}"
        print(m.format(self.pf(kwargs)))
        response = self.handler.stop_action(**kwargs)
        m = "++ Action ID stopped successfully: {}"
        print(m.format(response))
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
