from odoo import models, fields


class PartnerActivity(models.Model):
    _name = "partner.activity"
    _description = "Partner Activity"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one("custom.partner", string="Partner", required=True, tracking=True)
    name = fields.Char(string="Activity Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    status = fields.Selection(
        [
            ("planned", "Planned"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="planned",
        tracking=True
    )
    responsible_user_id = fields.Many2one("res.users", string="Responsible User", tracking=True)
