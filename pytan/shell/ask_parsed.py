from . import ask_manual
from . import base


class Worker(ask_manual.Worker):
# class Worker(base.Base):
    DESCRIPTION = 'Ask a parsed question and export the results to a file'
    GROUP_NAME = 'Parsed Question Options'
    ACTION = 'question'
    QTYPE = 'parsed'
    PREFIX = 'ask_parsed'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

        self.grp.add_argument(
            '-q', '--question_text',
            required=True, action='store', default='', dest='question_text',
            help='The question text you want the server to parse into a list of parsed results'
        )
        self.grp.add_argument(
            '--picker',
            required=False, action='store', type=int, dest='picker',
            help='The index number of the parsed results that correlates to the actual question you wish to run -- you can get this by running this once without it to print out a list of indexes'
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
            response = self.handler.ask_parsed(qtype=self.QTYPE, **kwargs)
        except:
            raise
        m = "++ Asked Question {} ID: {}"
        print(m.format(response.question_object.query_text, response.question_object.id))
        return response

    def get_result(self):
        grps = ['Export Results Options', 'Export Object Options', 'Report File Options']
        kwargs = self.get_parser_args(grps)
        response = self.get_question_response()
        report_file, result = self.handler.export(response.question_results.result_set, **kwargs)
        return response, report_file, result
