from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_notes = fields.Text('Delivery Notes')

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            for picking in order.picking_ids:
                picking.delivery_notes = order.delivery_notes
        return res