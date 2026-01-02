from odoo import models, fields, _

class PartnershipType(models.Model):
    _name = "partnership.type"
    _description = "Partnership Type"
    _rec_name = "name"
    _order = "name asc"

    name = fields.Char(string="Type Name", required=True, translate=True)
    code = fields.Char(string="Code", help="Unique code to identify the partnership type.")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True, tracking=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The partnership type name must be unique.')
    ]
