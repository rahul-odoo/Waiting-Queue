# -*- coding: utf-8 -*-
{
    'name': "Waiting Queue",

    'summary': """
        Waiting Queue""",

    'description': """
        Waiting Queue
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['report'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
       # 'views/views.xml',
        #'views/templates.xml',
        'views/wq.xml',
        'views/token_sequence.xml',
        'views/report_token.xml',
        'token_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}