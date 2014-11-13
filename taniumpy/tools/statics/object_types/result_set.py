from .column_set import ColumnSet

class ResultSet(object):
    """Wrap the result of GetResultData"""

    def __init__(self):
        self.age = None
        self.id = None
        self.report_count = None
        self.question_id = None
        self.archived_question_id = None
        self.seconds_since_issued = None
        self.issue_seconds = None
        self.expire_seconds = None
        self.tested = None
        self.passed = None
        self.mr_tested = None
        self.mr_passed = None
        self.estimated_total = None
        self.select_count = None
        self.row_count = None
        self.error_count = None
        self.no_result_count = None
        self.row_count_machines = None
        self.row_count_flag = None
        self.column_set = None
        self.row_set = None

    @classmethod
    def fromSOAPElement(cls, el):
        """Deserialize a ResultInfo from a result_info SOAPElement

        Assumes all properties are integer values (true today)

        """
        result = ResultSet()
        for property in vars(result):
            if property in ['column_set', 'row_set']:
                 continue
            val = el.find('.//{}'.format(property))
            if val is not None and val.text:
                setattr(result, property, int(val.text))
        val = el.find('.//cs')
        if val is not None:
            result.column_set = ColumnSet.fromSOAPElement(val)
        return result
