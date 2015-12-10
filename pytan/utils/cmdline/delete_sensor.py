


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
