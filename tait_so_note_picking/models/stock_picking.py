from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_notes = fields.Text('Delivery Notes')
    salesperson_id = fields.Many2one(
        'res.users',
        string='Sales Person',
        related='sale_id.user_id',
        store=True,
        readonly=True
    )
