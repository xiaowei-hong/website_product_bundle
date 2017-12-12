# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################

from odoo import api, fields, models, _


class WebkulWebsiteAddons(models.TransientModel):
    _inherit = 'webkul.website.addons'

    ##inherit the module for adding config option in webkul_website_addons
    @api.multi
    def get_store_locator_configuration_view(self):
        locator_config_ids = self.env['website.store.locator.settings'].search([])
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('website_store_locator.action_store_locator_settings')
        list_view_id = imd.xmlid_to_res_id('website_store_locator.view_store_locator_settings_tree')
        form_view_id = imd.xmlid_to_res_id('website_store_locator.view_store_locator_settings')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        if len(locator_config_ids) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = locator_config_ids[0].id
        return result
   