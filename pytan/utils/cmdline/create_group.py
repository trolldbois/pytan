
def create_group(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a group.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create Group Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='groupname',
        default=None,
        help='Name of group to create',
    )

    arggroup.add_argument(
        '-f',
        '--filter',
        required=False,
        action='append',
        dest='filters',
        default=[],
        help='Filters to use for group, supply --filters-help to see filter help',
    )

    arggroup.add_argument(
        '-o',
        '--option',
        required=False,
        action='append',
        dest='filter_options',
        default=[],
        help='Filter options to use for group, supply --options-help to see options'
        ' help',
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
    return parser


def process_create_group_args(parser, handler, args):
    """Process command line args supplied by user for create group object

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
        * response from :func:`pytan.handler.Handler.create_group`
    """
    obj_grp_names = ['Create Group Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_group(**obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    m = (
        "New group {0.name!r} created with ID {0.id!r}, filter text: {0.text!r}"
    ).format
    print(m(response))
    return response


