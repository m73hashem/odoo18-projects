from odoo import http, _
from odoo.http import request
import base64
import logging

_logger = logging.getLogger(__name__)

class GraduateCVPortal(http.Controller):

    @http.route(['/my/cv'], type='http', auth='user', website=True)
    def portal_view_cv(self, **kwargs):
        user = request.env.user
        partner = user.partner_id
        if not partner:
            return request.render('graduate_relations.portal_no_graduate', {})
        graduate = request.env['training.graduate'].sudo().search([('partner_id', '=', partner.id)], limit=1)
        if not graduate:
            return request.render('graduate_relations.portal_no_graduate', {})
        cv = request.env['graduate.cv'].sudo().search([('graduate_id', '=', graduate.id)], limit=1)
        if not cv:
            cv = request.env['graduate.cv'].sudo().create({'graduate_id': graduate.id})
        return request.render('graduate_relations.portal_graduate_cv_view', {
            'graduate': graduate,
            'cv': cv,
        })

    @http.route(['/my/cv/submit'], type='http', auth='user', methods=['POST'], csrf=True, website=True)
    def portal_submit_cv(self, **post):

        try:
            graduate_id = post.get('graduate_id')
            if not graduate_id:
                return request.redirect('/my/cv')
            graduate = request.env['training.graduate'].sudo().browse(int(graduate_id))
            if not graduate.exists():
                return request.redirect('/my/cv')

            cv = request.env['graduate.cv'].sudo().search([('graduate_id', '=', graduate.id)], limit=1)
            if not cv:
                cv = request.env['graduate.cv'].sudo().create({'graduate_id': graduate.id})

            # ========== Education==========
            education = post.get('education')
            if education is not None:
                cv.sudo().write({'education': education})

            # =========Experience  ==========
            experiences = request.httprequest.form.getlist('experience_ids[]')
            cv.experience_ids.sudo().unlink()  # remove old value
            for exp_name in experiences:
                if exp_name.strip():
                    request.env['graduate.experience'].sudo().create({
                        'graduate_cv_id': cv.id,
                        'exp_name': exp_name.strip(),
                    })

            # =========Language  ==========
            languages = request.httprequest.form.getlist('language_ids[]')
            cv.language_ids.sudo().unlink()
            for lang in languages:
                if lang.strip():
                    request.env['graduate.user.language'].sudo().create({
                        'graduate_cv_id': cv.id,
                        'name': lang.strip(),
                    })

            # ==========Skills  ==========
            skills = request.httprequest.form.getlist('skill_ids[]')
            cv.skill_ids.sudo().unlink()
            for skill in skills:
                if skill.strip():
                    request.env['graduate.skill'].sudo().create({
                        'graduate_cv_id': cv.id,
                        'name': skill.strip(),
                    })

            # =====  (Many2many unlink attachments from CV) =====
            removed_ids = post.get('removed_attachments', '')
            if removed_ids:
                ids = [int(i) for i in removed_ids.split(',') if i.strip().isdigit()]
                if ids:
                    cv.sudo().write({'attachment_ids': [(3, att_id) for att_id in ids]})

            # =====upload new attachments=====
            uploaded_files = request.httprequest.files.getlist('cv_files')
            if uploaded_files:
                for f in uploaded_files:
                    if not f or not getattr(f, 'filename', None):
                        continue
                    data = f.read()
                    if not data:
                        continue

                    b64data = base64.b64encode(data).decode('utf-8')
                    attachment = request.env['ir.attachment'].sudo().create({
                        'name': f.filename,
                        'datas': b64data,
                        'res_model': 'graduate.cv',
                        'res_id': cv.id,
                        'mimetype': getattr(f, 'content_type', 'application/octet-stream'),
                        'type': 'binary',
                    })

                    cv.sudo().write({'attachment_ids': [(4, attachment.id)]})

            # إredirect to cv page
            return request.redirect('/my/cv')

        except Exception as e:
            _logger.exception("Error saving CV attachments")
            user = request.env.user
            partner = user.partner_id
            graduate = request.env['training.graduate'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            cv = None
            if graduate:
                cv = request.env['graduate.cv'].sudo().search([('graduate_id', '=', graduate.id)], limit=1)
            return request.render('graduate_relations.portal_graduate_cv_view', {
                'graduate': graduate,
                'cv': cv,
                'error': str(e),
            })

    ##==========================
    ##move to a new controller
    #============================
    @http.route(['/my/main'], type='http', auth='user', website=True)
    def portal_my_main(self, **kwargs):
        user = request.env.user
        if not user.has_group('base.group_portal'):
            return request.redirect('/my')

        graduate = request.env['training.graduate'].sudo().search(
            [('partner_id', '=', user.partner_id.id)], limit=1
        )

        if not graduate:
            return request.render('graduate_relations.portal_no_graduate', {})

        values = {
            'graduate': graduate,
            'page_name': 'my_graduate_main',
        }
        return request.render('graduate_relations.portal_my_graduate_main', values)
        
   
    #courses
    @http.route(['/my/trainings'], type='http', auth='user', website=True)
    def portal_my_trainings(self, **kwargs):
        user = request.env.user
        if not user.has_group('base.group_portal'):
            return request.redirect('/my')

        graduate = request.env['training.graduate'].sudo().search(
            [('partner_id', '=', user.partner_id.id)], limit=1
        )

        if not graduate:
            return request.render('graduate_relations.portal_no_graduate', {})

        values = {
            'graduate': graduate,
            'course_names': graduate.course_ids.mapped('name'),  #course name only
            'page_name': 'my_trainings',
        }
        return request.render('graduate_relations.portal_my_trainings', values)
