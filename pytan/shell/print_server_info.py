import pprint
from . import base


class Worker(base.Base):
    DESCRIPTION = 'Print server info from /info page'
    GROUP_NAME = 'Print Server Info Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--json',
            required=False,
            default=False,
            action='store_true',
            dest='json',
            help='Just print the raw JSON, instead of pretty printing '
            'the elements',
        )

    def get_response(self, kwargs):
        m = "++ Getting server info"
        print(m.format())
        response = self.handler.SESSION.get_server_info()
        m = "++ Server info fetched successfully for {} sections"
        print(m.format(len(response['diags_flat'])))

        if kwargs['json']:
            print(response['diags_flat'])
        else:
            pprint.pprint(response['diags_flat'])

        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
