
def create_json_object(obj, doc):
    """Method to setup the base :class:`CustomArgParse` class for command line scripts using :func:`base_parser`, then add specific arguments for scripts that use :mod:`pytan` to create objects from json files.
    """
    parser = parent_parser(doc=doc)
    arggroup_name = 'Create {} from JSON Options'.format(obj.replace('_', ' ').capitalize())
    arggroup = parser.add_argument_group(arggroup_name)
    arggroup.add_argument(
        '-j',
        '--json',
        required=True,
        action='store',
        default='',
        dest='json_file',
        help='JSON file to use for creating the object',
    )
    return parser



def process_create_json_object_args(parser, handler, obj, args):
    """Process command line args supplied by user for create json object

    Parameters
    ----------
    parser : :class:`argparse.ArgParse`
        * ArgParse object used to parse `all_args`
    handler : :class:`pytan.handler.Handler`
        * Instance of Handler created from command line args
    obj : str
        * Object type for create json object
    args : args object
        * args parsed from `parser`

    Returns
    -------
    response : :class:`taniumpy.object_types.base.BaseType`
        * response from :func:`pytan.handler.Handler.create_from_json`
    """
    # put our query args into their own dict and remove them from all_args
    obj_grp_names = [
        'Create {} from JSON Options'.format(
            obj.replace('_', ' ').capitalize()
        )
    ]
    obj_grp_opts = get_grp_opts(parser=parser, grp_names=obj_grp_names)
    obj_grp_args = {k: getattr(args, k) for k in obj_grp_opts}
    try:
        response = handler.create_from_json(obj, **obj_grp_args)
    except Exception as e:
        traceback.print_exc()
        print "\n\nError occurred: {}".format(e)
        sys.exit(100)
    for i in response:
        obj_id = getattr(i, 'id', 'unknown')
        print "Created item: {}, ID: {}".format(i, obj_id)
    return response
