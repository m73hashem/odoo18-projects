from odoo import models, fields

class HrJobTask(models.Model):
    _name = "hr.job.task"
    _description = "Job Role Task"
    _order = "id"

    job_id = fields.Many2one("hr.job", string="Job Position", required=True, ondelete="cascade")
    task_name = fields.Char(string="Task Name", required=True)
    task_description = fields.Text(string="Description")



class HrJob(models.Model):
    _inherit = "hr.job"

    task_ids = fields.One2many("hr.job.task", "job_id", string="Role Tasks", 
                               help="Tasks that describe this job's responsibilities.")
