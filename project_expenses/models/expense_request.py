from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectExpenseRequest(models.Model):
    _name = 'project.expense.request'
    _description = 'Project Expense Request'
    _rec_name = 'name'

    name = fields.Char(string='Reference', readonly=True)
    date = fields.Datetime(default=fields.Datetime.now, required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True, domain=[('active','=',True)])
    project_manager_id = fields.Many2one('res.users', string='Project Manager', readonly=True)
    expense_line_ids = fields.One2many('project.expense.request.line', 'request_id', string='Expense Lines')
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('approved','Approved'),('done','Done'),('cancel','Cancelled')], default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', help='Customer for created pickings if product lines present')
    picking_id = fields.Many2one('stock.picking', string='Picking')
    product_line_ids = fields.One2many('project.expense.product.line','request_id',string='Product Lines')

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            self.project_manager_id = self.project_id.user_id and self.project_id.user_id.id or False

    def action_confirm(self):
        self.write({'state':'confirmed'})

    def action_approve(self):
        self.write({'state':'approved'})

    def action_done(self):
        total = 0.0
        for line in self.expense_line_ids:
            if line.amount <= 0:
                raise UserError(_('Expense amount must be greater than 0'))
            if line.amount > line.expense_type_id.limit:
                raise UserError(_('Amount for %s exceeds its limit of %s' ) % (line.expense_type_id.name, line.expense_type_id.limit))
            total += line.amount
        if self.project_id:
            self.project_id.total_expense_amount += total
        self.write({'state':'done'})
        if self.product_line_ids and self.partner_id:
            self._create_outgoing_picking()

    def action_cancel(self):
        self.write({'state':'cancel'})

    def action_set_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        if any(rec.state=='done' for rec in self):
            raise UserError(_('Cannot delete record in done state'))
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        if any(rec.state=='done' for rec in self):
            raise UserError(_('Cannot duplicate a done expense request'))
        return super().copy(default)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('project.expense.request.seq')
            if not seq:
                raise UserError(_('Please define the sequence "project.expense.request.seq" in system settings'))
            vals['name'] = seq
        return super().create(vals)

    def _create_outgoing_picking(self):
        self.ensure_one()
        Picking = self.env['stock.picking'].sudo()
        Move = self.env['stock.move'].sudo()
        warehouse = None
        if self.partner_id:
            warehouse = self.env['stock.warehouse'].search([('company_id','=',self.company_id.id)], limit=1)
        if not warehouse:
            warehouse = self.env['stock.warehouse'].search([], limit=1)
        if not warehouse:
            return
        picking_type = self.env['stock.picking.type'].search([('warehouse_id','=',warehouse.id),('code','=','outgoing')], limit=1)
        if not picking_type:
            return
        picking_vals = {
            'picking_type_id': picking_type.id,
            'partner_id': self.partner_id.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id or self.env.ref('stock.stock_location_customers').id,
            'origin': self.name,
            'company_id': self.company_id.id,
        }
        picking = Picking.create(picking_vals)
        moves = []
        for line in self.product_line_ids:
            move_vals = {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_uom.id,
                'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'picking_type_id': picking.picking_type_id.id,
                'company_id': self.company_id.id,
            }
            Move.create(move_vals)
        self.picking_id = picking.id

class ProjectExpenseRequestLine(models.Model):
    _name = 'project.expense.request.line'
    _description = 'Project Expense Request Line'

    request_id = fields.Many2one('project.expense.request', ondelete='cascade')
    expense_type_id = fields.Many2one('project.expense.type', string='Expense Type', required=True)
    amount = fields.Monetary(currency_field='company_currency_id', required=True)
    company_currency_id = fields.Many2one('res.currency', related='request_id.company_id.currency_id', readonly=True)

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise models.ValidationError('Amount must be greater than 0')
            if rec.expense_type_id and rec.amount > rec.expense_type_id.limit:
                raise models.ValidationError('Amount exceeds expense type limit')

class ProjectExpenseProductLine(models.Model):
    _name = 'project.expense.product.line'
    _description = 'Project Expense Product Line'

    request_id = fields.Many2one('project.expense.request', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True)