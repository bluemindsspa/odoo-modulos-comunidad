from odoo import fields, models


class SubstateSubstate(models.Model):
    """ To precise a state (state=refused; substates= reason 1, 2,...)
    """

    _name = "substate.substate"
    _description = "substate that precise a given state"

    name = fields.Char('Sub state', required=True)
    substate_descr = fields.Text('Description',
                                 help="To give more "
                                 "information about the sub state")
