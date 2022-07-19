# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api


class Cat(models.Model):
    _name = 'web_map_extended.cat'
    _description = "Cats!"

    name = fields.Char(required=True)
    color = fields.Selection([
        ('red', 'red'),
        ('green', 'green'),
        ('blue', 'blue'),
    ], required=True, default='green')

    display_name = fields.Char(compute='_compute_display_name')

    latitude = fields.Float('Geo Latitude', digits=(10, 7), default=51.762451)
    longitude = fields.Float('Geo Longitude', digits=(10, 7), default=5.526943)

    @api.depends('latitude', 'longitude')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'This {record.color} cat called {record.name} is at {record.latitude}, {record.longitude}!'

    partner_latitude = fields.Float(string='internal latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='internal longitude', digits=(10, 7))

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
