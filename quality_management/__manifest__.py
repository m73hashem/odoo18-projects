{
'name': 'Quality Management System',
'version': '1.0.0',
'summary': 'Central Quality Management for training services',
"license": "LGPL-3",

'author': 'Mahmoud Hashem',

'depends': ['base','web','board', 'mail', 'survey', 'project', 'helpdesk', 'training_package_management'],

'data': [
        'security/module_category.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/cron_data.xml',

        'views/quality_metric_views.xml',
        'views/quality_feedback_views.xml',
        'views/quality_plan_views.xml',
        'views/quality_plan_procedure_views.xml',
        'views/quality_alert_views.xml',
        'views/quality_team_views.xml',
        'views/survey_question_view.xml',
        'views/quality_menu.xml',
    ],

'installable': True,
'application': True,
}