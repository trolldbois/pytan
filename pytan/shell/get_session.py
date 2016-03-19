from . import base


class Worker(base.Base):
    DESCRIPTION = 'Get a new session ID'
    GROUP_NAME = 'Get Session Optipons'
    PREFIX = 'get_session'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

    def get_response(self, kwargs):
        response = self.handler.session_id
        print "{}".format(response)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
