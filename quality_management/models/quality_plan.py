from odoo import api, fields, models

class QualityPlan(models.Model):
    _name = 'quality.plan'
    _description = 'Quality Improvement Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title", required=True)
    plan_manager_id =  fields.Many2one("res.users", string="Responsible",)
    issue_description = fields.Text(string="Description")
    progress = fields.Float(string="Progress (%)", compute="_compute_progress", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], default='draft',string="State", tracking=True)

    # project_id = fields.Many2one('project.project', string="Related Project")
    start_date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    end_date = fields.Date()

    procedure_ids = fields.One2many(
        'quality.plan.procedure',
        'plan_id',
        string="Procedures")

    @api.depends('procedure_ids.state')
    def _compute_progress(self):
        for plan in self:
            procedures = plan.procedure_ids
            if not procedures:
                plan.progress = 0.0
            else:
                total = len(procedures)
                done_count = len(procedures.filtered(lambda p: p.state == 'done'))
                plan.progress = (done_count / total) * 100

            plan._update_plan_state()

    
    def action_start(self):
        for plan in self:
            plan.state = 'in_progress'

    def action_complete(self):
        for plan in self:
            plan.state = 'done'

    #procedures
    def action_view_procedures(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Plan Procedures',
            'res_model': 'quality.plan.procedure',
            'view_mode': 'kanban,form',
            'views': [
                    (self.env.ref('quality_management.view_quality_plan_procedure_kanban').id, 'kanban'),
                    (self.env.ref('quality_management.view_quality_plan_procedure_form').id, 'form'),
                ],
            'domain': [('plan_id', '=', self.id)],
            'context': {'default_plan_id': self.id},
        }
    
    def _update_plan_state(self):
        for plan in self:
            procedures = plan.procedure_ids

            if not procedures:
                plan.state = 'draft'
                continue

            if all(p.state == 'done' for p in procedures):
                plan.state = 'done'

            elif any(p.state in ('in_progress', 'done') for p in procedures):
                plan.state = 'in_progress'

            else:
                plan.state = 'draft'

    # def _notify_plan_completed(self):
    #     """Send notification when plan becomes done."""
    #     for plan in self:
    #         if plan.plan_manager_id:
    #             self.env['mail.activity'].create({
    #                 'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
    #                 'res_model_id': self.env['ir.model']._get_id('quality.plan'),
    #                 'res_id': plan.id,
    #                 'user_id': plan.plan_manager_id.id,
    #                 'note': "تم اكتمال جميع الإجراءات، والخطة الآن مكتملة.",
    #             })
