from odoo import models, fields, api
<<<<<<< HEAD
import logging
_logger = logging.getLogger(__name__)
_logger.info("✅ stock_picking.py LOADE=====================D")
=======
>>>>>>> e33d403681c1e931aad9215020742ea136542f3e


class StockPicking(models.Model):
    _inherit = 'stock.picking'

<<<<<<< HEAD
    delivery_notes = fields.Text(string="Delivery Notes", readonly=True)

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
=======
    delivery_notes = fields.Text('Delivery Notes')
    salesperson_id = fields.Many2one(
        'res.users',
        string='Sales Person',
>>>>>>> e33d403681c1e931aad9215020742ea136542f3e
        related='sale_id.user_id',
        store=True,
        readonly=True
    )
