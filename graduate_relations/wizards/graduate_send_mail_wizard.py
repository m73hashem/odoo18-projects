from odoo import models, fields, api

class SendGraduateEmailWizard(models.TransientModel):
    _name = "send.graduate.email.wizard"
    _description = "Wizard to Send Email to Graduates"

    subject = fields.Char(string="Email Subject", required=True)
    body = fields.Html(string="Email Body", required=True)

    graduate_ids = fields.Many2many(
        'training.graduate',
        string='Graduates'
    )

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="Attachments"
    )

    def action_send_email(self):
        """Send email to selected graduates"""
        Mail = self.env['mail.mail']

        for graduate in self.graduate_ids:
            if graduate.email:
                Mail.create({
                    'subject': self.subject,
                    'email_to': graduate.email,
                    'body_html': self.body,
                    'attachment_ids': [(6, 0, self.attachment_ids.ids)],
                }).send()

        return {'type': 'ir.actions.act_window_close'}
