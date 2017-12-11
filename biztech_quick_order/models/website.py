# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.http import request


class website(models.Model):
    _inherit = "website"
    _description = "website inherited"

    quick_order = fields.Boolean(string="Do you want to Enable quick order app?")
    title = fields.Char(string="Title", default="Quick Order")
    srt_message = fields.Char(string="Short Message")
    max_item_page = fields.Integer(
        string='Maximum number of product allowd on one page', default=15)
    multi_list = fields.Boolean(string="Do You want to enable multiple list?")

    def get_order(self, **post):
        order_name = self.env['quick.order'].sudo().search(
            [('create_uid', '=', request.website.env.user.id)])
        return order_name

    def biztech_get_product(self, template_id, prouct_id, **post):
        prod = []
        prod_temp_id = template_id
        list_id = prouct_id
        product = self.env['product.product'].sudo().search([('product_tmpl_id', '=', prod_temp_id.id)])
        for id in product:
            if id.id not in list_id:
                prod.append(id.id)
        product_new = self.env['product.product'].sudo().search(
            [('product_tmpl_id', '=', prod_temp_id.id), ('id', 'in', prod)])
        return product_new

    def biztech_edit_product(self, product_ids, **post):
        product = self.env['quick.order'].sudo().search([('id', '=', product_ids)])
        products = product.quick_products
        return products

    def get_variants(self, template_id, **post):
        product = self.env['product.product'].sudo().search([('product_tmpl_id', '=', template_id.id)])
        return product

    def return_title(self, title):
        msg = _('Oops! Your %s list is empty') % title
        return msg



class website_config_settings(models.TransientModel):
    _inherit = "website.config.settings"
    _description = "website.config.settings inherited"

    quick_order = fields.Boolean(
        string="Do you want to Enable quick order app?", related="website_id.quick_order")
    title = fields.Char(string="Title", default="Quick Order", related="website_id.title")
    srt_message = fields.Char(string="Short Message", related="website_id.srt_message")
    max_item_page = fields.Integer(
        string='Maximum number of product allowd on one page', default=15, related="website_id.max_item_page")
    multi_list = fields.Boolean(
        string="Do You want to enable multiple list?", related="website_id.multi_list")
