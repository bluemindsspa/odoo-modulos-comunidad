from odoo import models, fields, api


class crm_claim_category(models.Model):
    _name = "crm.claim.category"
    _description = "Category of claim"
    
    name = fields.Char('Name', required=True, translate=True)
    team_id = fields.Many2one('crm.team', 'Sales Team')