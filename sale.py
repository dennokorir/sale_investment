from openerp import models, fields, api

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def confirm_booking(self):
        for line in self.order_line:
            if line.product_id.product_category == 'land':
                line.product_id.status = 'reserved'
                line.product_id.sales_person = self.user_id.id
                line.product_id.customer = self.partner_id.id

    @api.multi
    def cancel_booking(self):
        for line in self.order_line:
            if line.product_category == 'land':
                line.product_id.status == 'available'
