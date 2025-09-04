from odoo import http
from odoo.http import request

class PublicProjectPortal(http.Controller):

    @http.route('/list/projects', type='http', auth='public', website=True)
    def public_projects(self, **kwargs):
        # جلب المشاريع النشطة فقط
        projects = request.env['project.project'].sudo().search([('active', '=', True)])
        return request.render('project_expenses.public_projects_list', {
            'projects': projects
        })
