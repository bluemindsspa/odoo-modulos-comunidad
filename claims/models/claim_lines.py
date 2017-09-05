from odoo import models, fields, api
from datetime import datetime
from dateutil import relativedelta


class ClaimLine(models.Model):

    _name = "claim.line"

    _inherit = 'mail.thread'
    _description = "List of product to return"
    _rec_name = "display_name"


    customer = fields.Many2one('res.partner', string='Customer')

    SUBJECT_LIST = [('none', 'Not specified'),
                    ('legal', 'Legal retractation'),
                    ('cancellation', 'Order cancellation'),
                    ('damaged', 'Damaged delivered product'),
                    ('error', 'Shipping error'),
                    ('exchange', 'Exchange request'),
                    ('lost', 'Lost during transport'),
                    ('perfect_conditions',
                     'Perfect Conditions'),
                    ('imperfection', 'Imperfection'),
                    ('physical_damage_client',
                     'Physical Damage by Client'),
                    ('physical_damage_company',
                     'Physical Damage by Company'),
                    ('other', 'Other')]
    WARRANT_COMMENT = [
        ('valid', ("Valid")),
        ('expired', ("Expired")),
        ('not_define', ("Not Defined"))]

    number = fields.Char(
        # readonly=True,        
        help='Claim Line Identification Number',copy=False, readonly=True,)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=False,
        change_default=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'claim.line'))
    date = fields.Date('Claim Line Date',
                       select=True,
                       default=fields.date.today())
    name = fields.Char('Description', default='none', required=False,
                       help="More precise description of the problem")
    responsible = fields.Many2one('res.partner',string= 'Responsible')
    priority = fields.Selection([('0_not_define', 'Not Define'),
                                 ('1_normal', 'Normal'),
                                 ('2_high', 'High'),
                                 ('3_very_high', 'Very High')],
                                'Priority', default='0_not_define',
                                store=True,
                                readonly=False,
                                help="Priority attention of claim line")
    claim_diagnosis = fields.\
        Selection([('damaged', 'Product Damaged'),
                   ('repaired', 'Product Repaired'),
                   ('good', 'Product in good condition'),
                   ('hidden', 'Product with hidden physical damage'),
                   ],
                  help="To describe the line product diagnosis")
    claim_origin = fields.Selection(SUBJECT_LIST, 'Claim Subject',
                                    required=False, help="To describe the "
                                    "line product problem")
    product_id = fields.Many2one('account.invoice.line', string='Product',
                                 help="Returned product")
    product_returned_quantity = \
        fields.Float('Quantity', digits=(12, 2),
                     help="Quantity of product returned")
    unit_sale_price = fields.Float(digits=(12, 2),
                                   help="Unit sale price of the product. "
                                   "Auto filled if retrun done "
                                   "by invoice selection. Be careful "
                                   "and check the automatic "
                                   "value as don't take into account "
                                   "previous refunds, invoice "
                                   "discount, can be for 0 if product "
                                   "for free,...")
    return_value = fields.Float(
                                string='Total return',
                                help="Quantity returned * Unit sold price",)
    prodlot_id = fields.Many2one('stock.production.lot',
                                 string='Serial/Lot number',
                                 help="The serial/lot of "
                                      "the returned product")
    applicable_guarantee = fields.Selection([('us', 'Company'),
                                             ('supplier', 'Supplier'),
                                             ('brand', 'Brand manufacturer')],
                                            'Warranty type')
    guarantee_limit = fields.Float(string='Warranty limit',
                                  help="The warranty limit is "
                                       "computed as: invoice date + warranty "
                                       "defined on selected product.")
    warranty = fields.Float(string='Warranty')
    warning = fields.Selection(WARRANT_COMMENT,
                               'Warranty', readonly=True,
                               help="If warranty has expired")
    display_name = fields.Char('Name')
    claim_id = fields.Many2one('crm.claim', string='Related claim',
                               ondelete='cascade',
                               help="To link to the case.claim object")
    state = fields.Selection([('draft', 'Draft'),('pending' ,'Pending'),('refused', 'Refused'),
                              ('approved', 'Approved')],
                             string='State', default='draft')
    substate_id = fields.Many2one('substate.substate', string='Sub state',
                                  help="Select a sub state to precise the "
                                       "standard state. Example 1: "
                                       "state = refused; substate could "
                                       "be warranty over, not in "
                                       "warranty, no problem,... . "
                                       "Example 2: state = to treate; "
                                       "substate could be to refund, to "
                                       "exchange, to repair,...")
    last_state_change = fields.Date(string='Last change', help="To set the"
                                    "last state / substate change",default=datetime.now())
    invoice_line_id = fields.Many2one('account.invoice.line',
                                      string='Invoice Line',
                                      help='The invoice line related'
                                      ' to the returned product')
    invoice_number = fields.Many2one('account.invoice',string='Invoice Number')
    refund_line_id = fields.Many2one('account.invoice.line',
                                     string='Refund Line',
                                     help='The refund line related'
                                     ' to the returned product')
    move_in_id = fields.Many2one('stock.move',
                                 string='Move Line from picking in',
                                 help='The move line related'
                                 ' to the returned product')
    move_out_id = fields.Many2one('stock.move',
                                  string='Move Line from picking out',
                                  help='The move line related'
                                  ' to the returned product')
    location_dest_id = fields.Many2one('stock.location',
                                       string='Return Stock Location',
                                       help='The return stock location'
                                       ' of the returned product')
    claim_type = fields.Many2one(related='claim_id.claim_type',
                                 string="Claim Line Type",
                                 store=True, help="Claim classification")
    product_lines = fields.Many2many('account.invoice.line',string='Products')

    account_id = fields.Many2one('account.invoice.line', string='Account' )

    


    @api.multi
    @api.onchange('customer')
    def get_invoice(self):

        res={}  
        for invoice in self.customer.invoice_ids:
            print invoice
            self.invoice_number=invoice
            res[invoice]= self.invoice_number
        return res

    @api.multi
    @api.onchange('invoice_number')
    def get_product(self):

        product_list = []
        res={}

        if self.invoice_number.create_date:
            invoice_date = self.invoice_number.create_date
            present_date= datetime.now()
            date1 = datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S')
            difference = relativedelta.relativedelta(present_date, date1)

            for product in self.invoice_number.invoice_line_ids:
                warranty_ramaining = float(product.product_id.warranty) - difference.months
                
                if product:
                    products_list_dict = {'product_id': product.product_id.id, 'quantity': product.quantity, 'price_unit': product.price_unit, 'name' : product.name, 'invoice_line_tax_ids':product.invoice_line_tax_ids.id, 'warranty':warranty_ramaining ,'account_id':product.account_id}
                product_list.append([0,0,products_list_dict])
                res[product.product_id.id]=self.product_id
        self.product_lines = product_list
        return res

    @api.multi
    def write(self,vals):
        vals['last_state_change'] = datetime.now()
        return super(ClaimLine,self).write(vals)

    @api.model
    def create(self, vals):
        """ create a sequence for order number """
        vals['state'] = 'pending'
        if not vals.get('number', False):
            vals['number'] = self.env['ir.sequence'].next_by_code(
                'claim.line') or '/'
        return super(ClaimLine, self).create(vals)

    @api.one
    def state_pending(self):
      self.write({
        'state' : 'pending',
        })

    @api.one
    def state_approved(self):
      self.write({
        'state' : 'approved',
        })

    @api.one
    def state_refused(self):
      self.write({
        'state' : 'refused',
        })


