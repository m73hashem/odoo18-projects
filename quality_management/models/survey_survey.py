from odoo import api, fields, models

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    metric_id = fields.Many2one(
        'quality.metric',
        string="Related Metric",
        help="Metric this survey belongs to"
    )
