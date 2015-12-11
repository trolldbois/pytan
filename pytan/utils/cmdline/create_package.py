import pprint
from . import base


class Worker(base.Base):
    DESCRIPTION = 'Create a package object from command line arguments'
    GROUP_NAME = 'Create Package Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-n', '--name',
            required=True, action='store', dest='name', default=None,
            help='Name of package to create',
        )
        self.grp.add_argument(
            '-c', '--command',
            required=True, action='store', dest='command', default='',
            help='Command to execute with package',
        )
        self.grp.add_argument(
            '-d', '--display-name',
            required=False, action='store', dest='display_name', default='',
            help='Display name of package',
        )
        self.grp.add_argument(
            '--command-timeout',
            required=False, action='store', dest='command_timeout_seconds', type=int, default=600,
            help='Command for this package timeout in N seconds',
        )
        self.grp.add_argument(
            '--expire-seconds',
            required=False, action='store', dest='expire_seconds', type=int, default=600,
            help='Expire actions created for this package in N seconds',
        )
        self.grp.add_argument(
            '-f', '--file-url',
            required=False, action='store', dest='file_urls', default=[],
            help='URL of file to include with package, can specify any of the '
            'following: "$url", or "$download_seconds::$url", or "$filename||$url",'
            ' or "$filename||$download_seconds::$url"',
        )
        self.grp.add_argument(
            '--parameters-file',
            required=False, action='store', dest='parameters_json_file', default='',
            help='JSON file describing parameters for this package, see '
            'doc/example_of_all_package_parameters.json for an example',
        )
        self.grp.add_argument(
            '-vf', '--verify-filter',
            required=False, action='append', dest='verify_filters', default=[],
            help='Filters to use for verifying the package after it is deployed',
        )
        self.grp.add_argument(
            '-vo', '--verify-option',
            required=False, action='append', dest='verify_filter_options', default=[],
            help='Options to use for the verify filters',
        )
        self.grp.add_argument(
            '--verify-expire-seconds',
            required=False, action='store', dest='verify_expire_seconds', type=int, default=600,
            help='Expire the verify filters used by this package in N seconds',
        )
        self.add_help_opts()

    def get_response(self, kwargs):
        m = "++ Creating package with arguments:\n{}"
        print m.format(pprint.pformat(kwargs))
        response = self.handler.create_package(**kwargs)
        m = "++ Package created successfully: {0.name!r}, ID: {0.id!r}, command: {0.command!r}"
        print m.format(response)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
