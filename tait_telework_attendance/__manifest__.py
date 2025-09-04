# -*- coding: utf-8 -*-
{
    'name': "Tele-Work Attendance",

    #'summary': "Short (1 phrase/line) summary of the module's purpose",
    "category": "Human Resources",


    'author': "Mahmoud Hashem",
     
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ["tait_telework_base","hr","hr_contract","hr_attendance","hr_holidays","resource"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_generation_wizard_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_attendance_views.xml',
        
         
        
    ],

    "installable": True,
}
