# -*- coding: utf-8 -*-
from odoo import models, fields, tools

class GraduateRelation(models.Model):
    _name = 'graduate.relation'
    _description = 'Graduates Relation'
    _auto = False  # SQL View Model

    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    name = fields.Char(related='partner_id.name', store=False, string='Name', readonly=True)
    email = fields.Char(related='partner_id.email', store=False, string='Email', readonly=True)
    phone = fields.Char(related='partner_id.phone', store=False, string='Phone', readonly=True)
    package_id = fields.Many2one(related='partner_id.package_id', string='Training Package', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    rp.id AS id,
                    rp.id AS partner_id
                FROM res_partner rp
                WHERE rp.partner_type = 'trainee'
                GROUP BY rp.id
            )
        """)
