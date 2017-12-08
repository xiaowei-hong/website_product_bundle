# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################

import json
import urllib
import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)

TypeSelection = [('roadmap', 'ROADMAP'),
                 ('satellite', 'SATELLITE'),
                 ('hybrid', 'HYBRID'),
                 ('terrain', 'TERRAIN')]


def map_geo_find(addr):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += urllib.quote(addr.encode('utf8'))
    try:
        result = json.load(urllib.urlopen(url))
    except Exception, e:
        raise UserError(
            _('Cannot contact geolocation servers. Please make sure that your internet connection is up and running (%s).') % e)
    if result['status'] != 'OK':
        return None
    # return lat and lng value
    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def map_geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        country = '{1} {0}'.format(*country.split(',', 1))
    addr = tools.ustr(', '.join(filter(None, [street,
                                              ("%s %s" % (zip or '',
                                                          city or '')).strip(),
                                              state,
                                              country])))
    return addr


class WebsiteStoreLocatorSettings(models.Model):
    _name = 'website.store.locator.settings'

    # google map information
    is_active = fields.Boolean(string="Active on website")
    name = fields.Char(string="Name", required=True)
    map_center = fields.Selection([('auto', 'Auto'),
                                   ('manually', 'Manually')
                                   ], string="Map Center", default="auto", required=True)

    manually_option = fields.Selection([('address', 'Address'),
                                        ('coordinate', 'Coordinate')
                                        ], string="Address Option", default='address')

    map_lat = fields.Float(string="Center Latitude")
    map_long = fields.Float(string="Center Longitude")
    street1 = fields.Char(string='Street 1')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='city')
    add_state = fields.Many2one('res.country.state', string="State Name")
    zipcode = fields.Char(string='zip code')
    country = fields.Many2one('res.country', string='Country Name')
    map_zoom = fields.Integer(string="Map Zoom", default=5)
    map_type = fields.Selection(TypeSelection, string="Map Type", default="roadmap")
    search_radius = fields.Integer(string="Search Radius", default=5000)
    google_api_key = fields.Char(string="Google Map API Key")

    @api.onchange('add_state')
    def add_state_change(self):
        self.country = self.add_state.country_id.id if self.add_state else False

    @api.model
    def create_wizard(self):
        wizard_id = self.env['website.message.wizard'].create(
            {'message': "Currently a Configuration Setting for Website Store Locator is active. You can not active other Configuration Setting. So, If you want to deactive the previous active configuration setting and active new configuration then click on 'Deactive Previous And Active New' button else click on 'cancel'."})
        return {
            'name': _("Message"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'website.message.wizard',
            'res_id': int(wizard_id.id),
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new'
        }

    @api.multi
    def toggle_is_active(self):
        """ Inverse the value of the field ``active`` on the records in ``self``. """

        active_ids = self.search([('is_active', '=', True), ('id', 'not in', [self.id])])
        for record in self:
            if active_ids:
                return self.create_wizard()
            record.is_active = not record.is_active
