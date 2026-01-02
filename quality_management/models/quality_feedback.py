from odoo import api, fields, models

class QualityFeedback(models.Model):
    _name = 'quality.feedback'
    _description = 'Quality Feedback'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one('res.partner', string="Beneficiary")
    course_id = fields.Many2one('training.course', string="Service")
    feedback_text = fields.Text(string="Impression")
    survey_score = fields.Float(string="Survey Result")
    sentiment = fields.Selection([
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative')
    ], string="Beneficiary feeling", compute='_compute_sentiment', store=True)

    @api.depends('feedback_text')
    def _compute_sentiment(self):
        positive_words = [
            'جيد', 'ممتاز', 'رائع', 'ممتازة', 'ممتازين', 'جميل', 'ممتاز جدا',
            'good', 'great', 'excellent', 'perfect', 'amazing', 'nice'
        ]

        negative_words = [
            'سيء', 'سئ', 'ضعيف', 'رديء', 'سيئ', 'غير جيد', 'مزعج',
            'bad', 'poor', 'terrible', 'awful', 'worse'
        ]

        for rec in self:
            text = (rec.feedback_text or "").lower()

            if not text:
                rec.sentiment = 'neutral'
                continue

            # check words
            if any(word in text for word in positive_words):
                rec.sentiment = 'positive'
            elif any(word in text for word in negative_words):
                rec.sentiment = 'negative'
            else:
                rec.sentiment = 'neutral'

