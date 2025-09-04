from odoo import models, fields, api

class ProjectExpenseType(models.Model):
    _name = 'project.expense.type'
    _description = 'Project Expense Type'

    name = fields.Char(required=True)
    limit = fields.Monetary(required=True, default=0.0, currency_field='company_currency_id')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    @api.constrains('limit')
    def _check_limit_positive(self):
        for rec in self:
            if rec.limit <= 0:
                raise models.ValidationError('Limit must be greater than 0')