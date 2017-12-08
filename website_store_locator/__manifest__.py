# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Website Store Locator",
  "summary"              :  "Store Locator display location of your store in the google map.",
  "category"             :  "Website",
  "version"              :  "1.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Store-Locator.html",
  "description"          :  """""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_store_locator&version=10.0&custom_url=/store/locator",
  "depends"              :  [
                             'sale_shop',
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/sale_shop_inherit_view.xml',
                             'views/res_config_view.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                             'data/store_set_default_values.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}