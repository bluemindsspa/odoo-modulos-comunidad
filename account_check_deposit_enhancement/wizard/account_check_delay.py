# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2016 TRESCLOUD Cia Ltda (www.trescloud.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time


class account_check_delay(osv.osv_memory):
    _name = "account.check.delay"
    _description = "Check delay"
    
    def _partial_voucher_for(self, cr, uid, voucher, context=None):
        '''
        Prepara la vista de los cheques que van a ser detenidos
        :param voucher: Cheque que se depositara
        :param context: Variables de contexto
        '''
        partial_move = {
            'check_number': voucher.check_number,
            'amount': voucher.amount or 0,
            'partner_id': voucher.partner_id.id,
            'old_deposit_date': voucher.deposit_date,
            'new_deposit_date': time.strftime('%Y-%m-%d'),
            'voucher_id': voucher.id,
        }
        return partial_move
    
    def default_get(self, cr, uid, fields, context=None):
        '''
        Se carga los campos por defecto en el asistente
        para detener los cheques
        :param fields: Campos que seran analizados
        :param context: Variables de contexto o de ambiente
        '''
        if context is None: context = {}
        res = {}
        voucher_obj = self.pool.get('account.voucher')
        voucher_ids = context.get('active_ids', False)
        # Si no estamos en account.voucher entonces no hacemos nada
        if not voucher_ids or not context.get('active_model') == 'account.voucher':
            return res
        # Si el campo por defecto que requerimos esta en los pendientes
        # entonces se analiza las lineas seleccionadas y se las carga 
        # en el asistente
        if 'delay_checks' in fields:
            voucher_ids = voucher_obj.browse(cr, uid, voucher_ids, context=context)
            vouchers = [self._partial_voucher_for(cr, uid, m, context=context) for m in voucher_ids]
            res.update(delay_checks=vouchers)
        return res
   
    def delay_checks(self, cr, uid, ids, context=None):
        """
        Cheques detenidos por el usuario
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: account period close’s ID or list of IDs
        @param context: Variables de contexto o de ambiente
         """
        account_voucher_obj = self.pool.get('account.voucher')
        for delayed_check_id in self.browse(cr, uid, ids, context=context):
            if context.get('active_model') == 'account.voucher':
                for line_id in delayed_check_id.delay_checks:
                    new_deposit_date = line_id.new_deposit_date
                    voucher_id = line_id.voucher_id.id
                    # Se escribe la nueva fecha de deposito en el pago
                    # Ademas se cambia de estado al pago.
                    account_voucher_obj.write(cr, uid, voucher_id, {'new_deposit_date': new_deposit_date,
                                                                    'state_check_control': 'delayed_check'}, context=context)
        return {'type': 'ir.actions.act_window_close'}

    _columns = {
        'delay_checks': fields.one2many('account.check.delay.line', 'wizard_id',string="Delayed Checks", help=""),
    }


account_check_delay()

class account_check_delay_line(osv.osv_memory):
    _name = "account.check.delay.line"
    _description = "Check delay line"
    
    _columns = {
        'wizard_id': fields.many2one('account.check.delay', string="Wizard"),
        'check_number': fields.char('Check number', help="Check Number from the customer"),
        'amount': fields.float('Amount', help="Amount of the check"),
        'partner_id': fields.many2one('res.partner', string='Partner',help="Customer of the check"),
        'old_deposit_date': fields.date('Old Deposit Date', help="Previous Date of the deposit"),
        'new_deposit_date': fields.date('New Deposit Date', help="New date of the deposit"),
        'voucher_id': fields.many2one('account.voucher', string='Voucher', help=""),
    }

account_check_delay_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: