# -*- coding: utf-8 -*-

from openerp import models, fields, api

class investor_registration(models.Model):
    _name = 'sale.investor.registration'
    _inherit = 'res.partner'

    investor = fields.Boolean(default = True)

    @api.one
    def create_investor(self):
        pass #create a duplicate entry on res.partner


class investor(models.Model):
    _inherit = 'res.partner'

    investor = fields.Boolean()

class project_costing(models.Model):
	_name = 'investment.project.costing.header'

	no = fields.Char()
	name = fields.Char()
	description = fields.Char()
	date = fields.Date(default = fields.Date.today())
	title_deed_no = fields.Char()
	vendor = fields.Many2one('res.partner')
	vendor_quotation = fields.Many2one('purchase.order')
	vendor_invoice = fields.Many2one('purchase.order')
	total_acreage = fields.Float()
	allocation_to_ammenities = fields.Float()
	useful_acreage = fields.Float()
	user_id	= fields.Char()
	state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")])
	posted = fields.Boolean()
	line_ids = fields.One2many('investment.project.costing.lines','no')
	costing_setup_ids = fields.One2many('investment.land.transaction.costs.local','no')

class project_costing_lines(models.Model):
	_name = 'investment.project.costing.lines'

	no = fields.Char()
	
	useful_acreage = fields.Float()
	unit_price = fields.Float()
	unit_of_measure = fields.Selection([('acre',"Acre"),('hectare',"Hectare")])
	size_of_plots = fields.Float()
	allocation_percentage = fields.Float()
	no_of_plots = fields.Integer()
	total_acreage = fields.Float()
	useful_acreage = fields.Float()
	land_purchase_cost = fields.Float()
	land_cost_per_plot = fields.Float()
	overheads = fields.Float()
	total_cost = fields.Float()
	overhead_ids = fields.One2many('investment.land.overheads','no')

class land_overheads(models.Model):
	_name = 'investment.land.overheads'

	no = fields.Char()
	code = fields.Many2one('investment.land.transactions')
	fee_charged = fields.Float()
	vat = fields.Float()
	total_cost = fields.Float()
	profit_margin = fields.Float()
	overhead_price = fields.Float(string = "Total Cost + Profit Margin")

class plot_transactions(models.Model):
	_name = 'investment.land.transactions'

	name = fields.Char(string = 'Code')
	description = fields.Char()
	attacts_vat = fields.Boolean()
	attracts_margin = fields.Boolean()

class land_overheads_setup(models.Model):
	_name = 'investment.land.transaction.costs'

	overhead = fields.Many2one('investment.land.transactions')
	based_on = fields.Selection([('flat',"Flat Rate"),('percentage',"Percentage")], default = 'flat')
	percentage = fields.Float()
	cost = fields.Float()
	

class land_overheads_setup_local(models.Model):
	_name = 'investment.land.transaction.costs.local'
	_inherit = 'investment.land.transaction.costs'

	no = fields.Char()


