from odoo import http
from odoo.http import request

class PartnerPortal(http.Controller):

    @http.route(['/my/partner'], type='http', auth='user', website=True)
    def portal_my_partner(self, **kwargs):
        partner = request.env['custom.partner'].sudo().search([('responsible_user_id', '=', request.env.user.id)], limit=1)
        return request.render('partners_management.portal_my_partner_page', {
            'partner': partner,
        })

    #partner_description
    @http.route(['/my/partner/update'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def portal_update_partner(self, **post):
        partner = request.env['custom.partner'].sudo().search([('responsible_user_id', '=', request.env.user.id)],limit=1)
        if partner and post.get('partner_description'):
            if partner.allow_portal_edit and partner.responsible_user_id.id == request.env.user.id:
                partner.sudo().write({'partner_description': post.get('partner_description')})
        return request.redirect('/my/partner')

    # to upload attachments
    @http.route(['/my/partner/upload_attachments'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def portal_upload_partner_attachments(self, **post):
        partner = request.env['custom.partner'].sudo().search([('responsible_user_id', '=', request.env.user.id)], limit=1)
        if partner and post.get('ufile'):
            files = request.httprequest.files.getlist('ufile')
            for ufile in files:
                data = ufile.read()
                request.env['ir.attachment'].sudo().create({
                    'name': ufile.filename,
                    'res_model': 'custom.partner',
                    'res_id': partner.id,
                    'datas': data.encode('base64') if hasattr(data, 'encode') else data,
                    'mimetype': ufile.content_type,
                })
        return request.redirect('/my/partner')
