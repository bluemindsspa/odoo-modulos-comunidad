from odoo import models, fields, api

class crm_claim_stage(models.Model):
    """ Model for claim stages. This models the main stages of a claim
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only tages, instead of state and stages.
        Stages are for example used to display the kanban view of records."""

    _name = "crm.claim.stage"
    _description = "Claim stages"
    _rec_name = 'name'
    _order = "sequence"

    
    name = fields.Char('Stage Name', required=True, translate=True)

    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.",default=lambda *args: 1)

    team_ids = fields.Many2many('crm.team', 'crm_team_claim_stage_rel', 'stage_id', 'team_id', string='Teams',
                        help="Link between stages and sales teams. When set, this limitate the current stage to the selected sales teams.")

    case_default = fields.Boolean('Common to All Teams',
                        help="If you check this field, this stage will be proposed by default on each sales team. It will not assign this stage to existing teams.")

    claim_type = fields.Many2one(
        'crm.claim.type',
        help="Claim classification"
    )

    claim_common = fields.Boolean(string='Common to All Claim Types',
                                  help="If you check this field,"
                                  " this stage will be proposed"
                                  " by default on each claim type.")
