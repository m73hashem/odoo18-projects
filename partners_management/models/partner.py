from datetime import date
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

EVALUATION_RATE = [
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'Medium'),
    ('3', 'High'),
]

class Partner(models.Model):
    _name = "custom.partner"
    _description = "Business Partners"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_logo = fields.Binary(string="Company Logo")
    name = fields.Char(string="Partner Name", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    partnership_duration = fields.Char(
        string="Partnership Duration",
        compute="_compute_partnership_duration",
        store=False,
    )
    website_url = fields.Char(string="Company Website", tracking=True)
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
    partnership_type_id = fields.Many2one(
        "partnership.type",
        string="Partnership Type",
        required=False,
        tracking=True,
        help="Specify the type of partnership for this partner.",
        ondelete="set null"
    )
    signature_date = fields.Date(
        string="Signature Date",
        tracking=True,
        help="The official date when the partnership agreement was signed."
    )
    partner_approved = fields.Boolean(string='Approved', default=False, tracking=True)
    responsible_user_id = fields.Many2one("res.users", string="Responsible Partner User", tracking=True)
    allow_portal_edit = fields.Boolean(
        string="Allow Portal User to Edit",
        default=False,
        tracking=True
    )

    
    priority = fields.Selection(EVALUATION_RATE, string='Priority', default='0', tracking=True)

    partner_description = fields.Text(string="Description", tracking=True)

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

    # Smart button counters # added store=True to use in filternig
    plan_count = fields.Integer(string="Plans", compute="_compute_counts", store=True)
    evaluation_count = fields.Integer(string="Evaluations", compute="_compute_counts", store=True)
    activity_count = fields.Integer(string="Activities", compute="_compute_counts", store=True)

    # Progress fields =====Begining=========
    plan_total_count = fields.Integer(
        string="Total Plans",
        compute="_compute_plan_progresses",
        store=True
    )
    plan_done_count = fields.Integer(
        string="Done Plans",
        compute="_compute_plan_progresses",
        store=True
    )
    plan_progress = fields.Float(
        string="Plan Completion (%)",
        compute="_compute_plan_progresses",
        store=True,
        digits=(5, 2),
        help="Percentage based on number of plans that are done"
    )

    # NEW: activity-weighted progress across all plans (0..100)
    activity_weighted_progress = fields.Float(
        string="Weighted Progress (%)",
        compute="_compute_plan_progresses",
        store=True,
        digits=(5, 2),
        help="Weighted average of plan progress based on activities"
    )



    @api.depends("plan_ids", "plan_ids.state", "plan_ids.plan_progress", "plan_ids.activities_ids")
    def _compute_plan_progresses(self):
        """Compute plan counts, simple done-count progress and weighted activity-based progress."""
        for rec in self:
            plans = rec.plan_ids or self.env["partnership.plan"]
            total = len(plans)
            done = len(plans.filtered(lambda p: p.state == 'done'))
            rec.plan_total_count = total
            rec.plan_done_count = done
            rec.plan_progress = (float(done) / total * 100.0) if total else 0.0

            # Weighted activity-based progress:
            # weight each plan by its number of activities; if no activities at all, fallback to plan_progress simple average
            total_activities = 0
            weighted_sum = 0.0
            for plan in plans:
                act_count = len(plan.activities_ids) or 0
                # use plan.plan_progress (0..100)
                weighted_sum += (plan.plan_progress or 0.0) * act_count
                total_activities += act_count

            if total_activities > 0:
                rec.activity_weighted_progress = weighted_sum / total_activities
            else:
                # fallback: average of plan_progress (unweighted) or 0 if no plans
                if total:
                    avg = sum([p.plan_progress or 0.0 for p in plans]) / total
                    rec.activity_weighted_progress = avg
                else:
                    rec.activity_weighted_progress = 0.0

    ####====End of progress fields ============
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

    # ============================================================
    # =============== NOTIFICATIONS ===============================
    # ============================================================

    def _create_activity(self, user, summary, note):
        """Helper to create an activity for a specific user."""
        if not user:
            return
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=user.id,
            summary=summary,
            note=note,
            date_deadline=fields.Date.today(),
        )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if vals.get('responsible_user_id'):
            user = record.responsible_user_id
            record._create_activity(
                user,
                summary=_("You have been assigned as the Responsible User"),
                note=_("Partner: %s") % record.name,
            )
        return record

    def write(self, vals):
        for rec in self:
            # Detect change of responsible user
            if 'responsible_user_id' in vals and vals['responsible_user_id'] != rec.responsible_user_id.id:
                new_user = self.env['res.users'].browse(vals['responsible_user_id'])
                rec._create_activity(
                    new_user,
                    summary=_("You have been assigned as the Responsible User"),
                    note=_("Partner: %s") % rec.name,
                )

            # Detect change in approval
            if 'partner_approved' in vals:
                status = _("Approved") if vals['partner_approved'] else _("Unapproved")
                assigned_user = rec.responsible_user_id or self.env.user
                rec._create_activity(
                    assigned_user,
                    summary=_("Partner Approval Status Changed"),
                    note=_("Partner '%s' has been %s.") % (rec.name, status),
                )
        return super().write(vals)
    
    ##
    end_date_notification_sent = fields.Boolean(
        string="End Date Notification Sent",
        default=False,
        tracking=False
    )

    @api.model
    def _cron_notify_unapproved_partners(self):
        """Send notification if end_date passed but not approved yet."""
        today = date.today()
        expired_partners = self.search([
            ('end_date', '<=', today),
            ('partner_approved', '=', False),
            ('responsible_user_id', '!=', False),
            ('end_date_notification_sent', '=', False),
        ])

        for partner in expired_partners:
            user = partner.responsible_user_id
            if not user:
                continue

            #  Activity
            partner._create_activity(
                user,
                summary=_("Partnership Ended Without Approval"),
                note=_("The partnership '%s' has ended on %s but has not been approved yet.") %
                     (partner.name, partner.end_date.strftime('%Y-%m-%d')),
            )

            partner.end_date_notification_sent = True


  