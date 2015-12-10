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


def process_stop_action_args(parser, handler, args):
    """Process command line args supplied by user for stopping an action

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
    stop_action
    """
    q_args = {'id': args.id}

    try:
        action_stop = handler.stop_action(**q_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    print "++ Action ID stopped successfully: {0.id!r}".format(action_stop)
    return action_stop
