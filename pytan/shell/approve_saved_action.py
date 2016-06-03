from . import base


class Worker(base.Base):
    DESCRIPTION = 'Approve a saved action by ID'
    GROUP_NAME = 'Approve Saved Action Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-i', '--id',
            required=True, type=int, action='store', dest='id',
            help='ID of Saved Action to approve',
        )

    def get_response(self, kwargs):
        m = "++ Approving saved action with arguments:\n{}"
        print(m.format(self.pf(kwargs)))
        response = self.handler.approve_saved_action(**kwargs)
        print("++ Saved Action ID approved successfully: {0.id!r}".format(response))
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
