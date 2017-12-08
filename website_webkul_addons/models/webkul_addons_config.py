# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _
from odoo.exceptions import Warning

class WebkulWebsiteAddons(models.TransientModel):
    _name = 'webkul.website.addons'
    _inherit = 'res.config.settings'

    # Social Network
    module_website_facebook_wallfeed = fields.Boolean(string="Website Facebook Wall Feed")

    # Product Management
    module_website_product_pack = fields.Boolean(string = "Website: Product Pack")
    module_website_multi_image = fields.Boolean(string = "Website: Multi Images")
    module_website_giftwrap = fields.Boolean(string = "Website: Gift Wrap")
    module_website_seo =  fields.Boolean(string = "Website: SEO")


    #Delivery Method
    module_website_store_pickup = fields.Boolean(string="Website: Store Pickup")

    # Stock Management
    module_website_stock = fields.Boolean(string = "Website: Product Stock")
    module_website_stock_notifiy = fields.Boolean(string = "Website: Stock Notify")
    module_website_hide_out_of_stock = fields.Boolean(string="Website : Hide out of stock products")

    # Product Web page
    module_website_product_quickview = fields.Boolean(string = "Website: Product Quickview")
    module_website_product_faq = fields.Boolean(string = "Frequently Asked Questions (FAQ) on Website's product")
    module_website_360degree_view = fields.Boolean(string="Website: Product 360° View")
    module_website_recently_viewed_products = fields.Boolean(string="Website: Recently Viewed Products")
    module_website_store_locator = fields.Boolean(string="Website: Store Locator")
    module_website_product_tags = fields.Boolean(string="Website: Product Tags")
    module_website_product_price_range = fields.Boolean(
                string="Website: Product  Price Range"
    )
    module_hidden_products = fields.Boolean(
        string = "Website: Hidden Product"
    )

    module_products_az_list = fields.Boolean(
        string = "Website: Product A-Z List"
    )
    module_products_az_filter = fields.Boolean(
        string = "Website: Product A-Z Filter"
    )

    # web Page
    module_advance_website_settings = fields.Boolean(string = "Website: Cart Settings")
    module_website_onepage_checkout = fields.Boolean(string = "Website: Onepage Checkout")
    module_website_country_restriction = fields.Boolean(string = "Website: Country Restriction")
    module_website_order_notes = fields.Boolean(string = "Website: Internal Notes on Order")
    module_website_wishlist = fields.Boolean(string = "Website: Product Wishlist")
    module_website_product_compare = fields.Boolean(string = "Website: Product Compare")
    module_website_estimated_delivery = fields.Boolean(string = "Website Estimated Delivery")
    module_website_daily_deals = fields.Boolean(string = "Website Daily Deals")
    module_website_cart_recovery = fields.Boolean(string = "Website: Abandoned Cart Recovery")
    module_website_cart_settings = fields.Boolean(string = "Website Cart Settings")
    module_email_verification = fields.Boolean(string = "Email Verification")

    # Sales Promotion
    module_website_product_vote = fields.Boolean(string = "Website: Product Vote")
    module_website_sales_count = fields.Boolean(string = "Website: Sales Count")
    module_wk_review = fields.Boolean(string="Website: Product Review")
    module_website_terms_conditions = fields.Boolean(string = "Website: Terms and Conditions")
    module_website_first_order_discount = fields.Boolean(string="Website: First Purchase Discount")
    module_website_newsletter = fields.Boolean(string="Website Newsletter")
    module_social_network_tabs = fields.Boolean(string="Social Network Tabs")
    module_dynamic_bundle_products = fields.Boolean(string = "Dynamic Bundle Products")
