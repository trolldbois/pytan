'''Post Install Tanium Tool'''
import os
import pprint

from localconfig import config as cp

from pytan import binsupport

__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.9'


def get_parser():
    binsupport.version_check(reqver=__version__)
    setupmethod = getattr(binsupport, 'setup_pytan_shell_argparser')
    parser = setupmethod(doc=__doc__)

    parser.add_argument(
        '-c', '--config',
        required=False, default='pitt.ini', action='store', dest='config_file',
        help='Path to PITT Configuration File',
    )
    parser.add_argument(
        '-d', '--debug',
        required=False, default=False, action='store_true', dest='debug',
        help='Enable debug mode',
    )
    return parser


def get_args(parser):
    args = parser.parse_args()
    return args


def get_handler(parser, args):
    handler = binsupport.process_handler_args(parser=parser, args=args)
    return handler


def spew(m, t="INFO"):
    z = "{0: <10} -- {1}".format(t, m)
    print(z)


def spew_error(m):
    spew(m, t="ERROR")


def spew_skip(m):
    spew(m, t="SKIPPED")


def spew_change(m):
    spew(m, t="CHANGED")


def spew_create(m):
    spew(m, t="CREATED")


def spew_disable(m):
    spew(m, t="DISABLED")


def spew_delete(m):
    spew(m, t="DELETED")


def spew_config(m):
    spew(m, t="CONFIG")


def read_config_file(config_file):
    if not os.path.isfile(config_file):
        m = "Unable to find config file '{}'".format(config_file)
        spew_error(m)
        raise Exception(m)

    m = "Loading file: '{}'".format(config_file)
    spew_config(m)

    try:
        cp.read(config_file)
    except Exception as e:
        m = "Failed to read config file: '{}', {}".format(config_file, e)
        spew_error(m)
        raise Exception(m)

    ret = {s: {k: v for k, v in cp.items(s)} for s in cp}
    return ret


def get_sections(section_prefix, full_config_dict, exact=False):
    ret = {k: v for k, v in full_config_dict.items() if k.startswith(section_prefix)}
    if exact and section_prefix in ret:
        ret = ret[section_prefix]
    return ret


def find_config_sections(full_config_dict):
    ret = {}
    ret['pitt_options'] = get_sections('pitt_options', full_config_dict, True)
    ret['global_settings'] = get_sections('global_settings', full_config_dict, True)
    ret['users'] = get_sections('user', full_config_dict)
    ret['user_groups'] = get_sections('group_user', full_config_dict)
    ret['saved_questions'] = get_sections('saved_question', full_config_dict)
    ret['computer_groups'] = get_sections('group_computer', full_config_dict)
    ret['dashboards'] = get_sections('dashboard', full_config_dict)
    return ret


def verify_config_sections(config_sections):
    name_req = [
        'computer_groups',
        'user_groups',
        'saved_questions',
        'dashboards',
        'users',
    ]
    key = 'name'
    for i in name_req:
        sect = config_sections.get(i, {})
        for a, b in sect.items():
            if key not in b:
                m = "Config section '{}' missing required key '{}'!".format(a, key)
                spew_error(m)
                raise Exception(m)


def disable_saved_action(handler, i):
    me = "saved action {!r} (ID: {})".format
    me = me(i.name, i.id)

    if i.status == 0:
        i.status = 1
        handler.session.save(i)
        m = "{}".format(me)
        spew_disable(m)
    else:
        m = "{}; already disabled".format(me)
        spew_skip(m)


def update_setting(handler, name, new_value):

    try:
        i = handler.get('setting', name=name, include_hidden_flag=1)[0]
    except:
        i = None

    if i is not None:
        me = "global setting name '{}' (ID: {}); old value '{}', new value '{}'".format
        me = me(name, i.id, i.value, new_value)
        orig_value = str(i.value)
        new_value = str(new_value)
        if orig_value != new_value:
            i.value = new_value
            try:
                handler.session.save(i)
                m = "{}".format(me)
                spew_change(m)
            except Exception as e:
                m = "{}; failed during update, error: {}".format(me, e)
                spew_error(m)
        else:
            m = "{}; already set".format(me)
            spew_skip(m)
    else:
        me = "global setting name '{}', new value '{}'".format
        me = me(name, new_value)
        m = "{}; failed during update, unable to find".format(me)
        spew_error(m)


def create_computer_group(handler, section_name, group_params, delete_existing=False):
    name = group_params['name']
    filters = [v for k, v in group_params.items() if k.startswith('filter')]
    options = group_params.get('options', None)
    if options:
        options = [x.strip() for x in options.split(',')]

    try:
        i = handler.get('group', name=name)[0]
    except:
        i = None

    if i is not None:
        me = "computer group '{}' (ID: {})".format
        me = me(name, i.id)

        if delete_existing:
            handler.session.delete(i)
            m = "{}; parsed text '{}'".format(me, i.text)
            spew_delete(m)
        else:
            m = "{}".format(me)
            spew_skip(m)
            return
    else:
        me = "computer group '{}'".format
        me = me(name)

    o = handler.create_group(
        groupname=name,
        filters=filters,
        filter_options=options,
    )
    me = "computer group '{}' (ID: {})".format
    me = me(name, o.id)

    m = "{}; filters {}, options {}, parsed text '{}'".format
    m = m(me, filters, options, o.text)
    spew_create(m)


def create_user_group(handler, section_name, group_params, delete_existing=False):
    name = group_params['name']
    try:
        i = handler.get_usergroups(name=name)[1][0]
    except:
        i = None

    if i is not None:
        me = "user group '{}' (ID: {})".format
        me = me(name, i.id)

        if delete_existing:
            handler.session.delete(i)
            m = "{}; parsed text '{}'".format(me, i.text)
            spew_delete(m)
        else:
            m = "{}".format(me)
            spew_skip(m)
            return
    else:
        me = "computer group '{}'".format
        me = me(name)

    o = handler.create_group(
        groupname=name,
        filters=filters,
        filter_options=options,
    )
    me = "computer group '{}' (ID: {})".format
    me = me(name, o.id)

    m = "{}; filters {}, options {}, parsed text '{}'".format
    m = m(me, filters, options, o.text)
    spew_create(m)

# __________________________________
parser = get_parser()
args = get_args(parser)
handler = get_handler(parser, args)

config_file = args.config_file
full_config_dict = read_config_file(config_file)
config_sections = find_config_sections(full_config_dict)

if args.debug:
    m = "parsed items from config file '{}'".format(config_file)
    spew_config(m)
    spew_config(pprint.pformat(full_config_dict))

    m = "found sections from config file '{}'".format(config_file)
    spew_config(m)
    spew_config(pprint.pformat(config_sections))

verify_config_sections(config_sections)

pitt_options = config_sections.get('pitt_options', {})
disable_all_saved_actions = pitt_options.get('disable_all_saved_actions', False)
delete_existing = pitt_options.get('delete_existing', False)


if disable_all_saved_actions:
    all_saved_actions = handler.get_all('saved_action')
    m = "Disabling all saved actions due to pitt_options=>disable_all_saved_actions=True"
    spew(m)
    for i in all_saved_actions:
        disable_saved_action(handler, i)
else:
    m = "NOT disabling all saved actions due to pitt_options=>disable_all_saved_actions=False"
    spew(m)


global_settings = config_sections.get('global_settings', {})
if global_settings:
    m = "Changing all global settings found in config file"
    spew(m)
    for name, new_value in global_settings.items():
        update_setting(handler, name, new_value)
else:
    m = "NOT changing any global settings, none found in config file"
    spew(m)


computer_groups = config_sections.get('computer_groups', {})
if computer_groups:
    m = "Creating all computer groups found in config file"
    spew(m)
    for section_name, group_params in computer_groups.items():
        create_computer_group(handler, section_name, group_params, delete_existing)
else:
    m = "NOT creating any computer groups, none found in config file"
    spew(m)


user_groups = config_sections.get('user_groups', {})
if user_groups:
    m = "Creating all user groups found in config file"
    spew(m)
    for section_name, group_params in user_groups.items():
        create_user_group(handler, section_name, group_params, delete_existing)
else:
    m = "NOT creating any user groups, none found in config file"
    spew(m)

'''
1x pitt options
2x global options
3x computer groups
4. user groups
5. users
6. saved questions
7. dashboards
'''
