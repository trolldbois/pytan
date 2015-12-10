# CHANGE THIS TO GET_QUESTION_RESULTS / etc


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


def process_get_results_args(parser, handler, args):
    """Process command line args supplied by user for getting results

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args
        * args object from parsing `parser`

    Returns
    -------
    report_path, report_contents : tuple
        * results from :func:`pytan.handler.Handler.export_to_report_file` on the return of :func:`pytan.handler.Handler.get_result_data`
    """
    try:
        obj = handler.get(**args.__dict__)[0]
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    m = "++ Found object: {}".format
    print(m(obj))

    if args.sse:
        try:
            results_obj = handler.get_result_data_sse(obj=obj, **args.__dict__)
        except Exception as e:
            print "\n\nError occurred: {}".format(e)
            sys.exit(99)

    else:
        try:
            results_obj = handler.get_result_data(obj=obj, **args.__dict__)
        except Exception as e:
            print "\n\nError occurred: {}".format(e)
            sys.exit(99)

    if isinstance(results_obj, taniumpy.object_types.result_set.ResultSet):
        if results_obj.rows:
            m = "++ Found results for object: {}".format
            print(m(results_obj))

            try:
                report_path, report_contents = handler.export_to_report_file(
                    obj=results_obj, **args.__dict__
                )
            except Exception as e:
                traceback.print_exc()
                print "\n\nError occurred: {}".format(e)
                sys.exit(99)

            m = "++ Report file {!r} written with {} bytes".format
            print(m(report_path, len(report_contents)))

        else:
            report_contents = results_obj
            report_path = ''
            m = "++ No rows returned for results: {}".format
            print(m(results_obj))

    else:
        report_contents = results_obj
        report_path = handler.create_report_file(contents=report_contents, **args.__dict__)
        m = "++ Report file {!r} written with {} bytes".format
        print(m(report_path, len(report_contents)))

    return report_path, report_contents

