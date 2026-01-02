from odoo import models, fields

class TrainingGraduateCourses(models.Model):
    _name = "graduate.courses"
    _description = "Unique Graduate Courses"
    _auto = False
    _rec_name = "course_name"

    course_id = fields.Many2one("training.course", string="Course", readonly=True)
    course_name = fields.Char(string="Course Name", readonly=True)
    graduate_count = fields.Integer(string="Graduates Count", readonly=True)

    # create SQL View
    # def init(self):
    #     self.env.cr.execute("""
    #         CREATE OR REPLACE VIEW graduate_course_unique AS (
    #             SELECT
    #                 MIN(rel.id) AS id,
    #                 rel.course_id,
    #                 c.name AS course_name,
    #                 COUNT(rel.graduate_id) AS graduate_count
    #             FROM partner_course_rel rel
    #             JOIN training_course c ON c.id = rel.course_id
    #             GROUP BY rel.course_id, c.name
    #         )
    #     """)
