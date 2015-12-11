from . import base


class Worker(base.GetResultsBase):
    OBJECT_TYPE = 'question'
    ACTION = 'export results'
    FILE_PREFIX = 'question_'
