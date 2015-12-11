from . import base


class Worker(base.GetResultsBase):
    OBJECT_TYPE = 'saved_question'
    ACTION = 'export results'
    FILE_PREFIX = 'saved_question_'
