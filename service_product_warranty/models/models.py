# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductWarranty(models.Model):
    _inherit = 'product.template'
    # _name = 'prod.temp'

    warranty = fields.Float(string="Warranty")


class SalesOrderWarranty(models.Model):
    _inherit = 'sale.order.line'

    sale_order_warranty = fields.Float(string="Warranty",compute='_compute_warranty')

    @api.depends('product_id')
    def _compute_warranty(self):
        for prod in self:
        	self.sale_order_warranty = prod.product_id.warranty
        	return self.sale_order_warranty