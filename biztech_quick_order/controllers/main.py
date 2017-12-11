# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

import ast
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID, _
from odoo.addons.website.models.website import slug



class QuickOrderController(http.Controller):

    def compute_price(self, variant_id):
        price_list = request.website.get_current_pricelist()
        variant = variant_id
        price = price_list.price_rule_get(variant, 1).values()[0][0]
        return round(price, 2)

    """This Controller will use to manage multiple list when admin has selected multiple list option"""
    @http.route(['/managelist', ], type='http', auth='public', website=True)
    def managelist(self, **post):

        if request.website.env.user:
            value = {}
            domain = [('create_uid', '=', request.website.env.user.id)]
            products = request.env['quick.order'].search(domain)
            value['products'] = products
            if post and post.get('error'):
                value['error_name'] = _("Sorry! This list name is already exists")
                del post['error']
            return request.render("biztech_quick_order.manage_list_biztech", value)
        else:
            return request.render("website.404")

    """This controller will use to show  the selected list to user"""
    @http.route(['/quickorder/<model("quick.order"):lists>',
                 '/quickorder/<model("quick.order"):lists>/page/<int:page>', ],
                type='http', auth='public', website=True)
    def quickorder(self, lists, page=0, search=None, **post):
        if request.website.env.user and lists.create_uid.id == request.website.env.user.id:
            url = "/quickorder/%s" % slug(lists)
            ppg = request.website.max_item_page
            temp_id = []
            temp_product_id = []
            domain = []
            """quick order search"""
            if lists.quick_products or not lists.quick_products:
                products = lists.quick_products
                for temp in products:
                    temp_product_id.append(temp.id)
                products_br = request.env['product.product'].search(
                    [('id', 'in', temp_product_id)])
                for products in products_br:
                    temp_id.append(products.product_tmpl_id.id)
                domain = request.website.sale_product_domain()
                domain += [('id', 'in', temp_id)]
                if search:
                    domain += [('name', 'ilike', search), ]
                product_count = request.env[
                    'product.template'].search_count(domain)
                pager = request.website.pager(
                    url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
                product_temp_products = request.env['product.template'].search(
                    domain, limit=ppg, offset=pager['offset'], order='website_published desc, website_sequence desc')

                values = {'product': product_temp_products, 'listname': lists.name, 'listid': lists.id, 'product_ids': temp_product_id,
                          'product_count': product_count, 'pager': pager, 'list_obj': lists, 'search_obj': search, 'compute_price': self.compute_price}
                return request.render("biztech_quick_order.quick_products_biztech", values)
            else:
                return request.render("website.404")

        else:
            return request.render("website.404")

    """This controller will use to delete  the selected list by user"""
    @http.route(['/customdelete', ], type='http', auth='public', website=True)
    def editquickorder(self, **post):
        if request.website.env.user:
            if post.get('id'):
                if post['id']:
                    delete_id = int(post['id'])
                    del post['id']
                    products = request.env['quick.order'].search([('id', '=', delete_id)])
                    if products and products.create_uid.id == request.website.env.user.id:
                        status = products = request.env['quick.order'].search(
                            [('id', '=', delete_id)]).unlink()
                        if status:
                            return request.redirect('/managelist')
                        else:
                            return "yes"
                    else:
                        return request.render("website.404")
        else:
            return request.render("website.404")

    """This controller will use to add and delete mutiple record from list"""
    @http.route(['/delete/item', ], type="json", auth="public", website="true")
    def delete_item(self, **post):
        list_product = []
        delete_status = ''
        editstatus = ''
        add_all_status = ''
        delete_all_status = ''
        cust_edit_status = ''
        if post:
            removeitem = post['deletelist'] if post.get('deletelist') else ''
            edit_items = post['edit_prod'] if post.get('edit_prod') else ''
            addall = post['add_all'] if post.get('add_all') else ''
            deleteall = post['delete_all'] if post.get('delete_all') else ''
            cust_edit = post['edit_custom'] if post.get('edit_custom') else ''
            listid = post['listid']
            products = request.env['quick.order'].search([('id', '=', int(listid))])
            for prodlist_id in products.quick_products:
                list_product.append(prodlist_id.id)
            if products and products.create_uid.id == request.website.env.user.id:
                if removeitem:
                    for item_del in removeitem:
                        val_del = {'quick_products': [(3, int(item_del))]}
                        delete_status = products.write(val_del)
                if edit_items:
                    for item in edit_items:
                        val_edit = {'quick_products': [(4, int(item))]}
                        editstatus = products.write(val_edit)
                if addall:
                    for prod in addall:
                        product_products = request.env[
                            'product.template'].search([('id', '=', int(prod))])
                        for variant in product_products.product_variant_ids:
                            val_addall = {'quick_products': [(4, variant.id)]}
                            add_all_status = products.write(val_addall)
                if deleteall:
                    for prod in deleteall:
                        product_products = request.env[
                            'product.template'].search([('id', '=', int(prod))])
                        for variant in product_products.product_variant_ids:
                            val_addall = {'quick_products': [(3, variant.id)]}
                            delete_all_status = products.write(val_addall)
                if cust_edit:
                    for prod in cust_edit:
                        product = request.env['product.product'].search([('id', '=', int(prod))])
                        product_products = request.env['product.template'].search(
                            [('id', '=', int(product.product_tmpl_id))])
                        for variant in product_products.product_variant_ids:
                            val_cust_add = {'quick_products': [(4, variant.id)]}
                            cust_edit_status = products.write(val_cust_add)

            if delete_status or editstatus or add_all_status or delete_all_status:
                return False
        else:
            return request.render("website.404")

    """This controller will use to show edit template to user"""
    @http.route(['/editlist/<model("quick.order"):lists>',
                 '/editlist/<model("quick.order"):lists>/page/<int:page>', ], type="http", auth="public", website="true")
    def edit_list(self, lists, page=0, search=None, **post):
        user_id = request.website.env.user
        if user_id and lists.create_uid.id == user_id.id:
            url = "/editlist/%s" % slug(lists)
            ppg = request.website.max_item_page
            temp_id = []
            template_id = []
            value = {}
            if lists.quick_products or not lists.quick_products:
                if lists.quick_products:
                    products = lists.quick_products
                    for temp in products:
                        temp_id.append(temp.id)
                    domain = [('id', 'not in', temp_id)]
                else:
                    domain = []
                products_br = request.env['product.product'].search(domain)
                for products in products_br:
                    template_id.append(products.product_tmpl_id.id)
                domain = request.website.sale_product_domain()
                if search:
                    domain += [('name', 'ilike', search), ]
                if user_id.id != SUPERUSER_ID:
                    domain += [('website_published', '=', True)]
                domain += [('id', 'in', template_id)]
                product_count = request.env[
                    'product.template'].search_count(domain)
                pager = request.website.pager(
                    url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
                product_temp_products = request.env['product.template'].search(
                    domain, limit=ppg, offset=pager['offset'], order='website_published desc, website_sequence desc')
                value['products'] = product_temp_products
                value['listid'] = lists.id
                value['temp'] = temp_id
                value['list_obj'] = lists
                value['search_obj'] = search
                value['edit_list_name'] = lists.name
                value['product_count'] = product_count
                value['pager'] = pager
                value['compute_price'] = self.compute_price
                return request.render("biztech_quick_order.edit_products_biztech", value)
            else:
                return request.render("website.404")
        else:
            return request.render("website.404")

    @http.route(['/createlist'], type="http", auth="public", website=True)
    def create_list(self, **post):
        if request.website.env.user:
            user_id = request.website.env.user
            if post and post.get('create_name'):
                createname = post['create_name']
                product = request.env['quick.order'].search([
                    ('name', '=', createname), 
                    ('store_user_id', '=', user_id.id)])
                if product:
                    return request.redirect('/managelist?error=sry')
                else:
                    val = {'name': createname, 
                           'store_user_id': user_id}
                    order_id = request.env['quick.order'].create(val)
                    if order_id:
                        del post['create_name']
                        del val
                        return request.redirect('/managelist')
        else:
            return request.render("website.404")

    @http.route(['/custom/add'], type="json", auth="public", website=True)
    def add_to_cart(self, **post):
        order = []
        if post and post.get('add_cart'):
            cart_list = post['add_cart']
            list_cart = ast.literal_eval(cart_list['product_list'])
            for item in list_cart:
                if int(list_cart[item]) >= 1:
                    sale_order_id = request.website.sale_get_order(force_create=1)._cart_update(
                        product_id=int(item), add_qty=float(list_cart[item]))
                    order.append(sale_order_id)
            if order:
                return True

    @http.route(['/quickorder/price_calculate'], type="json", auth="public", website=True)
    def price_count(self, **post):
        if post and post.get('price_count_id') and post.get('prodcount'):
            prod_id_count = int(post['price_count_id'])
            prod_qunat = int(post['prodcount'])
            product = request.env['product.product'].search([('id', '=', prod_id_count)])
            return_price = self.compute_price(product.id) * prod_qunat
            return return_price

    @http.route(['/user/login/validation'], type="json", auth="public", website=True)
    def user_login_validation(self, **post):
        if request.website.env.user:
            return "True"
        else:
            return "False"
