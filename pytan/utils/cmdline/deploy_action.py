
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


def process_deploy_action_args(parser, handler, args):
    """Process command line args supplied by user for deploy action

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response
        * response from :func:`pytan.handler.Handler.deploy_action`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = ['Deploy Action Options', 'Report File Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    print "++ Deploying action:\n{}".format(pytan.utils.jsonify(obj_grp_args))

    try:
        response = handler.deploy_action(**obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    action = response['action_object']
    print "++ Deployed Action {0.name!r} ID: {0.id!r}".format(action)
    print "++ Command used in Action: {0.package_spec.command!r}".format(action)

    if response['action_result_map']:
        print "++ Deploy action progress results:"
        for k, v in sorted(response['action_result_map'].iteritems()):
            print "Total {}: {}".format(k, v['total'])

    results = response['action_results']
    if results:
        if not obj_grp_args.get('report_file'):
            obj_grp_args['prefix'] = obj_grp_args.get('prefix', 'deploy_action_')

        try:
            report_file, report_contents = handler.export_to_report_file(
                obj=results, **obj_grp_args
            )
        except Exception as e:
            print "\n\nError occurred: {}".format(e)
            sys.exit(99)

        response['report_file'] = report_file
        response['report_contents'] = report_contents

        m = "++ Deploy results written to {!r} with {} bytes".format
        print(m(report_file, len(report_contents)))

    else:
        print (
            "++ No action results returned, run get_results.py to get the results"
        )

    return response
