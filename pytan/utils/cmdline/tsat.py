
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


class TsatWorker(object):
    '''no doc as of yet, push to re-write

    relies on functions in binsupport:
        * filter_filename
        * csvdictwriter
        * filter_sourced_sensors
        * filter_sensors

    '''
    DEBUG_FORMAT = (
        '[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n'
        '%(levelname)-8s %(name)s %(message)s'
    )
    """
    Logging format for debugformat=True
    """

    CON_INFO_FORMAT = (
        '%(levelname)-8s %(message)s'
    )
    """
    Console Logging format for debugformat=False
    """

    FILE_INFO_FORMAT = (
        '%(asctime)s %(levelname)-8s %(message)s'
    )
    """
    Console Logging format for debugformat=False
    """

    LOG_LEVEL = logging.DEBUG
    MY_NAME = "tsat"
    ARGS = None
    PARSER = None
    HANDLER = None
    MY_KWARGS = None
    CON_LOG_OUTPUT = sys.stdout
    SHOW_ARGS = False
    FINAL_REPORT_HEADERS = [
        'sensor',
        'msg',
        'failure_msg',
        'question',
        'question_id',
        'elapsed_seconds',
        'rows_returned',
        'report_file',
        'estimated_total_clients',
    ]

    PARAM_VALS = {'global': {}}

    def __init__(self, parser, args, handler, **kwargs):
        self.ARGS = args
        self.PARSER = parser
        self.HANDLER = handler
        self.MY_KWARGS = kwargs

    def start(self):
        self.check_help_args()
        self.check_log_format()
        self.set_log_level()
        self.set_mylog()
        show_opts = self.get_parser_args(['TSAT Show Options'])
        if any(show_opts.values()):
            self.handle_show_opts()
        else:
            self.check_report_dir()
            logfile_path = self.get_logfile_path(self.MY_NAME, self.ARGS.report_dir)
            self.add_file_log(logfile_path)
            self.set_sensors()
            self.check_config_file()
            if self.ARGS.build_config_file:
                self.build_config_file()
            else:
                self.add_cmdline_global_params()
                reports = self.run_sensors()
                self.write_final_results(reports)

    def handle_show_opts(self):
        self.sensors = self.HANDLER.get_all('sensor')
        if self.ARGS.show_platforms:
            self.show_platforms()
        if self.ARGS.show_categories:
            self.show_categories()
        if self.ARGS.show_sensors:
            self.show_sensors()

    def load_parameters(self, sensor):
        param_def = sensor.parameter_definition or {}
        if param_def:
            try:
                param_def = json.loads(param_def)
            except:
                m = "Error loading JSON parameter definition for sensor {}: {}".format
                self.mylog.error(m(sensor.name, param_def))
                param_def = {}
        params = param_def.get('parameters', [])
        return params

    def show_sensors(self):
        for x in sorted(self.sensors, key=lambda x: x.category):
            platforms = parse_sensor_platforms(x)
            params = self.load_parameters(x)
            desc = (x.description or '').replace('\n', ' ').strip()

            out = [
                "* Sensor Name: '{sensor.name}'",
                "  * Platforms: {platforms}",
                "  * Category: {sensor.category}",
                "  * Description: {description}",
            ]

            skip_attrs = [
                'model',
                'parameterType',
                'snapInterval',
                'validationExpressions',
                'key',
            ]

            for param in params:
                for k, v in sorted(param.iteritems()):
                    if k in skip_attrs:
                        continue
                    out.append("  * Parameter '{}' - '{}': {}".format(param['key'], k, v))

            linesep = '__________________________________________\n'
            out = (linesep + '\n'.join(out)).format
            self.mylog.info(out(sensor=x, platforms=', '.join(platforms), description=desc))

    def show_categories(self):
        cats = sorted(list(set([x.category for x in self.sensors if x.category])))
        cats = '\n\t'.join(cats)
        self.mylog.info("List of valid categories:\n\t{}".format(cats))

    def show_platforms(self):
        all_plats = []
        for x in self.sensors:
            platforms = parse_sensor_platforms(x)
            if not platforms:
                continue
            for p in platforms:
                if p in all_plats:
                    continue
                all_plats.append(p)
        all_plats = '\n\t'.join(sorted(all_plats))
        self.mylog.info("List of valid platforms:\n\t{}".format(all_plats))

    def check_help_args(self):
        help_args = self.get_parser_args(['Help Options'])
        if any(help_args.values()):
            self.HANDLER.ask_manual(**help_args)
            raise Exception("Help option supplied!")

    def check_log_format(self):
        if self.ARGS.debugformat:
            self.CON_INFO_FORMAT = self.DEBUG_FORMAT
            self.FILE_INFO_FORMAT = self.DEBUG_FORMAT

    def set_log_level(self):
        if self.ARGS.tsatdebug or self.ARGS.loglevel >= 4:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
        self.LOG_LEVEL = log_level

    def remove_file_log(self, logfile):
        """Utility to remove a log file from python's logging module"""
        basename = os.path.basename(logfile)
        root_logger = logging.getLogger()
        try:
            for x in root_logger.handlers:
                if x.name == basename:
                    root_logger.removeHandler(x)
                    self.mylog.debug('Stopped file logging to: {}'.format(logfile))
        except:
            pass

    # TODO WRAP ME AROUND THE log.py funcs!
    def add_file_log(self, logfile):
        """Utility to add a log file from python's logging module"""
        self.remove_file_log(logfile)
        root_logger = logging.getLogger()
        basename = os.path.basename(logfile)
        try:
            self.mylog.debug('Adding file logging to: {}'.format(logfile))
            file_handler = logging.FileHandler(logfile)
            file_handler.set_name(basename)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(self.FILE_INFO_FORMAT))
            root_logger.addHandler(file_handler)
        except Exception as e:
            self.mylog.error('Problem setting up file logging to {}: {}'.format(logfile, e))
            raise

    def set_mylog(self):
        logging.Formatter.converter = time.gmtime

        ch = logging.StreamHandler(self.CON_LOG_OUTPUT)
        ch.setLevel(self.LOG_LEVEL)
        ch.setFormatter(logging.Formatter(self.CON_INFO_FORMAT))

        mylog = logging.getLogger(self.MY_NAME)
        mylog.setLevel(logging.DEBUG)

        for handler in mylog.handlers:
            mylog.removeHandler(handler)

        mylog.addHandler(ch)
        self.mylog = mylog

    def check_report_dir(self):
        if not os.path.exists(self.ARGS.report_dir):
            os.makedirs(self.ARGS.report_dir)
            self.mylog.debug("Created report_dir: {}".format(self.ARGS.report_dir))

        self.mylog.info("Using report_dir: {}".format(self.ARGS.report_dir))

    def set_sensors(self):
        sensors = self.HANDLER.get_all('sensor')
        self.mylog.info("Found {} total sensors".format(len(sensors)))

        # filter out all sensors that have a source_id
        # (i.e. are created as temp sensors for params)
        real_sensors = filter_sourced_sensors(sensors=sensors)
        self.mylog.info("Filtered out sourced sensors: {}".format(len(real_sensors)))

        if not real_sensors:
            m = "No sensors found!"
            self.mylog.error(m)
            raise Exception(m)

        filtered_sensors = filter_sensors(
            sensors=real_sensors,
            filter_platforms=self.ARGS.platforms,
            filter_categories=self.ARGS.categories,
        )
        m = "Filtered out sensors based on platform/category filters: {}".format
        self.mylog.info(m(len(filtered_sensors)))

        # only include sensors with params
        # filtered_sensors = [x for x in filtered_sensors if self.load_parameters(x)]

        if self.ARGS.sensors:
            filtered_sensors = [
                x for x in filtered_sensors
                if x.name.lower() in [y.lower() for y in self.ARGS.sensors]
            ]
        m = "Filtered out sensors based on sensor names: {}".format
        self.mylog.info(m(len(filtered_sensors)))

        if not filtered_sensors:
            m = (
                "Platform/Category/Sensor name filters too restrictive, no sensors match! "
                "Try --show_platforms and/or --show_categories"
            )
            self.mylog.error(m)
            raise Exception(m)

        self.sensors = filtered_sensors

    def build_config_file(self):
        for sensor in self.sensors:
            sensor_param_defs = self.load_parameters(sensor)

            if not sensor_param_defs:
                m = "Skipping sensor {!r}, no parameters defined".format
                self.mylog.debug(m(sensor.name))
                continue

            for sp in sensor_param_defs:
                key = str(sp['key'])
                sp['sensor_value'] = self.PARAM_VALS.get(sensor.name, {}).get(key, None)
                sp['global_value'] = self.PARAM_VALS.get('global', {}).get(key, None)
                if not any([sp['sensor_value'], sp['global_value']]):
                    self.param_value_prompt(sensor, sp)
                    m = "parameter values updated to: {}".format
                    self.mylog.debug(m(self.PARAM_VALS))

        config = {}
        config['parameters'] = self.PARAM_VALS
        config_json = pytan.utils.jsonify(config)
        try:
            fh = open(self.ARGS.build_config_file, 'wb')
            fh.write(config_json)
            fh.close()
            m = "Configuration file written to: {}".format
            self.mylog.info(m(self.ARGS.build_config_file))
        except:
            m = "Unable to write configuration to: {}".format
            self.mylog.error(m(self.ARGS.build_config_file))
            raise

    def check_config_file(self):
        cfile = self.ARGS.config_file

        if not cfile:
            return

        if not os.path.isfile(cfile):
            m = "Configuration file does not exist: {}".format
            raise Exception(m(cfile))

        try:
            fh = open(cfile)
            config = json.load(fh)
            fh.close()
            m = "Configuration file read from: {}".format
            self.mylog.info(m(cfile))
        except:
            m = "Configuration file unable to be read from: {}".format
            self.mylog.error(m(cfile))
            raise

        if 'parameters' not in config:
            m = "No 'parameters' section in configuration file, not loading parameter values"
            self.mylog.error(m)
            return

        self.PARAM_VALS.update(config['parameters'])
        m = "Loaded 'parameters' section from configuration file"
        self.mylog.info(m)
        return

    def add_cmdline_global_params(self):
        if self.ARGS.globalparams:
            cgp = dict(self.ARGS.globalparams)
            self.PARAM_VALS['global'].update(cgp)
            self.mylog.debug("Updated global parameters to: {}".format(self.PARAM_VALS['global']))

    def run_sensors(self):
        if self.ARGS.build_config_file:
            m = "Not running sensors, --build_config_file was specified!".format
            self.mylog.info(m())
            return

        self.all_start_time = datetime.datetime.now()

        reports = []
        for idx, sensor in enumerate(self.sensors):
            sensor_dir = self.get_sensor_dir(sensor.name)
            logfile_path = self.get_logfile_path(sensor.name, sensor_dir)
            self.add_file_log(logfile_path)

            start_time = datetime.datetime.now()
            report_info = self.run_sensor(idx, sensor)
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            report_info['elapsed_seconds'] = elapsed_time.seconds

            if report_info['status']:
                loglvl = self.mylog.info
                report_info['prefix'] = '++'
            else:
                loglvl = self.mylog.error
                report_info['prefix'] = '!!'

            m = '{prefix} {msg} for question {question!r} in {elapsed_seconds} seconds'.format
            loglvl(m(**report_info))

            if report_info['failure_msg']:
                self.mylog.error("!! {}".format(report_info['failure_msg']))

            # m = 'report_info:\n{}'.format
            # self.mylog.debug(m(pprint.pformat(report_info)))
            self.remove_file_log(logfile_path)

            reports.append(report_info)
            time.sleep(self.ARGS.sleep)

        self.all_end_time = datetime.datetime.now()
        self.all_elapsed_time = self.all_end_time - self.all_start_time
        return reports

    def get_parser_args(self, grps):
        parser_opts = get_grp_opts(parser=self.PARSER, grp_names=grps)
        p_args = {k: getattr(self.ARGS, k) for k in parser_opts}
        return p_args

    def param_type_prompt(self, sensor, param_def):
        key = param_def['key']
        typeprompt = (
            "\n"
            "Choose from the following type for parameter '{}' in sensor '{}':\n"
            "\n"
            "   (1) Global sensor value (default)\n"
            "   (2) Sensor specific value\n"
            "\n"
            "Global sensor values will be used for all sensors with the same parameter name "
            "unless they have their own sensor specific value specified\n"
            "\n"
            "Enter Choice: "
        ).format(key, sensor.name)

        typemap = {
            "": 'global',
            "1": 'global',
            "2": sensor.name,
        }

        param_section = None

        while True:
            ptype = raw_input(typeprompt)
            if ptype not in typemap:
                m = "\n!! Invalid choice '{}', must be one of: {}\n".format
                print m(ptype, ', '.join(typemap.keys()))
                continue

            if param_section == 'global':
                ptxt = 'global sensor'
            else:
                ptxt = 'sensor specific'

            print "\n~~ Will store value as {}".format(ptxt)
            param_section = typemap[ptype]
            break
        return param_section

    def param_value_prompt(self, sensor, param_def, param_section=None):
        key = param_def['key']
        ptxt = {
            'ptype': 'sensor specific',
            'key': key,
            'sname': sensor.name,
            'help_str': "No help defined",
        }

        if param_section is None:
            param_section = self.param_type_prompt(sensor, param_def)

        if param_section == 'global':
            ptxt['ptype'] = 'global sensor'

        valueprompt = [
            "",
            "Supply the {ptype} value for parameter '{key}' in sensor '{sname}'"
            "",
            "",
        ]

        defval = str(param_def.get('defaultValue', ''))
        if defval:
            ptxt['defval'] = defval
            valueprompt.append("  * Default Defined Value: {defval}")

        label = param_def.get('label', '')
        if label:
            ptxt['label'] = label
            valueprompt.append("  * Label: {label}")

        valid_values = param_def.get('values', [])
        if valid_values:
            ptxt['valid_values'] = ', '.join(valid_values)
            valueprompt.append("  * Valid Values: {valid_values}")

        help_str = param_def.get('helpString', '')
        if help_str:
            ptxt['help_str'] = help_str
            valueprompt.append("  * Help string: {help_str}")

        prompt_str = param_def.get('promptText', '')
        if prompt_str:
            ptxt['prompt_str'] = prompt_str
            valueprompt.append("  * Prompt string: {prompt_str}")

        maxchars = param_def.get('maxChars', None)
        if maxchars is not None:
            ptxt['maxchars'] = maxchars
            valueprompt.append("  * Maximum Characters: {maxchars}")

        minval = param_def.get('minimum', None)
        if minval is not None:
            ptxt['minval'] = minval
            valueprompt.append("  * Minimum Value: {minval}")

        maxval = param_def.get('maximum', None)
        if maxval is not None:
            ptxt['maxval'] = maxval
            valueprompt.append("  * Maximum Value: {maxval}")

        valueprompt.append("\nEnter value: ")
        valueprompt = '\n'.join(valueprompt).format(**ptxt)

        param_value = None
        while True:
            param_value = raw_input(valueprompt)
            if not param_value:
                if defval:
                    print "\n~~ Using default value of: '{}'".format(defval)
                    param_value = defval
                    break

                if valid_values:
                    print "\n~~ Using first valid value of: '{}'".format(valid_values[0])
                    param_value = valid_values[0]
                    break

            if valid_values and param_value not in valid_values:
                m = "\n!! Invalid choice '{}', must be one of: {}\n".format
                print m(param_value, valid_values)
                continue

            if not param_value:
                m = "\n!! No default value defined, must supply a value!\n".format
                print m()
                continue

            if param_value:
                break

        if param_section not in self.PARAM_VALS:
            self.PARAM_VALS[param_section] = {}

        self.PARAM_VALS[param_section][key] = param_value

        return param_value

    def run_sensor(self, idx, sensor):
        handler = self.HANDLER
        report_info = {
            'sensor': sensor.name,
            'msg': 'Not yet run question for {}'.format(sensor.name),
            'report_file': '',
            'elapsed_seconds': -1,
            'question': '',
            'failure_msg': '',
            'status': False,
            'estimated_total_clients': -1,
            'rows_returned': -1,
        }

        current_count = "({}/{})".format(idx + 1, len(self.sensors))

        param_dict = {}
        sensor_param_defs = self.load_parameters(sensor)

        if sensor_param_defs:
            m = "-- Parsing parameters for sensor: {} {}".format
            self.mylog.info(m(sensor.name, current_count))

        fetch_map = [
            {'section': sensor.name, 'name': 'Sensor specific param'},
            {'section': 'global', 'name': 'Global param'},
        ]

        for sp in sensor_param_defs:
            key = str(sp['key'])

            for x in fetch_map:
                value = self.PARAM_VALS.get(x['section'], {}).get(key, None)
                if value is None:
                    m = "{} not found for key '{}', checking global".format
                    self.mylog.debug(m(x['name'], key))
                else:
                    m = "{} found for key '{}', value '{}'".format
                    self.mylog.debug(m(x['name'], key, value))
                    break

            if value is None:
                if self.ARGS.param_prompt is None:
                    m = "Skipped sensor {!r}, no parameter value supplied for '{}'".format
                    report_info['failure_msg'] = m(sensor.name, key)
                    return report_info

                elif self.ARGS.param_prompt is False:
                    m = "Stopped at sensor {!r}, no parameter value supplied for '{}'".format
                    raise Exception(m(sensor.name, key))

                elif self.ARGS.param_prompt is True:
                    value = self.param_value_prompt(sensor, sp)

            if value is None:
                m = "Stopped at sensor {!r}, still no parameter value supplied for '{}'".format
                raise Exception(m(sensor.name, key))
            else:
                param_dict[key] = value
                continue

        if param_dict:
            for k, v in param_dict.iteritems():
                if v.startswith('eval:'):
                    orig_v = v.replace('eval:', '')
                    try:
                        v = eval(orig_v)
                        param_dict[k] = v
                        m = "Evaluated key '{}' value '{}' into value '{}' for sensor: '{}'".format
                        self.mylog.info(m(k, orig_v, v, sensor.name))
                    except:
                        m = "Failed to evaluate key '{}' using value '{}' for sensor: '{}'".format
                        self.mylog.error(m(k, v, sensor.name))
                        raise

                m = "@@ Parameter key '{}' using value '{}' for sensor: '{}'".format
                self.mylog.info(m(k, v, sensor.name))

        m = "-- Asking question for sensor: '{}' {}".format
        self.mylog.info(m(sensor.name, current_count))

        sensor_defs = []
        sensor_def = {'filter': {}, 'params': param_dict, 'name': sensor.name, 'options': {}}
        sensor_defs.append(sensor_def)

        if self.ARGS.add_sensor:
            add_sensor_defs = pytan.utils.dehumanize_sensors(sensors=self.ARGS.add_sensor)
            sensor_defs += add_sensor_defs

        q_filter_defs = pytan.utils.dehumanize_question_filters(
            question_filters=self.ARGS.question_filters
        )
        q_option_defs = pytan.utils.dehumanize_question_options(
            question_options=self.ARGS.question_options
        )

        q_args = {}
        q_args['sensor_defs'] = sensor_defs
        q_args['question_filter_defs'] = q_filter_defs
        q_args['question_option_defs'] = q_option_defs
        q_args['get_results'] = False

        if self.SHOW_ARGS:
            self.mylog.debug("_ask_manual args:\n{}".format(pprint.pformat(q_args)))

        try:
            ret = handler._ask_manual(**q_args)
            report_info['msg'] = "Successfully asked"
            report_info['question'] = ret['question_object'].query_text
            report_info['question_id'] = ret['question_object'].id
        except Exception as e:
            m = "Question failed to be asked: {}".format(e)
            report_info['failure_msg'] = m
            return report_info

        m = "-- Polling question for sensor: '{}' {}".format
        self.mylog.info(m(sensor.name, current_count))

        p_args = self.get_parser_args(['Answer Polling Options'])
        p_args['handler'] = handler
        p_args['obj'] = ret['question_object']

        if self.SHOW_ARGS:
            self.mylog.debug("QuestionPoller args:\n{}".format(pprint.pformat(p_args)))

        try:
            poller = pytan.pollers.QuestionPoller(**p_args)
            poller_result = poller.run()
            report_info['msg'] = "Successfully asked and polled"
            report_info['estimated_total_clients'] = poller.result_info.estimated_total
        except Exception as e:
            m = "Question failed to be polled for answers: {}".format(e)
            report_info['failure_msg'] = m
            return report_info

        m = "-- Getting answers for sensor: '{}' {}".format
        self.mylog.info(m(sensor.name, current_count))

        # TODO: LATER, flush out SSE OPTIONS
        # if self.ARGS.sse and handler.session.platform_is_6_5():
        #     grd = handler.get_result_data_sse
        #     grd_args = self.get_parser_args(['Server Side Export Options'])
        # else:
        grd = handler.get_result_data
        grd_args = {}
        grd_args['obj'] = ret['question_object']

        if self.SHOW_ARGS:
            self.mylog.debug("{} args:\n{}".format(grd.__name__, pprint.pformat(grd_args)))

        try:
            rd = grd(**grd_args)
            rows_returned = len(getattr(rd, 'rows', []))
            report_info['rows_returned'] = rows_returned
            m = "Successfully asked, polled, and retrieved answers ({} rows)".format
            report_info['msg'] = m(rows_returned)
        except Exception as e:
            m = "Failed to retrieve answers: {}".format(e)
            report_info['failure_msg'] = m
            return report_info

        if not rd:
            m = "Unable to export question results to report file, no answers returned!"
            report_info['failure_msg'] = m
            return report_info

        if not rows_returned:
            m = "Unable to export question results to report file, no rows returned!"
            report_info['failure_msg'] = m
            return report_info

        m = "-- Exporting answers ({} rows) for sensor: '{}' {}".format
        self.mylog.info(m(rows_returned, sensor.name, current_count))

        e_args = self.get_parser_args(['Answer Export Options'])
        e_args['obj'] = rd
        e_args['report_dir'] = self.get_sensor_dir(sensor.name)

        if self.SHOW_ARGS:
            self.mylog.debug("export_to_report_file args:\n{}".format(pprint.pformat(p_args)))

        try:
            report_file, result = handler.export_to_report_file(**e_args)
            report_info['report_file'] = report_file
            m = "Successfully asked, polled, retrieved, and exported answers ({} rows)".format
            report_info['msg'] = m(rows_returned)
        except Exception as e:
            m = "Unable to export answers to report file, error: {}".format(e)
            report_info['failure_msg'] = m
            return report_info

        report_info['status'] = poller_result
        return report_info

    def get_sensor_dir(self, sensor_name):
        sensor_dir = os.path.join(self.ARGS.report_dir, filter_filename(sensor_name))
        if not os.path.exists(sensor_dir):
            os.makedirs(sensor_dir)
        return sensor_dir

    def get_logfile_path(self, logname, logdir):
        logfile = '{}_{}.log'.format(logname, pytan.utils.get_now())
        logfile = filter_filename(logfile)
        logfile_path = os.path.join(logdir, logfile)
        return logfile_path

    def write_final_results(self, reports):
        csv_str = csvdictwriter(reports, headers=self.FINAL_REPORT_HEADERS)
        csv_file = '{}_{}.csv'.format(self.MY_NAME, pytan.utils.get_now())
        csv_file = filter_filename(csv_file)
        csv_file_path = os.path.join(self.ARGS.report_dir, csv_file)

        csv_fh = open(csv_file_path, 'wb')
        csv_fh.write(csv_str)
        csv_fh.close()

        m = "Final CSV results of from all questions run written to: {}".format
        self.mylog.info(m(csv_file_path))
        m = "TSAT started: {}".format
        self.mylog.info(m(self.all_start_time))
        m = "TSAT ended: {}".format
        self.mylog.info(m(self.all_end_time))
        m = "TSAT elapsed time: {}".format
        self.mylog.info(m(self.all_elapsed_time))


def process_tsat_args(parser, handler, args):
    """Process command line args supplied by user for tsat

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    try:
        tsatworker = TsatWorker(parser=parser, handler=handler, args=args)
        tsatworker.start()
    except Exception as e:
        traceback.print_exc()
        print "\nError occurred: {}".format(e)
        sys.exit(100)
