from odoo import models, fields

class EventInherit(models.Model):
    _inherit = 'event.event'

    show_to_graduates = fields.Boolean(
        string="Visible to Graduates",
        help="If checked, this event will be visible to all graduates."
    )
    
