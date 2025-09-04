from odoo import models, fields

class HrContract(models.Model):
    _inherit = "hr.contract"

    actual_wage_percent = fields.Float(string="Actual Wage %",
                                       help="Actual wage percentage applied to the contract's wage.")

