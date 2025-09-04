from odoo import http
from odoo.http import request


class TestPublicPortalController(http.Controller):

    # صفحة عرض المشاريع
    @http.route('/show/projects', type='http', auth='public', website=True)
    def projects_portal(self, **kwargs):
        projects = request.env['project.project'].sudo().search([('active', '=', True)])
        return request.render('test_portal.test_portal_projects_template', {
            'projects': projects
        })