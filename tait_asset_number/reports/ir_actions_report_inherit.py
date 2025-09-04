'''
from odoo import models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _get_report_paperformat(self):
        """
        Allow overriding the default paperformat dynamically
        via context['paperformat_id'].
        """
        paperformat_id = self.env.context.get('paperformat_id')
        if paperformat_id:
            pf = self.env['report.paperformat'].browse(paperformat_id)
            if pf.exists():
                return pf
            else:
                raise ValueError(f"Invalid paperformat_id {paperformat_id} passed in context")
        return super()._get_report_paperformat()
        '''
'''
        paperformat_id = self.env.context.get('paperformat_id')
        if paperformat_id:
            return self.env['report.paperformat'].browse(paperformat_id)
        return super()._get_report_paperformat()
        '''
'''