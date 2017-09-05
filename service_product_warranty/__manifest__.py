# -*- coding: utf-8 -*-
{
    'name': "Service Product Warranty",

    'summary': """
        Service Product Warranty adds a field in the product, that adds warranty of that product in months.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Techspawn Solutions",
    'website': "https://techspawn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sales_order_warranty.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}