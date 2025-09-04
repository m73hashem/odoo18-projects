# -*- coding: utf-8 -*-
{
    'name': 'Project Expense Tracking',
    'version': '1.0',
    'summary': 'Track expenses for each project',

    'author': "Mahmoud Hashem",
    'website': "https://github.com/m73hashem",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project', 'stock','product'],

    # always loaded
    'data': [
        #'security/security.xml',
        'security/ir.model.access.csv',
        'data/expense_sequence.xml',

        'views/project_views.xml',
        'views/expense_type_views.xml',
        'views/expense_request_views.xml',
        'views/expense_report_views.xml',
        'views/expense_request_extension_views.xml',
        'views/expense_product_line_views.xml',
        'views/menu.xml',
    ],


    #'installable': True,
    #'application': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

