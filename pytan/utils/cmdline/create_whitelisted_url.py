
def create_whitelisted_url(doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create a whitelisted_url.
    """
    parser = base_parser(desc=doc, help=True)
    arggroup_name = 'Create Whitelisted URL Options'
    arggroup = parser.add_argument_group(arggroup_name)

    arggroup.add_argument(
        '--url',
        required=True,
        action='store',
        dest='url',
        default=None,
        help='Text of new Whitelisted URL',
    )

    arggroup.add_argument(
        '--regex',
        required=False,
        action='store_true',
        dest='regex',
        default=False,
        help='Whitelisted URL is a regex pattern',
    )

    arggroup.add_argument(
        '-d',
        '--download',
        required=False,
        action='store',
        dest='download_seconds',
        type=int,
        default=86400,
        help='Download Whitelisted URL every N seconds',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to Whitelisted URL',
    )
    return parser


def process_create_whitelisted_url_args(parser, handler, args):
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
    obj_grp_names = ['Create Whitelisted URL Options']
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}

    try:
        response = handler.create_whitelisted_url(**obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(99)

    m = "New Whitelisted URL {0.url_regex!r} created with ID {0.id!r}".format
    print(m(response))
    return response

