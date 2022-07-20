<img align="left" src="/static/description/icon.png" width=100 height=100/>

# web_map_extended
<br clear="left"/>
This module, made by [Advance Insight](https://www.advanceinsight.dev/), allows you to use the map view in Odoo Enterprise with other models besides the standard contacts and companies (the `res.partner` model).


----

### License
This module is available under the MIT license. For more details, see the `license.md` file that came with this module. While not mandatory, we highly encourage you to share with the community any improvements you might make to this module.

----

### How it works:
By default the map view can only be used with the `res.partner` model. This module alters the setup of the map view to allow other data sources, while keeping the view backwards compatible with the default behaviour.


## How to use in your model
After installing the module, all you have to do in your target model is to inherit `web_map_extended.marker`:

```
class MyModel(models.Model):
    _name = 'my_module.my_model'
    _inherit = 'web_map_extended.marker'
```
Then, in your view record, add the `map` option:
```
    <record model="ir.actions.act_window" id="my_action_window">
      <field name="res_model">my_module.my_model</field>
      <field name="view_mode">tree,form,map</field>
    </record>
```

## Setting the location
### Option 1: using coordinates
By inheriting `web_map_extended.marker` your model gets access to a `latitude` and `longitude` field.
To access these add them to your `form` or `list` view using `<field name="latitude"/>` and `<field name="longitude" />`. Set these to a valid geo coordinate to show the record on the map.

### Option 2: using an address
You can add an address to your record by adding a field called `contact_address_complete` to your model (this name is used to stay compatible with the old `web_map` behaviour).

The address stored in the field will be resolved to a geo coordinate using OpenStreetMap, or any of the other map providers available. The following code snippet is an example of how the `res.partner` model defines and populates its `contact_address_complete` field:

```
    contact_address_complete = fields.Char(compute='_compute_complete_address', store=True)

    @api.depends('street', 'zip', 'city', 'country_id')
    def _compute_complete_address(self):
        for record in self:
            record.contact_address_complete = ''
            if record.street:
                record.contact_address_complete += record.street + ', '
            if record.zip:
                record.contact_address_complete += record.zip + ' '
            if record.city:
                record.contact_address_complete += record.city + ', '
            if record.state_id:
                record.contact_address_complete += record.state_id.name + ', '
            if record.country_id:
                record.contact_address_complete += record.country_id.name
            record.contact_address_complete = record.contact_address_complete.strip().strip(',')
```
