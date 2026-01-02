from odoo import api, fields, models

class QualityAlert(models.Model):
    _name = 'quality.alert'
    _description = 'Quality Alert'
    _inherit = ['mail.thread']

    name = fields.Char(string="Alert Name", required=True)
    metric_id = fields.Many2one('quality.metric', string="Related Metric", required=True)
    min_threshold = fields.Float(string="Minimum Permissible (%)", default=50)
    last_state = fields.Selection([('low', 'Less than the minimum'), ('exact', 'Exact'), ('high', 'Above the limit')],
                                  string="Previous State", default='high')