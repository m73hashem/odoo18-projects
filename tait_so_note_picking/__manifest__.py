# -*- coding: utf-8 -*-
{
    'name': "Sales Order Notes on Picking",

    'summary': "Short (1 phrase/line) summary of the module's purpose",
 
    'author': "Mahmoud Hashem",
     
    'depends': ['base', 'sale_management', 'stock'],

    # always loaded
    'data': [
       
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'reports/report_delivery.xml',
        'reports/report_picking_operation.xml',
        
    ],
     
}
