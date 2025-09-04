{
    "name": "Action Demo Lab",
    "version": "18.0.1.0.0",
    "summary": "Practice all Odoo action types",
    "author": "Mahmoud Hashem",
    "license": "LGPL-3",
    "depends": ["base", "web"],



    "data": [
        "security/ir.model.access.csv",
        'views/action_demo_views.xml',

        'views/action_demo_client_action.xml',

    ],

"assets": {

"web.assets_backend": [
                'action_demo_lab/static/src/js/client_action_demo.js',
                'action_demo_lab/static/src/js/template.xml',
                #'action_demo_lab/views/client_action_templates.xml'
            ],

        },

    "application": True,
}
