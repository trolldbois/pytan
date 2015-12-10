
def create_user(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a user.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create User Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of user to create',
    )

    arggroup.add_argument(
        '-rn',
        '--rolename',
        required=False,
        action='append',
        dest='rolename',
        default=[],
        help='Name of role to assign to new user',
    )

    arggroup.add_argument(
        '-ri',
        '--roleid',
        required=False,
        action='append',
        type=int,
        dest='roleid',
        default=[],
        help='ID of role to assign to new user',
    )
    arggroup.add_argument(
        '-g',
        '--group',
        required=False,
        action='store',
        dest='group',
        default='',
        help='Name of group to assign to user',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to user',
    )
    return parser


def process_create_user_args(parser, handler, args):
    """Process command line args supplied by user for create user object

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
    obj_grp_names = ['Create User Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_user(**obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    roles_txt = ', '.join([x.name for x in response.roles])

    m = (
        "New user {0.name!r} created with ID {0.id!r}, roles: {1!r}, "
        "group id: {0.group_id!r}"
    ).format
    print(m(response, roles_txt))
    return response

