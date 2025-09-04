from odoo import models, fields, api
from odoo.exceptions import ValidationError
from lxml import etree


class ProjectExpenseRequest(models.Model):
    _inherit = 'project.expense.request'

    product_line_ids = fields.One2many(
        'project.expense.request.product.line',
        'request_id',
        string="Product Lines"
    )
    picking_id = fields.Many2one('stock.picking', string="Related Picking", readonly=True)

    def action_done(self):
        for rec in self:
            if rec.state != 'approved':
                raise ValidationError("Only approved requests can be marked as done.")

            # Create stock picking if product lines exist
            if rec.product_line_ids:
                picking = rec._create_picking()
                if picking:
                    rec.picking_id = picking.id

            # Update project expense total
            rec.project_id.write({
                'expense_total': rec.project_id.expense_total + rec.total_amount
            })

            rec.state = 'done'

    def _create_picking(self):
        picking_type = self.env.ref('stock.picking_type_out')
        partner = self.manager_id.partner_id

        move_lines = []
        for line in self.product_line_ids:
            if not line.product_id:
                raise ValidationError(f"Missing product in request '{self.name}'.")
            move_lines.append((0, 0, {
                'name': line.product_id.display_name or line.product_id.name or 'Unnamed Product',
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_id.uom_id.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
            }))

        if not move_lines:
            raise ValidationError("No product lines provided.")

        picking = self.env['stock.picking'].create({
            'partner_id': partner.id if partner else False,
            'picking_type_id': picking_type.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'origin': self.name,
            'move_ids_without_package': move_lines,
        })

        picking.action_confirm()
        return picking

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            arch = etree.fromstring(res['arch'])
            for node in arch.xpath("//button[@name='action_set_to_draft']"):
                node.set("modifiers", '{"invisible": [["state", "!=", "cancel"]]}')
            res['arch'] = etree.tostring(arch, encoding='unicode')
        return res


class ProjectExpenseRequestProductLine(models.Model):
    _name = 'project.expense.request.product.line'
    _description = 'Project Expense Product Line'

    request_id = fields.Many2one('project.expense.request', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")