# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Matrix Quick Order',
    'description': 'Matrix Quick Order',
    'category': 'Website',
    'version': '10.0.1.0.0',
    'author': 'AppJetty',
    'website': 'https://www.appjetty.com',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_web_view.xml',
        'views/template.xml',
    ],
    'support': 'support@appjetty.com',
    'images': ['static/description/splash-screen.png'],
    'application': True,
    'installable': True,
    'price': 39.00,
    'currency': 'EUR',
}
