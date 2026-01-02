from odoo import api, fields, models, _
from datetime import date


class QualityMetric(models.Model):
    _name = 'quality.metric'
    _description = 'Quality Metric'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)

    metric_target = fields.Selection([
        ('package', 'Training Package'),
        ('course', 'Course'),
    ], string="Evaluation Goal", required=True)

    metric_manager_id =  fields.Many2one("res.users", string="Responsible",)

    package_id = fields.Many2one('training.package', string="Training Package",)
    course_id = fields.Many2one('training.course',string="Course") 
    survey_id = fields.Many2one('survey.survey', string="Survey", store=True)
    satisfaction_rate = fields.Float(string="Satisfaction Rate (%)", compute='_compute_satisfaction_rate', store=True)
    success_rate = fields.Float(string="Success Rate (%)")
    complaint_count = fields.Integer(string="Complaint Count")
    target_value = fields.Float(string="Target Value (%)", default=0.0)
    metric_state = fields.Selection([
        ('low', 'Low'),
        ('stable', 'Stable'),
        ('improving', 'Improving'),
    ], string="Metric State", compute='_check_metric_state', store=True)

    start_date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    end_date = fields.Date()

    participant_ids = fields.One2many('quality.metric.participant', 'metric_id', string="Participant")
    criteria_ids = fields.One2many('quality.metric.criteria', 'metric_id', string="Criteria")
    recommendations = fields.Html(compute='_compute_recommendations', store=True, readonly=False)
    notes = fields.Html(compute='_compute_notes', store=True, readonly=False)
    
    participant_count = fields.Integer(
        string="Participant Count",
        compute='_compute_participant_count')
    
    ####
    alert_state = fields.Selection([
        ('low', 'Low'),
        ('exact', 'Exact'),
        ('high', 'High')
    ], string="Previous State", compute='_check_alert_state', store=True)

    alert_ids = fields.One2many(
        'quality.alert', 'metric_id',
        string="Related Alerts"
    )

    team_id = fields.Many2one(
    'quality.team',
    string="Team"
    )

    team_member_ids = fields.Many2many(
        'res.users',
        string="Team Members",
        related='team_id.member_ids',
        store=False
    )


    @api.model
    def create(self, vals):
        metric = super().create(vals)
        # create alert for every new metric
        existing_alert = self.env['quality.alert'].search([('metric_id', '=', metric.id)], limit=1)
        if not existing_alert:
            self.env['quality.alert'].create({
                'name': _('Alert of : %s') % metric.name,
                'metric_id': metric.id,
                'min_threshold': 50,  # default value
                'last_state': 'high',
            })
        return metric

    @api.depends('satisfaction_rate', 'target_value')
    def _check_metric_state(self):
        for rec in self:
            if rec.satisfaction_rate < rec.target_value:
                rec.metric_state = 'low'
            elif rec.satisfaction_rate == rec.target_value:
                rec.metric_state = 'stable'
            else:
                rec.metric_state = 'improving'
           
    @api.depends('satisfaction_rate')
    def _check_alert_state(self):
        for rec in self:
            alert = self.env['quality.alert'].search([('metric_id', '=', rec.id)], limit=1)
            if not alert:
                continue

            if rec.satisfaction_rate < alert.min_threshold:
                state = 'low'
            elif rec.satisfaction_rate == alert.min_threshold:
                state = 'exact'
            else:
                state = 'high'

            rec.alert_state = state

            # alert in chatter
            if state != alert.last_state:
                if rec.metric_manager_id:
                    message = self._generate_colored_alert_message(rec, state, alert)
                    rec.message_post(
                        body=message,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment'
                    )

                     #  activity for metric manager
                    rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary='تنبيه جودة',
                    note=message,
                    user_id=rec.metric_manager_id.id
                    )


                alert.last_state = state

    def _generate_colored_alert_message(self, rec, state, alert):
        state_labels = {
            'low': 'Low',
            'exact': 'Exact',
            'high': 'High'
        }

        icons = {
            'low': '⚠️',
            'exact': '📌',
            'high': '✅',
        }

        return (
            f"{icons.get(state, '')} Quality Alert\n"
            f"---------------------------------\n"
            f"The assessment status for Standard: {rec.name} has been updated.\n"
            f"New State: {state_labels.get(state)}\n"
            f"Current satisfaction rate: {rec.satisfaction_rate:.2f}%\n"
            f"Minimum acceptable: {alert.min_threshold:.2f}%"
        )



    def action_view_alerts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alerts',
            'res_model': 'quality.alert',
            'view_mode': 'list,form',
            'views': [
                    (self.env.ref('quality_management.view_quality_alert_list').id, 'list'),
                    (self.env.ref('quality_management.view_quality_alert_form').id, 'form'),
                ],
            'domain': [('metric_id', '=', self.id)],
            'context': {'default_metric_id': self.id},
        }

    ####
    @api.depends('criteria_ids.avg_score')
    def _compute_satisfaction_rate(self):
        for rec in self:
            scores = rec.criteria_ids.mapped('avg_score')
            rec.satisfaction_rate = sum(scores) / len(scores) if scores else 0.0

    @api.depends('participant_ids')
    def _compute_participant_count(self):
        for rec in self:
            rec.participant_count = len(rec.participant_ids)


    @api.depends('participant_ids.comment')
    def _compute_notes(self):
        for rec in self:
            comments = rec.participant_ids.mapped('comment')
            if comments:
                rec.notes = "<ul>" + "".join(
                    f"<li>{comment}</li>" for comment in comments) + "</ul>" if comments else ""
            else:
                rec.notes = ''

    @api.depends('participant_ids.recommendation')
    def _compute_recommendations(self):
        for rec in self:
            recommendations = rec.participant_ids.mapped('recommendation')
            if recommendations:
                rec.recommendations = "<ul>" + "".join(
                    f"<li>{recommendation}</li>" for recommendation in
                    recommendations) + "</ul>" if recommendations else ""
            else:
                rec.recommendations = ''

    def action_open_survey(self):
        self.ensure_one()
        Survey = self.env['survey.survey']

        if self.survey_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'survey.survey',
                'view_mode': 'form',
                'res_id': self.survey_id.id,
                'target': 'current',
            }
        else:
            new_survey = Survey.create({
                'title': self.name,
                'survey_type': 'survey',
                'metric_id': self.id,
            })
            self.survey_id = new_survey.id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'survey.survey',
                'view_mode': 'form',
                'res_id': new_survey.id,
                'target': 'current',
            }

    def action_open_plans(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quality improvement plans',
            'res_model': 'quality.plan',
            'view_mode': 'list,form',
            'target': 'current',
        }

    @api.model
    def compute_kpis(self):
        """Compute KPIs automatically."""
        metrics = self.search([])
        for metric in metrics:
            # مثال توضيحي لحساب معدل الرضا والنجاح
            if metric.course_id:
                metric.success_rate = 85.0  # Replace with real logic from training results
                metric.satisfaction_rate = 92.0  # Replace with real survey data
                metric.metric_state = 'improving' if metric.satisfaction_rate > 80 else 'declining'


class QualityMetricParticipant(models.Model):
    _name = "quality.metric.participant"

    metric_id = fields.Many2one('quality.metric', string="Quality Metric", required=True, ondelete='cascade')
    name = fields.Char(string="Criteria", required=True)
    
    partner_id = fields.Many2one('res.partner', string="Answered By")
    
    score = fields.Float(digits=(5, 2), default=0.0)
    comment = fields.Text()
    recommendation = fields.Text()
    criteria_id = fields.Many2one('quality.metric.criteria', string="Metric Criteria")


class QualityMetricCriteria(models.Model):
    _name = "quality.metric.criteria"
    _description = "Quality Metric Criteria"

    metric_id = fields.Many2one('quality.metric', string="Quality Metric", required=True, ondelete='cascade')
    name = fields.Char(string="Criteria", required=True)
    weight = fields.Float(string="Weight(%)")
    
    total_score = fields.Float(string='Total Score')

    count = fields.Float(string='Count')
    avg_score = fields.Float(string='Average', compute='_compute_avg_score')

    @api.depends('total_score', 'count')
    def _compute_avg_score(self):
        for rec in self:
            if rec.total_score and rec.count:
                rec.avg_score = rec.total_score / rec.count
            else:
                rec.avg_score = 0.0
