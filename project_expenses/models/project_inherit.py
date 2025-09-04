from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    total_expense_amount = fields.Monetary(string='Total Expense Amount', readonly=True, default=0.0, currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)