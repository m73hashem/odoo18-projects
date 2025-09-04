from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    expense_total = fields.Float(string="Total Expenses", readonly=True) #or expense_amount
    #edit after complete part 1.4 of the task
    task_count = fields.Integer(string="Task Count", compute="_compute_task_count", store=True)

    @api.depends('task_ids')
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)
            #rec.task_count = rec.task_ids and len(rec.task_ids) or 0
