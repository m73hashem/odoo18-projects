from odoo import models, fields


class PartnerEvaluation(models.Model):
    _name = "partner.evaluation"
    _description = "Partner Evaluation"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one("custom.partner", string="Partner", required=True, tracking=True)
    evaluation_date = fields.Date(string="Evaluation Date", tracking=True)
    criteria = fields.Text(string="Criteria", tracking=True)
    score = fields.Float(string="Score", tracking=True)
    comments = fields.Text(string="Comments", tracking=True)
