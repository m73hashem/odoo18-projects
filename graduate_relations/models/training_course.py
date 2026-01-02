from odoo import models, fields, api


class TrainingCourse(models.Model):
    _name = "training.courses"
    _description = "Training Course"


    name = fields.Char(string="Course Name", required=True)
    description = fields.Text(string="Description")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    participant_ids = fields.One2many(
        'training.course.participant',
        'course_id',
        string="Participants"
    )

    trainer_count = fields.Integer(
        string="Trainers",
        compute="_compute_counts",
        store=False
    )

    trainee_count = fields.Integer(
        string="Trainees",
        compute="_compute_counts",
        store=False
    )

    @api.depends('participant_ids.role')
    def _compute_counts(self):
        for course in self:
            course.trainer_count = sum(1 for p in course.participant_ids if p.role == 'trainer')
            course.trainee_count = sum(1 for p in course.participant_ids if p.role == 'trainee')


#############
from odoo import models, fields, api


class TrainingCourseParticipant(models.Model):
    _name = "training.course.participant"
    _description = "Training Course Participant"
    _rec_name = "partner_id"
    _order = "role, partner_id"

    partner_id = fields.Many2one(
        'res.partner',
        string="Participant",
        required=True,
        ondelete='cascade'
    )

    course_id = fields.Many2one(
        'training.courses',
        string="Course",
        required=True,
        ondelete='cascade'
    )

    role = fields.Selection([
        ('trainer', 'Trainer'),
        ('trainee', 'Trainee'),
    ], string="Role", required=True)

    email = fields.Char(related='partner_id.email', string="Email", readonly=True)
    phone = fields.Char(related='partner_id.phone', string="Phone", readonly=True)

    _sql_constraints = [
        ('unique_course_partner', 'unique(course_id, partner_id)', 'This participant is already added to the course!')
    ]

