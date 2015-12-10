
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



def process_ask_saved_args(parser, handler, args):
    """Process command line args supplied by user for ask saved

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
        * response from :func:`pytan.handler.Handler.ask_saved`
    """
    id_arg = args.id
    name_arg = args.name
    refresh_arg = args.__dict__.get('refresh_data', False)

    q_args = {}

    if id_arg:
        q_args['id'] = id_arg
    elif name_arg:
        q_args['name'] = name_arg
    else:
        parser.error("Must supply --id or --name")

    q_args['refresh_data'] = refresh_arg

    print "++ Asking saved question: {}".format(pytan.utils.jsonify(q_args))

    try:
        response = handler.ask(qtype='saved', **q_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    question = response['question_object']
    results = response['question_results']
    print "++ Saved Question {0.query_text!r} ID: {0.id!r}".format(question)

    try:
        report_file, report_contents = handler.export_to_report_file(obj=results, **args.__dict__)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    response['report_file'] = report_file
    response['report_contents'] = report_contents

    m = "Report file {!r} written with {} bytes".format
    print(m(report_file, len(report_contents)))
    return response

