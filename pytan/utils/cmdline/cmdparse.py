import os
import sys
import copy
import argparse
from argparse import ArgumentDefaultsHelpFormatter as A1 # noqa
from argparse import RawDescriptionHelpFormatter as A2 # noqa

from .. import constants
from .. import calc
from .. import tanium_obj


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
        self.my_name = kwargs.get('my_name', __name__)
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = CustomArgFormat
        # print kwargs
        argparse.ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message):
        self.print_help()
        print('ERROR:{}:{}\n'.format(self.my_name, message))
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


def base_parser(desc, help=False):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts that use :mod:`pytan`. This establishes the basic arguments that are needed by all such scripts, such as:

        * --help
        * --username
        * --password
        * --host
        * --port
        * --loglevel
        * --debugformat
    """
    parser = CustomArgParse(description=desc, add_help=help)
    arggroup_name = 'Handler Authentication'
    auth_group = parser.add_argument_group(arggroup_name)
    auth_group.add_argument(
        '-u',
        '--username',
        required=False,
        action='store',
        dest='username',
        default=None,
        help='Name of user',
    )
    auth_group.add_argument(
        '-p',
        '--password',
        required=False,
        action='store',
        default=None,
        dest='password',
        help='Password of user',
    )
    auth_group.add_argument(
        '--session_id',
        required=False,
        action='store',
        default=None,
        dest='session_id',
        help='Session ID to authenticate with instead of username/password',
    )
    auth_group.add_argument(
        '--host',
        required=False,
        action='store',
        default=None,
        dest='host',
        help='Hostname/ip of SOAP Server',
    )
    auth_group.add_argument(
        '--port',
        required=False,
        action='store',
        default="443",
        dest='port',
        help='Port to use when connecting to SOAP Server',
    )

    arggroup_name = 'Handler Options'
    opt_group = parser.add_argument_group(arggroup_name)
    opt_group.add_argument(
        '-l',
        '--loglevel',
        required=False,
        action='store',
        type=int,
        default=0,
        dest='loglevel',
        help='Logging level to use, increase for more verbosity',
    )
    opt_group.add_argument(
        '--debugformat',
        required=False,
        action='store_true',
        default=False,
        dest='debugformat',
        help="Enable debug format for logging",
    )
    opt_group.add_argument(
        '--debug_method_locals',
        required=False,
        action='store_true',
        default=False,
        dest='debug_method_locals',
        help="Enable debug logging for each methods local variables",
    )
    opt_group.add_argument(
        '--record_all_requests',
        required=False,
        action='store_true',
        default=False,
        dest='record_all_requests',
        help="Record all requests in handler.session.ALL_REQUESTS_RESPONSES",
    )
    opt_group.add_argument(
        '--stats_loop_enabled',
        required=False,
        action='store_true',
        default=False,
        dest='stats_loop_enabled',
        help="Enable the statistics loop",
    )
    opt_group.add_argument(
        '--http_auth_retry',
        required=False,
        action='store_false',
        default=True,
        dest='http_auth_retry',
        help="Disable retry on HTTP authentication failures",
    )
    opt_group.add_argument(
        '--http_retry_count',
        required=False,
        action='store',
        type=int,
        default=5,
        dest='http_retry_count',
        help="Retry count for HTTP failures/invalid responses",
    )
    opt_group.add_argument(
        '--pytan_user_config',
        required=False,
        action='store',
        default='',
        dest='pytan_user_config',
        help=(
            "PyTan User Config file to use for PyTan arguments (defaults to: {})"
        ).format(constants.PYTAN_USER_CONFIG),
    )
    opt_group.add_argument(
        '--force_server_version',
        required=False,
        action='store',
        default='',
        dest='force_server_version',
        help=(
            "Force PyTan to consider the server version as this, instead of relying on the "
            "server version derived from the server info page."
        ),
    )
    return parser


def parent_parser(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`pytan.utils.parser` and return a parser object for adding arguments to
    """
    parser_parent = base_parser(desc=doc, help=False)
    parser = CustomArgParse(description=doc, parents=[parser_parent])
    return parser


def add_ask_report(parser):
    """Method to extend a :class:`CustomArgParse` class for command line scripts with arguments for scripts that need to supply export format subparsers for asking questions.
    """
    parser = add_report_file_options(parser=parser)

    arggroup_name = 'Export Options'
    arggroup = parser.add_argument_group(arggroup_name)

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--enable_sse',
        action='store_true',
        dest='sse',
        default=True,
        required=False,
        help='Perform a server side export when getting data'
    )
    group.add_argument(
        '--disable_sse',
        action='store_false',
        dest='sse',
        required=False,
        help='Perform a normal get result data export when getting data'
    )

    arggroup.add_argument(
        '--sse_format',
        required=False,
        action='store',
        default='xml_obj',
        choices=['csv', 'xml', 'xml_obj', 'cef'],
        dest='sse_format',
        help='If sse = True, perform server side export in this format',
    )

    arggroup.add_argument(
        '--leading',
        required=False,
        action='store',
        default='',
        dest='leading',
        help='If sse = True, and sse_format = "cef", prepend each row with this text',
    )
    arggroup.add_argument(
        '--trailing',
        required=False,
        action='store',
        default='',
        dest='trailing',
        help='If sse = True, and sse_format = "cef", append each row with this text',
    )

    arggroup.add_argument(
        '--export_format',
        action='store',
        default='csv',
        choices=['csv', 'xml', 'json'],
        dest='export_format',
        help='Export Format to create report file in, only used if sse = False',
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='For export_format: csv, Sort headers by given names'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Sort the headers with a basic alphanumeric sort (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--add-sensor',
        action='store_true',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Add the sensor names to each header'
    )
    group.add_argument(
        '--no-add-sensor',
        action='store_false',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not add the sensor names to each header (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--add-type',
        action='store_true',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Add the result type to each header'
    )
    group.add_argument(
        '--no-add-type',
        action='store_false',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not add the result type to each header (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--expand-columns',
        action='store_true',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Expand multi-line cells into their own rows that have sensor correlated columns in the new rows'
    )
    group.add_argument(
        '--no-columns',
        action='store_false',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='For export_format: csv, Do not add expand multi-line cells into their own rows (default)'
    )
    return parser


def add_report_file_options(parser):
    """Method to extend a :class:`CustomArgParse` class for command line scripts with arguments for scripts that need to supply export file and directory options.
    """
    opt_group = parser.add_argument_group('Report File Options')
    opt_group.add_argument(
        '--file',
        required=False,
        action='store',
        default=None,
        dest='report_file',
        help='File to save report to (will be automatically generated if not '
        'supplied)',
    )
    opt_group.add_argument(
        '--dir',
        required=False,
        action='store',
        default=None,
        dest='report_dir',
        help='Directory to save report to (current directory will be used if '
        'not supplied)',
    )
    return parser


def add_get_object_report(parser):
    """Method to extend a :class:`CustomArgParse` class for command line scripts with arguments for scripts that need to supply export format subparsers for getting objects.
    """
    parser = add_report_file_options(parser)
    arggroup_name = 'Export Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--export_format',
        action='store',
        default='csv',
        choices=['csv', 'xml', 'json'],
        dest='export_format',
        help='Export Format to create report file in, only used if sse = False',
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='Only for export_format csv, Sort headers by given names'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv, Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv, Sort the headers with a basic alphanumeric sort (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--no-explode-json',
        action='store_false',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv or json, Do not explode any embedded JSON into their own columns'
    )
    group.add_argument(
        '--explode-json',
        action='store_true',
        dest='explode_json_string_values',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format csv or json, Only for export_format csv, Explode any embedded JSON into their own columns (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--no-include_type',
        action='store_false',
        dest='include_type',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format json, Do not include SOAP type in JSON output'
    )
    group.add_argument(
        '--include_type',
        action='store_true',
        dest='include_type',
        required=False,
        default=argparse.SUPPRESS,
        help='Only for export_format json, Include SOAP type in JSON output (default)'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--no-minimal',
        action='store_false',
        dest='minimal',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format xml, Produce the full XML representation, including empty attributes'
    )
    group.add_argument(
        '--minimal',
        action='store_true',
        dest='minimal',
        default=argparse.SUPPRESS,
        required=False,
        help='Only for export_format xml, Only include attributes that are not empty (default)'
    )

    return parser


def write_pytan_user_config(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to write a pytan user config file.
    """
    parser = parent_parser(doc=doc)
    output_group = parser.add_argument_group('Write PyTan User Config Options')

    output_group.add_argument(
        '--file',
        required=False,
        default='',
        action='store',
        dest='file',
        help=(
            "PyTan User Config file to write for PyTan arguments (defaults to: {})"
        ).format(constants.PYTAN_USER_CONFIG),
    )
    return parser


def tsat(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to get objects.
    """
    parser = parent_parser(doc=doc)

    output_dir = os.path.join(os.getcwd(), 'TSAT_OUTPUT', calc.get_now())

    arggroup = parser.add_argument_group('TSAT General Options')
    arggroup.add_argument(
        '--platform',
        required=False,
        default=[],
        action='append',
        dest='platforms',
        help='Only ask questions for sensors on a given platform',
    )
    arggroup.add_argument(
        '--category',
        required=False,
        default=[],
        action='append',
        dest='categories',
        help='Only ask questions for sensors in a given category',
    )
    arggroup.add_argument(
        '--sensor',
        required=False,
        default=[],
        action='append',
        dest='sensors',
        help='Only run sensors that match these supplied names',
    )
    arggroup.add_argument(
        '--add_sensor',
        required=False,
        action='append',
        default=[],
        dest='add_sensor',
        help='Add sensor to every question that gets asked (i.e. "Computer Name")',
    )

    arggroup.add_argument(
        '--output_dir',
        required=False,
        action='store',
        default=output_dir,
        dest='report_dir',
        help='Directory to save output to',
    )
    arggroup.add_argument(
        '--sleep',
        required=False,
        type=int,
        action='store',
        default=1,
        dest='sleep',
        help='Number of seconds to wait between asking questions',
    )
    arggroup.add_argument(
        '--tsatdebug',
        required=False,
        action='store_true',
        default=False,
        dest='tsatdebug',
        help='Enable debug messages for just TSAT (not all of PyTan)',
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--prompt_missing_params',
        action='store_true',
        dest='param_prompt',
        default=True,
        required=False,
        help='If a sensor has parameters and none are supplied, prompt for the value (default)'
    )
    group.add_argument(
        '--no_missing_params',
        action='store_false',
        dest='param_prompt',
        default=argparse.SUPPRESS,
        required=False,
        help='If a sensor has parameters and none are supplied, error out.'
    )
    group.add_argument(
        '--skip_missing_params',
        action='store_const',
        const=None,
        dest='param_prompt',
        default=argparse.SUPPRESS,
        required=False,
        help='If a sensor has parameters and none are supplied, skip it',
    )

    arggroup.add_argument(
        '--build_config_file',
        required=False,
        action='store',
        default=None,
        dest='build_config_file',
        help='Build a configuration file by finding all sensors that have parameters and prompting for the values, then saving the key/value pairs as a JSON file that can be used by --config_file',
    )
    arggroup.add_argument(
        '--config_file',
        required=False,
        action='store',
        default=None,
        dest='config_file',
        help='Use a parameter configuration file built by --build_config_file for sensor parameters'
    )
    arggroup.add_argument(
        '-gp',
        '--globalparam',
        required=False,
        action='append',
        nargs=2,
        dest='globalparams',
        default=[],
        help='Global parameters in the format of "KEY" "VALUE" -- if any sensor uses "KEY" as a parameter name, then "VALUE" will be used for that sensors parameter',
    )

    arggroup = parser.add_argument_group('Question Asking Options')

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='question_filters',
        help='Whole question filter; pass --filters-help to get a full description',
    )
    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='question_options',
        help='Whole question option; pass --options-help to get a full description',
    )

    arggroup = parser.add_argument_group('Answer Polling Options')

    arggroup.add_argument(
        '--complete_pct',
        required=False,
        type=float,
        action='store',
        default=constants.Q_COMPLETE_PCT_DEFAULT,
        dest='complete_pct',
        help='Percent to consider questions complete',
    )
    arggroup.add_argument(
        '--override_timeout_secs',
        required=False,
        type=int,
        action='store',
        default=0,
        dest='override_timeout_secs',
        help='If supplied and not 0, instead of using the question expiration timestamp as the timeout, timeout after N seconds',
    )
    arggroup.add_argument(
        '--polling_secs',
        required=False,
        type=int,
        action='store',
        default=constants.Q_POLLING_SECS_DEFAULT,
        dest='polling_secs',
        help='Number of seconds to wait in between GetResultInfo loops while polling for each question',
    )
    arggroup.add_argument(
        '--override_estimated_total',
        required=False,
        type=int,
        action='store',
        default=0,
        dest='override_estimated_total',
        help='If supplied and not 0, use this as the estimated total number of systems instead of what Tanium Platform reports',
    )
    arggroup.add_argument(
        '--force_passed_done_count',
        required=False,
        type=int,
        action='store',
        default=0,
        dest='force_passed_done_count',
        help='If supplied and not 0, when this number of systems have passed the right hand side of the question (the question filter), consider the question complete instead of relying the estimated total that Tanium Platform reports',
    )

    # TODO: LATER, flush out SSE OPTIONS

    # arggroup_name = 'Server Side Export Options'
    # arggroup = parser.add_argument_group(arggroup_name)

    # arggroup.add_argument(
    #     '--sse',
    #     action='store_true',
    #     dest='sse',
    #     default=False,
    #     required=False,
    #     help='Perform a server side export when getting data'
    # )

    # arggroup.add_argument(
    #     '--sse_format',
    #     required=False,
    #     action='store',
    #     default='csv',
    #     choices=['csv', 'xml', 'cef'],
    #     dest='sse_format',
    #     help='If --sse, perform server side export in this format',
    # )

    # arggroup.add_argument(
    #     '--leading',
    #     required=False,
    #     action='store',
    #     default='',
    #     dest='leading',
    #     help='If --sse, and --sse_format = "cef", prepend each row with this text',
    # )
    # arggroup.add_argument(
    #     '--trailing',
    #     required=False,
    #     action='store',
    #     default='',
    #     dest='trailing',
    #     help='If --sse, and --sse_format = "cef", append each row with this text',
    # )

    arggroup_name = 'Answer Export Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--export_format',
        action='store',
        default='csv',
        choices=['csv', 'xml', 'json'],
        dest='export_format',
        help='If --no_sse, export Format to create report file in',
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--sort',
        default=[],
        action='append',
        dest='header_sort',
        required=False,
        help='If --no_sse and --export_format = csv, Sort headers by given names and then sort the rest alphabetically'
    )
    group.add_argument(
        '--no-sort',
        action='store_false',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='If --no_sse and --export_format = csv, Do not sort the headers at all'
    )
    group.add_argument(
        '--auto_sort',
        action='store_true',
        dest='header_sort',
        default=argparse.SUPPRESS,
        required=False,
        help='If --no_sse and --export_format = csv, Sort the headers with a basic alphanumeric sort'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--add-sensor',
        action='store_true',
        dest='header_add_sensor',
        default=argparse.SUPPRESS,
        required=False,
        help='If --no_sse and --export_format = csv, Add the sensor names to each header'
    )
    group.add_argument(
        '--no-add-sensor',
        action='store_false',
        dest='header_add_sensor',
        default=False,
        required=False,
        help='If --no_sse and --export_format = csv, Do not add the sensor names to each header'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--add-type',
        action='store_true',
        dest='header_add_type',
        default=argparse.SUPPRESS,
        required=False,
        help='If --no_sse and --export_format = csv, Add the result type to each header'
    )
    group.add_argument(
        '--no-add-type',
        action='store_false',
        dest='header_add_type',
        default=False,
        required=False,
        help='If --no_sse and --export_format = csv, Do not add the result type to each header'
    )

    group = arggroup.add_mutually_exclusive_group()
    group.add_argument(
        '--expand-columns',
        action='store_true',
        dest='expand_grouped_columns',
        default=argparse.SUPPRESS,
        required=False,
        help='If --no_sse and --export_format = csv, Expand multi-line cells into their own rows that have sensor correlated columns in the new rows'
    )
    group.add_argument(
        '--no-columns',
        action='store_false',
        dest='expand_grouped_columns',
        default=False,
        required=False,
        help='If --no_sse and --export_format = csv, Do not add expand multi-line cells into their own rows'
    )

    arggroup = parser.add_argument_group('PyTan Help Options')
    arggroup.add_argument(
        '--sensors-help',
        required=False,
        action='store_true',
        default=False,
        dest='sensors_help',
        help='Get the full help for sensor strings and exit',
    )
    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings and exit',
    )
    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings and exit',
    )

    arggroup = parser.add_argument_group('TSAT Show Options')
    arggroup.add_argument(
        '--show_platforms',
        required=False,
        action='store_true',
        default=False,
        dest='show_platforms',
        help='Print a list of all valid platforms (does not run sensors)',
    )
    arggroup.add_argument(
        '--show_categories',
        required=False,
        action='store_true',
        default=False,
        dest='show_categories',
        help='Print a list of all valid categories (does not run sensors)',
    )
    arggroup.add_argument(
        '--show_sensors',
        required=False,
        action='store_true',
        default=False,
        dest='show_sensors',
        help='Print a list of all valid sensor names, their categories, their platforms, and their parameters (does not run sensors)',
    )
    return parser


def get_object(obj, doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to get objects.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    get_object_group = parser.add_argument_group(arggroup_name)

    get_object_group.add_argument(
        '--all',
        required=False,
        default=False,
        action='store_true',
        dest='all',
        help='Get all {}s'.format(obj),
    )

    obj_map = tanium_obj.get_obj_map(obj)
    search_keys = copy.copy(obj_map['search'])

    if 'id' not in search_keys:
        search_keys.append('id')

    if obj == 'whitelisted_url':
        search_keys.append('url_regex')
    elif obj == 'user':
        search_keys.append('name')

    for k in search_keys:
        get_object_group.add_argument(
            '--{}'.format(k),
            required=False,
            action='append',
            default=[],
            dest=k,
            help='{} of {} to get'.format(k, obj),
        )

    return parser


def print_server_info(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to print sensor info.
    """
    parser = parent_parser(doc=doc)
    output_group = parser.add_argument_group('Output Options')

    output_group.add_argument(
        '--json',
        required=False,
        default=False,
        action='store_true',
        dest='json',
        help='Show a json dump of the server information',
    )
    return parser


def print_sensors(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to print server info.
    """
    parser = get_object(obj='sensor', doc=__doc__)
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--category',
        required=False,
        default=[],
        action='append',
        dest='categories',
        help='Only show sensors in given category',
    )
    output_group.add_argument(
        '--platform',
        required=False,
        default=[],
        action='append',
        dest='platforms',
        help='Only show sensors for given platform',
    )
    output_group.add_argument(
        '--hide_params',
        required=False,
        default=False,
        action='store_true',
        dest='hide_params',
        help='Do not show parameters in output',
    )
    output_group.add_argument(
        '--params_only',
        required=False,
        default=False,
        action='store_true',
        dest='params_only',
        help='Only show sensors with parameters',
    )
    output_group.add_argument(
        '--json',
        required=False,
        default=False,
        action='store_true',
        dest='json',
        help='Show a json dump of the server information',
    )
    return parser


def create_sensor(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a sensor.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create Sensor Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--unsupported',
        required=False,
        action='store',
        dest='unsupported',
        default=None,
        help='Creating sensors using this method not yet supported, use create_sensor_from_json instead!',
    )
    return parser


def create_group(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a group.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create Group Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='groupname',
        default=None,
        help='Name of group to create',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        dest='filters',
        default=[],
        help='Filters to use for group, supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        dest='filter_options',
        default=[],
        help='Filter options to use for group, supply --options-help to see options'
        ' help',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    return parser


def create_whitelisted_url(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a whitelisted_url.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create Whitelisted URL Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--url',
        required=True,
        action='store',
        dest='url',
        default=None,
        help='Text of new Whitelisted URL',
    )

    arggroup.add_argument(
        '--regex',
        required=False,
        action='store_true',
        dest='regex',
        default=False,
        help='Whitelisted URL is a regex pattern',
    )

    arggroup.add_argument(
        '-d',
        '--download',
        required=False,
        action='store',
        dest='download_seconds',
        type=int,
        default=86400,
        help='Download Whitelisted URL every N seconds',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to Whitelisted URL',
    )
    return parser


def create_package(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a package.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create Package Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of package to create',
    )

    arggroup.add_argument(
        '-c',
        '--command',
        required=True,
        action='store',
        dest='command',
        default='',
        help='Command to execute with package',
    )

    arggroup.add_argument(
        '-d',
        '--display-name',
        required=False,
        action='store',
        dest='display_name',
        default='',
        help='Display name of package',
    )

    arggroup.add_argument(
        '--command-timeout',
        required=False,
        action='store',
        dest='command_timeout_seconds',
        type=int,
        default=600,
        help='Command for this package timeout in N seconds',
    )

    arggroup.add_argument(
        '--expire-seconds',
        required=False,
        action='store',
        dest='expire_seconds',
        type=int,
        default=600,
        help='Expire actions created for this package in N seconds',
    )

    arggroup.add_argument(
        '-f',
        '--file-url',
        required=False,
        action='store',
        dest='file_urls',
        default=[],
        help='URL of file to include with package, can specify any of the '
        'following: "$url", or "$download_seconds::$url", or "$filename||$url",'
        ' or "$filename||$download_seconds::$url"',
    )

    arggroup.add_argument(
        '--parameters-file',
        required=False,
        action='store',
        dest='parameters_json_file',
        default='',
        help='JSON file describing parameters for this package, see '
        'doc/example_of_all_package_parameters.json for an example',
    )
    arggroup.add_argument(
        '-vf',
        '--verify-filter',
        required=False,
        action='append',
        dest='verify_filters',
        default=[],
        help='Filters to use for verifying the package after it is deployed, '
        ', supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-vo',
        '--verify-option',
        required=False,
        action='append',
        dest='verify_filter_options',
        default=[],
        help='Options to use for the verify filters, supply --options-help to see '
        'options help',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )

    arggroup.add_argument(
        '--verify-expire-seconds',
        required=False,
        action='store',
        dest='verify_expire_seconds',
        type=int,
        default=600,
        help='Expire the verify filters used by this package in N seconds',
    )
    return parser


def pytan_shell(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a python shell.
    """
    parser = base_parser(desc=doc, help=True)
    return parser


def get_session(doc):
    """Method to setup the base :clas:`CustomArgParse` class for command line scripts using :func:`base_parser`,then add specific
        arguments for scripts that use :mod:`pytan` to create a tanium session.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Get Session Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--persistent',
        required=False,
        action='store_true',
        dest='persistent',
        default=argparse.SUPPRESS,
        help='Persist session for 1 week after last use.',
    )

    return parser


def close_session(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`,then add specific
        arguments for scripts that use :mod:`pytan` to close open tanium sessions.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Close Session Optipons'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--all_session_ids',
        required=False,
        action='store_true',
        dest='all_session_ids',
        default=argparse.SUPPRESS,
        help='Closes all open tanium sessions.'
    )

    return parser


def create_user(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a user.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create User Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of user to create',
    )

    arggroup.add_argument(
        '-rn',
        '--rolename',
        required=False,
        action='append',
        dest='rolename',
        default=[],
        help='Name of role to assign to new user',
    )

    arggroup.add_argument(
        '-ri',
        '--roleid',
        required=False,
        action='append',
        type=int,
        dest='roleid',
        default=[],
        help='ID of role to assign to new user',
    )
    arggroup.add_argument(
        '-g',
        '--group',
        required=False,
        action='store',
        dest='group',
        default='',
        help='Name of group to assign to user',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to user',
    )
    return parser


def create_json_object(obj, doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create objects from json files.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Create {} from JSON Options'.format(obj.replace('_', ' ').capitalize())
    arggroup = parser.add_argument_group(arggroup_name)
    arggroup.add_argument(
        '-j',
        '--json',
        required=True,
        action='store',
        default='',
        dest='json_file',
        help='JSON file to use for creating the object',
    )
    return parser


def delete_object(obj, doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to delete objects.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    arggroup = parser.add_argument_group(arggroup_name)

    obj_map = tanium_obj.get_obj_map(obj)
    search_keys = copy.copy(obj_map['search'])

    if obj == 'whitelisted_url':
        search_keys.append('url_regex')
    elif obj == 'user':
        search_keys.append('name')

    for k in search_keys:
        arggroup.add_argument(
            '--{}'.format(k),
            required=False,
            action='append',
            default=[],
            dest=k,
            help='{} of {} to get'.format(k, obj),
        )

    return parser


def ask_saved(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask saved questions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Saved Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup_name = 'Saved Question Selectors'
    arggroup = parser.add_argument_group(arggroup_name)

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-refresh_data',
        action='store_false',
        dest='refresh_data',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not refresh the data available for a saved question (default)'
    )

    group.add_argument(
        '--refresh_data',
        action='store_true',
        dest='refresh_data',
        default=argparse.SUPPRESS,
        required=False,
        help='Refresh the data available for a saved question',
    )

    group = arggroup.add_mutually_exclusive_group()

    obj = 'saved_question'
    obj_map = tanium_obj.get_obj_map(obj)
    search_keys = copy.copy(obj_map['search'])
    for k in search_keys:
        group.add_argument(
            '--{}'.format(k),
            required=False,
            action='store',
            dest=k,
            help='{} of {} to ask'.format(k, obj),
        )

    parser = add_ask_report(parser=parser)
    return parser


def approve_saved_action(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to approve saved actions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Approve Saved Action Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-i',
        '--id',
        required=True,
        type=int,
        action='store',
        dest='id',
        help='ID of Saved Action to approve',
    )

    return parser


def stop_action(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to stop actions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Stop Action Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-i',
        '--id',
        required=True,
        type=int,
        action='store',
        dest='id',
        help='ID of Deploy Action to stop',
    )

    return parser


def deploy_action(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to deploy actions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Deploy Action Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--run',
        required=False,
        action='store_true',
        default=False,
        dest='run',
        help='Run the deploy action, if not supplied the deploy action will '
        'only ask the question that matches --filter and save the results to '
        'csv file for verification',
    )

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-results',
        action='store_false',
        dest='get_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not get the results after starting the deploy '
        'action'
    )
    group.add_argument(
        '--results',
        action='store_true',
        dest='get_results',
        default=True,
        required=False,
        help='Get the results after starting the deploy action '
        '(default)',
    )

    arggroup.add_argument(
        '-k',
        '--package',
        required=False,
        action='store',
        default='',
        dest='package',
        help='Package to deploy action with, optionally describe parameters, '
        'pass --package-help to get a full description',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='action_filters',
        help='Filter to deploy action against; pass --filters-help'
        'to get a full description',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='action_options',
        help='Options for deploy action filter; pass --options-help to get a '
        'full description',
    )

    arggroup.add_argument(
        '--start_seconds_from_now',
        required=False,
        action='store',
        type=int,
        default=None,
        dest='start_seconds_from_now',
        help='Start the action N seconds from now',
    )

    arggroup.add_argument(
        '--expire_seconds',
        required=False,
        action='store',
        type=int,
        default=None,
        dest='expire_seconds',
        help='Expire the action N seconds after it starts, if not supplied '
        'the packages own expire_seconds will be used',
    )

    arggroup.add_argument(
        '--package-help',
        required=False,
        action='store_true',
        default=False,
        dest='package_help',
        help='Get the full help for package string',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    parser = add_report_file_options(parser=parser)
    return parser


def get_results(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to get results for questions or actions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Get Result Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-o',
        '--object',
        action='store',
        default='question',
        choices=['saved_question', 'question', 'action'],
        dest='objtype',
        help='Type of object to get results for',
    )

    arggroup.add_argument(
        '-i',
        '--id',
        required=False,
        action='store',
        type=int,
        dest='id',
        help='id of object to get results for',
    )

    arggroup.add_argument(
        '-n',
        '--name',
        required=False,
        action='store',
        default='',
        dest='name',
        help='name of object to get results for',
    )
    parser = add_ask_report(parser)
    return parser


def ask_parsed(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask parsed questions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Parsed Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-q',
        '--question_text',
        required=True,
        action='store',
        default='',
        dest='question_text',
        help='The question text you want the server to parse into a list of parsed results',
    )

    arggroup.add_argument(
        '--picker',
        required=False,
        action='store',
        type=int,
        dest='picker',
        help='The index number of the parsed results that correlates to the actual question you wish to run -- you can get this by running this once without it to print out a list of indexes',
    )

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-results',
        action='store_false',
        dest='get_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not get the results after asking the quesiton '
        'action'
    )
    group.add_argument(
        '--results',
        action='store_true',
        dest='get_results',
        default=True,
        required=False,
        help='Get the results after asking the quesiton (default)',
    )
    parser = add_ask_report(parser=parser)
    return parser


def ask_manual(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to ask manual questions.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Manual Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-s',
        '--sensor',
        required=False,
        action='append',
        default=[],
        dest='sensors',
        help='Sensor, optionally describe parameters, options, and a filter'
        '; pass --sensors-help to get a full description',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        default=[],
        dest='question_filters',
        help='Whole question filter; pass --filters-help to get a full description',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        default=[],
        dest='question_options',
        help='Whole question option; pass --options-help to get a full description',
    )

    arggroup.add_argument(
        '--sensors-help',
        required=False,
        action='store_true',
        default=False,
        dest='sensors_help',
        help='Get the full help for sensor strings',
    )

    arggroup.add_argument(
        '--filters-help',
        required=False,
        action='store_true',
        default=False,
        dest='filters_help',
        help='Get the full help for filters strings',
    )

    arggroup.add_argument(
        '--options-help',
        required=False,
        action='store_true',
        default=False,
        dest='options_help',
        help='Get the full help for options strings',
    )
    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-results',
        action='store_false',
        dest='get_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not get the results after asking the quesiton '
        'action'
    )
    group.add_argument(
        '--results',
        action='store_true',
        dest='get_results',
        default=True,
        required=False,
        help='Get the results after asking the quesiton '
        '(default)',
    )
    parser = add_ask_report(parser=parser)
    return parser


def get_saved_question_history(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to get saved question history.
    """
    parser = parent_parser(doc=doc)

    arggroup_name = 'Saved Question Options'
    arggroup = parser.add_argument_group(arggroup_name)

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-empty_results',
        action='store_false',
        dest='empty_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not include details for questions with no data (default)'
    )

    group.add_argument(
        '--empty_results',
        action='store_true',
        dest='empty_results',
        default=argparse.SUPPRESS,
        required=False,
        help='Include details for questions with no data ',
    )

    group = arggroup.add_mutually_exclusive_group()

    group.add_argument(
        '--no-all_questions',
        action='store_false',
        dest='all_questions',
        default=argparse.SUPPRESS,
        required=False,
        help='Do not include details for ALL questions, only the ones associated with a given saved question via --name or --id (default)'
    )

    group.add_argument(
        '--all_questions',
        action='store_true',
        dest='all_questions',
        default=argparse.SUPPRESS,
        required=False,
        help='Include details for ALL questions',
    )

    opt_group = parser.add_argument_group('Report File Options')
    opt_group.add_argument(
        '--file',
        required=False,
        action='store',
        default='pytan_question_history_{}.csv'.format(calc.get_now()),
        dest='report_file',
        help='File to save report to',
    )
    opt_group.add_argument(
        '--dir',
        required=False,
        action='store',
        default=None,
        dest='report_dir',
        help='Directory to save report to (current directory will be used if not supplied)',
    )

    arggroup_name = 'Saved Question Selectors'
    arggroup = parser.add_argument_group(arggroup_name)

    group = arggroup.add_mutually_exclusive_group()

    obj = 'saved_question'
    obj_map = tanium_obj.get_obj_map(obj)
    search_keys = copy.copy(obj_map['search'])
    for k in search_keys:
        group.add_argument(
            '--{}'.format(k),
            required=False,
            action='store',
            dest=k,
            help='{} of {} to ask'.format(k, obj),
        )

    return parser
