from . import base
from .. import pretty


class Worker(base.Base):
    DESCRIPTION = 'Print server info from /info page'
    GROUP_NAME = 'Print Server Info Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--json',
            required=False, default=False, action='store_true', dest='json',
            help='Just print the raw JSON, instead of pretty printing the elements',
        )

    def get_response(self, kwargs):
        m = "++ Getting server info"
        print(m.format())
        response = self.handler.session.get_server_info()
        m = "++ Server info fetched successfully for {} sections"
        print(m.format(len(response['diags_flat'])))

        if kwargs['json']:
            result = pretty.jsonify(response['diags_flat'])
        else:
            result = pretty.pretty_dict(response['diags_flat'])
        print(result)

        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
