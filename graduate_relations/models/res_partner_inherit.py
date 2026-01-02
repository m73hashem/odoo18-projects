from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    partner_type = fields.Selection(
        selection_add=[('graduate', 'Graduate')],
    )

# """this part to show the partner_id without repeat in the form"""
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        # شرط partner_type = trainee
        domain = [('partner_type', '=', 'trainee')] + args
        if name:
            domain = ['|', ('name', operator, name), ('email', operator, name)] + domain

        partners = self.search(domain, limit=limit)

        # إزالة التكرار حسب الاسم
        seen_names = set()
        unique_partners = []
        for partner in partners:
            normalized_name = (partner.name or '').strip().lower()
            if normalized_name not in seen_names:
                seen_names.add(normalized_name)
                unique_partners.append(partner)

        return [(p.id, p.display_name) for p in unique_partners]