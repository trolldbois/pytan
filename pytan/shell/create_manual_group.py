from . import base


class Worker(base.Base):
    DESCRIPTION = 'Create a manual group from file or list of provided computers'
    GROUP_NAME = 'Create Groups'
    ACTION = 'groups'
    PREFIX = 'create_manual_groups'
    NAME = 'groups'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

        self.grp.add_argument(
            '-g', '--group_name',
            required=True, action='store', dest='group_name', type=str, default='',
            help='Name of computer group to create'
        )
        self.grp.add_argument(
            '-a', '--add',
            required=False, action='append', dest='adds', type=str, default=[],
            help='Name or IP of computer to add to computer group'
        )
        self.grp.add_argument(
            '-l', '--list',
            required=False, action='store', dest='file', type=str, default='',
            help='Name of file containing names or IPs of computers to add to group. One per line.'
        )
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()
        self.grp_choice_results()

    def get_response(self, kwargs):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        m = "++ Creating {} with values:\n{}"
        print(m.format(self.NAME, self.pf(kwargs)))
        response = self.handler.create_manual_group(**kwargs)
        self.handler.MYLOG.debug("{}".format(response))
        return response

    def get_result(self):
        grps = []
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        if response:
            m = "++ Added group named {} with id {}".format
            print(m(response.name, response.id))
        else:
            print("!! Unable to create group.")
