# -*- coding: utf-8 -*-
{
    'name': "web_map_extended",
    'summary': """Allow using maps with other model types than res.partner""",
    'description': """""",
    'author': "Advance Insight",
    'website': "https://advanceinsight.dev",
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'version': '0.1.5',
    'depends': [
        'base',
        'contacts',
        'web_map'
    ],
    'data': [
        'security/ir.model.access.csv'
    ],
    # 'demo': [
    #     'views/views.xml',
    #     'views/menu.xml',
    # ],
    'assets': {
        'web.assets_backend': [
            'web_map_extended/static/src/js/map_view_extended.js',
        ],
    },
}
