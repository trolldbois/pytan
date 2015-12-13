from . import base


class Worker(base.Base):
    DESCRIPTION = 'Create a user object from command line arguments'
    GROUP_NAME = 'Create User Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-n', '--name',
            required=True, action='store', dest='name', default=None,
            help='Name of user to create',
        )
        self.grp.add_argument(
            '-rn', '--rolename',
            required=False, action='append', dest='rolename', default=[],
            help='Name of role to assign to new user',
        )
        self.grp.add_argument(
            '-ri', '--roleid',
            required=False, action='append', type=int, dest='roleid', default=[],
            help='ID of role to assign to new user',
        )
        self.grp.add_argument(
            '-g', '--group',
            required=False, action='store', dest='group', default='',
            help='Name of group to assign to user',
        )
        self.grp.add_argument(
            '-prop', '--property',
            required=False, action='append', dest='properties', nargs=2, default=[],
            help='Property name and value to assign to user',
        )

    def get_response(self, kwargs):
        m = "++ Creating user with arguments:\n{}"
        print m.format(self.pf(kwargs))
        response = self.handler.create_package(**kwargs)
        roles_txt = ', '.join([x.name for x in response.roles])
        m = (
            "++ User created successfully: {0.name!r}, ID: {0.id!r}, group: {0.group_id!r}, "
            "roles: {1}"
        )
        print m.format(response, roles_txt)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
