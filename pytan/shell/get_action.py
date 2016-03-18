from . import base


class Worker(base.GetBase):
    OBJECT_TYPE = 'action'

    def setup(self):
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()
        self.grp_choice_results()

    def get_response(self, **kwargs):


    def get_result(self):
