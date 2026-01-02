from odoo import api, fields, models

class QualityPlanProcedure(models.Model):
    _name = 'quality.plan.procedure'
    _description = 'Quality Improvement Procedure'

    name = fields.Char(string="Procedure Name", required=True)
    description = fields.Text(string="Description")

    plan_id = fields.Many2one("quality.plan", string="Plan", ondelete="cascade")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string="State", default='draft')

    def action_start(self):
        self.state = 'in_progress'
        self.plan_id._compute_progress()

    def action_done(self):
        self.state = 'done'
        self.plan_id._compute_progress()

    def action_draft(self):
        self.state = 'draft'
        self.plan_id._compute_progress()
