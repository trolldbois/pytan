from . import ask_manual


class Worker(ask_manual.Worker):
    DESCRIPTION = 'Ask a parsed question and export the results to a file'
    GROUP_NAME = 'Parsed Question Options'
    ACTION = 'question'
    QTYPE = 'parsed'

    def setup(self):
        self.add_export_results_opts()
        self.add_report_opts()

        self.grp = self.parser.add_argument_group(self.GROUP_NAME)
        self.grp.add_argument(
            '-q', '--question_text',
            required=True, action='store', default='', dest='question_text',
            help='The question text you want the server to parse into a list of parsed results',
        )
        self.grp.add_argument(
            '--picker',
            required=False, action='store', type=int, dest='picker',
            help='The index number of the parsed results that correlates to the actual question you wish to run -- you can get this by running this once without it to print out a list of indexes',
        )
        self.grp_choice_results()
