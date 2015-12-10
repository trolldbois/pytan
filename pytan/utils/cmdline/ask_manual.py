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


def process_ask_manual_args(parser, handler, args):
    """Process command line args supplied by user for ask manual

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
        * response from :func:`pytan.handler.Handler.ask_manual`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = ['Manual Question Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    other_args = {a: b for a, b in args.__dict__.iteritems() if a not in obj_grp_args}

    print "++ Asking manual question:\n{}".format(pytan.utils.jsonify(obj_grp_args))

    try:
        response = handler.ask(qtype='manual', **obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    question = response['question_object']
    results = response['question_results']
    print "++ Asked Question {0.query_text!r} ID: {0.id!r}".format(question)

    if results:
        try:
            report_file, report_contents = handler.export_to_report_file(obj=results, **other_args)
        except Exception as e:
            traceback.print_exc()
            print "\n\nError occurred: {}".format(e)
            sys.exit(99)

        m = "++ Report file {!r} written with {} bytes".format
        print(m(report_file, len(report_contents)))
    else:
        print "++ No action results returned, run get_results.py to get the results"

    return response

