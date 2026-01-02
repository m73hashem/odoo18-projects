from odoo import models, fields, api

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def create_quality_metric_from_survey(self):
        self.ensure_one()
        for user_input in self:
            survey_id = user_input.survey_id
            evaluation = survey_id.metric_id
           

            if evaluation:
                avg_score = 0.0
                all_comments = ''
                all_recommendations = ''

                score = user_input.user_input_line_ids.filtered(
                    lambda q: q.participant_field == 'score' and not q.skipped)
                comment = user_input.user_input_line_ids.filtered(
                    lambda q: q.participant_field == 'comment' and not q.skipped)
                recommendation = user_input.user_input_line_ids.filtered(
                    lambda q: q.participant_field == 'recommendation' and not q.skipped)

                for criteria in evaluation.criteria_ids:
                    criteria_lines = score.filtered(lambda l: l.metric_criteria_id.id == criteria.id)

                    if not criteria_lines:
                        continue

                    scores = criteria_lines.mapped("value_scale")
                    max_scale = criteria_lines[0].question_id.scale_max

                    avg_value = sum(scores) / len(scores)

                    avg_percent = (avg_value / max_scale) * 100

                    criteria.total_score += avg_percent
                    criteria.count += 1

                    #avg_score += avg_percent * (criteria.weight / 100.0)
                    avg_score = ((sum(scores) / len(scores)) / max_scale) * 100

                if comment:
                    comments = comment.mapped('display_name')
                    all_comments = "\n".join(comment for comment in comments) if comments else ""

                if recommendation:
                    recommendations = recommendation.mapped('display_name')
                    all_recommendations = "\n".join(
                        recommendation for recommendation in recommendations) if recommendations else ""
                    

                self.env['quality.metric.participant'].create({
                    'metric_id': evaluation.id,
                    'name': f"Survey Result from {self.partner_id.name or 'Anonymous'}",
                    'partner_id': self.partner_id.id,
                    'score': avg_score,
                    'comment': all_comments,
                    'recommendation': all_recommendations,
                })

    def _mark_done(self):
        res = super()._mark_done()
        for user_input in self:
            user_input.create_quality_metric_from_survey()
        return res


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    metric_criteria_id = fields.Many2one(related='question_id.metric_criteria_id')

