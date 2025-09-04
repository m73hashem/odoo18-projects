from odoo import models, fields

class RegistrationType(models.Model):
    _name = "registration.type"
    _description = "Employee Registration Type"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
