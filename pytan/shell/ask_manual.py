from . import base

class Worker(base.Base):
    DESCRIPTION = 'Ask a manual question and export the results to a file'
    GROUP_NAME = 'Manual Question Options'
    ACTION = 'question'
    QTYPE = 'manual'
    PREFIX = 'ask_manual'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

        self.grp.add_argument(
            '-sl', '--sensor_left',
            required=False, action='append', default=[], dest='sensor_left',
            help='Left side sensors, optionally describe parameters, options, and a filter'
        )
        self.grp.add_argument(
            '-sr', '--sensor_right',
            required=False, action='append', default=[], dest='sensor_right',
            help='Right side sensors, optionally describe parameters, options, and a filter'
        )
        self.grp.add_argument(
            '-o', '--option',
            required=False, action='append', default=[], dest='options',
            help='Whole question options, controls question filters',
        )
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()
        self.grp_choice_results()

    def get_question_response(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        m = "++ Asking {} question with arguments:\n{}"
        print(m.format(self.QTYPE, self.pf(kwargs)))
        response = self.handler.ask_manual(qtype=self.QTYPE, **kwargs)
        m = "++ Asked Question {question_object.query_text!r} ID: {question_results.id!r}"
        print(m.format(**response))
        return response

    def get_result(self):
        response = self.get_question_response()
        report_file, result = self.export_results(response['question_results'])
        return response, report_file, result
