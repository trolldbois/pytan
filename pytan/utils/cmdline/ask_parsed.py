
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


def process_ask_parsed_args(parser, handler, args):
    """Process command line args supplied by user for ask parsed

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
        * response from :func:`pytan.handler.Handler.ask_parsed`
    """
    # TODO: SSE FORMAT NOT BEING RECOGNIZED?
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = ['Parsed Question Options', 'Export Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts if getattr(args, k, None)}

    print "++ Asking parsed question:\n{}".format(pytan.utils.jsonify(obj_grp_args))

    try:
        response = handler.ask(qtype='parsed', **obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    question = response['question_object']
    results = response['question_results']
    print "++ Asked Question {0.query_text!r} ID: {0.id!r}".format(question)

    if results:
        try:
            report_file, report_contents = handler.export_to_report_file(
                obj=results, **args.__dict__
            )
        except Exception as e:
            print "\n\nError occurred: {}".format(e)
            sys.exit(99)

        m = "++ Report file {!r} written with {} bytes".format
        print(m(report_file, len(report_contents)))
    else:
        print "++ No action results returned, run get_results.py to get the results"

    return response

