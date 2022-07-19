/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
const MapModel = require('web_map.MapModel');

patch(MapModel.prototype, "patch_web_map_map_model", {
    __load: function (params) {
        if (this.model !== 'res.partner') {
            arguments[0].fieldNames = arguments[0].fieldNames.filter((val) => val !== 'partner_id');
        }
        return this._super(...arguments);
    },
    _addPartnerToRecord: function () {
        if (this.model === 'res.partner') {
            this._super(...arguments);
        } else {
            this.data.records.map((record, idx) => {
                this.numberOfLocatedRecords++;
                record.partner = this.data.partners[idx];
                return record;
            })
        }
    },
    _fetchRecordsPartner: function (ids) {
        if (this.model === 'res.partner') {
            return this._super(...arguments);
        }
        return this._rpc({
            model: this.model,
            method: 'search_read',
            fields: ['latitude', 'longitude', 'partner_latitude', 'partner_longitude'],
            domain: [['id', 'in', ids]],
        });
    },
    _fillPartnerIds: function (records) {
        if (this.model === 'res.partner') {
            return this._super(...arguments);
        }
        return records.forEach(record => {
            this.partnerIds.push(record.id);
        });
    },
    _writeCoordinatesUsers: function () {
        if (this.partnerToCache.length) {
            this._rpc({
                model: this.model,
                method: 'update_latitude_longitude',
                context: this.context,
                args: [this.partnerToCache]
            });
            this.partnerToCache = [];
        }
    },
    _openStreetMapAPIAsync: function () {
        // Group partners by address to reduce address list
        const addressPartnerMap = new Map();
        for (const partner of this.data.partners) {
            if (!('contact_address_complete' in partner) && 'latitude' in partner && 'longitude' in partner) {
                partner['contact_address_complete'] = `${partner.latitude},${partner.longitude}`;
            }

            if (partner.contact_address_complete && (!partner.partner_latitude || !partner.partner_longitude)) {
                if (!addressPartnerMap.has(partner.contact_address_complete)) {
                    addressPartnerMap.set(partner.contact_address_complete, []);
                }
                addressPartnerMap.get(partner.contact_address_complete).push(partner);
                partner.fetchingCoordinate = true;
            } else if (!this._checkCoordinatesValidity(partner)) {
                partner.partner_latitude = undefined;
                partner.partner_longitude = undefined;
            }
        }

        // `fetchingCoordinates` is used to display the "fetching banner"
        // We need to check if there are coordinates to fetch before reload the
        // view to prevent flickering
        this.data.fetchingCoordinates = addressPartnerMap.size > 0;
        const fetch = async () => {
            const partnersList = Array.from(addressPartnerMap.values());
            for (let i = 0; i < partnersList.length; i++) {
                const partners = partnersList[i];
                try {
                    const coordinates = await this._fetchCoordinatesFromAddressOSM(partners[0]);
                    if (coordinates.length) {
                        for (const partner of partners) {
                            partner.partner_longitude = coordinates[0].lon;
                            partner.partner_latitude = coordinates[0].lat;
                            this.partnerToCache.push(partner);
                        }
                    }
                } finally {
                    for (const partner of partners) {
                        partner.fetchingCoordinate = false;
                    }
                    this.data.fetchingCoordinates = (i < partnersList.length - 1);
                    this._notifyFetchedCoordinate();
                    await new Promise((resolve) => {
                        this.coordinateFetchingTimeoutHandle =
                            setTimeout(resolve, this.COORDINATE_FETCH_DELAY);
                    });
                }
            }
        }
        return fetch();
    },
})
