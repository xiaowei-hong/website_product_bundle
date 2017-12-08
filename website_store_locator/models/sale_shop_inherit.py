# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################

import json
import urllib

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


def map_geo_find(addr):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += urllib.quote(addr.encode('utf8'))
    try:
        result = json.load(urllib.urlopen(url))
    except Exception, e:
        raise UserError( _('Cannot contact geolocation servers. Please make sure that your internet connection is up and running (%s).') % e)
    if result['status'] != 'OK':
        return None
    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def map_geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        country = '{1} {0}'.format(*country.split(',', 1))

    addr = tools.ustr(', '.join(filter(None, [street,("%s %s" % (zip or '', city or '')).strip(), state, country])))
    return addr


class SaleShop(models.Model):
    _inherit = 'sale.shop'

    store_image = fields.Binary(string="Store Image")
    # adress information
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    store_state = fields.Many2one('res.country.state', string="State Name")
    zipcode = fields.Char(string='Zip-Code')
    country = fields.Many2one('res.country', string='Country Name')
    store_web = fields.Char(string='Website')
    store_phone = fields.Char(string='Phone Number')
    store_mob = fields.Char(string='Mobile Number ')
    store_fax = fields.Char(string='Fax Number')
    store_email = fields.Char(string='Email Address')
    coordinates_calc = fields.Selection([('by_addr', 'By Address'),
                                         ('manual', 'Manually')
                                         ], string="Store Co-ordinates", default="by_addr")
    store_lat = fields.Char(string="Store Latitude")
    store_long = fields.Char(string="Store Longitude")
    store_active = fields.Boolean(string="Visible on Website")

    @api.multi
    def toggle_store_show_hide(self):
        self.store_active = not self.store_active

    def on_address_change(self):
        values = {}
        result = map_geo_find(map_geo_query_address(street=self.street,
                                                    zip=self.zipcode,
                                                    city=self.city,
                                                    state=self.store_state.name,
                                                    country=self.country.name))
        if result:
            values['store_lat'] = str(result[0])
            values['store_long'] = str(result[1])
        return values

    @api.model
    def create(self, vals):
        res = super(SaleShop, self).create(vals)
        if res.coordinates_calc == 'by_addr':
            result = res.on_address_change()
            res.write({'store_lat': result.get('store_lat'),
                       'store_long': result.get('store_long')})
        return res

    @api.multi
    def write(self, vals):
        param = ('street', 'zipcode', 'city', 'store_state', 'country')
        for rec in self:
            res = super(SaleShop, rec).write(vals)
            if (vals.get('coordinates_calc') == 'by_addr') or (rec.coordinates_calc == 'by_addr' and any(key in vals for key in param)):
                result = rec.on_address_change()
                rec.write({'store_lat': result.get('store_lat'),
                           'store_long': result.get('store_long')})
            return res

    @api.onchange('store_state')
    def add_state_change(self):
        self.country = self.store_state.country_id.id if self.store_state else False


class Website(models.Model):
    _inherit = 'website'

    @api.model
    def get_map_api_url(self):
        map_api_url = '//maps.googleapis.com/maps/api/js?libraries=places'
        locator_config = self.env['website.store.locator.settings']
        config_obj = locator_config.sudo().search([('is_active','=',True)],limit=1)
        google_api_key = config_obj.google_api_key
        if google_api_key:
            map_api_url = '//maps.googleapis.com/maps/api/js?libraries=places&key=' + str(google_api_key)
        return map_api_url
