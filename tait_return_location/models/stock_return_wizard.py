from odoo import models, fields, api


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    location_id = fields.Many2one(
        'stock.location',
        string="Return Location",
        domain="[('usage', '=', 'internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Location where the returned products will be moved.",
        default=lambda self: self._get_default_location_id()
    )

    @api.model
    def _get_default_location_id(self):
        """Get default return location like Odoo 16 logic."""
        picking = self.env['stock.picking'].browse(self._context.get('active_id'))
        if picking.picking_type_id.return_picking_type_id:
            return picking.picking_type_id.return_picking_type_id.default_location_dest_id.id
        return picking.location_id.id

    def _prepare_picking_default_values(self):
        vals = super()._prepare_picking_default_values()

        if self.location_id:
            vals['location_dest_id'] = self.location_id.id

        return_picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'incoming'),
            ('name', 'ilike', 'return'),
            ('company_id', 'in', [False, self.picking_id.company_id.id])
        ], limit=1)

        if return_picking_type:
            vals['picking_type_id'] = return_picking_type.id
        else:
             vals['picking_type_id'] = self.env['stock.picking.type'].create({
                'name': 'Returns',
                'code': 'incoming',
                'sequence_code': 'RET',
                'default_location_dest_id': self.location_id.id if self.location_id else self.picking_id.location_id.id,
                'company_id': self.picking_id.company_id.id,
            }).id

        return vals