from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectExpenseRequest(models.Model):
    _name = 'project.expense.request'
    _description = 'Project Expense Request'

    name = fields.Char(string="Reference", default="New", copy=False, readonly=True)
    date = fields.Date(string="Request Date", default=fields.Date.context_today)
    project_id = fields.Many2one('project.project', string="Project", domain=[('active', '=', True)], required=True)
    manager_id = fields.Many2one('res.users', string="Project Manager", readonly=True)
    line_ids = fields.One2many('project.expense.line', 'request_id', string="Expense Lines")
    total_amount = fields.Float(string="Total", compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft', string='Status')#, tracking=True

    @api.depends('line_ids.amount')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.project_id.user_id:
            self.manager_id = self.project_id.user_id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('project.expense.request') or 'New'

        # تعيين المدير عند الإنشاء
        if vals.get('project_id') and not vals.get('manager_id'):
            project = self.env['project.project'].browse(vals['project_id'])
            if project.user_id:
                vals['manager_id'] = project.user_id.id

        return super().create(vals)

    def write(self, vals):
        for rec in self:
            if rec.state in ['done', 'cancel'] and 'state' not in vals:
                raise ValidationError("You cannot modify a request in Done or Cancel state.")

            # تحديث المدير إذا تغيّر المشروع
            if 'project_id' in vals:
                project = self.env['project.project'].browse(vals['project_id'])
                if project.user_id:
                    vals['manager_id'] = project.user_id.id

        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("You cannot delete a Done request.")
        return super().unlink()

    def copy(self, default=None):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("You cannot duplicate a Done request.")
        return super().copy(default)

    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError("Only draft requests can be confirmed.")
            rec.state = 'confirmed'

    def action_approve(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise ValidationError("Only confirmed requests can be approved.")
            rec.state = 'approved'

    def action_done(self):
        for rec in self:
            if rec.state != 'approved':
                raise ValidationError("Only approved requests can be marked as done.")

            # تحديث قيمة المصاريف في المشروع بشكل آمن
            new_total = rec.project_id.expense_total + rec.total_amount
            rec.project_id.write({'expense_total': new_total})

            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state not in ['draft', 'confirmed', 'approved']:
                raise ValidationError("Only draft, confirmed, or approved requests can be cancelled.")
            rec.state = 'cancel'

    def action_set_to_draft(self):
        for rec in self:
            if rec.state != 'cancel':
                raise ValidationError("Only cancelled requests can be reset to draft.")
            rec.state = 'draft'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            from lxml import etree
            arch = etree.fromstring(res['arch'])
            for node in arch.xpath("//field"):
                name = node.get('name')
                if name and name not in ['state', 'manager_id']:
                    modifiers = {"readonly": [["state", "in", ["done", "cancel"]]]}
                    node.set("modifiers", str(modifiers).replace("'", '"'))
            res['arch'] = etree.tostring(arch, encoding='unicode')
        return res

class ProjectExpenseLine(models.Model):
    _name = 'project.expense.line'
    _description = 'Project Expense Line'

    request_id = fields.Many2one('project.expense.request', required=True, ondelete='cascade')
    expense_type_id = fields.Many2one('project.expense.type', string='Expense Type', required=True)
    amount = fields.Float(string='Amount', required=True)

    @api.constrains('amount')
    def _check_amount(self):
        for line in self:
            if line.amount <= 0:
                raise ValidationError("Amount must be greater than 0.")
            if line.expense_type_id and line.amount > line.expense_type_id.limit:
                raise ValidationError("Amount cannot exceed the limit defined for this expense type.")
