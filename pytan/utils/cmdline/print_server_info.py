
def print_server_info(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to print sensor info.
    """
    parser = parent_parser(doc=doc)
    output_group = parser.add_argument_group('Output Options')

    output_group.add_argument(
        '--json',
        required=False,
        default=False,
        action='store_true',
        dest='json',
        help='Show a json dump of the server information',
    )
    return parser



def process_print_server_info_args(parser, handler, args):
    """Process command line args supplied by user for printing server info

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    si = handler.session.get_server_info()

    if args.json:
        print pytan.utils.jsonify(si['diags_flat'])
    else:
        print str(handler)
        print_obj(si['diags_flat'])
