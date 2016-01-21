import logging
import datetime

from pytan import PytanError
from pytan.tickle.tools import b64encode, obfuscate, deobfuscate

from pytan.constants import CRED_DEFAULTS, PYTAN_KEY

MYLOG = logging.getLogger(__name__)
CREDLOG = logging.getLogger(__name__ + '.credstore')


class CredentialsError(PytanError):
    pass


class Store(dict):

    def __init__(self, *args, **kwargs):
        super(Store, self).__init__(*args, **kwargs)
        _store_name = self.get('_store_name', '')
        class_name = self.__class__.__name__
        self._store_name = _store_name or class_name

    def __str__(self):
        me = self._store_name
        ret = []
        if not self.items():
            ret.append('** {} with no items'.format(me))

        for k, v in self.items():
            if k.startswith('_'):
                continue
            if isinstance(v, Store):
                a = "** {} attribute '{}' sub store with {} items".format(me, k, len(v.items()))
            else:
                a = "** {} attribute '{}': '{}'".format(me, k, v)
            ret.append(a)

        ret = '\n'.join(ret)
        return ret

    def __repr__(self):
        me = self._store_name
        ret = []
        if not self.items():
            ret.append('** {} with no items')

        for k, v in self.items():
            if k.startswith('_'):
                continue
            if isinstance(v, Store):
                a = "** {} attribute '{}' sub store with {} items".format(me, k, len(v.items()))
            else:
                a = "** {} attribute '{}': {!r}".format(me, k, v)
            ret.append(a)

        ret = '\n'.join(ret)
        return ret

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value
        try:
            super(Store, self).__setattr__(name, value)
        except:
            pass

    def __delattr__(self, name):
        if name in self:
            del self[name]
            try:
                super(Store, self).__delattr__(name)
            except:
                pass
        else:
            raise AttributeError("No such attribute: " + name)


class ArgStore(Store):
    pass


class HelpStore(Store):
    pass


class ResultStore(Store):
    pass


class TokenStore(Store):
    pass


class CredStore(dict):

    _NORMAL_CREDS = ['username', 'password', 'domain', 'secondary']

    def __init__(self):
        self.username = CRED_DEFAULTS['username']
        self.password = CRED_DEFAULTS['password']
        self.domain = CRED_DEFAULTS['domain']
        self.secondary = CRED_DEFAULTS['secondary']
        self.persistent = CRED_DEFAULTS['persistent']
        self.session_id = CRED_DEFAULTS['session_id']
        self.session_dt = None
        self.user_obj = None

    def __str__(self):
        me = self.__class__.__name__
        ret = ["    ** {} '{}': '{}'".format(me, k, getattr(self, k, '')) for k in sorted(self)]
        ret = '\n'.join(ret)
        return ret

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        if name == 'password' and self.get(name, ''):
            value = '**PASSWORD**'
        else:
            value = self.get(name, '')
        return value

    def __setattr__(self, name, value):
        old_value = self.get(name, '')
        old_attr_value = getattr(self, name, '')

        if name in self._NORMAL_CREDS and value:
            self.session_id = ''

        if name == 'persistent' and old_value != value:
            self.session_id = ''

        if name == 'password':
            value = obfuscate(key=PYTAN_KEY, string=value)

        if name == 'session_id' and (not value or old_value != value):
            self.session_dt = None
            self.user_obj = None

        if old_value != value:
            self[name] = value
            new_attr_value = getattr(self, name, '')
            m = "  ** {!r} updated from '{}' to '{}'"
            m = m.format(name, old_attr_value, new_attr_value)
            CREDLOG.debug(m)

    def __delattr__(self, name):
        if name in self:
            self[name] = ''

    def auth_type(self):
        if self.has_session_creds:
            if self.has_normal_creds:
                result = 'session_id (received by authenticating with {})'
                result = result.format(', '.join(self.normal_creds))
            else:
                result = 'session_id (supplied manually)'
        elif self.has_normal_creds:
            result = ', '.join(self.normal_creds)
        else:
            err = "Need username, password, domain, and/or secondary if not supplying session_id"
            raise CredentialsError(err)
        return result

    def persist_type(self):
        if self.persistent:
            result = "persistent (up to 1 week)"
        else:
            result = "non-persistent (up to 5 minutes)"
        return result

    @property
    def normal_creds(self):
        result = [k for k in self._NORMAL_CREDS if self.get(k, '')]
        return result

    @property
    def session_creds(self):
        result = [k for k in ['session_id'] if self.get(k, '')]
        return result

    @property
    def has_normal_creds(self):
        result = any(self.normal_creds)
        return result

    @property
    def has_session_creds(self):
        result = any(self.session_creds)
        return result

    def get_headers(self, **kwargs):
        """pass."""
        result = {}
        supplied_headers = kwargs.get('headers', {}) or {}
        result.update(supplied_headers)

        # if session_id is in creds, add that to the result
        if self.has_session_creds:
            m = "  ** Using Session ID for authentication headers"
            CREDLOG.debug(m)
            result['session'] = self.session_id
            [result.pop(k) for k in self._NORMAL_CREDS if k in result]
        elif self.has_normal_creds:
            adds = []
            if 'session' in result:
                result.pop('session')
            for k in self._NORMAL_CREDS:
                if not self.get(k):
                    continue
                if k == 'username':
                    result[k] = b64encode(self.get(k))
                elif k == 'password':
                    result[k] = b64encode(self._true_password)
                else:
                    result[k] = self.get(k)
                adds.append(k)

            m = "  ** Using {} for authentication headers"
            m = m.format(', '.join(adds))
            CREDLOG.debug(m)
        else:
            err = "Need username, password, domain, and/or secondary if not supplying session_id"
            raise CredentialsError(err)
        return result

    @property
    def _true_password(self):
        return deobfuscate(key=PYTAN_KEY, string=self.get('password'))

    def session_seconds(self):
        if self.session_dt:
            result = (datetime.datetime.utcnow() - self.session_dt).seconds
        else:
            result = -1
        m = "  ** session id issued {} seconds ago"
        m = m.format(result)
        CREDLOG.debug(m)
        return result

    def session_is_expired(self):
        if not self.session_id or self.session_dt is None:
            result = True
        elif self.persistent:
            result = False
        elif self.session_seconds() > 260:
            result = True
        else:
            result = False
        return result
