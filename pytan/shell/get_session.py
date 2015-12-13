from . import base


class Worker(base.Base):
    DESCRIPTION = 'Get a new session ID'
    GROUP_NAME = 'Get Session Optipons'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--persistent',
            required=False, action='store_true', dest='persistent', default=False,
            help='Request a session ID that expires 1 week after last use instead of 5 minutes',
        )

    def get_response(self, kwargs):
        response = self.handler.session._session_id
        print "++ Session ID returned: {}".format(response)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
