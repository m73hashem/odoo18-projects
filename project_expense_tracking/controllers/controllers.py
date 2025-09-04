# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectExpenseTracking(http.Controller):
#     @http.route('/project_expense_tracking/project_expense_tracking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_expense_tracking/project_expense_tracking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_expense_tracking.listing', {
#             'root': '/project_expense_tracking/project_expense_tracking',
#             'objects': http.request.env['project_expense_tracking.project_expense_tracking'].search([]),
#         })

#     @http.route('/project_expense_tracking/project_expense_tracking/objects/<model("project_expense_tracking.project_expense_tracking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_expense_tracking.object', {
#             'object': obj
#         })

