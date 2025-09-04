from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AttendanceGenerationWizard(models.TransientModel):
    _name = "attendance.generation.wizard"
    _description = "Attendance Generation Wizard"

    date_from = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    date_to = fields.Date(string="End Date", required=True, default=fields.Date.context_today)
    intensity_level = fields.Selection([
        ('normal', 'Normal'),
        ('strict', 'Strict'),
        ('flexible', 'Flexible'),
    ], string="Intensity Level", default='normal', required=True)

    def action_confirm_generation(self):
        employees = self.env['hr.employee'].browse(self.env.context.get('active_ids', []))
        if not employees:
            raise UserError(_("No employees selected."))

        for emp in employees:
            emp._generate_attendance_records(
                start_date=self.date_from,
                end_date=self.date_to
            )
        return {'type': 'ir.actions.act_window_close'}
