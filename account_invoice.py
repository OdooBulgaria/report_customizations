from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.addons.account.account_invoice import account_invoice as so


class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.one
    @api.depends('invoice_line.discount','invoice_line.quantity','invoice_line.price_unit')
    def _compute_discount(self):
        self.discount_total = sum(line.price_unit*line.quantity*float(line.discount or 0.0) / float(100.0) for line in self.invoice_line)
        
    @api.one
    @api.depends('invoice_line.discount','invoice_line.quantity','invoice_line.price_unit')
    def _compute_amounts(self):
        self.before_discount_total = sum(line.price_unit*line.quantity for line in self.invoice_line)
   
    def calculate_percent(self,cr,uid,ids,global_discount_amount,before_discount_total,discount_total,context=None):
        res={}
        try:
            amount=(global_discount_amount*100)/(before_discount_total-discount_total)
            
            res['global_discount']=amount
        except:print"divisin by zero"
        return {'value':res}
        
    
    def global_discount1(self,cr,uid,ids,global_discount,before_discount_total,discount_total,context=None):
        res={}
        percent_amount=(global_discount*(before_discount_total-discount_total))/100
        res['global_discount_amount']=percent_amount
        return {'value':res}
    
    
    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amouant for line in self.tax_line)
        self.amount_untaxed=((self.before_discount_total-self.discount_total)-self.global_discount_amount)
        #amount_tax=self.amount_tax
        #self.amount_untaxed=(self.amount_untaxed-self.discount_total)-self.global_discount_amount
        self.amount_total = self.amount_untaxed + self.amount_tax
       # self.amount_total=self.amount_untaxed+self.amount_tax 
            
            
     #   global_discount=global_discount.split("%")
      #  global_discount=float(global_discount[0])
       # global_percent=(self.amount_untaxed*global_discount)/100
        #self.amount_untaxed=self.amount_untaxed-global_percent
        #self.amount_total=self.amount_untaxed+self.amount_tax
        
            
    
    
    discount_total = fields.Float(string='Line Discount', store=True, readonly=True, compute='_compute_discount', track_visibility='always',
                                  digits= dp.get_precision('Discount'))
    before_discount_total = fields.Float(string='Amount', store=True, readonly=True, compute='_compute_amounts', track_visibility='always',
                                  digits= dp.get_precision('Account'))
    global_discount=fields.Float("Global Discount(%)",default=0.0)
    global_discount_amount=fields.Float("Global Discount")
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
        
    

    
    
'''@api.onchange("global_discount_amount","amount_untaxed") 
    def calculate_percent(self):
        try:
            amount=(self.global_discount_amount*100)/self.amount_untaxed
            self.global_discount=amount
        except:print"divisin by zero"

    @api.onchange("global_discount","amount_untaxed")            
    def global_discount1(self):
        #print"gllllllllllllll",global_discount,amount_untaxed
        percent_amount=(self.global_discount*self.amount_untaxed)/100
        self.global_discount_amount=percent_amount'''
    