from odoo import http
from odoo.http import request

class PublicProjects(http.Controller):

    @http.route('/show/projects', type='http', auth='public', website=True)
    def public_projects(self, **kwargs):

        projects = request.env['project.project'].sudo().search([('active', '=', True)])
        return request.render('public_projects_portal.template_public_projects', {
            'projects': projects
        })
