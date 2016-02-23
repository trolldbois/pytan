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
            '-l', '--left-sensor',
            required=False, action='append', default=[], dest='left_sensors',
            help='Left side sensors, optionally describe parameters, options, and a filter'
        )
        self.grp.add_argument(
            '-r', '--right-sensor',
            required=False, action='append', default=[], dest='right_sensors',
            help='Right side sensors, optionally describe parameters, options, and a filter'
        )
        self.grp.add_argument(
            '-lt', '--lot',
            required=False, action='append', default=[], dest='lot',
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
        m = "++ Asked Question {} ID: {}"
        print(m.format(response.question.query_text, response.question.id))
        return response

    def get_result(self):
        response = self.get_question_response()
        print(response.result_data.result_set.to_csv_resultset())
        # Needs handler.export_file method
        # report_file, result = self.export_results(response.result_data.result_set)
        # return response, report_file, result
