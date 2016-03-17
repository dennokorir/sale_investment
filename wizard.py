from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime

class project_costing_wizard(models.TransientModel):
	_name = 'project.costing.wizard'

	project_id = fields.Char(required = True)
	project_no = fields.Char(required = True)
	project_name = fields.Char(required = True)
	numbering_prefix = fields.Char(required = True)

	@api.one
	def reclassify(self):
		project = self.env['investment.project.costing.header'].search([('id','=',self.project_id)])
		if len(project)>0:
			setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
			if not (setup.land_asset_account.id and setup.land_asset_account.id and setup.land_income_account.id and setup.land_expense_account.id):
				raise ValidationError('Ensure all options are filled in Sections under General Setup > Accounting')
			stock_input = setup.land_input_account.id
			stock_output = setup.land_output_account.id
			stock_income = setup.land_income_account.id
			stock_expense = setup.land_expense_account.id
			valuation = 'real_time'
			cost_method = 'standard'


			product_category = self.env['product.category'].create({'name':self.project_no,'parent_id':1,'type':'normal',
				'property_stock_valuation_account_id':setup.land_asset_account.id})
			#all product fields will be the same except internal reference
			#internal reference will use number series.
			#NB: Internal Reference === default_code
			name = self.project_name
			categ_id = product_category.id
			product_type = 'product'   #product -->this should be the correct one to imply stock
			state = 'sellable'
			uom_id = 1
			qty_available = 1
			virtual_available = 1
			active = True
			no = ''
			start = 1
			today = datetime.now().strftime("%Y/%m/%d")
			for line in project.line_ids:
				end = line.no_of_plots + start
				for plot in range(start, end):
					no = self.numbering_prefix.upper() + str(plot)
					land_parcel = self.env['product.template'].create({'name':name,'categ_id':categ_id,'type':product_type,
						'state':state,'uom_id':uom_id,'qty_available':qty_available,'virtual_available':virtual_available,
						'default_code':no,'standard_price':line.land_cost_per_plot,'list_price':line.price_per_plot,
						'product_category':'land','sale_ok':True,'purchase_ok':False,'total_acreage':line.size_of_plots,
						'valuation':valuation,'cost_method':cost_method,'property_stock_account_input':stock_input,'property_stock_account_output':stock_output,
						'property_account_income':stock_income,'property_account_expense':stock_expense})

					#create stock move to effect inventory
					self.env['stock.move'].create({'name':'LAND RECLASS['+no+']' ,'product_id':land_parcel.id,'product_uom_qty':1,'product_uom':1,'location_id':setup.inbound_from_location.id,
						'location_dest_id':setup.inbound_to_location.id,'state':'done','date':today,'date_expected':today})

					#create stock quant
					self.env['stock.quant'].create({'product_id':land_parcel.id,'qty':1,'location_id':setup.inbound_to_location.id,'company_id':1})


					#product category is a field added to product table to identify plots/land
					#self.env['test'].create({'field1':no})
					start += 1

			#if successful, mark project as posted
			project.posted = True
			if project.costing_from == 'quotation':
				for line in project.vendor_quotation.order_line.product_id:
					line.sale_ok = False
					line.purchase_ok = False
			else:
				for line in project.vendor_quotation.order_line.product_id:
					line.sale_ok = False
					line.purchase_ok = False

