from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    registration_status_id = fields.Many2one("registration.type", string="Registration Status",
                                             help="Registration status/type of the employee.")
