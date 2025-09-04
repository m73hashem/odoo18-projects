{
    'name': 'Project Expenses Management',
    'version': '1.0',
    'summary': 'Trace expenses per project, product lines, portal submission and reporting',
    'description': """
Custom module to track expenses per project with expense types, multi-line requests,
stock pickings creation for product lines, portal form access and reporting.
""",
    'author': 'Mahmoud Hashem',
    'category': 'Project',
    'depends': ['base', 'project', 'stock', 'website', 'portal', 'contacts'],
    'data': [
        'security/project_expense_security.xml',
        'security/ir.model.access.csv',
        'views/test_menus.xml',
        'views/portal_templates.xml',
        'views/portal_public_templates.xml',

        'views/project_inherit_views.xml',
        'data/sequence_data.xml',
        'views/project_expense_views.xml',
        'views/expense_type_views.xml',
        'views/expense_request_views.xml',
        'views/stock_templates.xml',
        'wizards/project_expense_report_views.xml',
        'reports/report_template.xml',

        'views/menu.xml',

    ],
    'installable': True,
    'application': False,
}