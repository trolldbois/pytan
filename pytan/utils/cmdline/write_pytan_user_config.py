
def write_pytan_user_config(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to write a pytan user config file.
    """
    parser = parent_parser(doc=doc)
    output_group = parser.add_argument_group('Write PyTan User Config Options')

    output_group.add_argument(
        '--file',
        required=False,
        default='',
        action='store',
        dest='file',
        help=(
            "PyTan User Config file to write for PyTan arguments (defaults to: {})"
        ).format(constants.PYTAN_USER_CONFIG),
    )
    return parser


def process_write_pytan_user_config_args(parser, handler, args):
    """Process command line args supplied by user for writing pytan user config

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    args : args object
        * args parsed from `parser`
    """
    puc = handler.write_pytan_user_config(pytan_user_config=args.file)
    m = "PyTan User config file successfully written: {} ".format
    print m(puc)

