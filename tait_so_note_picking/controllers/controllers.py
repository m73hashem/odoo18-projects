# -*- coding: utf-8 -*-
# from odoo import http


# class Mytask(http.Controller):
#     @http.route('/tait_so_note_picking/tait_so_note_picking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tait_so_note_picking/tait_so_note_picking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tait_so_note_picking.listing', {
#             'root': '/tait_so_note_picking/tait_so_note_picking',
#             'objects': http.request.env['tait_so_note_picking.tait_so_note_picking'].search([]),
#         })

#     @http.route('/tait_so_note_picking/tait_so_note_picking/objects/<model("tait_so_note_picking.tait_so_note_picking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tait_so_note_picking.object', {
#             'object': obj
#         })

