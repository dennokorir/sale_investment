from openerp import fields, api, models
from openerp.exceptions import ValidationError

class invoice(models.Model):

	_inherit = 'account.invoice'

	@api.multi
	def check_product_state(self):
		for line in self.invoice_line:
			if line.product_id.product_category == 'land':
				#raise ValidationError("It worked!!")
				line.product_id.sale_ok = False
				line.product_id.purchase_ok = False
                line.product_id.status = 'sold'
