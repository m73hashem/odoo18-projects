from odoo import models, fields, api
from odoo.exceptions import UserError

class AssignTasksWizard(models.TransientModel):
    _name = "assign.tasks.wizard"
    _description = "Assign Tasks to Employees"

    task_count = fields.Integer(string="Number of Tasks", required=True)
    recurring = fields.Boolean(string="Recurring")
    project_id = fields.Many2one("project.project", string="Project")

    def action_assign_tasks(self):
        if self.task_count <= 0:
            raise UserError("Task count must be greater than 0.")

        employees = self.env['hr.employee'].browse(self.env.context.get('active_ids', []))
        if not employees:
            raise UserError("No employees selected.")

        for emp in employees:
            if not emp.job_id or not emp.job_id.task_ids:
                continue  # if no assigned tasks to the job

            tasks = emp.job_id.task_ids
            for i in range(self.task_count):
                for task in tasks:
                    self.env['project.task'].create({
                        'name': task.task_name,
                        'description': task.task_description,
                        'project_id': self.project_id.id if self.project_id else False,
                        'user_id': emp.user_id.id if emp.user_id else False,
                    })
        return {'type': 'ir.actions.act_window_close'}
