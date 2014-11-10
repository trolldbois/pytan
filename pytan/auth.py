# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import logging
from . import constants


class Auth(object):
    def __init__(self, username, password, **kwargs):
        super(Auth, self).__init__()

        self.AUTHLOG = logging.getLogger("pytan.auth").debug
        self._username = username
        self._password = password
        self.session_id = None
        self._token = {}

        constant_args = [
            'SHOW_SESSION_ID',
        ]
        for a in constant_args:
            v = kwargs.get(a) or getattr(constants, a)
            setattr(self, a, v)
        self.update_token()

    def __str__(self):
        str_tpl = "Auth {}".format
        ret = str_tpl(self.token_type_details)
        return ret

    def update_token(self):
        """updates self.token with either session ID or user/pass auth"""
        upd_tpl = "SOAP Token updated to: {}".format
        if self.session_id:
            token = self.token_session_id
        else:
            token = self.token_userpass
        if self._token != token:
            self._token = token
            self.AUTHLOG(upd_tpl(self.token_type_details))

    def auth_fallback(self):
        """removes the session ID from the token, and reverts back to
        user and password auth"""
        self.session_id = None
        self.update_token()

    def session_id_text(self, session_id):
        """returns session ID if SHOW_SESSION_ID = True"""
        if self.SHOW_SESSION_ID:
            id_text = session_id
        else:
            id_text = "..."
        return id_text

    @property
    def token(self):
        """returns the token"""
        if not hasattr(self, '_token'):
            return None
        return self._token

    @token.setter
    def token(self, value):
        """sets the token"""
        self._token = value

    @property
    def via_session_id(self):
        """returns True if self.token dict has 'session' in it"""
        return 'session' in self._token.keys()

    @property
    def via_userpass(self):
        """returns True if token dict has 'auth' in it"""
        return 'auth' in self._token.keys()

    @property
    def token_type_details(self):
        """returns token type and details in text form"""
        tok_tpl = 'auth type: {} [{}: "{}"]'.format

        if self.via_session_id:
            token_predetails = 'ID'
            token_details = self.session_id_text(self._token.get('session'))
            token_type = 'session ID'
        elif self.via_userpass:
            token_predetails = 'username'
            token_details = self._token.get('auth').get('username')
            token_type = 'username/password'
        else:
            token_predetails = 'None'
            token_details = 'None'
            token_type = 'Not yet set'

        token_type_details = tok_tpl(
            token_type, token_predetails, token_details
        )
        return token_type_details

    @property
    def token_userpass(self):
        """returns a dictionary that has 'auth': SOAP element: auth,
        $username, $password
        """
        token = {
            'auth': {'username': self._username, 'password': self._password}
        }
        return token

    @property
    def token_session_id(self):
        """returns a dictionary that has 'session': '$session_id' """
        token = {'session': self.session_id}
        return token
