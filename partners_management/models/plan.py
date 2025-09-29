from odoo import models, fields


class PartnershipPlan(models.Model):
    _name = "partnership.plan"
    _description = "Partnership Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one("custom.partner", string="Partner", required=True, tracking=True)
    name = fields.Char(string="Plan Name", required=True, tracking=True)
    year = fields.Integer(string="Year", tracking=True)
    objectives = fields.Text(string="Objectives", tracking=True)
    approved = fields.Boolean(string="Approved", tracking=True)
    tasks = fields.Text(string="Tasks", tracking=True)


