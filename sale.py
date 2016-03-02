'''
from openerp import models, fields, api

class order_lines(models.Model):
	_inherit = 'sale.order.line'

	
	@api.onchange('product_id')
	def mark_as_sold(self):
		if self.product_id.product_category == 'land':
			self.product_id.sale_ok = False
		else:
			pass
'''