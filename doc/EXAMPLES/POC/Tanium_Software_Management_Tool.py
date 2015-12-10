#!/usr/bin/env python -i
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Tanium Software Management Tool

This is a proof of concept showing how to use the following workflow using Tanium via PyTan
1) Shows available applications from Tanium that the user can install on their machine
2) Show the installed applications from a users client
3) Execute an installation of a package
4) Execute an uninstall of a package
5) Perform a repair of a given application

No Results return for Computer ID (perhaps getresultdata too soon)
Add expire_seconds to package deploy

This is a POC of a workflow and is not meant for general use, but as an example.
'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.3'

import os
import sys
import getpass
import logging

sys.dont_write_bytecode = True

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils

examples = []

mylog = logging.getLogger("TSMT")
mylog.setLevel(logging.INFO)
max_data_age = 60


def user_input(m):
    m = "[USER INPUT] {}".format(m)
    return raw_input(m).strip()


def backend_input(m):
    m = "[BACKEND INPUT] {}".format(m)
    return raw_input(m).strip()


def dictify_resultset(rs):
    return [dictify_resultset_row(x) for x in rs.rows]


def dictify_resultset_row(rs_row):
    d = dict(zip(
        [x.display_name for x in rs_row.columns],
        [join_list(x, ', ') for x in rs_row.vals]
    ))
    return d


def join_list(l, j='\n'):
    if None in l:
        l = ""
    if type(l) == list:
        l = j.join(l)
    return l


def process_handler_args(parser, all_args):
    handler_grp_names = ['Tanium Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args[k] for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception as e:
        print e
        sys.exit(99)
    return h


def get_logged_in_matches(handler, logged_in_user):
    m = "Searching for all servers with a Logged In user that equals '{}'".format(logged_in_user)
    mylog.info(m)

    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Computer ID',
            'Computer Name',
            'IP Address',
            'Logged In Users',
            'Operating System',
        ],
        'question_filters': [
            'Logged In Users, that =:{}'.format(logged_in_user)
        ],
    }

    m = "Asking question with args:\n{}".format(utils.jsonify(kwargs))
    mylog.debug(m)

    ask_logged_in_ret = handler.ask(**kwargs)
    ask_logged_in_results = ask_logged_in_ret['question_results']

    if not ask_logged_in_results.rows:
        m = "No servers found that match the question '{}'".format(
            ask_logged_in_ret['question_object'].query_text
        )
        mylog.critical(m)
        sys.exit(1)

    ask_logged_in_dict = dictify_resultset(ask_logged_in_results)

    m = "Received resultset from question:\n{}".format(utils.jsonify(ask_logged_in_dict))
    mylog.debug(m)
    return ask_logged_in_dict


def get_installed_apps(handler, computer_id):
    m = "Getting all Installed Applications for Computer ID that equals {!r}".format(computer_id)
    mylog.info(m)

    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Installed Applications, opt:max_data_age:{}'.format(max_data_age)
        ],
        'question_filters': [
            'Computer ID, that =:{}'.format(computer_id)
        ],
        'question_options': [
            'max_data_age:{}'.format(max_data_age),
        ],
    }

    m = "Asking question with args:\n{}".format(utils.jsonify(kwargs))
    mylog.debug(m)

    ask_ia_ret = handler.ask(**kwargs)
    ask_ia_results = ask_ia_ret['question_results']
    ask_ia_dict = dictify_resultset(ask_ia_results)

    m = "Received resultset from question:\n{}".format(utils.jsonify(ask_ia_dict))
    mylog.debug(m)
    return ask_ia_dict


def get_uninstallable_apps(handler, computer_id):
    installed = get_installed_apps(handler, computer_id)

    m = "Filtering Uninstallable Applications from Installed Applications"
    mylog.info(m)

    uninstallables = [x for x in installed if x['Uninstallable'] == 'Is Uninstallable']
    if not uninstallables:
        m = "No applications available for uninstallation!!"
        mylog.critical(m)
        sys.exit(1)

    return uninstallables


def get_installable_apps(handler, prefix='SWD'):
    m = "Getting all Installable Applications that start with {!r}".format(prefix)
    mylog.info(m)

    # get all packages in tanium
    pkgs = handler.get_all('package')

    mylog.debug("Retrieved {} packages from Tanium".format(len(pkgs)))

    # filter to packages that begin with "prefix" if prefix is not None
    if prefix:
        pkgs = [x for x in pkgs if x.name.startswith(prefix)]
        mylog.debug("Filtered down to {} packages that start with '{}'".format(len(pkgs), prefix))

    if not pkgs:
        m = "No packages available for installation!!"
        mylog.critical(m)
        sys.exit(1)

    return pkgs


def get_repairable_apps(handler, computer_id):
    m = "Getting all Repairable Applications for Computer ID that equals {!r}".format(computer_id)
    mylog.info(m)

    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Repairable Applications, opt:max_data_age:{}'.format(max_data_age),
        ],
        'question_filters': [
            'Computer ID, that =:{}'.format(computer_id)
        ],
        'question_options': [
            'max_data_age:{}'.format(max_data_age),
        ],
    }

    m = "Asking question with args:\n{}".format(utils.jsonify(kwargs))
    mylog.debug(m)

    ask_ra_ret = handler.ask(**kwargs)
    ask_ra_results = ask_ra_ret['question_results']
    ask_ra_dict = dictify_resultset(ask_ra_results)

    m = "Received resultset from question:\n{}".format(utils.jsonify(ask_ra_dict))
    mylog.debug(m)

    if not ask_ra_dict:
        m = "No applications available for repair!!"
        mylog.critical(m)
        sys.exit(1)

    return ask_ra_dict


def install_package(handler, package_name, computer_id):
    m = "Installing package {!r} to Computer ID that equals {!r}".format(package_name, computer_id)
    mylog.info(m)

    kwargs = {
        'package': package_name,
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            'Online, that =:True',
        ],
        'run': True,
    }
    m = "Installing Application with args:\n{}".format(utils.jsonify(kwargs))
    mylog.debug(m)
    dep_ret = handler.deploy_action_human(**kwargs)

    m = "Package {!r} finished installing on Computer ID that equals {!r}".format(
        package_name, computer_id)
    mylog.info(m)

    return dep_ret


def uninstall_package(handler, uninstall_string, computer_id):
    m = "Issuing uninstall string {!r} to Computer ID that equals {!r}".format(
        uninstall_string, computer_id)
    mylog.info(m)

    # escape any {}'s in the uninstall string so they dont break pytans param parsing
    uninstall_string = uninstall_string.replace('{', '\\{').replace('}', '\\}')
    kwargs = {
        'package': 'Uninstall MSI Parameterized{{$1={}}}'.format(uninstall_string),
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            'Online, that =:True',
        ],
        'run': True,
    }
    m = "Uninstalling Application with args:\n{}".format(utils.jsonify(kwargs))
    mylog.debug(m)
    dep_ret = handler.deploy_action_human(**kwargs)

    m = "Uninstall string {!r} finished running on Computer ID that equals {!r}".format(
        uninstall_string, computer_id)
    mylog.info(m)

    return dep_ret


def repair_package(handler, guid, computer_id):
    m = "Repairing GUID {!r} to Computer ID that equals {!r}".format(guid, computer_id)
    mylog.info(m)

    kwargs = {
        'package': 'Repair MSI{{$1={}}}'.format(guid),
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            'Online, that =:True',
        ],
        'run': True,
    }
    m = "Repairing Application with args:\n{}".format(utils.jsonify(kwargs))
    mylog.debug(m)
    dep_ret = handler.deploy_action_human(**kwargs)

    m = "GUID {!r} finished repairing on Computer ID that equals {!r}".format(guid, computer_id)
    mylog.info(m)

    return dep_ret


def get_computer_choice(handler, logged_in_user):
    ask_logged_in_dict = get_logged_in_matches(handler, logged_in_user)

    while True:
        print "\n"
        for idx, x in enumerate(ask_logged_in_dict):
            kvs = "\n".join(["\t{}: {}".format(k, v) for k, v in x.iteritems()])
            print "Choice #{}:\n{}".format(idx, kvs)

        m = "Choose one of the above computers (0 through {}): ".format(
            ask_logged_in_dict.index(ask_logged_in_dict[-1])
        )
        computer_choice = user_input(m)
        try:
            computer_choice = ask_logged_in_dict[int(computer_choice)]
            break
        except:
            m = "Invalid choice {}!".format(computer_choice)
            print m
    return computer_choice


def get_path_choice():
    while True:
        print "\n"
        m = "Choose [I]nstall or [U]ninstall or [R]epair Software: "
        path_choice = user_input(m).lower()
        if path_choice in ['i', 'u', 'r']:
            break
        print "Invalid choice {!r}, try again...".format(path_choice)
    return path_choice


def install_path(handler, computer_id):
    installables = get_installable_apps(handler)

    while True:
        print "\n"
        for idx, x in enumerate(installables):
            print "Package Choice #{}: {} (cmd: {!r})".format(idx, x.name, x.command)

        m = "Choose one of the above packages to install (0 through {}) or [G]o back: ".format(
            installables.index(installables[-1])
        )
        package_choice = user_input(m)

        if package_choice.lower() == 'g':
            return None

        try:
            package_choice = installables[int(package_choice)]
            break
        except:
            m = "Invalid choice {}!".format(package_choice)
            print m

    install_ret = install_package(handler, package_choice.name, computer_id)
    return install_ret


def uninstall_path(handler, computer_id):
    uninstallables = get_uninstallable_apps(handler, computer_id)

    while True:
        print "\n"
        for idx, x in enumerate(uninstallables):
            print "Application Choice #{}: {} (cmd: {!r})".format(
                idx, x['Name'], x['Silent Uninstall String']
            )

        m = (
            "Choose one of the above applications to uninstall (0 through {}) or [G]o back: "
        ).format(uninstallables.index(uninstallables[-1]))
        app_choice = user_input(m)

        if app_choice.lower() == 'g':
            return None

        try:
            app_choice = uninstallables[int(app_choice)]
            uninstall_string = app_choice['Silent Uninstall String']
            break
        except:
            m = "Invalid choice {}!".format(app_choice)
            print m

    uninstall_ret = uninstall_package(handler, uninstall_string, computer_id)
    return uninstall_ret


def repair_path(handler, computer_id):
    repairables = get_repairable_apps(handler, computer_id)

    while True:
        print "\n"
        for idx, x in enumerate(repairables):
            print "Application Choice #{}: {} (GUID: {!r})".format(
                idx, x['Name'], x['Install GUID']
            )

        m = "Choose one of the above applications to repair (0 through {}) or [G]o back: ".format(
            repairables.index(repairables[-1])
        )
        app_choice = user_input(m)

        if app_choice.lower() == 'g':
            return None

        try:
            app_choice = repairables[int(app_choice)]
            guid = app_choice['Install GUID']
            break
        except:
            m = "Invalid choice {}!".format(app_choice)
            print m

    repair_ret = repair_package(handler, guid, computer_id)
    return repair_ret


if __name__ == "__main__":
    utils.version_check(__version__)
    parser = utils.CustomArgParse(
        description=__doc__,
        add_help=True,
        formatter_class=utils.CustomArgFormat,
    )
    auth_group = parser.add_argument_group('Tanium Authentication')
    auth_group.add_argument(
        '-u', '--username', required=False, action='store', dest='username', default=None,
        help='Name of user',
    )
    auth_group.add_argument(
        '-p', '--password', required=False, action='store', default=None, dest='password',
        help='Password of user',
    )
    auth_group.add_argument(
        '--host', required=False, action='store', default=None, dest='host',
        help='Hostname/ip of SOAP Server',
    )
    auth_group.add_argument(
        '--port', required=False, action='store', default="444", dest='port',
        help='Port to use when connecting to SOAP Server',
    )

    opt_group = parser.add_argument_group('Handler Options')
    opt_group.add_argument(
        '-l', '--loglevel', required=False, action='store', type=int, default=0, dest='loglevel',
        help='Logging level to use, increase for more verbosity',
    )

    args = parser.parse_args()

    all_args = args.__dict__

    if not args.username:
        username = backend_input('Tanium Username: ')
        all_args['username'] = username.strip()

    if not args.password:
        password = getpass.getpass('[BACKEND INPUT] Tanium Password: ')
        all_args['password'] = password.strip()

    if not args.host:
        host = backend_input('Tanium Host: ')
        all_args['host'] = host.strip()

    handler = process_handler_args(parser, all_args)
    if args.loglevel >= 1:
        mylog.setLevel(logging.DEBUG)
    else:
        mylog.setLevel(logging.INFO)

    # START TSMT WORKFLOW
    m = 'Provide Logged In account name to search for on all servers: '
    logged_in_user = backend_input(m)

    while True:
        computer_choice = get_computer_choice(handler, logged_in_user)
        computer_id = computer_choice['Computer ID']

        path_choice = get_path_choice()

        if path_choice == 'i':
            install_ret = install_path(handler, computer_id)

        elif path_choice == 'u':
            uninstall_ret = uninstall_path(handler, computer_id)

        elif path_choice == 'r':
            repair_ret = repair_path(handler, computer_id)
