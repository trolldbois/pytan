#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4 softtabstop=1 shiftwidth=4 expandtab:
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Tanium Software Management Tool

This is a proof of concept showing how to use the following workflow using Tanium via PyTan
0) Get logged in username to filter machines and allow user to pick a machine
    Paths.start() == 0_start_path.html,  0_server_select.html
1) Shows available applications from Tanium that the user can install on their machine
    Paths.install_select() == 1_install_select.html
2) Show the installed applications from a users client
    Paths.show_installed() == 2_show_installed.html
3) Execute an installation of a package
    Paths.install_app() == 3_install_app.html
4) Execute an uninstall of a package
    Paths.uninstall_select() == 4_uninstall_select.html
    Paths.uninstall_app() == 4_uninstall_app.html
5) Perform a repair of a given application
    Paths.repair_select() == 5_repair_select.html
    Paths.repair_app() == 5_repair_app.html

http://localhost/~jolsen/swd_tanium_portal
'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.3'

appinfo = {}
appinfo['name'] = 'SWD Tanium Software Portal'
appinfo['ver'] = '0.1a'

import os
import sys
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
sys.path.append(my_dir)

from config import config
import common
sys.path.append(config['pytan_dir'])

import pytan
import cgi
import jinja2
import urllib
import cgitb
cgitb.enable()


def get_logged_in_matches(handler, logged_in_user):
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
    ask_logged_in_ret = handler.ask(**kwargs)
    ask_logged_in_results = ask_logged_in_ret['question_results']
    ask_logged_in_dict = common.dictify_resultset(ask_logged_in_results)
    return ask_logged_in_dict


def get_installable_apps(handler, prefix='SWD'):
    # get all packages in tanium
    pkgs = handler.get_all('package')

    # filter to packages that begin with "prefix" if prefix is not None
    if prefix:
        pkgs = [x for x in pkgs if x.name.startswith(prefix)]

    return pkgs


def get_installed_apps(handler, computer_id):
    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Installed Applications, opt:max_data_age:{}'.format(config['max_data_age'])
        ],
        'question_filters': [
            'Computer ID, that =:{}'.format(computer_id)
        ],
        'question_options': [
            'max_data_age:{}'.format(config['max_data_age']),
        ],
    }
    ask_ia_ret = handler.ask(**kwargs)
    ask_ia_results = ask_ia_ret['question_results']
    ask_ia_dict = common.dictify_resultset(ask_ia_results)
    return ask_ia_dict


def get_uninstallable_apps(handler, computer_id):
    installed = get_installed_apps(handler, computer_id)
    uninstallables = [x for x in installed if x['Uninstallable'] == 'Is Uninstallable']
    return uninstallables


def get_repairable_apps(handler, computer_id):
    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Repairable Applications, opt:max_data_age:{}'.format(config['max_data_age']),
        ],
        'question_filters': [
            'Computer ID, that =:{}'.format(computer_id)
        ],
        'question_options': [
            'max_data_age:{}'.format(config['max_data_age']),
        ],
    }
    ask_ra_ret = handler.ask(**kwargs)
    ask_ra_results = ask_ra_ret['question_results']
    ask_ra_dict = common.dictify_resultset(ask_ra_results)
    return ask_ra_dict


def install_package(handler, package_name, computer_id):
    kwargs = {
        'package': package_name,
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            'Online, that =:True',
        ],
        'run': True,
        'get_results': False,
    }
    dep_ret = handler.deploy_action_human(**kwargs)
    return dep_ret


def uninstall_package(handler, uninstall_string, computer_id):
    # escape any {}'s in the uninstall string so they dont break pytans param parsing
    uninstall_string = uninstall_string.replace('{', '\\{').replace('}', '\\}')
    kwargs = {
        'package': 'Uninstall MSI Parameterized{{$1={}}}'.format(uninstall_string),
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            'Online, that =:True',
        ],
        'run': True,
        'get_results': False,
    }
    dep_ret = handler.deploy_action_human(**kwargs)
    return dep_ret


def repair_package(handler, guid, computer_id):
    kwargs = {
        'package': 'Repair MSI{{$1={}}}'.format(guid),
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            'Online, that =:True',
        ],
        'run': True,
        'get_results': False,
    }
    dep_ret = handler.deploy_action_human(**kwargs)
    return dep_ret


class Paths(object):
    def __init__(self, form, handler, default_path='start', **kwargs):
        super(Paths, self).__init__()

        self.next_action = 'main.py'

        # setup jinja2 template system
        self.jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('jinja_templates'))
        self.jinja2_env.filters['getitem'] = common.getitem

        # convert the form to a python dictionary
        self.formdict = common.formtodict(form)

        self.handler = handler

        # get the path key from formdict, default to 'start' if not defined
        self.path_choice = self.formdict.get('path', default_path)

        # get the path method from Paths class based on path_choice
        self.path_method = getattr(self, self.path_choice, self.unsupported)

        # get the return from path_method
        self.path_return = self.path_method()

    # STEP 0
    def start(self):
        next_path = 'server_select'
        template_file = '0_start_path.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Provide Logged In account name to search for on all servers:'
        logged_in_user = self.formdict.get('logged_in_user', "")

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            topmsg=title,
            next_path=next_path,
            logged_in_user=logged_in_user,
        )
        return j_render

    def server_select(self):
        template_file = '0_server_select.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Select a server and an operation:'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        servers = get_logged_in_matches(self.handler, logged_in_user)
        # TODO: IF NONE, THROW ERROR PAGE

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            servers=servers,
            logged_in_user=logged_in_user,
        )
        return j_render

    # STEP 2
    def show_installed(self):
        template_file = '2_show_installed.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'List of Installed Applications:'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        apps = get_installed_apps(self.handler, server)

        j_render = j_template.render(
            app=appinfo,
            title=title,
            apps=apps,
            logged_in_user=logged_in_user,
            server=server,
        )
        return j_render

    # STEP 1
    def install_select(self):
        next_path = 'install_app'
        template_file = '1_install_select.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Select an application to install:'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        pkgs = get_installable_apps(self.handler)
        # TODO: IF NONE, THROW ERROR PAGE

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            pkgs=pkgs,
            server=server,
            logged_in_user=logged_in_user,
            next_path=next_path,
        )
        return j_render

    # STEP 3
    def install_app(self):
        next_path = 'start'
        template_file = '3_install_app.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Application Install Progress'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        application = self.formdict.get('application', None)
        # TODO: IF NONE, THROW ERROR PAGE

        deploy_ret = install_package(handler, application, server)

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            server=server,
            application=application,
            logged_in_user=logged_in_user,
            deploy_ret=deploy_ret,
            next_path=next_path,
        )
        return j_render

    # STEP 4
    def uninstall_select(self):
        next_path = 'uninstall_app'
        template_file = '4_uninstall_select.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Select an application to uninstall:'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        pkgs = get_uninstallable_apps(self.handler, server)
        # TODO: IF NONE, THROW ERROR PAGE

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            pkgs=pkgs,
            server=server,
            logged_in_user=logged_in_user,
            next_path=next_path,
        )
        return j_render

    # STEP 4
    def uninstall_app(self):
        next_path = 'start'
        template_file = '4_uninstall_app.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Application Uninstall Progress'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        application = self.formdict.get('application', None)
        # TODO: IF NONE, THROW ERROR PAGE

        application, uninst_string = urllib.unquote(application).split('||')
        # TODO: IF NONE, THROW ERROR PAGE

        deploy_ret = uninstall_package(handler, uninst_string, server)

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            server=server,
            application=application,
            uninst_string=uninst_string,
            logged_in_user=logged_in_user,
            deploy_ret=deploy_ret,
            next_path=next_path,
        )
        return j_render

    # STEP 5
    def repair_select(self):
        next_path = 'repair_app'
        template_file = '5_repair_select.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Select an application to Repair:'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        pkgs = get_repairable_apps(self.handler, server)
        # TODO: IF NONE, THROW ERROR PAGE

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            pkgs=pkgs,
            server=server,
            logged_in_user=logged_in_user,
            next_path=next_path,
        )
        return j_render

    # STEP 5
    def repair_app(self):
        next_path = 'start'
        template_file = '5_repair_app.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Application Repair Progress'

        logged_in_user = self.formdict.get('logged_in_user', None)
        # TODO: IF NONE, THROW ERROR PAGE

        server = self.formdict.get('server', None)
        # TODO: IF NONE, THROW ERROR PAGE

        application = self.formdict.get('application', None)
        # TODO: IF NONE, THROW ERROR PAGE

        application, guid = urllib.unquote(application).split('||')
        # TODO: IF NONE, THROW ERROR PAGE

        deploy_ret = repair_package(handler, guid, server)

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            server=server,
            application=application,
            guid=guid,
            logged_in_user=logged_in_user,
            deploy_ret=deploy_ret,
            next_path=next_path,
        )
        return j_render

    def unsupported(self):
        # TODO: THROW ERROR PAGE
        return 'unsupported path'


# get the form submission
form = cgi.FieldStorage()
# common.print_html(form)

# connect to Tanium
handler = pytan.Handler(
    username=config['tanium_username'],
    password=config['tanium_password'],
    host=config['tanium_host'],
)

# instantiate our Paths class, passing in form and handler
paths = Paths(form, handler)
# TODO: TRY/EXCEPT THROW ERROR PAGE

common.print_html(paths.path_return)
