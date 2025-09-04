# -*- coding: utf-8 -*-
{
    'name': "Tele-Work Base",

    #'summary': "Short (1 phrase/line) summary of the module's purpose",



    'author': "Mahmoud Hashem",
     
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base',"hr","hr_contract","project"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/registration_type_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_job_views.xml',
        'views/assign_tasks_wizard_views.xml',
             
        
    ],
    
}
