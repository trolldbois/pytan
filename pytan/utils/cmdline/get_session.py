

def get_session(doc):
    """Method to setup the base :clas:`CustomArgParse` class for command line scripts using :func:`base_parser`,then add specific
        arguments for scripts that use :mod:`pytan` to create a tanium session.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Get Session Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--persistent',
        required=False,
        action='store_true',
        dest='persistent',
        default=argparse.SUPPRESS,
        help='Persist session for 1 week after last use.',
    )

    return parser





def process_get_session_args(parser, handler, args):
    """Process command line args supplied by user for getting a session

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    print handler.session._session_id



