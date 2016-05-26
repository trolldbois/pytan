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


def spew(m, error=False):
    if error:
        m = "ERROR!! {}".format(m)
    print(m)


def read_config_file(config_file):
    if not os.path.isfile(config_file):
        m = "CONFIG: Unable to find config file '{}'".format
        raise Exception(m(config_file))

    m = "CONFIG: Loading file: '{}'".format
    spew(m(config_file))

    try:
        cp.read(config_file)
    except Exception as e:
        m = "CONFIG: Failed to read config file: '{}', {}".format
        raise Exception(m(config_file, e))

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
                m = "Config section '{}' missing required key '{}'!".format
                raise Exception(m(a, key))


def disable_saved_action(handler, i):
    if i.status == 0:
        i.status = 1
        handler.session.save(i)
        m = "Disabled saved action {!r}".format
    else:
        m = "Saved action {!r} already disabled, leaving alone".format
    spew(m(i.name))


def update_setting(handler, name, new_value):
    try:
        i = handler.get('setting', name=name, include_hidden_flag=1)[0]
    except:
        i = None

    if i is not None:
        orig_value = str(i.value)
        new_value = str(new_value)
        if orig_value != new_value:
            i.value = new_value

            try:
                handler.session.save(i)
                m = "Changed global setting name '{}' from '{}' to '{}'".format
                spew(m(name, orig_value, new_value))
            except Exception as e:
                m = "Failed to change global setting name '{}' from '{}' to '{}' Error: {}".format
                spew(m(name, orig_value, new_value, e), True)
        else:
            m = "NOT changing global setting name '{}', already set to '{}'".format
            spew(m(i.name, new_value))
    else:
        m = "Unable to find a global setting named '{}'".format
        spew(m(name), True)


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
        if delete_existing:
            handler.session.delete(i)
            m = (
                "Deleted pre-existing computer group '{}' due to pitt_options=>delete_existing=True"
            ).format
            spew(m(name))
        else:
            m = (
                "NOT Deleting pre-existing computer group '{}' due to "
                "pitt_options=>delete_existing=False, group will not be re-created via PITT"
            ).format
            spew(m(name))
            return

    o = handler.create_group(
        groupname=name,
        filters=filters,
        filter_options=options,
    )
    m = (
        "Created computer group '{}' using filters {} and options {}, ID: {}, "
        "parsed text '{}'"
    ).format
    spew(m(o.name, filters, options, o.id, o.text))

parser = get_parser()
args = get_args(parser)
handler = get_handler(parser, args)

config_file = args.config_file
full_config_dict = read_config_file(config_file)
config_sections = find_config_sections(full_config_dict)

if args.debug:
    m = "============CONFIG: parsed items from config file '{}'".format
    spew(m(config_file))
    spew(pprint.pformat(full_config_dict))

    m = "============CONFIG: found sections from config file '{}'".format
    spew(m(config_file))
    spew(pprint.pformat(config_sections))

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
    for name, new_value in global_settings.items():
        update_setting(handler, name, new_value)
else:
    m = "NOT changing any global settings, none found in config file"
    spew(m)

computer_groups = config_sections.get('computer_groups', {})
if computer_groups:
    for section_name, group_params in computer_groups.items():
        create_computer_group(handler, section_name, group_params, delete_existing)
else:
    m = "NOT creating any computer groups, none found in config file"
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
