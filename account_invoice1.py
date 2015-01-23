from openerp.osv import fields, osv 
from openerp.tools.translate import _
from openerp.addons.account.account_invoice import account_invoice as so
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _

class account_invoice(models.Model):
    _inherit="account.invoice"
    
    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        print"===========================================hello"
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)
        self.amount_total = self.amount_untaxed + self.amount_tax
        global_discount=self.global_discount
        print"====================",self.global_discount
        if "%" in self.global_discount:
            global_discount=global_discount.split("%")
            global_discount=float(global_discount[0])
            global_percent=(self.amount_untaxed*global_discount)/100
            self.amount_untaxed=self.amount_untaxed-global_percent
            self.amount_total=self.amount_untaxed+self.amount_tax
        else:
            self.amount_untaxed=self.amount_untaxed-float(self.global_discount)
            self.amount_total=self.amount_untaxed+self.amount_tax 
            
            
                 
        #global_dicount=self.global_dicount.split("%")
        #global_dicount= global_dicount[0]
        #print"ggggggggggggggggg",self.global_discount.split("%")
        #amount_untaxed=self.amount_untaxed
        #amount_tax=self.amount_tax
        #self.amount_untaxed=self.amount_untaxed-float(self.global_discount)
        #self.amount_total=self.amount_untaxed+self.amount_tax
    amount_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
        
    