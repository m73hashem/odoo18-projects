from odoo import models, fields, api


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    metric_id = fields.Many2one('quality.metric', related='survey_id.metric_id')

    metric_criteria_id = fields.Many2one(
        'quality.metric.criteria',
        string="Quality Criteria",
        domain="[('metric_id', '=', metric_id)]",
        help="Score from this question will count toward this criteria."
    )
