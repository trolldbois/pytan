from . import base


class Worker(base.Base):
    DESCRIPTION = 'Provides an interactive console with pytan available as handler'
    INTERACTIVE = True

    def get_exec(self):
        s = 'from pytan.utils.debug import *'
        return s
