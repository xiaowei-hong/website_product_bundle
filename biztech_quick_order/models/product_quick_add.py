# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class QuickOrder(models.Model):
    _name = 'quick.order'

    name = fields.Char(string="Quick Order Label",
                       help="Label which will show at website quick order menu", default="Quick Order", translate=True)
    quick_products = fields.Many2many('product.product', string='Products', required=True)
    store_user_id = fields.Integer()
    