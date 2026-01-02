from odoo import models, fields, api


class GraduateCV(models.Model):
    _name = "graduate.cv"
    _description = "Graduate CV"

    graduate_id = fields.Many2one(
        'training.graduate',
        string='Graduate',
        ondelete='cascade',
        required=True
    )

    name = fields.Char(
        string="Name",
        related="graduate_id.partner_id.name",
        store=True,
        readonly=True
    )

    education = fields.Text(string="Education")

    # العلاقات
    experience_ids = fields.One2many(
        'graduate.experience',
        'graduate_cv_id',
        string="Experiences")

    skill_ids = fields.One2many(
        'graduate.skill',
        'graduate_cv_id',
        string="Skills")



    language_ids = fields.One2many(
        'graduate.user.language',
        'graduate_cv_id',
        string="Languages")

    attachment_ids = fields.Many2many(
        'ir.attachment',
        'graduate_cv_attachment_rel',
        'cv_id', 'attachment_id',
        string='Attachments'
    )

    _sql_constraints = [
        ('unique_graduate_id', 'unique(graduate_id)', 'Each graduate can have only one CV.')
    ]




# -------------------------------
#   جدول الخبرات (Experiences)
# -------------------------------
class GraduateExperience(models.Model):
    _name = "graduate.experience"
    _description = "Graduate Experience"

    graduate_cv_id = fields.Many2one(
        'graduate.cv',
        string="Graduate CV",
        ondelete='cascade'
    )
    exp_name = fields.Char(string="Company Name")


# -------------------------------
#   جدول المهارات (Skills)
# -------------------------------
class GraduateSkill(models.Model):
    _name = "graduate.skill"
    _description = "Graduate Skill"

    graduate_cv_id = fields.Many2one(
        'graduate.cv',
        string="Graduate CV",
        ondelete='cascade'
    )
    name = fields.Char(string="Skill")


# -------------------------------
#   جدول اللغات (Languages)
# -------------------------------
class GraduateUserLanguage(models.Model):
    _name = "graduate.user.language"
    _description = "Graduate Language"

    graduate_cv_id = fields.Many2one(
        'graduate.cv',
        string="Graduate CV",
        ondelete='cascade'
    )
    name = fields.Char(string="Language")
