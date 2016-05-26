'''Post Install Tanium Tool'''
import os
import pprint

from localconfig import config as cp

from pytan import binsupport

__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.9'


def read_config_file(config_file):
    if not os.path.isfile(config_file):
        m = "CONFIG: Unable to find config file '{}'".format
        raise Exception(m(config_file))

    m = "CONFIG: Loading file: '{}'".format
    print(m(config_file))

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
    ret['usergroups'] = get_sections('group_user', full_config_dict)
    ret['saved_questions'] = get_sections('saved_question', full_config_dict)
    ret['group_computers'] = get_sections('group_computer', full_config_dict)
    ret['dashboards'] = get_sections('dashboard', full_config_dict)
    return ret


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

args = parser.parse_args()
handler = binsupport.process_handler_args(parser=parser, args=args)
responsemethod = getattr(binsupport, 'process_pytan_shell_args')
response = responsemethod(parser=parser, handler=handler, args=args)

config_file = args.config_file
full_config_dict = read_config_file(config_file)
config_sections = find_config_sections(full_config_dict)

if args.debug:
    m = "CONFIG: parsed items from config file '{}': {}".format
    print(m(config_file, pprint.pformat(full_config_dict)))

    m = "CONFIG: found sections from config file '{}': {}".format
    print(m(config_file, pprint.pformat(config_sections)))

pitt_options = config_sections.get('pitt_options', {})
disable_all_saved_actions = pitt_options.get('disable_all_saved_actions', False)

if disable_all_saved_actions:
    all_saved_actions = handler.get_all('saved_action')
    m = "Disabling all saved actions due to pitt_options=>disable_all_saved_actions=True"
    print(m)
    for i in all_saved_actions:
        if i.status == 0:
            i.status = 1
            handler.session.save(i)
            m = "Disabled saved action {!r}".format
        else:
            m = "Saved action {!r} already disabled, leaving alone".format
        print(m(i.name))
else:
    m = "NOT disabling all saved actions due to pitt_options=>disable_all_saved_actions=False"
    print(m)

global_options = config_sections.get('global_options', {})
if global_options:
    for k, v in global_options.items():


'''
1. pitt options
2. global options
3. computer groups
4. user groups
5. users
6. saved questions
7. dashboards
'''
