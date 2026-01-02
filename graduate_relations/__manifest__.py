{
    "name": "Graduate Relations",
    "summary": "Manage Graduate Relations",
    "author": "Mahmoud Hashem",
    "version": "1.0",
    
    "depends": ["base",'contacts','training_package_management','web', 'website', 'website_event'],
    "data": [
        "security/module_category.xml",
        "security/security.xml",
        #"security/rules.xml",
        "security/ir.model.access.csv",

        'data/graduate_cron.xml',
        
        'views/cv_template.xml',
        'views/graduates_view.xml',
        'views/graduate_cv_views.xml',

        'views/portal_graduate_relation_login.xml',
        'views/portal_graduate_relation_main.xml',
        'views/menus.xml',
        'views/courses_views.xml',
        'views/training_graduate_views.xml',
        'views/event_inherit_views.xml',
        'views/event_template_inherit.xml',
        'views/graduate_send_mail_wizard.xml',
    ],
    
    "application": True,
}
