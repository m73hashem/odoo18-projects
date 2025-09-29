{
    "name": "Partners Management",
    "version": "1.1",
    "summary": "Manage Business Partners",
    "author": "Mahmoud Hashem",

    "depends": ["base", "mail"],

    "data": [
        'security/security.xml',
        "security/ir.model.access.csv",

        "views/partner_views.xml",
        "views/plan_views.xml",
        "views/evaluation_views.xml",
        "views/activity_views.xml",
        "views/menus.xml",
    ],
    
    "installable": True,
    "application": True,
}
