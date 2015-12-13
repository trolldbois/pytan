from . import base


class Worker(base.Base):
    DESCRIPTION = 'Create a group object from command line arguments'
    GROUP_NAME = 'Create Group Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-n', '--name',
            required=True, action='store', dest='groupname', default=None,
            help='Name of group to create',
        )
        self.grp.add_argument(
            '-f', '--filter',
            required=False, action='append', dest='filters', default=[],
            help='Filters to use for group',
        )
        self.grp.add_argument(
            '-o', '--option',
            required=False, action='append', dest='filter_options', default=[],
            help='Filter options to use for group',
        )
        self.add_help_opts()

    def get_response(self, kwargs):
        m = "++ Creating group with arguments:\n{}"
        print m.format(self.pf(kwargs))
        response = self.handler.create_group(**kwargs)
        m = "++ Group created successfully: {0.name!r}, ID: {0.id!r}, filter: {0.text!r}"
        print m.format(response)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
