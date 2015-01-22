from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.one
    @api.depends('order_line.discount','order_line.product_uom_qty','order_line.price_unit')
    def _compute_discount(self):
        self.discount_total = sum(line.price_unit*line.product_uom_qty*float(line.discount or 0.0) / float(100.0) for line in self.order_line)
    
    discount_total = fields.Float(string='Discount', store=True, readonly=True, compute='_compute_discount', track_visibility='always',
                                  digits= dp.get_precision('Discount'))