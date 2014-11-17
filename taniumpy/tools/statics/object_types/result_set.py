from .column_set import ColumnSet
from .row import Row
import csv
import re


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
        self.columns = None
        self.rows = None

    def __str__(self):
        class_name = self.__class__.__name__
        ret = '{} for {}, {}'.format(
            class_name, self.question_id, self.columns,
        )
        return ret

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
            result.columns = ColumnSet.fromSOAPElement(val)
        result.rows = []
        # TODO: Make sure that each "r" is a row, with one value
        # per column in "c/v". This was tested with just one client.
        rows = el.findall('.//rs/r')
        for row in rows:
            result.rows.append(Row.fromSOAPElement(row, result.columns))
        return result

    @staticmethod
    def write_csv(fd, val, **kwargs):
        def fix_newlines(val):
            # turn \n into \r\n
            if type(val) == str:
                val = re.sub(r"([^\r])\n", r"\1\r\n", val)
            return val

        if not isinstance(val, ResultSet):
            raise Exception("{} is not a ResultSet instance!".format(val))

        # TODO:
        '''
        via kwargs:
        Add type to header
        Add sensor name to header
        Remove count column if it's only one for everything
        Add expanded groups logic
        '''
        headers = [x.display_name for x in val.columns]
        headers_sorted = sorted(headers)
        rows = [[fix_newlines(r[h]) for h in headers_sorted] for r in val.rows]

        writer = csv.writer(fd)
        writer.writerow(headers_sorted)
        writer.writerows(rows)
