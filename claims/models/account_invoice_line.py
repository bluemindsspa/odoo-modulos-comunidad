from odoo import models, fields, api


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"
    warranty = fields.Float(string='Warranty')


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice"
