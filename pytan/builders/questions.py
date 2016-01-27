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

    if not selectlist:
        m = "No left side supplied for build_question, question will be 'Get Online from...'"
        MYLOG.info(m)

    if not group:
        m = "No right side supplied for build_question, question will be '... from all machines'"
        MYLOG.info(m)

    oargs = {k: kwargs.get(k, v) for k, v in QUESTION_DEFAULTS.items()}
    result = Question(selects=selectlist, group=group, **oargs)
    log_result('build_question', result, locals())
    return result
