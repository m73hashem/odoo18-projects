from odoo import models, fields, api

class TrainingGraduate(models.Model):
    _name = "training.graduate"
    _description = "Training Graduate"
    _rec_name = "partner_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    partner_id = fields.Many2one(
        'res.partner',
        string="Graduate",
        required=True,
        ondelete='cascade', 
            )

    email = fields.Char(related='partner_id.email', string="Email", readonly=True)
    phone = fields.Char(related='partner_id.phone', string="Phone", readonly=True)
    national_id = fields.Char(related='partner_id.national_id', string='National ID', readonly=True)
    mobile = fields.Char(related='partner_id.mobile', string='Mobile', readonly=True)
    division = fields.Char(related='partner_id.division', string="Division", readonly=True)
    function = fields.Char(related='partner_id.function', string="Job Position", readonly=True)
    program = fields.Char(related='partner_id.program', string="Program", readonly=True)
    specialization = fields.Char(related='partner_id.specialization', string="Specialization", readonly=True)
    
    #gender
    #level
    

    course_ids = fields.Many2many(
    comodel_name='training.course',
    string='Courses',
    compute='_compute_course_ids',
    store=False,
    )

    trainee_count = fields.Integer(
    compute="_compute_course_ids",
    string="Number of Courses"
    )

    event_ids = fields.Many2many(
        'event.event',
        'graduate_event_rel',
        'graduate_id',
        'event_id',
        string="Events"
    )


    _sql_constraints = [
        ('unique_partner', 'unique(partner_id)', 'This graduate already exists!')
    ]

    @api.depends('partner_id.course_ids')
    def _compute_course_ids(self):
        for rec in self:
            rec.course_ids = rec.partner_id.course_ids
            rec.trainee_count = len(rec.partner_id.course_ids)

    

    ## courses
    def action_view_graduate_courses(self):
        self.ensure_one()
        return {
            'name': "Courses as Trainee",
            'type': 'ir.actions.act_window',
            'res_model': 'training.course',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.course_ids.ids)],
            'target': 'current',
        }
    ###cv
    def action_view_cv(self):
        self.ensure_one()
        cv = self.env['graduate.cv'].search([('graduate_id', '=', self.id)], limit=1)
        if not cv:
            cv = self.env['graduate.cv'].create({'graduate_id': self.id})
        return {
            'name': f"CV of {self.partner_id.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'graduate.cv',
            'view_mode': 'form',
            'view_id': self.env.ref('graduate_relations.view_graduate_cv_form').id,
            'res_id': cv.id,
            'target': 'current',
        }

    ##Events
    def action_event(self):
        self.ensure_one()
        events = self.env['event.event'].search([
            ('show_to_graduates', '=', True)
        ])

        return {
            'name': "Available Events",
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,list,form',
            'domain': [('id', 'in', events.ids)],
            'target': 'current',
        }


    @api.model
    def cron_create_graduates(self):
        """Create training.graduate records for partners marked as graduates"""

        partners = self.env['res.partner'].search([
            ('is_graduate', '=', True)
        ])

        for partner in partners:
            # to avoid dublicate records
            existing = self.env['training.graduate'].search_count([
                ('partner_id', '=', partner.id)
            ])

            if not existing:
                self.env['training.graduate'].create({
                    'partner_id': partner.id
                })

