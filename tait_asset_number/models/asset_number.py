from odoo import models, fields, api

class AssetNumber(models.Model):
    _inherit = 'account.asset'

    asset_sequence = fields.Char(string='Asset Number', readonly=True, copy=False, default="New Asset")

    
    
    @api.model
    def create(self, vals):
        if not vals.get('asset_sequence') or vals['asset_sequence'] == 'New Asset':
            vals['asset_sequence'] = self.env['ir.sequence'].next_by_code('account.asset.seq') or '/'
            return super().create(vals)

    def read(self, fields=None, load='_classic_read'):
        include_display_name = fields and 'display_name' in fields
        if include_display_name:
            fields = list(fields)
            fields.remove('display_name')

        if fields is not None:
            if 'name' not in fields:
                fields.append('name')
            if 'asset_sequence' not in fields: #field that display beside the name
                fields.append('asset_sequence') #field that display beside the name

        records = super().read(fields, load)

        if include_display_name:
            for rec in records:
                name = rec.get('name') or ''
                refrence_no = rec.get('asset_sequence') or ''  #field that display beside the name
                rec['display_name'] = f"[{refrence_no}] {name}" if refrence_no else name

        return records

 
    #زر الطباعة
    '''
    def action_print_asset_label(self):
        print("Self:", self) 
        return self.env.ref('tait_asset_number.asset_label_report_action').report_action(
            self[:1].id,
            config=False,
            data={'label_format_code': '6x10_size'}  # 6x10_size  or 4x6_size
        )
    '''

    def action_print_asset_label(self):
        if len(self) != 1:
            raise UserError("Please select exactly one asset to print the label.")
            
        return self.env.ref('tait_asset_number.asset_label_report_action').report_action(
            self.id,
            config=False,
            data={'label_format_code': '6x10_size'}
        )
