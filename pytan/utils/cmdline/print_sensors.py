# DO TSAT FIRST
from . import base
from .. import pretty


class Worker(base.Base):
    DESCRIPTION = 'Get sensors based on options and print their information out'
    GROUP_NAME = 'Print Sensors Options'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '--json',
            required=False, default=False, action='store_true', dest='json',
            help='Just print the raw JSON, instead of pretty printing the elements',
        )
        self.grp.add_argument(
            '--hide_params',
            required=False, default=False, action='store_true', dest='hide_params',
            help='Do not show parameters in output',
        )

        self.grp = self.parser.add_argument_group('Filtering Options')
        self.grp.add_argument(
            '--category',
            required=False, default=[], action='append', dest='categories',
            help='Only show sensors in given category',
        )
        self.grp.add_argument(
            '--platform',
            required=False, default=[], action='append', dest='platforms',
            help='Only show sensors for given platform',
        )
        self.grp.add_argument(
            '--params_only',
            required=False, default=False, action='store_true', dest='params_only',
            help='Only show sensors with parameters',
        )

    def get_response(self, kwargs):
        m = "++ Getting server info"
        print m.format()
        response = self.handler.session.get_server_info()
        m = "++ Server info fetched successfully for {} sections"
        print m.format(len(response['diags_flat']))

        if kwargs['json']:
            result = pretty.jsonify(response['diags_flat'])
        else:
            result = pretty.pretty_dict(response['diags_flat'])
        print result

        return response

    def get_result(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        return response


def print_sensors(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to print server info.
    """
    return parser



def process_print_sensors_args(parser, handler, args):
    """Process command line args supplied by user for printing sensors

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    all_sensors = process_get_object_args(
        parser=parser, handler=handler, obj='sensor', args=args, report=False
    )

    real_sensors = filter_sourced_sensors(all_sensors)
    print "Filtered out sourced sensors: {}".format(len(real_sensors))

    filtered_sensors = filter_sensors(
        sensors=real_sensors, filter_platforms=args.platforms, filter_categories=args.categories,
    )
    print "Filtered out sensors based on user filters: {}".format(len(filtered_sensors))

    if args.json:
        for x in filtered_sensors:
            result = handler.export_obj(obj=x, export_format='json')
            print "{}:\n{}".format(x, result)
        sys.exit()

    for x in sorted(filtered_sensors, key=lambda x: x.category):
        platforms = parse_sensor_platforms(x)

        param_def = x.parameter_definition or {}
        if param_def:
            try:
                param_def = json.loads(param_def)
            except:
                print "Error loading JSON parameter definition {}".format(param_def)
                param_def = {}

        params = param_def.get('parameters', [])
        if args.params_only and not params:
            continue

        desc = (x.description or '').replace('\n', ' ').strip()
        print (
            "\n  * Sensor Name: '{0.name}', Platforms: {1}, Category: {0.category}"
        ).format(x, ', '.join(platforms))
        print "  * Description: {}".format(desc)

        if args.hide_params:
            continue

        skip_attrs = [
            'model',
            'parameterType',
            'snapInterval',
            'validationExpressions',
            'key',
        ]

        for param in params:
            print "  * Parameter '{}':".format(param['key'])
            for k, v in sorted(param.iteritems()):
                if k in skip_attrs:
                    continue
                if not v:
                    continue
                print "    - '{}': {}".format(k, v)

