from . import base


class Worker(base.Base):
    DESCRIPTION = 'Create a whitelisted URL from command line arguments'
    GROUP_NAME = 'Create whitelisted URL Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--url',
            required=True, action='store', dest='url', default=None,
            help='Text of new Whitelisted URL',
        )
        self.grp.add_argument(
            '--regex',
            required=False, action='store_true', dest='regex', default=False,
            help='Whitelisted URL is a regex pattern',
        )
        self.grp.add_argument(
            '-d', '--download',
            required=False, action='store', dest='download_seconds', type=int, default=86400,
            help='Download Whitelisted URL every N seconds',
        )
        self.grp.add_argument(
            '-prop', '--property',
            required=False, action='append', dest='properties', nargs=2, default=[],
            help='Property name and value to assign to Whitelisted URL',
        )

    def get_response(self, kwargs):
        m = "++ Creating whitelisted URL with arguments:\n{}"
        print m.format(self.pf(kwargs))
        response = self.handler.create_package(**kwargs)
        m = "++ Whitelisted URL created successfully: {0.url_regex!r}, ID: {0.id!r}"
        print m.format(response)
        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response
