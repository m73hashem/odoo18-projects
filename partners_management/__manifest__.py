{
    "name": "Partners Management",
    "version": "1.2",
    "summary": "Manage Business Partners",
    "author": "Mahmoud Hashem",

    "depends": ["base", "mail", 'survey', 'portal', 'website'],

    "data": [
        'security/ir_module_category.xml',
        'security/security.xml',
        "security/ir.model.access.csv",
        "views/partnership_type_views.xml",
        "views/partner_views.xml",
        "views/plan_views.xml",
        'views/portal_template_inherit.xml',
        'views/portal_views.xml',
        "views/evaluation_views.xml",
        "views/activity_views.xml",
        "views/menus.xml",
        'data/partner_cron.xml',
    ],

    "installable": True,
    "application": True,
}
