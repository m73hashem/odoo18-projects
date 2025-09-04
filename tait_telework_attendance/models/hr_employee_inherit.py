from odoo import models, fields
from datetime import datetime, timedelta
import random


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def get_current_contract(self):
        self.ensure_one()
        return self.env['hr.contract'].search([
            ('employee_id', '=', self.id),
            ('state', '=', 'open')
        ], limit=1)

    def get_actual_wage_amount(self):
        contract = self.get_current_contract()
        if contract and contract.actual_wage_percent:
            return contract.wage * (contract.actual_wage_percent / 100.0)
        return 0.0
 
    def action_generate_attendance(self):
        for employee in self:
            employee._generate_attendance_records()
        return True
 
    def _generate_attendance_records(self, start_date=None, end_date=None, intensity_level='normal'):
        self.ensure_one()
    
        if not start_date:
            start_date = fields.Date.today() - timedelta(days=30)
        if not end_date:
            end_date = fields.Date.today()
    
        contract = self.get_current_contract()
        if not contract or not contract.resource_calendar_id:
            return
    
        # تحديد معاملات الغياب والتأخير بناءً على intensity_level
        if intensity_level == 'strict':
            absence_multiplier = 1.5
            late_multiplier = 1.2
            early_leave_multiplier = 1.2
        elif intensity_level == 'flexible':
            absence_multiplier = 0.5
            late_multiplier = 0.7
            early_leave_multiplier = 0.7
        else:  # normal
            absence_multiplier = 1.0
            late_multiplier = 1.0
            early_leave_multiplier = 1.0
    
        attendance_rate = contract.actual_wage_percent / 100.0
        absence_probability = max(0.05, (1 - attendance_rate) * absence_multiplier)
        late_probability = max(0.05, 0.3 * (1 - attendance_rate) * late_multiplier)
        early_leave_probability = max(0.05, 0.3 * (1 - attendance_rate) * early_leave_multiplier)
    
        # حذف السجلات المولدة مسبقًا في نفس الفترة
        self.env['hr.attendance'].search([
            ('employee_id', '=', self.id),
            ('generated_by_system', '=', True),
            ('check_in', '>=', start_date),
            ('check_out', '<=', end_date),
        ]).unlink()
    
        calendar = contract.resource_calendar_id
        public_holidays = self.env['resource.calendar.leaves'].search([
            ('date_from', '<=', end_date),
            ('date_to', '>=', start_date),
            ('resource_id', '=', False),
        ])
        leaves = self.env['hr.leave'].search([
            ('employee_id', '=', self.id),
            ('state', '=', 'validate'),
            ('request_date_to', '>=', start_date),
            ('request_date_from', '<=', end_date),
        ])
    
        current = start_date
        while current <= end_date:
            if any(ph.date_from.date() <= current <= ph.date_to.date() for ph in public_holidays):
                current += timedelta(days=1)
                continue
    
            if any(l.request_date_from <= current <= l.request_date_to for l in leaves):
                current += timedelta(days=1)
                continue
    
            day_attendances = calendar.attendance_ids.filtered(lambda a: int(a.dayofweek) == current.weekday())
            if not day_attendances:
                current += timedelta(days=1)
                continue
    
            if random.random() < absence_probability:
                current += timedelta(days=1)
                continue
    
            for att in day_attendances:
                check_in_time = datetime.combine(current, datetime.min.time()) + timedelta(hours=att.hour_from)
                check_out_time = datetime.combine(current, datetime.min.time()) + timedelta(hours=att.hour_to)
    
                if random.random() < late_probability:
                    check_in_time += timedelta(minutes=random.randint(5, 60))
    
                if random.random() < early_leave_probability:
                    check_out_time -= timedelta(minutes=random.randint(5, 60))
    
                self.env['hr.attendance'].create({
                    'employee_id': self.id,
                    'check_in': check_in_time,
                    'check_out': check_out_time,
                    'generated_by_system': True,
                })
    
            current += timedelta(days=1)
    
        self.message_post(body=f"Attendances generated for the period {start_date} → {end_date} with intensity: {intensity_level}.")
