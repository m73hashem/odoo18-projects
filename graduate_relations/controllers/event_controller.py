from odoo import http
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController as OriginalWebsiteEventController


class WebsiteEventControllerExtend(OriginalWebsiteEventController):

    @http.route(
        ['/event', '/event/page/<int:page>', '/events', '/events/page/<int:page>'],
        type='http', auth="public", website=True,
        sitemap=OriginalWebsiteEventController.sitemap_event, readonly=True
    )
    def events(self, page=1, **searches):
        
        user = request.env.user
        is_graduate = bool(
            request.env['training.graduate'].sudo().search([('partner_id','=', user.partner_id.id)], limit=1)
        )
       #call original controller
        response = super().events(page=page, **searches)

        # add the new value
        response.qcontext.update({
            'is_graduate': is_graduate,
        })

        return response
