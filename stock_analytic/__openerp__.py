# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Julius Network Solutions SARL <contact@julius.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

{
    "name" : "Stock analytic",
    "version" : "1.0",
    "author" : "Julius Network Solutions",
    "website" : "http://www.julius.fr/",
    'complexity': "easy",
    "category" : "Warehouse Management",
    "depends" : [
        "base",
        "stock",
        "sale",
        "purchase",
        "account",
    ],
    "description": """
    Adds an analytic account in stock move to be able to get analytic info when generating the account move line
    """,
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
#        "security/service_security.xml",
#        "security/ir.model.access.csv",
        "stock_view.xml",
    ],
    'installable' : True,
    'active' : True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: