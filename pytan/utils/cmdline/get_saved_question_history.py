
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


def process_get_saved_question_history_args(parser, handler, args):
    """Process command line args supplied by user for getting saved question history

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
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_user`
    """

    all_questions_bool = args.__dict__.get('all_questions', False)
    empty_results_bool = args.__dict__.get('empty_results', False)

    # if the user didn't specify ALL questions, lets find the saved question object so we can
    # filter all the questions down to just the ones for this saved question
    if not all_questions_bool:
        get_args = {'objtype': 'saved_question'}

        if args.id:
            get_args['id'] = args.id
        elif args.name:
            get_args['name'] = args.name
        else:
            parser.error("Must supply --id or --name of saved question if not using --all_questions")

        print "++ Finding saved question: {}".format(pytan.utils.jsonify(get_args))

        try:
            saved_question = handler.get(**get_args)[0]
        except Exception as e:
            traceback.print_exc()
            print "\n\nError occurred: {}".format(e)
            sys.exit(99)

        print "Found Saved Question: '{}'".format(saved_question)

    # get all questions
    try:
        all_questions = handler.get_all('question', include_hidden_flag=1)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    print "Found {} Total Questions".format(len(all_questions))

    if not all_questions_bool:
        all_questions = [
            x for x in all_questions
            if getattr(x.saved_question, 'id', '') == saved_question.id
        ]

        print (
            "Found {} Questions asked for Saved_question '{}'"
        ).format(len(all_questions), saved_question)

    print "Getting ResultInfo for {} Questions".format(len(all_questions))

    # store the ResultInfo for each question as x.result_info
    [
        setattr(x, 'result_info', handler.get_result_info(x))
        for x in all_questions
    ]

    if not empty_results_bool:
        all_questions = [
            x for x in all_questions
            if x.result_info.row_count
        ]
        print "Found {} Questions that actually have data".format(len(all_questions))

    # flatten out saved_question.id
    [
        setattr(x, 'saved_question_id', getattr(x.saved_question, 'id', '???'))
        for x in all_questions
    ]

    # derive start time from expiration and expire_seconds
    [
        setattr(x, 'start_time', pytan.utils.calculate_question_start_time(x)[0])
        for x in all_questions
    ]

    # flatten out result info attributes
    result_info_attrs = [
        'row_count',
        'estimated_total',
        'mr_tested',
        'passed',
    ]
    [
        setattr(x, y, getattr(x.result_info, y, '???'))
        for x in all_questions
        for y in result_info_attrs
    ]

    # dictify all questions for use with csv_dictwriter
    question_attrs = [
        'id',
        'query_text',
        'saved_question_id',
        'start_time',
        'expiration',
        'row_count',
        'estimated_total',
        'mr_tested',
        'passed',
    ]

    human_map = [
        'Question ID',
        'Question Text',
        'Spawned by Saved Question ID',
        'Question Started',
        'Question Expired',
        'Row Count',
        'Client Count Right Now',
        'Client Count that saw this question',
        'Client Count that passed this questions filters',
    ]

    all_question_dicts = [
        {human_map[question_attrs.index(k)]: str(getattr(x, k, '???')) for k in question_attrs}
        for x in all_questions
    ]

    # turn the list of dicts into a CSV string
    all_question_csv = csvdictwriter(
        rows_list=all_question_dicts,
        headers=human_map,
    )

    report_file = handler.create_report_file(
        contents=all_question_csv,
        report_file=args.report_file,
        report_dir=args.report_dir,
    )

    print "Wrote {} bytes to report file: '{}'".format(len(all_question_csv), report_file)
    return report_file
