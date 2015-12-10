

def get_object(obj, doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to get objects.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    get_object_group = parser.add_argument_group(arggroup_name)

    get_object_group.add_argument(
        '--all',
        required=False,
        default=False,
        action='store_true',
        dest='all',
        help='Get all {}s'.format(obj),
    )

    obj_map = tanium_obj.get_obj_map(obj)
    search_keys = copy.copy(obj_map['search'])

    if 'id' not in search_keys:
        search_keys.append('id')

    if obj == 'whitelisted_url':
        search_keys.append('url_regex')
    elif obj == 'user':
        search_keys.append('name')

    for k in search_keys:
        get_object_group.add_argument(
            '--{}'.format(k),
            required=False,
            action='append',
            default=[],
            dest=k,
            help='{} of {} to get'.format(k, obj),
        )

    return parser



def process_get_object_args(parser, handler, obj, args, report=True):
    """Process command line args supplied by user for get object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    obj : str
        * Object type for get object
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.get`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Get {} Options'.format(obj.replace('_', ' ').capitalize())
    ]
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    get_all = obj_grp_args.pop('all')
    o_dict = {'objtype': obj}
    obj_grp_args.update(o_dict)

    if get_all:
        try:
            response = handler.get_all(**o_dict)
        except Exception as e:
            traceback.print_exc()
            print "\n\nError occurred: {}".format(e)
            sys.exit(100)
    else:
        try:
            response = handler.get(**obj_grp_args)
        except Exception as e:
            traceback.print_exc()
            print "\n\nError occurred: {}".format(e)
            sys.exit(100)

    print "Found items: ", response

    if report:
        report_file, result = handler.export_to_report_file(obj=response, **args.__dict__)

        m = "Report file {!r} written with {} bytes".format
        print(m(report_file, len(result)))

    return response
