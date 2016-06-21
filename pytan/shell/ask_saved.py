from . import base


class Worker(base.Base):
    DESCRIPTION = 'Ask a saved question and export the results to a file'
    GROUP_NAME = 'Saved Question Options'
    ACTION = 'question'
    QTYPE = 'saved'
    PREFIX = 'ask_saved'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

        self.grp.add_argument(
            '--search',
            required=True, action='store', default='', dest='search',
            help='The question text you want to search for saved questions.'
        )
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()
        self.grp_choice_results()

    def get_question_response(self, **kwargs):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        m = "++ Asking {} question with arguments:\n{}"
        print(m.format(self.QTYPE, self.pf(kwargs)))
        try:
            response = self.handler.ask_saved(qtype=self.QTYPE, **kwargs)
        except:
            raise
        m = "++ Asked Question {} ID: {}"
        print(m.format(response.question.query_text, response.question.id))
        return response

    def get_result(self):
        grps = ['Export Results Options', 'Export Object Options',
                'Report File Options']
        kwargs = self.get_parser_args(grps)
        response = self.get_question_response()
        result_set = response.result_data.result_set
        report_file, result = self.handler.export(result_set, **kwargs)
        return response, report_file, result
