# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError


class LabelReportWizard(models.TransientModel):
    _name = 'label.report.wizard'
    _description = 'Label Report Wizard'

    paperformat_code = fields.Selection([
        ('4x6_size', 'Label 4 x 6 cm'),
        ('6x10_size', 'Label 6 x 10 cm'),
    ], string='Label Size', required=True)

    def print_label(self):
        # Step 1: Get selected asset IDs from context
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError("No active records selected.")

        # Step 2: Map format codes to external paperformat XML IDs
        paperformat_map = {
            '4x6_size': 'paperformat_4x6cm',
            '6x10_size': 'paperformat_label_6x10cm',
        }

        # Step 3: Get the paperformat XML ID corresponding to selection
        paperformat_external_id = paperformat_map.get(self.paperformat_code)
        if not paperformat_external_id:
            raise UserError("Invalid label format selected.")

        # Step 4: Get paperformat record using env.ref
        try:
            paperformat = self.env.ref(f'tait_asset_number.{paperformat_external_id}')
        except ValueError:
            raise UserError("Paper format record not found. Please ensure the XML record exists.")

        # Step 5: Trigger report with paperformat and custom label format context
        return self.env.ref('tait_asset_number.action_report_asset_label').with_context(
            paperformat_id=paperformat.id,
            label_format_code=self.paperformat_code
        ).report_action(self.env['account.asset'].browse(active_ids))

'''
from odoo import models, fields, api

class LabelReportWizard(models.TransientModel):
    _name = 'label.report.wizard'
    _description = 'Label Report Wizard'
    
    paperformat_code = fields.Selection([
        ('4x6_size', '4 x 6 size'),
        ('6x10_size', '6 x 10 size'),
    ], string='Format', required=True)
    
    def print_label(self):
        active_ids = self.env.context.get('active_ids')
        
        # Map format code to paperformat record (you must create these records manually)
        paperformat_map = {
            '4x6_size': 'paperformat_4x6cm',
            '6x10_size': 'paperformat_label_6x10cm',
        }

        paperformat_external_id = paperformat_map.get(self.paperformat_code)
        paperformat = self.env.ref(f'tait_asset_number.{paperformat_external_id}')

        
        
        return self.env.ref('tait_asset_number.asset_label_report_action').with_context(
            paperformat_id=paperformat.id).report_action(self.env['account.asset'].browse(active_ids))
'''