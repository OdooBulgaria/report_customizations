from openerp.osv import fields, osv 
from openerp.tools.translate import _
from openerp.addons.sale.sale import sale_order as so
import openerp.addons.decimal_precision as dp
class sale_order(osv.osv):
    _inherit="sale.order"
    _description="sale order"
    
    def _amount_all_wrappers(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        print "===========================++++++++++++++++++++shivam+==",cr, uid, ids, field_name, arg
       #print "======================================trial",self._amount_all(cr, uid, ids, field_name, arg, context=context)
        a=self._amount_all(cr, uid, ids, field_name, arg, context=context)
        obj=self.pool.get("sale.order").browse(cr,uid,ids,context)
        global_discount=obj.global_discount
        for i in a:
            if "%" in global_discount:
                global_discount=global_discount.split("%")
                global_discount=float(global_discount[0])
                untaxed_amount=a[i].get("amount_untaxed")
                global_percent=(untaxed_amount* global_discount)/100
                untaxed_amount=untaxed_amount-global_percent
                a[i]["amount_untaxed"]=untaxed_amount
                amount_tax=a[i].get("amount_tax")
                amount_total=untaxed_amount+amount_tax
                a[i]["amount_total"]=amount_total
            else:
                untaxed_amount=a[i].get("amount_untaxed")
                amount_tax=a[i].get("amount_tax")
                untaxed_amount=untaxed_amount-float(global_discount)
                amount_total=untaxed_amount+amount_tax
                print"bbbbbbbbbbbb",untaxed_amount
                a[i]["amount_untaxed"]=untaxed_amount
                a[i]["amount_total"]=amount_total
            
        print"splitttttttttttttttt",global_discount
        """for i in a:
           # print"iiiiiiiiiiiii",a[i].get("amount_untaxed")
           # print"iiiiiiiiiiiii",a.get(i,False)
            #"============",a[i].key("amount_untaxed")
            #print"gglobalSSS",obj.global_discount
            
           # b=a.get(i,False).get("untaxed_amount"
          untaxed_amount=a[i].get("amount_untaxed")
            amount_tax=a[i].get("amount_tax")
            untaxed_amount=untaxed_amount-float(global_discount)
            amount_total=untaxed_amount+amount_tax
            print"bbbbbbbbbbbb",untaxed_amount
            a[i]["amount_untaxed"]=untaxed_amount
            a[i]["amount_total"]=amount_total"""
            
        return a
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
                                
    
    _columns={
              'amount_untaxed': fields.function(_amount_all_wrappers, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all_wrappers, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all_wrappers, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },multi='sums', help="The total amount."),

        }
                                        
   
    
    
    