# -*- coding: utf-8 -*-
{
    'name': "Claims",

    'summary': """
        The Warranty module allows the user to claim a request based on the products warranty specified in months.""",

    
    'author': "Techspawn Solutions",
    'website': "https://techspawn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','sale','stock','procurement','service_product_warranty'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_type.xml',
        'views/claim_type.xml',
        'views/substates.xml',
        'views/claim_categories.xml',
        'views/stock_warehouse.xml',
        'views/claim_lines.xml',
        'views/claim_stage.xml',
        'views/claims.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}