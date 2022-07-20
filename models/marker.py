# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api


class Marker(models.Model):
    _name = 'web_map_extended.marker'
    _description = "Enables map view for non-res.partner models"

    latitude = fields.Float('Latitude', digits=(10, 7), default=0.0)
    longitude = fields.Float('Longitude', digits=(10, 7), default=0.0)

    # @api.depends('latitude', 'longitude')
    # def _compute_display_name(self):
    #     for record in self:
    #         record.display_name = 'some text''

    partner_latitude = fields.Float(string='Internal latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Internal longitude', digits=(10, 7))

    @api.onchange('latitude', 'longitude')
    def _delete_coordinates(self):
        self.write({
            'partner_latitude': 0.0,
            'partner_longitude': 0.0,
        })

    @api.model
    def update_latitude_longitude(self, partners):
        """
        This method receives location data after the map updates a coordinate.
        Direct copy-paste from res.partner.update_latitude_longitude() for ease of use
        """
        partners_data = defaultdict(list)

        for partner in partners:
            if 'id' in partner and 'partner_latitude' in partner and 'partner_longitude' in partner:
                partners_data[(partner['partner_latitude'], partner['partner_longitude'])].append(partner['id'])

        for values, partner_ids in partners_data.items():
            # NOTE this should be done in sudo to avoid crashing as soon as the view is used
            self.browse(partner_ids).sudo().write({
                'partner_latitude': values[0],
                'partner_longitude': values[1],
            })

        return {}

    @api.model_create_multi
    def create(self, vals_list):
        """ On create copy lat/long to partner_lat/long"""
        for vals in vals_list:
            if 'latitude' in vals:
               vals['partner_latitude'] = vals['latitude']
            if 'longitude' in vals:
                vals['partner_longitude'] = vals['longitude']
        return super(Marker, self).create(vals_list)
