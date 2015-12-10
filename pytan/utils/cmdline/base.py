import os
import sys
import json
import copy
import getpass
import argparse
from argparse import ArgumentDefaultsHelpFormatter as A1 # noqa
from argparse import RawDescriptionHelpFormatter as A2 # noqa
from .. import constants
from .. import tanium_obj
from .. import files


class CustomArgFormat(A1, A2):
    """Multiple inheritance Formatter class for :class:`argparse.ArgumentParser`.

    If a :class:`argparse.ArgumentParser` class uses this as it's Formatter class, it will show the defaults for each argument in the `help` output
    """
    pass


class CustomArgParse(argparse.ArgumentParser):
    """Custom :class:`argparse.ArgumentParser` class which does a number of things:

        * Uses :class:`pytan.utils.CustomArgFormat` as it's Formatter class, if none was passed in
        * Prints help if there is an error
        * Prints the help for any subparsers that exist
    """
    def __init__(self, *args, **kwargs):
        self.my_file = __name__

        if 'my_file' in kwargs:
            self.my_file = kwargs.pop('my_file')

        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomArgFormat

        # print kwargs
        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message):
        self.print_help()
        print('\n!! Argument Parsing Error in "{}": {}\n'.format(self.my_file, message))
        sys.exit(2)

    def print_help(self, **kwargs):
        super(CustomArgParse, self).print_help(**kwargs)
        subparsers_actions = [
            action for action in self._actions
            if isinstance(action, argparse._SubParsersAction)
        ]
        for subparsers_action in subparsers_actions:
            print ""
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                # print subparser
                # print(" ** {} '{}':".format(
                    # subparsers_action.dest, choice))
                print(subparser.format_help())


class Base(object):

    DESCRIPTION = ""
    INTERACTIVE = False

    def __init__(self, **kwargs):
        from ... import handler
        self.handler_module = handler
        self.kwargs = kwargs
        self.my_filepath = os.path.abspath(sys.argv[0])
        self.my_file = os.path.basename(self.my_filepath)
        self.my_name = os.path.splitext(self.my_file)[0]
        self.constants = constants
        self.CustomArgFormat = CustomArgFormat
        self.CustomArgParse = CustomArgParse
        self.pre_init()
        self.set_base()
        self.set_parser()
        self.post_init()

    def pre_init(self):
        pass

    def post_init(self):
        pass

    def set_base(self):
        self.base = self.CustomArgParse(
            my_file=self.my_file,
            description=self.DESCRIPTION,
            add_help=False,
        )
        self.add_handler_auth()
        self.add_handler_opts()

    def set_parser(self):
        self.parser = self.CustomArgParse(
            my_file=self.my_file,
            description=self.DESCRIPTION,
            parents=[self.base]
        )

    def add_handler_auth(self):
        name = 'PyTan Authentication'
        self.grp = self.base.add_argument_group(name)
        self.grp.add_argument(
            '-u', '--username',
            required=False, action='store', dest='username', default=None,
            help='Name of user',
        )
        self.grp.add_argument(
            '-p', '--password',
            required=False, action='store', default=None, dest='password',
            help='Password of user',
        )
        self.grp.add_argument(
            '--session_id',
            required=False, action='store', default=None, dest='session_id',
            help='Session ID to authenticate with instead of username/password',
        )
        self.grp.add_argument(
            '--host',
            required=False, action='store', default=None, dest='host',
            help='Hostname/ip of SOAP Server',
        )
        self.grp.add_argument(
            '--port',
            required=False, action='store', default="443", dest='port',
            help='Port to use when connecting to SOAP Server',
        )

    def add_handler_opts(self):
        name = 'PyTan Options'
        self.grp = self.base.add_argument_group(name)
        self.grp.add_argument(
            '-l', '--loglevel',
            required=False, action='store', type=int, default=0, dest='loglevel',
            help='Logging level to use, increase for more verbosity',
        )
        self.grp.add_argument(
            '--debugformat',
            required=False, action='store_true', default=False, dest='debugformat',
            help="Enable debug format for logging",
        )
        self.grp.add_argument(
            '--record_all_requests',
            required=False, action='store_true', default=False, dest='record_all_requests',
            help="Record all requests in handler.session.ALL_REQUESTS_RESPONSES",
        )
        self.grp.add_argument(
            '--stats_loop_enabled',
            required=False, action='store_true', default=False, dest='stats_loop_enabled',
            help="Enable the statistics loop",
        )
        self.grp.add_argument(
            '--http_auth_retry',
            required=False, action='store_false', default=True, dest='http_auth_retry',
            help="Disable retry on HTTP authentication failures",
        )
        self.grp.add_argument(
            '--http_retry_count',
            required=False, action='store', type=int, default=5, dest='http_retry_count',
            help="Retry count for HTTP failures/invalid responses",
        )

        puc_h = "PyTan User Config file to use for PyTan arguments (defaults to: {})"
        puc_h = puc_h.format(constants.PYTAN_USER_CONFIG)
        self.grp.add_argument(
            '--pytan_user_config',
            required=False, action='store', default='', dest='pytan_user_config',
            help=puc_h
        )
        self.grp.add_argument(
            '--force_server_version',
            required=False, action='store', default='', dest='force_server_version',
            help="Force PyTan to consider the server version as this"
        )

    def add_help_opts(self):
        name = 'PyTan Help Options'
        self.grp = self.parser.add_argument_group(name)
        self.grp.add_argument(
            '--sensors-help',
            required=False, action='store_true', default=False, dest='sensors_help',
            help='Get the full help for sensor strings and exit',
        )
        self.grp.add_argument(
            '--filters-help',
            required=False, action='store_true', default=False, dest='filters_help',
            help='Get the full help for filters strings and exit',
        )
        self.grp.add_argument(
            '--options-help',
            required=False, action='store_true', default=False, dest='options_help',
            help='Get the full help for options strings and exit',
        )

    def add_report_opts(self):
        name = 'Report File Options'
        self.grp = self.parser.add_argument_group(name)
        self.grp.add_argument(
            '--file',
            required=False, action='store', default=None, dest='report_file',
            help='File to save report to (if not supplied, will be generated)',
        )
        self.grp.add_argument(
            '--dir',
            required=False, action='store', default=None, dest='report_dir',
            help='Directory to save report to (if not supplied, use current directory)',
        )

    def grp_choice_results(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--no-results',
            action='store_false', dest='get_results', default=argparse.SUPPRESS, required=False,
            help='Do not get the results, just add the object and return right away'
        )
        choice.add_argument(
            '--results',
            action='store_true', dest='get_results', default=True, required=False,
            help='Wait until all results are in before returning'
        )

    def grp_choice_sse(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--enable_sse',
            required=False, action='store_true', dest='sse', default=True,
            help='Perform a server side export when getting data'
        )
        choice.add_argument(
            '--disable_sse',
            required=False, action='store_false', dest='sse', default=True,
            help='Perform a normal get result data export when getting data'
        )

    def grp_sse_opts(self):
        self.grp.add_argument(
            '--sse_format',
            required=False, action='store', default='xml_obj', dest='sse_format',
            choices=['csv', 'xml', 'xml_obj', 'cef'],
            help='If sse = True, perform server side export in this format',
        )
        self.grp.add_argument(
            '--leading',
            required=False, action='store', default='', dest='leading',
            help='If sse = True, and sse_format = "cef", prepend each row with this text',
        )
        self.grp.add_argument(
            '--trailing',
            required=False, action='store', default='', dest='trailing',
            help='If sse = True, and sse_format = "cef", append each row with this text',
        )

    def grp_format(self):
        self.grp.add_argument(
            '--export_format',
            required=False, action='store', default='csv', dest='export_format',
            choices=['csv', 'xml', 'json'],
            help='Export Format to create report file in, only used if sse = False',
        )

    def grp_choice_csv_sort(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--sort',
            required=False, action='append', default=[], dest='header_sort',
            help='For export_format: csv, Sort headers by given names'
        )
        choice.add_argument(
            '--no-sort',
            required=False, action='store_false', default=argparse.SUPPRESS, dest='header_sort',
            help='For export_format: csv, Do not sort the headers at all'
        )
        choice.add_argument(
            '--auto_sort',
            required=False, action='store_true', default=argparse.SUPPRESS, dest='header_sort',
            help='For export_format: csv, Sort the headers with a basic alphanumeric sort'
        )

    def grp_choice_csv_sensor(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--add-sensor',
            required=False, action='store_true', default=argparse.SUPPRESS,
            dest='header_add_sensor',
            help='For export_format: csv, Add the sensor names to each header'
        )
        choice.add_argument(
            '--no-add-sensor',
            required=False, action='store_false', default=False, dest='header_add_sensor',
            help='For export_format: csv, Do not add the sensor names to each header'
        )

    def grp_choice_csv_type(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--add-type',
            required=False, action='store_true', default=argparse.SUPPRESS,
            dest='header_add_type',
            help='For export_format: csv, Add the result type to each header'
        )
        choice.add_argument(
            '--no-add-type',
            required=False, action='store_false', default=False, dest='header_add_type',
            help='For export_format: csv, Do not add the result type to each header'
        )

    def grp_choice_csv_expand(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--expand-columns',
            required=False, action='store_true', default=argparse.SUPPRESS,
            dest='expand_grouped_columns',
            help='For export_format: csv, Expand multi-line cells into their own rows'
        )
        choice.add_argument(
            '--no-columns',
            required=False, action='store_false', default=False, dest='expand_grouped_columns',
            help='For export_format: csv, Do not add expand multi-line cells into their own rows'
        )

    def grp_choice_explode(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--no-explode-json',
            required=False, action='store_false', default=False, dest='explode_json_string_values',
            help='Do not explode any embedded JSON into their own columns'
        )
        choice.add_argument(
            '--explode-json',
            required=False, action='store_true', default=argparse.SUPPRESS,
            dest='explode_json_string_values',
            help='Explode any embedded JSON into their own columns'
        )

    def grp_choice_include_type(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--no-include_type',
            required=False, action='store_false', default=argparse.SUPPRESS, dest='include_type',
            help='Only for export_format json, Do not include SOAP type in JSON output'
        )
        choice.add_argument(
            '--include_type',
            required=False, action='store_true', default=True, dest='include_type',
            help='Only for export_format json, Include SOAP type in JSON output'
        )

    def grp_choice_minimal(self):
        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--no-minimal',
            required=False, action='store_false', dest='minimal', default=argparse.SUPPRESS,
            help='Only for export_format xml, include empty attributes'
        )
        choice.add_argument(
            '--minimal',
            required=False, action='store_true', dest='minimal', default=True,
            help='Only for export_format xml, Only include attributes that are not empty'
        )

    def add_export_results_opts(self):
        name = 'Export Results Options'
        self.grp = self.parser.add_argument_group(name)
        # self.grp_choice_sse()
        # self.grp_sse_opts()
        self.grp_format()
        self.grp_choice_csv_sort()
        self.grp_choice_csv_sensor()
        self.grp_choice_csv_type()
        self.grp_choice_csv_expand()

    def add_export_object_opts(self):
        name = 'Export Object Options'
        self.grp = self.parser.add_argument_group(name)
        self.grp_format()
        self.grp_choice_csv_sort()
        self.grp_choice_explode()
        self.grp_choice_include_type()
        self.grp_choice_minimal()

    def _input_prompts(self):
        """Utility function to prompt for username, `, and host if empty"""
        puc_default = os.path.expanduser(self.constants.PYTAN_USER_CONFIG)
        puc_kwarg = self.args.__dict__.get('pytan_user_config', '')
        puc = puc_kwarg or puc_default
        puc_dict = {}

        if os.path.isfile(puc):
            try:
                with open(puc) as fh:
                    puc_dict = json.load(fh)
            except Exception as e:
                m = "PyTan User Config file exists at '{}' but is not valid, Exception: {}".format
                print m(puc, e)

        if not self.args.session_id:
            if not self.args.username and not puc_dict.get('username', ''):
                username = raw_input('Tanium Username: ')
                self.args.username = username.strip()

            if not self.args.password and not puc_dict.get('password', ''):
                password = getpass.getpass('Tanium Password: ')
                self.args.password = password.strip()

        if not self.args.host and not puc_dict.get('host', ''):
            host = raw_input('Tanium Host: ')
            self.args.host = host.strip()

        return self.args

    def _get_grp_opts(self, grps):
        action_grps = [a for a in self.parser._action_groups if a.title in grps]
        opts = [a.dest for b in action_grps for a in b._group_actions]
        return opts

    def version_check(self, version):
        return files.version_check(self.my_name, version)

    def interactive_check(self):
        self.console = None
        if self.INTERACTIVE:
            from .. import historyconsole
            self.historyconsole = historyconsole
            self.console = self.historyconsole.HistoryConsole()
        return self.console

    def get_parser_args(self, grps):
        parser_opts = self._get_grp_opts(grps=grps)
        p_args = {k: getattr(self.args, k) for k in parser_opts}
        return p_args

    def get_other_args(self, kwargs):
        other_args = {a: b for a, b in self.args.__dict__.iteritems() if a not in kwargs}
        return other_args

    def check(self):
        return

    def setup(self):
        return

    def parse_args(self):
        self.args = self.parser.parse_args()
        return self.args

    def get_handler(self):
        self._input_prompts()
        grps = ['PyTan Authentication', 'PyTan Options']
        kwargs = self.get_parser_args(grps)
        self.handler = self.handler_module.Handler(**kwargs)
        return self.handler

    def get_result(self):
        return

    def get_exec(self):
        s = 'exec_result = None'
        return s


class GetBase(Base):
    OBJECT_TYPE = ''
    NAME_TEMP = 'Get {} Options'
    DESC_TEMP = 'Get an object of type "{}" and export it to a file'
    ACTION = 'get'

    def pre_init(self):
        self.OBJECT_STR = self.OBJECT_TYPE.replace('_', ' ').capitalize()
        self.GROUP_NAME = self.NAME_TEMP.format(self.OBJECT_STR)
        self.DESCRIPTION = self.DESC_TEMP.format(self.OBJECT_STR)

    def add_get_opts(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        obj_map = tanium_obj.get_obj_map(self.OBJECT_TYPE)
        search_keys = copy.copy(obj_map['search'])

        if 'id' not in search_keys:
            search_keys.append('id')

        if self.OBJECT_TYPE == 'whitelisted_url':
            search_keys.append('url_regex')
        elif self.OBJECT_TYPE == 'user':
            search_keys.append('name')

        for k in search_keys:
            self.grp.add_argument(
                '--{}'.format(k),
                required=False, action='append', default=[], dest=k,
                help='{} of {} to {}'.format(k, self.OBJECT_STR, self.ACTION),
            )

    def setup(self):
        self.add_get_opts()
        self.grp.add_argument(
            '--all',
            required=False, default=False, action='store_true', dest='all',
            help='Get all objects of type {}'.format(self.OBJECT_STR),
        )
        self.add_export_object_opts()
        self.add_report_opts()

    def get_kwargs(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        return kwargs

    def get_response(self, kwargs):
        get_all = kwargs.pop('all')

        o_dict = {'objtype': self.OBJECT_TYPE}
        kwargs.update(o_dict)

        if get_all:
            response = self.handler.get_all(**o_dict)
        else:
            response = self.handler.get(**kwargs)

        print "Found items: {}".format(response)
        return response

    def export_response(self, response):
        report_file, result = self.handler.export_to_report_file(
            obj=response,
            **self.args.__dict__
        )

        m = "Report file {!r} written with {} bytes".format
        print(m(report_file, len(result)))
        return report_file, result

    def get_result(self):
        kwargs = self.get_kwargs()
        response = self.get_response(kwargs)
        report_file, result = self.export_response(response)
        return response, report_file, result


class CreateJsonBase(GetBase):
    NAME_TEMP = 'Create {} from JSON Options'
    DESC_TEMP = 'Create an object of type "{}" from a JSON file'

    def add_create_opts(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-j', '--json',
            required=True, action='store', default='', dest='json_file',
            help='JSON file to use for creating the object',
        )

    def setup(self):
        self.add_create_opts()

    def get_response(self, kwargs):
        response = self.handler.create_from_json(self.OBJECT_TYPE, **kwargs)
        for i in response:
            obj_id = getattr(i, 'id', 'unknown')
            print "Created item: {}, ID: {}".format(i, obj_id)
        return response

    def get_result(self):
        kwargs = self.get_kwargs()
        response = self.get_response(kwargs)
        return response


class DeleteBase(GetBase):
    NAME_TEMP = 'Delete {} Options'
    DESC_TEMP = 'Delete an object of type "{}"'
    ACTION = 'delete'

    def setup(self):
        self.add_get_opts()

    def get_response(self, kwargs):
        o_dict = {'objtype': self.OBJECT_TYPE}
        kwargs.update(o_dict)

        response = self.handler.delete(self.OBJECT_TYPE, **kwargs)
        for i in response:
            print "Deleted item: {}".format(i)
        return response

    def get_result(self):
        kwargs = self.get_kwargs()
        response = self.get_response(kwargs)
        return response
