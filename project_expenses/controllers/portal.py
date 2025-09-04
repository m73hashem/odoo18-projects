from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class ProjectExpensesPortal(http.Controller):

    @http.route(['/project_expenses/portal/new'], type='http', auth='user', website=True)
    def portal_new_expense(self, **kwargs):
        projects = request.env['project.project'].sudo().search([('active', '=', True)])
        return request.render('project_expenses.portal_expense_form', {'projects': projects, 'error': kwargs.get('error')})

    @http.route(['/project_expenses/portal/submit'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def portal_submit_expense(self, **post):
        # التحقق من المدخلات
        project_id = post.get('project_id')
        expense_type_id = post.get('expense_type')
        amount_str = post.get('amount')

        if not project_id or not expense_type_id or not amount_str:
            return request.redirect('/project_expenses/portal/new?error=Please+fill+all+fields')

        try:
            amount = float(amount_str)
        except ValueError:
            return request.redirect('/project_expenses/portal/new?error=Invalid+amount')

        if amount <= 0:
            return request.redirect('/project_expenses/portal/new?error=Amount+must+be+greater+than+0')

        project = request.env['project.project'].sudo().browse(int(project_id))
        if not project or project.user_id.id != request.env.user.id:
            return request.redirect('/project_expenses/portal/new?error=You+are+not+the+project+manager')

        # إنشاء طلب المصروف
        req = request.env['project.expense.request'].sudo().create({
            'project_id': int(project_id),
            'project_manager_id': request.env.user.id,
        })

        # إضافة السطر
        request.env['project.expense.request.line'].sudo().create({
            'request_id': req.id,
            'expense_type_id': int(expense_type_id),
            'amount': amount,
        })

        return request.redirect('/web')
