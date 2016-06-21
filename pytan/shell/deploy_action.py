from . import base


class Worker(base.Base):
    DESCRIPTION = 'Deploy an action and export the results to a file'
    GROUP_NAME = 'Deploy Action Options'
    PREFIX = 'deploy_action'
    ACTION = 'action'

    def setup(self):
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--run',
            required=False, action='store_true', default=False, dest='run',
            help='Run the deploy action, required to actually start '
            'the action',
        )
        self.grp.add_argument(
            '-k', '--package',
            required=True, action='store', default='', dest='package',
            help='Package to deploy action with, optionally describe '
            'parameters',
        )
        self.grp.add_argument(
            '-f', '--filter',
            required=False, action='append', default=[], dest='filters',
            help='Filter to deploy action against',
        )
        self.grp.add_argument(
            '-o', '--option',
            required=False, action='append', default=[], dest='options',
            help='Options for deploy action filter',
        )
        self.grp.add_argument(
            '--start_seconds_from_now',
            required=False, action='store', type=int, default=None,
            dest='start_seconds_from_now',
            help='Start the action N seconds from now',
        )
        self.grp.add_argument(
            '--expire_seconds',
            required=False, action='store', type=int, default=None,
            dest='expire_seconds',
            help='Expire the action N seconds after it starts',
        )
        self.grp_choice_results()

    def get_action_response(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        m = "++ Deploying action with arguments:\n{}"
        print(m.format(self.pf(kwargs)))
        response = self.handler.deploy_action(**kwargs)

        m = (
            "++ Deployed Action {action_object.name!r} ID: "
            "{action_object.id!r}\n"
            "++ Command used in Action: '{action_object.package_spec.command}'"
        )
        print(m.format(**response))

        if response['action_result_map']:
            print("++ Deploy action progress results:")
            for k, v in sorted(response['action_result_map'].iteritems()):
                print("\n Total {}: {}".format(k, v['total']))

        return response

    def get_result(self):
        response = self.get_action_response()
        report_file, result = self.export_results(response['action_results'])
        return response, report_file, result
