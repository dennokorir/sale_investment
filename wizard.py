from openerp import models, fields, api
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
			product_category = self.env['product.category'].create({'name':self.project_no,'parent_id':1,'type':'normal'})
			#all product fields will be the same except internal reference
			#internal reference will use number series.
			#NB: Internal Reference === default_code
			name = self.project_name
			categ_id = product_category.id
			product_type = 'consu'
			state = 'sellable'
			uom_id = 1
			qty_available = 1
			virtual_available = 1
			active = True
			no = ''
			start = 1
			for line in project.line_ids:
				end = line.no_of_plots + start
				for plot in range(start, end):
					no = self.numbering_prefix.upper() + str(plot)
					self.env['product.template'].create({'name':name,'categ_id':categ_id,'type':product_type,
						'state':state,'uom_id':uom_id,'qty_available':qty_available,'virtual_available':virtual_available,
						'default_code':no,'standard_price':line.land_cost_per_plot,'list_price':line.price_per_plot,
						'product_category':'land','sale_ok':True,'purchase_ok':False,'total_acreage':line.size_of_plots})
					#product category is a field added to product table to identify plots
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

