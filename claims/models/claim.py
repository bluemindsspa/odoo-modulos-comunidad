# -*- coding: utf-8 -*-

from odoo import models, fields, api

class crm_claim(models.Model):
    """ Crm claim
    """
    _name = "crm.claim"
    _description = "Claim"
    _order = "priority,date desc"
    _inherit = ['mail.thread']



    # name = fields.Char('Claim Subject', required=True)
    # active = fields.Boolean('Active', default=True)
    # action_next = fields.Char('Next Action')
    # date_action_next = fields.Datetime('Next Action Date')
    # description = fields.Text('Description')
    # resolution = fields.Text('Resolution')
    # create_date = fields.Datetime('Creation Date' , readonly=True)
    # write_date = fields.Datetime('Update Date' , readonly=True)
    # date_deadline = fields.Date('Deadline')
    # date_closed = fields.Datetime('Closed', readonly=True)
    # date = fields.Datetime('Claim Date', select=True)
    # categ_id = fields.Many2one('crm.claim.category', 'Category')
    # priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
    # type_action = fields.Selection([('correction','Corrective Action'),('prevention','Preventive Action')], 'Action Type')
    # user_id = fields.Many2one('res.users', 'Responsible', track_visibility='always',)
    # user_fault = fields.Char('Trouble Responsible')
    # team_id = fields.Many2one('crm.team', 'Sales Team',select=True)
    # company_id =  fields.Many2one('res.company', 'Company')
    # partner_id =  fields.Many2one('res.partner', 'Partner')
    # email_cc =  fields.Text('Watchers Emails', size=252, help="These email addresses will be added to the CC field of all inbound and outbound emails for this record before being sent. Separate multiple email addresses with a comma")
    # email_from =  fields.Char('Email', size=128, help="Destination email for email gateway.")
    # partner_phone =  fields.Char('Phone')
    # cause = fields.Text('Root Cause')
    claim_type = fields.Many2one('crm.claim.type', help="Claim classification")

    # stage_id = fields.Many2one(
    #     'crm.claim.stage',
    #     string='Stage',)
        # track_visibility='onchange',
        # domain="[ '&',"
        #        "'|',('team_ids', '=', team_id), "
        #        "('case_default', '=', True), "
        #        "'|',('claim_type', '=', claim_type)"
        #        ",('claim_common', '=', True)]")