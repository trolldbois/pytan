from . import base
from .. import calc
from .. import pretty


class Worker(base.GetBase):
    DESCRIPTION = 'Gets the Result Info for all the questions asked for a given saved question, or for all questions asked ever, and exports the question information to a CSV file'
    OBJECT_TYPE = 'saved_question'
    ACTION = 'get'
    SECOND_GROUP_NAME = 'Saved Question History Options'
    GROUP_NAME = 'Get Saved Question Options'

    def pre_init(self):
        self.OBJECT_STR = self.OBJECT_TYPE.replace('_', ' ').capitalize()

    def setup(self):
        self.add_report_opts()
        self.add_get_opts()
        self.grp = self.parser.add_argument_group(self.SECOND_GROUP_NAME)
        self.grp.add_argument(
            '--empty',
            action='store_true', dest='empty', default=False, required=False,
            help='Include details for questions with no data',
        )
        self.grp.add_argument(
            '--all',
            action='store_true', dest='all', default=False, required=False,
            help='Include details for ALL questions',
        )
        self.grp.add_argument(
            '--verbose',
            action='store_true', dest='verbose', default=False, required=False,
            help='Print out verbose information about question data/filtering',
        )

    def verbose(self, t):
        if self.args.verbose:
            print(t)

    def get_result(self):
        q_kwargs = {'objtype': 'question', 'include_hidden_flag': 1}
        m = "-- Getting all questions with arguments:\n{}"
        print m.format(self.pf(q_kwargs))
        all_questions = self.handler.get_all(**q_kwargs)
        print "++ Found {} total questions".format(len(all_questions))

        sq_ids = []
        sq_txt = ''
        if not self.args.all:
            sq_kwargs = self.get_kwargs()
            saved_questions = self.get_response(sq_kwargs)
            sq_ids = [getattr(y, 'id', -1) for y in saved_questions]
            sq_txt = "saved question ids: {}".format(', '.join([str(y) for y in sq_ids]))

        # flatten out result info attributes
        result_info_attrs = [
            'row_count',
            'estimated_total',
            'mr_tested',
            'passed',
        ]

        # dictify all questions for use with csv_dictwriter
        qattr = [
            'id',
            'query_text',
            'saved_question_id',
            'start_time',
            'expiration',
            'row_count',
            'estimated_total',
            'mr_tested',
            'passed',
        ]

        human_map = [
            'Question ID',
            'Question Text',
            'Spawned by Saved Question ID',
            'Question Started',
            'Question Expired',
            'Row Count',
            'Client Count Right Now',
            'Client Count that saw this question',
            'Client Count that passed this questions filters',
        ]

        q_dicts = []

        print "-- Filtering questions"

        for x in all_questions:
            if not self.args.all and getattr(x.saved_question, 'id', '') in sq_ids:
                m = "-- skipping question: {}, not asked for {}"
                self.verbose(m.format(x, sq_txt))

            ri = self.handler.get_result_info(x)
            if not self.args.empty and not ri.row_count:
                m = "-- Skipping question: {}, no rows available"
                self.verbose(m.format(x))
                continue

            m = "-- question: {} has {} rows available"
            self.verbose(m.format(x, ri.row_count))

            setattr(x, 'result_info', ri)
            setattr(x, 'saved_question_id', getattr(x.saved_question, 'id', '???'))
            setattr(x, 'start_time', calc.question_start_time(x)[0])
            for y in result_info_attrs:
                setattr(x, y, getattr(x.result_info, y, '???'))
            d = {human_map[qattr.index(k)]: str(getattr(x, k, '???')) for k in qattr}
            q_dicts.append(d)

        empty_txt = "that currently have data/rows"
        all_txt = "that are related to {}".format(sq_txt)

        m = []
        if not self.args.empty:
            m.append(empty_txt)

        if not self.args.all:
            m.append(all_txt)

        m = ' and '.join(m)
        f = "-- Filtered {} questions down to {}".format(len(all_questions), len(q_dicts))
        m = ' '.join([f, m])
        print m

        # turn the list of dicts into a CSV string
        q_csv = pretty.csvdictwriter(rows_list=q_dicts, headers=human_map)

        report_file = self.handler.create_report_file(
            contents=q_csv,
            report_file=self.args.report_file,
            report_dir=self.args.report_dir,
        )

        print "++ Wrote {} bytes to report file: '{}'".format(len(q_csv), report_file)
        return all_questions, q_dicts, q_csv, report_file
