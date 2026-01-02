from odoo import models, fields, api

class QualityTeam(models.Model):
    _name = "quality.team"
    _description = "Quality Evaluation Team"

    name = fields.Char(string="Team Name", required=True)

    manager_id = fields.Many2one(
        'res.users',
        string="Team Manager",
        required=True
    )

    member_ids = fields.Many2many(
        'res.users',
        string="Team Members"
    )

    description = fields.Text(string="Description")

    active = fields.Boolean(default=True)

    metric_ids = fields.One2many(
        'quality.metric',
        'team_id',
        string="Related Metrics"
    )


