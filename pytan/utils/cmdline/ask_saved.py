import copy
from . import ask_manual


class Worker(ask_manual.Worker):
    DESCRIPTION = 'Ask a saved question and export the results to a file'
    GROUP_NAME = 'Saved Question Options'
    ACTION = 'question'
    QTYPE = 'saved'

    def setup(self):
        self.add_export_results_opts()
        self.add_report_opts()

        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

        obj_map = self.tanium_obj.get_obj_map("{}_question".format(self.QTYPE))
        search_keys = copy.copy(obj_map['search'])

        choice = self.grp.add_mutually_exclusive_group()
        for k in search_keys:
            choice.add_argument(
                '--{}'.format(k),
                required=False, action='store', dest=k, default=self.SUPPRESS,
                help='{} of {} question to ask'.format(k, self.QTYPE),
            )

        choice = self.grp.add_mutually_exclusive_group()
        choice.add_argument(
            '--no-refresh_data',
            action='store_false', dest='refresh_data', default=False, required=False,
            help='Do not refresh the data available for a saved question'
        )
        choice.add_argument(
            '--refresh_data',
            action='store_true', dest='refresh_data', default=self.SUPPRESS, required=False,
            help='Refresh the data available for a saved question',
        )
