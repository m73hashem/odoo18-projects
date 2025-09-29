from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

class Partner(models.Model):
    _name = "custom.partner"
    _description = "Business Partners"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Partner Name", required=True, tracking=True)
    country = fields.Char(string="Country", tracking=True)
    partner_type = fields.Selection(
        [
            ("local", "Local"),
            ("international", "International"),
        ],
        string="Partner Type",
        default="local",
        tracking=True
    )
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    partnership_duration = fields.Char(
        string="Partnership Duration",
        compute="_compute_partnership_duration",
        store=False,   
    )
    website_url = fields.Char(string="Company Website", tracking=True)
    company_logo = fields.Binary(string="Company Logo")

    responsible_user_id = fields.Many2one("res.users", string="Responsible User", tracking=True)

    # Attachments
    custom_attachment_ids = fields.One2many(
        "ir.attachment",
        "res_id",
        string="Attachments",
        domain=[('res_model', '=', 'custom.partner')],
        tracking=True
    )

    # Relations
    plan_ids = fields.One2many("partnership.plan", "partner_id", string="Plans")
    evaluation_ids = fields.One2many("partner.evaluation", "partner_id", string="Evaluations")
    custom_activity_ids = fields.One2many("partner.activity", "partner_id", string="Activities")

    # Smart button counters
    plan_count = fields.Integer(string="Plans", compute="_compute_counts")
    evaluation_count = fields.Integer(string="Evaluations", compute="_compute_counts")
    activity_count = fields.Integer(string="Activities", compute="_compute_counts")

    #compute counts
    @api.depends("plan_ids", "evaluation_ids", "custom_activity_ids")
    def _compute_counts(self):
        for rec in self:
            rec.plan_count = len(rec.plan_ids)
            rec.evaluation_count = len(rec.evaluation_ids)
            rec.activity_count = len(rec.custom_activity_ids)

    # Compute the partnership duration
    @api.depends("start_date", "end_date")
    def _compute_partnership_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                delta = relativedelta(rec.end_date, rec.start_date)
                parts = []
                if delta.years:
                    parts.append(f"{delta.years} {_('Year(s)')}")
                if delta.months:
                    parts.append(f"{delta.months} {_('Month(s)')}")
                if delta.days:
                    parts.append(f"{delta.days} {_('Day(s)')}")
                rec.partnership_duration = ", ".join(parts) if parts else _("0 Days")
            else:
                rec.partnership_duration = ""

    # ----------------------
    # Smart button actions
    # ----------------------
    #Open list/form view of related partnership plans.
    def action_view_plans(self):
        return {
            "name": "Plans",
            "type": "ir.actions.act_window",
            "res_model": "partnership.plan",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

    # Open list/form view of related partnership evaluations.
    def action_view_evaluations(self):
        return {
            "name": "Evaluations",
            "type": "ir.actions.act_window",
            "res_model": "partner.evaluation",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

    # Open list/form view of related partnership activities.
    def action_view_activities(self):
        return {
            "name": "Activities",
            "type": "ir.actions.act_window",
            "res_model": "partner.activity",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }
