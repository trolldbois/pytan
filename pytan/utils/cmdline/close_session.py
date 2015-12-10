
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


def process_close_session_args(parser, handler, args):
    """Process command line args supplied by user for getting a session

    Parameters
    ----------
    Parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of handler created for command line args
    args : args object
        * args parsed from `parser`
    """
    handler.session.logout(args)

