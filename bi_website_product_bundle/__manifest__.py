# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Website Product Bundle",
    "summary": "Combine two or more products together in order to create a bundle product by website",
    "category": "eCommerce",
    "version": "10.0.0.1",
    "author": "BrowseInfo",
    "description": """
    BrowseInfo developed a new odoo/OpenERP module apps.    
    Purpose :- 
    
Product bundling is offering several products for sale as one combined product. It is a common feature in many imperfectly competitive product markets where price plays important roles, using these module you can act set competitive price for same or different products and variants to increase your sales graph.
        -Point Of sale Product Bundle
        -POS product bundle
        -Point of sale Pack
        -POS product pack
        -Point of sale product pack
        -Custom pack on POS
        -Combined product on POS
        -Product Pack, Custom Combo Product, Bundle Product. Customized product, Group product.Custom product bundle. Custom Product Pack.
         -Pack Price, Bundle price, Bundle Discount, Bundle Offer.
	This module is use to create Product Bundle,Product Pack, Bundle Pack of Product, Combined Product pack.
    -Product Pack, Custom Combo Product, Bundle Product. Customized product, Group product.Custom product bundle. Custom Product Pack.
    -Pack Price, Bundle price, Bundle Discount, Bundle Offer.
    -Website Product Bundle Pack, Website Product Pack, eCommerce Product bundle. All Product bundle feature, All IN one product pack 
    """,
    "depends": ["product_bundle_pack","website_sale"],
    "data": [
        "views/template.xml",
    ],
    "price": 20,
    "currency": "EUR",
    "application": True,
    "installable": True,
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
