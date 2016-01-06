from . import base


class Worker(base.Base):
    DESCRIPTION = (
        'Provides an interactive python console with pytan\'s Handler available as handler'
    )
    INTERACTIVE = True

    def get_exec(self):
        s = 'from pytan.utils import *'
        return s
