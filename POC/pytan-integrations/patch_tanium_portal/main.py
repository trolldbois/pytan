#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4 softtabstop=1 shiftwidth=4 expandtab:
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Tanium Patch Management Tool

Inputs:

FQDN of servername:
JIRA Ticket ID:

1) Prompt user for computer names
2) Get computer ID and computer name from all machines where computer name == FQDN of computer names
2a) if no match, error
2b) show verification screen for computer ID / name/ OS / IP /etc
2c) User verifies server choices
--) Get JIRA Ticket ID from JIRA
3) Perform patch operations against each computer
3a) Run patch scan action via tanium
3b) get results of patch scan action
3c) Get available patches via tanium
3d) deploy action "deploy available patches" via tanium (via patch whitelist)
3e) reboot
4) repeat step 3 until no available patches


http://localhost/~jolsen/patch_tanium_portal
'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.3'

appinfo = {}
appinfo['name'] = 'Tanium Patch Portal'
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
# import urllib
import cgitb
cgitb.enable()


def async_find_computer_id(handler, computer_name):
    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Computer ID',
            'Computer Name',
            'IP Address',
            'Operating System',
            'Is Windows',
        ],
        'question_filters': [
            'Computer Name, that =:{}'.format(computer_name)
        ],
        'get_results': False,
    }
    ask_ret = handler.ask(**kwargs)
    ret = {
        'computer_name': computer_name,
        'question_id': ask_ret['question_object'].id,
        'question_query': ask_ret['question_object'].query_text,
    }
    return ret


def async_find_all_windows(handler):
    kwargs = {
        'qtype': 'manual_human',
        'sensors': [
            'Computer ID',
            'Computer Name',
            'IP Address',
            'Operating System',
            'Is Windows',
        ],
        'question_filters': [
            'Is Windows, that =:True'
        ],
        'get_results': False,
    }
    ask_ret = handler.ask(**kwargs)
    ret = {
        'computer_name': '',
        'question_id': ask_ret['question_object'].id,
        'question_query': ask_ret['question_object'].query_text,
    }
    return [ret]


def async_find_computer_ids(handler, computer_names):
    rets = [async_find_computer_id(handler, x) for x in computer_names]
    return rets


class Paths(object):
    def __init__(self, form, handler, default_path='get_computer_names', **kwargs):
        super(Paths, self).__init__()

        self.next_action = 'main.py'

        # setup jinja2 template system
        self.jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('jinja_templates'))
        self.jinja2_env.filters['getitem'] = common.getitem

        # convert the form to a python dictionary
        self.formdict = common.formtodict(form)

        self.handler = handler

        # get the path key from formdict, default to 'get_computer_names' if not defined
        self.path_choice = self.formdict.get('path', default_path)

        # get the path method from Paths class based on path_choice
        self.path_method = getattr(self, self.path_choice, self.unsupported)

        # get the return from path_method
        self.path_return = self.path_method()

    # STEP 1
    def get_computer_names(self):
        next_path = 'computer_select'
        template_file = '1_get_computer_names.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Step 1: Provide Computer Names to perform patch operations on: '

        j_render = j_template.render(
            app=appinfo,
            title=title,
            nextaction=self.next_action,
            topmsg=title,
            next_path=next_path,
        )
        return j_render

    # STEP 2
    def computer_select(self):
        next_path = 'patch_computers'
        template_file = '2_computer_select.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Step 2: Select Computers'

        computer_names = self.formdict.get('computer_names', [])
        if type(computer_names) != list:
            computer_names = [computer_names]
        computer_names = [x for x in computer_names if x]
        # TODO: IF NONE, THROW ERROR PAGE
        if 'GET_ALL_WINDOWS' in computer_names:
            server_searches = async_find_all_windows(handler)
        else:
            server_searches = async_find_computer_ids(handler, computer_names)
        j_render = j_template.render(
            app=appinfo,
            title=title,
            topmsg=title,
            nextaction=self.next_action,
            server_searches=server_searches,
            next_path=next_path,
        )
        return j_render

    # STEP 3
    def patch_computers(self):
        next_path = 'get_computer_names'
        template_file = '3_patch_computers.html'
        j_template = self.jinja2_env.get_template(template_file)
        title = 'Step 3: Patch Computers'

        servers = self.formdict.get('server', [])
        if type(servers) != list:
            servers = [servers]
        servers = [x for x in servers if x]
        # TODO: IF NONE, THROW ERROR PAGE

        j_render = j_template.render(
            app=appinfo,
            title=title,
            topmsg=title,
            nextaction=self.next_action,
            servers=servers,
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

# common.print_html(paths.formdict)
common.print_html(paths.path_return)
