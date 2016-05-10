'''Post Install Tanium Tool'''
import os
import pprint

from localconfig import config as cp

from pytan import binsupport

__author__ = 'Jim Olsen <jim.olsen@tanium.com>'
__version__ = '2.1.9'


def get_sections(prefix, d):
    sections = {k: v for k, v in d.iteritems() if k.startswith(prefix)}
    return sections


if __name__ == "__main__":
    binsupport.version_check(reqver=__version__)
    setupmethod = getattr(binsupport, 'setup_pytan_shell_argparser')
    parser = setupmethod(doc=__doc__)

    parser.add_argument(
        '--config_file',
        required=False,
        default='pitt.ini',
        action='store',
        dest='config_file',
        help='Path to PITT Configuration File',
    )

    args = parser.parse_args()
    handler = binsupport.process_handler_args(parser=parser, args=args)
    responsemethod = getattr(binsupport, 'process_pytan_shell_args')
    response = responsemethod(parser=parser, handler=handler, args=args)

    cf = args.config_file
    if not os.path.isfile(cf):
        m = "CONFIG: Unable to find file '{}'".format
        raise Exception(m(args.config_file))

    m = "CONFIG: Loading file: '{}'".format
    print(m(cf))

    try:
        cp.read(cf)
    except Exception as e:
        m = "CONFIG: Failed to read ini file: {}, {}".format
        raise Exception(m(cf, e))

    parsed_items = {s: {k: v for k, v in cp.items(s)} for s in cp}

    # m = "CONFIG: parsed values from config file '{}': {}".format
    # print(m(cf, pprint.pformat(parsed_items)))

    users = get_sections('user', parsed_items)
    usergroups = get_sections('group_user', parsed_items)
    pitt_options = get_sections('pitt_options', parsed_items)
    global_settings = get_sections('global_settings', parsed_items)
    saved_questions = get_sections('saved_question', parsed_items)
    group_computers = get_sections('group_computer', parsed_items)
    dashboards = get_sections('dashboard', parsed_items)

    pprint.pprint(dashboards)
    '''
    create saved question!

    archive_enabled_flag
    expire_seconds
    hidden_flag
    issue_seconds
    issue_seconds_never_flag
    keep_seconds
    name
    packages ??
    public_flag
    question --> ??

    Process all users
    Process all user groups
    Put users into their associated groups???
    create computer groups

    create dashboards
    put sq's in dashboards

    process global settings
    process pitt options
    '''
