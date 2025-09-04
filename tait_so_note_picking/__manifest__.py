# -*- coding: utf-8 -*-
{
<<<<<<< HEAD
    'name': "tait_so_note_picking",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Mahmoud Hashem",
    'website': "abcd",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
=======
    'name': "Sales Order Notes on Picking",

    'summary': "Short (1 phrase/line) summary of the module's purpose",
 
    'author': "Mahmoud Hashem",
     
>>>>>>> e33d403681c1e931aad9215020742ea136542f3e
    'depends': ['base', 'sale_management', 'stock'],

    # always loaded
    'data': [
<<<<<<< HEAD
        #'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_return_wizard_view.xml',
        'reports/report_delivery.xml',
        'reports/report_picking_operation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

=======
       
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'reports/report_delivery.xml',
        'reports/report_picking_operation.xml',
        
    ],
     
}
>>>>>>> e33d403681c1e931aad9215020742ea136542f3e
