from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PartnershipPlan(models.Model):
    _name = "partnership.plan"
    _description = "Partnership Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one(
        "custom.partner", string="Partner", required=True, tracking=True)
    name = fields.Char(string="Plan Name", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    objectives = fields.Text(string="Objectives", tracking=True)

    activities_ids = fields.One2many("partner.activity",'plan_id', string="Activities")
    ##state
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string="Status", default="draft", tracking=True,
        compute="_compute_activity_state", store=True)

    activity_count = fields.Integer(
        string="Number of Activities",
        compute="_compute_activity_state",
        store=True
    )
    
    #NEW: progress of this plan based on activities (0..100)
    plan_progress = fields.Float(
        string="Plan Progress (%)",
        compute="_compute_plan_progress",
        store=True,
        digits=(5, 2),
        help="Percentage of activities done inside this plan"
    )
    
    @api.depends('activities_ids', 'activities_ids.status')
    def _compute_plan_progress(self):
        for plan in self:
            total_acts = len(plan.activities_ids) if plan.activities_ids else 0
            if total_acts:
                done_acts = len(plan.activities_ids.filtered(lambda a: a.status == 'done'))
                plan.plan_progress = (float(done_acts) / total_acts) * 100.0
            else:
                plan.plan_progress = 0.0


    @api.depends('activities_ids.status')
    def _compute_activity_state(self):
        for plan in self:
            plan.activity_count = len(plan.activities_ids)
            done_count = len(plan.activities_ids.filtered(lambda a: a.status == 'done'))
            if plan.activity_count == 0:
                plan.state = 'draft'
            elif done_count == 0:
                plan.state = 'draft'
            elif done_count < plan.activity_count:
                plan.state = 'in_progress'
            else:
                plan.state = 'done'

    @api.onchange('activities_ids')
    def _onchange_activities_status(self):
        # keep behavior similar to compute (onchange helps UI before save)
        for plan in self:
            done_count = len(plan.activities_ids.filtered(lambda a: a.status == 'done'))
            if len(plan.activities_ids) == 0:
                plan.state = 'draft'
            elif done_count == 0:
                plan.state = 'draft'
            elif done_count < len(plan.activities_ids):
                plan.state = 'in_progress'
            else:
                plan.state = 'done'

    def action_view_activities(self):
        self.ensure_one()
        return {
            'name': 'Activities',
            'type': 'ir.actions.act_window',
            'res_model': 'partner.activity',
            'view_mode': 'list,form,kanban',
            'domain': [('plan_id', '=', self.id)],
            'context': {
                'default_plan_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
            'target': 'current',
        }


    # check plan date validation
    @api.constrains('start_date', 'end_date', 'partner_id')
    def _check_dates_within_partner(self):
        for rec in self:
            if rec.partner_id:
                if rec.start_date and (
                        rec.start_date < rec.partner_id.start_date or rec.start_date > rec.partner_id.end_date):
                    raise ValidationError("Start Date must be within the partnership period.")
                if rec.end_date and (
                        rec.end_date < rec.partner_id.start_date or rec.end_date > rec.partner_id.end_date):
                    raise ValidationError("End Date must be within the partnership period.")

