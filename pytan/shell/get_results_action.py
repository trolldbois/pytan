from . import base


class Worker(base.GetResultsBase):
    OBJECT_TYPE = 'action'
    ACTION = 'export results'
    FILE_PREFIX = 'action_'
