# -*- coding: utf-8 -*-
{
    'name': "Tait Asset Number",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Mahmoud Hashem",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_asset'],

    'assets':{
        'web.report_assets_common':['tait_asset_number/static/src/css/font.css']
    },


    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/asset_number_views.xml',
        
        'reports/asset_summery_report.xml',
        'reports/report_paperformat.xml',
        'reports/template1.xml',
        'reports/asset_label_report_template.xml',
        'reports/asset_lable_template.xml',
        
        
        'views/label_report_wizard_views.xml',
        
    ],

    
    
}

