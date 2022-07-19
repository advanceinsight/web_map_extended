from odoo import _, api, models
from lxml.builder import E
from odoo.exceptions import UserError


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _get_default_map_view(self):
        view = E.map()

        if 'partner_longitude' in self._fields and 'partner_latitude' in self._fields:
            view.set('res_partner', 'partner_id')
        else:
            raise UserError(_("You need to set latitude, longitude, partner_latitude and partner_longitude fields on this model to use the Map View"))

        return view
