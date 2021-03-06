# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2016 TRESCLOUD Cia Ltda (trescloud.com)
#    All Rights Reserved.
############################################################################
#    Coded by: Santiago Orozco (santiago.orozco@trescloud.com)
############################################################################
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

from openerp.osv import osv, fields
from openerp.tools.translate import _


class mrp_production(osv.Model):
    
    _name = 'mrp.production'
    _inherit = ['mail.thread', "mrp.production"]
    
    def action_account_reprocess(self, cr, uid, ids, context=None):
        '''
        Reprocesamiento de asientos contables de ordenes de produccion
        :param cr: Cursor de la base de datos
        :param uid: Id de usuario para la transaccion
        :param ids: Ids de las ordenes de produccion
        :param context: Variables de contexto como zona horaria, lenguaje, etc
        '''
        account_move_line_obj = self.pool.get('account.move.line')
        account_move_obj = self.pool.get('account.move')
        stock_move_obj = self.pool.get('stock.move')
        # Buscamos las lineas los asientos contables asociados a la orden de produccion
        journal_items_ids = account_move_line_obj.search(cr, uid, [('production_id','in', ids if isinstance(ids, (list,tuple)) else [ids])],context=context)
        # Buscamos los asientos contables asociados a la orden de produccion
        journal_entries_ids = list(set([journal_item.move_id.id for journal_item in account_move_line_obj.browse(cr, uid, journal_items_ids, context=context)]))
        # Eliminamos los apuntes contables
        account_move_line_obj.unlink(cr, uid, journal_items_ids, context=context)
        # Cancelamos los asientos contables
        account_move_obj.button_cancel(cr, uid, journal_entries_ids, context=context)
        # Eliminamos los asientos contables
        journal_entries_ids = account_move_obj.unlink(cr, uid, journal_entries_ids, context=context)
        # Regeneramos los asientos contables y los apuntes
        for production in self.browse(cr, uid, ids, context=context):
            for move in production.move_lines2:
                stock_move_obj._create_product_valuation_moves_mrp(cr, uid, move, context=context)
            extra_info = ''
            if production.state == 'done':
                extra_info = "\n\nEl costo del producto debe ser actualizado manualmente por el usuario." 
            message = _("La orden de producción número %s ha sido reprocesada por %s." + extra_info
                        ) %(production.name, self.pool.get('res.users').browse(cr, uid, uid, context=context).name)
            self.message_post(cr, uid, production.id,
                        body=message,
                        subtype='mail.mt_comment',
                        context=context)
        return True
    
    _columns = {
        'landing_cost_id': fields.many2one('stock.picking.in', 'Landing Cost', 
                                           help='If you select an import cost accounting entries are generated based on the cost CIF')
    }

mrp_production()


class stock_move(osv.osv):
    
    _inherit = "stock.move"
    
    def _create_product_valuation_moves_mrp(self, cr, uid, move, context=None):
        """
        Generate the appropriate accounting moves if the product being moves is subject
        to real_time valuation tracking, and the source or destination location is
        a transit location or is outside of the company.
        """
        move_created = [] 
        if move.product_id.valuation == 'real_time': # FIXME: product valuation should perhaps be a property?
            if context is None:
                context = {}
            src_company_ctx = dict(context,force_company=move.location_id.company_id.id)
            dest_company_ctx = dict(context,force_company=move.location_dest_id.company_id.id)
            # do not take the company of the one of the user
            # used to select the correct period
            company_ctx = dict(context, company_id=move.company_id.id)
            account_moves = []
            # Outgoing moves (or cross-company output part)
            if move.location_id.company_id \
                and (move.location_id.usage == 'internal' and move.location_dest_id.usage != 'internal'\
                     or move.location_id.company_id != move.location_dest_id.company_id):
                journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation(cr, uid, move, src_company_ctx)
                reference_amount, reference_currency_id = self._get_reference_accounting_values_for_valuation(cr, uid, move, src_company_ctx)
                #En caso que exista costo de importacion los asientos contables se generan en base al costo CIF
                if move.move_dest_id.production_id.landing_cost_id:
                    for line in move.move_dest_id.production_id.landing_cost_id.move_lines:
                        if line.product_id.id == move.product_id.id:
                            #En caso que exista conversion de unidades de medida
                            qty = self.pool.get('product.uom')._compute_qty(cr, uid, move.product_uom.id, move.product_qty, move.product_uom.id)
                            reference_amount = qty * line.price_unit
                #returning goods to supplier
                if move.location_dest_id.usage == 'supplier':
                    account_moves += [(journal_id, self._create_account_move_line(cr, uid, move, acc_valuation, acc_src, reference_amount, reference_currency_id, context))]
                else:
                    account_moves += [(journal_id, self._create_account_move_line(cr, uid, move, acc_valuation, acc_dest, reference_amount, reference_currency_id, context))]

            # Incoming moves (or cross-company input part)
            if move.location_dest_id.company_id \
                and (move.location_id.usage != 'internal' and move.location_dest_id.usage == 'internal'\
                     or move.location_id.company_id != move.location_dest_id.company_id):
                journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation(cr, uid, move, dest_company_ctx)
                reference_amount, reference_currency_id = self._get_reference_accounting_values_for_valuation(cr, uid, move, src_company_ctx)
                #goods return from customer
                if move.location_id.usage == 'customer':
                    account_moves += [(journal_id, self._create_account_move_line(cr, uid, move, acc_dest, acc_valuation, reference_amount, reference_currency_id, context))]
                else:
                    account_moves += [(journal_id, self._create_account_move_line(cr, uid, move, acc_src, acc_valuation, reference_amount, reference_currency_id, context))]

            move_obj = self.pool.get('account.move')
            account_period_obj = self.pool.get('account.period')
            for j_id, move_lines in account_moves:
                period_id = account_period_obj.find(cr, uid, move.date, context=context)
                id = move_obj.create(cr, uid,
                        {
                         'journal_id': j_id,
                         'line_id': move_lines,
                         'date': move.date,
                         'period_id': period_id and period_id[0] or False,
                         'company_id': move.company_id.id,
                         'ref': move.picking_id and move.picking_id.name}, context=company_ctx)
                
    def action_return_product_to_consume(self, cr, uid, ids, context=None):
        '''
        Este método devuelve el producto seleccionado de consumido a por consumir y elimina los apuntes contables asociados
        :param cr: Cursor de la base de datos
        :param uid: ID del usuario actual
        :param ids: IDs del movimiento
        :param context: Diccionario de contexto adicional
        '''
        if context is None:
            context = {}
        changes = []
        for move in  self.browse(cr, uid, ids, context=context):
            oldvalue = 'Productos consumidos'
            newvalue = 'Productos a consumir'
            changes.append(_("Producto: %s: from %s to %s") %(move.product_id.name, oldvalue, newvalue))
            if len(changes) > 0:
                try:
                    self.pool.get('mrp.production').message_post(cr, uid, [move.move_dest_id.production_id.id], body=", ".join(changes), context=context)
                except:
                    #Cuando el producto es agregado manualmente al listado de productos a consumir
                    cr.execute('''
                        select production_id 
                        from mrp_production_move_ids 
                        where move_id in %s
                    ''', (tuple(ids),))
                    res = cr.fetchall()
                    if res:
                        self.pool.get('mrp.production').message_post(cr, uid, [res[0][0]], body=", ".join(changes), context=context)
        #Regresamos el producto consumido a producto por consumir
        cr.execute('''
            update stock_move
            set state='waiting'
            where id in %s
        ''', (tuple(ids),))
        #Eliminamos los asientos contables generados
        cr.execute('''
            delete 
            from account_move_line 
            where stock_move_id in %s
        ''', (tuple(ids),))
        return True
    
stock_move()
