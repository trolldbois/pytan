import logging

from pytan.builders import log_result
from pytan.builders.selects import build_selectlist
from pytan.builders.groups import build_parent_group
from pytan.tanium_ng import Question
from pytan.builders.constants import QUESTION_DEFAULTS

MYLOG = logging.getLogger(__name__)


def build_question(handler, **kwargs):
    selectlist = build_selectlist(handler, **kwargs)
    group = build_parent_group(handler, **kwargs)
    oargs = {k: kwargs.get(k, v) for k, v in QUESTION_DEFAULTS.items()}
    result = Question(selects=selectlist, group=group, **oargs)
    log_result('build_question', result, locals())
    return result
