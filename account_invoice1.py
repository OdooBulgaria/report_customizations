from openerp.osv import fields, osv 
from openerp.tools.translate import _
from openerp.addons.account.account_invoice import account_invoice as so
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _

class account_invoice(models.Model):
    _inherit="account.invoice"
    
    