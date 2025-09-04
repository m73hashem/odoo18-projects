from odoo import models, api

class ReportAssetLabel(models.AbstractModel):
    _name = 'report.tait_asset_number.asset_label_report_template_id'
    _description = 'Asset Label Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("DOCIDS:", docids)
        print("DATA:", data)
        records = self.env['account.asset'].browse(docids)
        #4x6_size is the default value in case label_format_code not specified od data = none
        label_format = (data or {}).get('label_format_code', '4x6_size') 
        return {
            'doc_ids': docids,
            'doc_model': 'account.asset',
            'docs': records,
            'label_format_code': label_format,
        }
