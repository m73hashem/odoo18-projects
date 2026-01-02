from odoo import models, fields, api

class Graduate(models.Model):
    _name = "graduates"
    _description = "graduates Archive"

    partner_id = fields.Many2one(
        'res.partner',
        string='User',
        domain=[('partner_type', '=', 'trainee')],
        required=True,
        ondelete='cascade'
    )

    name = fields.Char(string="Name", related="partner_id.name", store=True, readonly=True)
    phone = fields.Char(string="Phone", related="partner_id.phone", store=True, readonly=True)
    email = fields.Char(string="Email", related="partner_id.email", store=True, readonly=True)

    #experience = fields.Char(string="Experiences")
    language = fields.Char(string="Languages")

    """attachment_ids = fields.One2many(
        'ir.attachment', 'res_id',
        string='Attachments',
        domain=lambda self: [('res_model', '=', self._name)],
        readonly=False,)"""
    # Attachments field fixed
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'graduates_ir_attachments_rel',
        'graduate_id', 'attachment_id',
        string='Attachments'
    )

    # ---------- Smart Buttons ----------
    def action_view_packages(self):
        """Open a list view of all packages of the selected trainee"""
        self.ensure_one()  # تأكد أن الزر يُضغط على سجل واحد

        # جلب كل الدورات من res.partner التي يكون اسمها مطابق للمتدرب الحالي
        packages = self.env['res.partner'].search([
            ('name', '=', self.partner_id.name),
            ('partner_type', '=', 'trainee')
        ]).mapped('package_id')

        return {
            'name': f"Training Packages of {self.partner_id.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'training.package',
            'view_mode': 'list,form',
            'domain': [('id', 'in', packages.ids)],
            'target': 'current',
        }

    # ###cv
    # def action_view_cv(self):
    #     self.ensure_one()
    #     cv = self.env['graduate.cv'].search([('graduate_id', '=', self.id)], limit=1)
    #     if not cv:
    #         cv = self.env['graduate.cv'].create({'graduate_id': self.id})
    #     return {
    #         'name': f"CV of {self.partner_id.name}",
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'graduate.cv',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('graduate_relations.view_graduate_cv_form').id,
    #         'res_id': cv.id,
    #         'target': 'current',
    #     }
    #
    # ##Events
    # def action_event(self):
    #     pass


    #collect the training packeges for the user
    package_line_ids = fields.One2many(
        'graduate.package.line',
        'graduate_id',
        string='Training Packages'
    )




    _sql_constraints = [
        ('unique_partner_id', 'unique(partner_id)', 'Each trainee can only appear once in the graduates Archive.')
    ]

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """copy all packages/courses to sub table when select user/graduate"""
        for rec in self:
            rec.package_line_ids = [(5, 0, 0)]
            if rec.partner_id:
                partners = self.env['res.partner'].search([
                    ('name', '=', rec.partner_id.name),
                    ('partner_type', '=', 'trainee')
                ])
                rec.package_line_ids = [
                    (0, 0, {
                        'package_id': p.package_id.id,
                        'package_name': p.package_id.name,
                    })
                    for p in partners if p.package_id
                ]


class GraduatePackageLine(models.Model):
    _name = "graduate.package.line"
    _description = "graduate Training Package Line"

    graduate_id = fields.Many2one('graduates', string='Graduate', ondelete='cascade')
    package_id = fields.Many2one('training.package', string='Training Package', ondelete='restrict')
    package_name = fields.Char(string='Package Name')

