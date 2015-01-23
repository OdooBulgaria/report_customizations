from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    _defaults={
               "global_discount":0.0
               }
    @api.one
    @api.depends('invoice_line.discount','invoice_line.quantity','invoice_line.price_unit')
    def _compute_discount(self):
        self.discount_total = sum(line.price_unit*line.quantity*float(line.discount or 0.0) / float(100.0) for line in self.invoice_line)
        
    @api.one
    @api.depends('invoice_line.discount','invoice_line.quantity','invoice_line.price_unit')
    def _compute_amounts(self):
        self.before_discount_total = sum(line.price_unit*line.quantity for line in self.invoice_line)
    
    discount_total = fields.Float(string='Line Discount', store=True, readonly=True, compute='_compute_discount', track_visibility='always',
                                  digits= dp.get_precision('Discount'))
    before_discount_total = fields.Float(string='Amount', store=True, readonly=True, compute='_compute_amounts', track_visibility='always',
                                  digits= dp.get_precision('Account'))
    global_discount=fields.Char("Global Discount")