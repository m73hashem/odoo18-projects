from odoo import http
from odoo.http import request

class ActionDemoController(http.Controller):
    @http.route('/action_demo/client_dashboard', type='http', auth='user')
    def client_dashboard(self, **kw):
        return request.render("action_demo_lab.client_action_template", {})
