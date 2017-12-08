# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################

from odoo import http
from odoo.http import request


class StoreLocator(http.Controller):

    @http.route(["/store/locator/vals"], type='json', auth="public", website=True)
    def store_locator_vals(self, carrier_value=None):
        sale_store_obj = request.env['sale.shop'].sudo()
        key, sum_lat, sum_lng, store_dict, vals = 0, 0, 0, {}, {}
        if carrier_value:
            carrier_obj = request.env['delivery.carrier'].sudo().browse(int(carrier_value))
            if carrier_obj and carrier_obj.is_store_pickup and carrier_obj.store_ids:
                store_ids = carrier_obj.store_ids
            else:
                store_ids = None
        else:
            store_ids = sale_store_obj.search([('store_active', '=', True)])
        if store_ids:
            for store in store_ids:
                if store.store_lat and store.store_long:
                    store_dict.update(self.get_store_data_dict(store, key))
                    sum_lat = sum_lat + float(store.store_lat)
                    sum_lng = sum_lng + float(store.store_long)
                    key = key + 1
            if key != 0:
                cen_lat, cen_lng, value = sum_lat/key, sum_lng/key, self.get_map_config()
                if not value.get('auto'):
                    cen_lat, cen_lng = value.get('cen_lat'), value.get('cen_lng')
                zoom, map_type = value.get('zoom'), value.get('type')
                vals.update({'map_init_data': {'map_center_lat': cen_lat,
                                               'map_center_lng': cen_lng,
                                               'map_zoom':  int(zoom),
                                               'map_type': str(map_type)
                                               },
                             'map_stores_data': store_dict,
                             'map_search_radius': value.get('search_radius'),
                             })
                return vals
            else:
                return False

    @http.route(["/store/locator"], type='http', auth="public", website=True)
    def store_locator_page(self):
        vals = {}
        return request.render("website_store_locator.store_locator_page", vals)

    def get_locator_config_settings_values(self):
        """ this function retrn all configuration value for website stock locator module."""

        res = {}
        store_locator_config_values = request.env['website.store.locator.settings'].sudo().search([('is_active','=',True)],limit=1)
        if store_locator_config_values:
            res = {
              'map_center' : store_locator_config_values.map_center,
              'manually_option' : store_locator_config_values.manually_option,
              'map_lat' : store_locator_config_values.map_lat,
              'map_long' : store_locator_config_values.map_long,
              'street1' : store_locator_config_values.street1,
              'street2' : store_locator_config_values.street2,
              'city' : store_locator_config_values.city,
              'add_state' : store_locator_config_values.add_state,
              'zipcode' : store_locator_config_values.zipcode,
              'country' : store_locator_config_values.country,
              'map_zoom' :store_locator_config_values.map_zoom,
              'map_type' : store_locator_config_values.map_type,
              'search_radius' : store_locator_config_values.search_radius,
              'google_api_key' : store_locator_config_values.google_api_key,
            }
        return res

    def get_map_config(self):
        vals = {'auto': True, 'zoom': 5, 'type': 'satellite'}
        res = self.get_locator_config_settings_values()
        if res.get('map_center') == 'manually' and res.get('map_lat') and res.get('map_long'):
            vals['auto'] = False
            vals.update({'cen_lat': res.get('map_lat'),
                         'cen_lng': res.get('map_long')})
        if res.get('map_zoom'):
            vals['zoom'] = res.get('map_zoom')
        if res.get('map_type'):
            vals['type'] = res.get('map_type')
        vals['search_radius'] = res.get(
            'search_radius') if res.get('search_radius') else 50
        return vals

    def get_store_data_dict(self, store=None, key=None):
        data = {key: {'store_lat': store.store_lat,
                      'store_lng': store.store_long,
                      'store_name': store.name,
                      'store_image': False if not store.store_image else request.website.image_url(store, 'store_image'),
                      'store_address': [store.street, store.city, store.store_state.name, store.country.name, store.zipcode, store.store_web, store.store_phone, store.store_mob, store.store_fax, store.store_email],
                      'store_id': store.id
                      }
                }
        return data
