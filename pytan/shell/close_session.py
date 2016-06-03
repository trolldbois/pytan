from . import base


class Worker(base.Base):
    DESCRIPTION = 'Closes targeted session ID, or all open sessions'
    GROUP_NAME = 'Close Session Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--all_session_ids',
            required=False, action='store_true', dest='all_session_ids', default=False,
            help='Close all open tanium sessions, instead of just the one supplied'
        )

    def get_response(self, kwargs):
        m = "++ Calling handler.session.logout with arguments:\n{}"
        print(m.format(self.pf(kwargs)))
        response = self.handler.SESSION.logout(**kwargs)
        print("++ Logout finished successfully")
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
