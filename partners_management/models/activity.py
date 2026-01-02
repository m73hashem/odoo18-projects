from odoo import models, fields,api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class PartnerActivity(models.Model):
    _name = "partner.activity"
    _description = "Partner Activity"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one("custom.partner", string="Partner")
    name = fields.Char(string="Activity Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)

    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("done", "Done"),
        ],
        string="Status",
        default="pending",
        tracking=True,
    )

    plan_id = fields.Many2one(
    "partnership.plan",
    string="Source Plan",
    required=True,
    default=lambda self: self.env.context.get('default_plan_id'),
    readonly=True
)

                              
    responsible_user_id = fields.Many2one(
        "res.users", string="Responsible User", required=True, tracking=True
    )
    show_done_button = fields.Boolean(
        string="Show Done Button",
        compute="_compute_show_done_button"
    )
    
    

    #show button for the responsible user only
    @api.depends('responsible_user_id')
    def _compute_show_done_button(self):
        for rec in self:
            rec.show_done_button = (rec.responsible_user_id == self.env.user)


    def action_set_pending(self):
        for rec in self:
            rec.status = 'pending'

    def action_set_done(self):
        for rec in self:
            rec.status = 'done'
            
    # ===============================
    # Overrides
    # ===============================
    @api.model
    def create(self, vals):
        if not vals.get('plan_id'):
            ctx_plan = self.env.context.get('default_plan_id')
            if ctx_plan:
                vals['plan_id'] = ctx_plan

        if vals.get('plan_id') and not vals.get('partner_id'):
            plan = self.env['partnership.plan'].browse(vals.get('plan_id'))
            if plan and plan.partner_id:
                vals['partner_id'] = plan.partner_id.id

        if not vals.get('plan_id') and vals.get('partner_id'):
            partner = self.env['custom.partner'].browse(vals.get('partner_id'))
            if partner and partner.plan_ids:
                vals['plan_id'] = partner.plan_ids[0].id

        return super(PartnerActivity, self).create(vals)


    #check date validation
    @api.constrains('start_date', 'end_date', 'plan_id')
    def _check_dates_within_plan(self):
        for rec in self:
            if rec.plan_id:
                if rec.start_date and (rec.start_date < rec.plan_id.start_date or rec.start_date > rec.plan_id.end_date):
                    raise ValidationError("Start Date must be within the Plan period.")
                if rec.end_date and (rec.end_date < rec.plan_id.start_date or rec.end_date > rec.plan_id.end_date):
                    raise ValidationError("End Date must be within the Plan period.")

