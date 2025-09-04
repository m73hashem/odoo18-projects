from odoo import models, fields, api

class WizardProjectExpenses(models.TransientModel):
    _name = 'wizard.project.expenses'
    _description = 'Wizard to print project expenses report'

    project_ids = fields.Many2many('project.project', string='Projects', required=True)

    def action_print(self):
        data = []
        for proj in self.project_ids:
            data.append({
                'project_name': proj.name,
                'project_manager': proj.user_id.name or '',
                'task_count': proj.task_count,
                'total_expenses': proj.total_expense_amount,
            })
        return self.env.ref('project_expenses.action_report_project_expenses').report_action(self, data={'rows': data})