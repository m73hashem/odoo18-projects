from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExpenseType(models.Model):
    _name = 'project.expense.type'
    _description = 'Project Expense Type'

    name = fields.Char(string='Expense Type Name', required=True)
    limit = fields.Float(string='Limit Amount', required=True)

    @api.constrains('limit')
    def _check_limit_positive(self):
        for rec in self:
            if rec.limit <= 0:
                raise ValidationError("Limit must be greater than 0.")
