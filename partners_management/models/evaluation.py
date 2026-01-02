from odoo import models, fields


class PartnerEvaluation(models.Model):
    _name = "partner.evaluation"
    _description = "Partner Evaluation"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Evaluation Name", required=True, tracking=True)
    partner_id = fields.Many2one("custom.partner", string="Partner", required=True, tracking=True)
    evaluation_date = fields.Date(string="Evaluation Date", tracking=True)
    criteria = fields.Text(string="Criteria", tracking=True)

    survey_id = fields.Many2one("survey.survey", string="Survey")

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
            })
            self.survey_id = new_survey.id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'survey.survey',
                'view_mode': 'form',
                'res_id': new_survey.id,
                'target': 'current',
            }