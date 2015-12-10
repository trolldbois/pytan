import pprint
from . import base


class Worker(base.Base):
    DESCRIPTION = 'Ask a manual question and export the results to a file'
    GROUP_NAME = 'Manual Question Options'

    def setup(self):
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()

        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-s', '--sensor',
            required=False, action='append', default=[], dest='sensors',
            help='Sensor, optionally describe parameters, options, and a filter'
        )
        self.grp.add_argument(
            '-f', '--filter',
            required=False, action='append', default=[], dest='filters',
            help='Whole question filters, only return results for machines that match',
        )
        self.grp.add_argument(
            '-o', '--option',
            required=False, action='append', default=[], dest='options',
            help='Whole question options, controls question filters',
        )
        self.grp_choice_results()

    def export_response(self, response):
        if response['question_results']:
            grps = ['Export Results Options']
            kwargs = self.get_parser_args(grps)
            m = "++ Exporting {} with arguments:\n{}"
            print m.format(response['question_results'], pprint.pformat(kwargs))
            report_file, result = self.handler.export_to_report_file(
                obj=response['question_results'],
                **kwargs
            )
            m = "++ Report file {!r} written with {} bytes"
            print(m.format(report_file, len(result)))
        else:
            report_file, result = None, None
            m = "++ No results returned, run get_question_results.py to get the results"
            print m.format()
        return report_file, result

    def get_response(self):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        m = "++ Asking manual question with arguments:\n{}"
        print m.format(pprint.pformat(kwargs))
        response = self.handler.ask_manual(**kwargs)
        m = "++ Asked Question {question_object.query_text!r} ID: {question_results.id!r}"
        print m.format(**response)
        return response

    def get_result(self):
        response = self.get_response()
        report_file, result = self.export_response(response)
        return response
