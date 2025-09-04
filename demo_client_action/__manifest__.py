# -*- coding: utf-8 -*-
{
    'name': "Demo Client Action",
    'version': '1.0',
    'category': 'Tools',
    'summary': "Example module to demonstrate client action in Odoo 18",
    'description': """
This module demonstrates how to create a custom client action in Odoo 18.
    """,
    'author': "Your Name",
    'depends': ['web'],
    'data': [
        'views/client_action_demo_views.xml',
        #'views/client_action_demo_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'demo_client_action/static/src/js/client_action_demo.js',
            'demo_client_action/static/src/js/templates.xml',
        ],


    },
    'installable': True,
    'application': False,
}
