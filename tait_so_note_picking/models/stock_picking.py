from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
_logger.info("✅ stock_picking.py LOADE=====================D")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_notes = fields.Text(string="Delivery Notes", readonly=True)

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        related='sale_id.user_id',
        store=True,
        readonly=True
    )
