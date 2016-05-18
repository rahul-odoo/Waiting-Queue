# -*- coding: utf-8 -*-
{
    'name': "Website Waiting Queue",

    'summary': """
        Website Waiting Queue""",

    'description': """
        Website Waiting Queue
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website', 'wq'],

    # always loaded
    'data': [
        'views/services_view.xml',
        'views/website_services.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}