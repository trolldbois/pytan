


def delete_object(obj, doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to delete objects.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    arggroup = parser.add_argument_group(arggroup_name)

    obj_map = tanium_obj.get_obj_map(obj)
    search_keys = copy.copy(obj_map['search'])

    if obj == 'whitelisted_url':
        search_keys.append('url_regex')
    elif obj == 'user':
        search_keys.append('name')

    for k in search_keys:
        arggroup.add_argument(
            '--{}'.format(k),
            required=False,
            action='append',
            default=[],
            dest=k,
            help='{} of {} to get'.format(k, obj),
        )

    return parser


def process_delete_object_args(parser, handler, obj, args):
    """Process command line args supplied by user for delete object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    obj : str
        * Object type for delete object
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.delete`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Delete {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    obj_grp_args['objtype'] = obj
    try:
        response = handler.delete(**obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(100)
    for i in response:
        print "Deleted item: ", i
    return response

