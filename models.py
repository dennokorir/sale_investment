# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class investor_registration(models.Model):
    _name = 'sale.investor.registration'

    no = fields.Char()
    name = fields.Char(string = 'Name')
    address = fields.Char(string = 'Address')
    phone_no = fields.Char(string = 'Phone No.')
    mobile_no = fields.Char()
    email = fields.Char(string = 'Email')
    registration_date = fields.Date(default = fields.Date.today)
    status = fields.Selection([('open',"Open"),('pending',"Pending"),('approved',"Approved"),('rejected',"Rejected")],default = 'open')
    date_of_birth = fields.Date(string = 'Date of Birth')
    home_address = fields.Char()
    location = fields.Char()
    sublocation = fields.Char()
    district = fields.Char()
    payrollno = fields.Char()
    basic_pay = fields.Float()
    house_allowance = fields.Float()
    other_benefits = fields.Float()
    transport_allowance = fields.Float()
    total_deductions = fields.Float()
    net_income = fields.Float()
    idno = fields.Char() 
    passportno = fields.Char()
    marital_status = fields.Selection([('single','Single'),('married','Married')])
    gender = fields.Selection([('male','Male'),('female','Female')])
    monthly_contribution = fields.Float()
    dividend_amount = fields.Float()
    occupation = fields.Char()
    designation = fields.Selection([('mr',"MR"),('mrs',"Mrs"),('miss',"Miss")])
    contact_person = fields.Char()
    contact_person_phone_no = fields.Char()
    contact_person_relation = fields.Selection([('kin','Kin'),('relative','Relative'),('friend','Friend')])
    recruited_by = fields.Char()
    approved_by = fields.Char()
    bank_name = fields.Char()
    bank_account_no = fields.Char()
    member_pin = fields.Char()
    image = fields.Binary("Image",help = "Member Image")

    @api.one
    def create_member(self):
        pass

class investor(models.Model):  
    _inherit = 'res.partner'

    investor = fields.Boolean()
    investor_no = fields.Char()

class investor_closure(models.Model):
    _name = 'sale.investment.investor.closure'
    no = fields.Char()
    investor_no = fields.Many2one('res.partner' ,store = True , domain = [('investor','=',True)])
    image = fields.Binary(help = 'Member Image')
    closing_date = fields.Date()
    status = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")],default='open')
    closed = fields.Boolean(default = False)
    closure_type = fields.Selection([('dismissal',"Summary Dismissal")])
    remarks = fields.Text()

class investor_activation(models.Model):
    _name = 'sale.investment.investor.activation'
    no = fields.Char()
    investor_no = fields.Many2one('res.partner', store = True ,domain = [('investor','=',True)])
    activation_date = fields.Date()
    status = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")],default='open')
    activated = fields.Boolean(default = False)
    
    

class project_costing(models.Model):
    _name = 'investment.project.costing.header'

    no = fields.Char()
    name = fields.Char()
    description = fields.Char()
    date = fields.Date(default = fields.Date.today())
    title_deed_no = fields.Char()
    costing_from = fields.Selection([('quotation',"Quotation"),('invoice',"Invoice")], default = 'quotation')
    vendor = fields.Many2one('res.partner')
    vendor_quotation = fields.Many2one('purchase.order')
    vendor_invoice = fields.Many2one('purchase.order')
    purchase_cost = fields.Float(compute = 'compute_purchase_cost')
    total_acreage = fields.Float()
    allocation_to_ammenities = fields.Float()
    useful_acreage = fields.Float(store = True, readonly = True)
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    profit_margin = fields.Float(string = "% Profit Margin")
    state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")], default = 'open')
    posted = fields.Boolean()
    line_ids = fields.One2many('investment.project.costing.lines', 'no', ondelete = 'cascade', required = True, store = True, string = "Lines")
    costing_setup_ids = fields.One2many('investment.land.transaction.costs.local','no')
    percentage_allocation = fields.Float(compute = 'compute_allocation')

    @api.onchange('total_acreage','allocation_to_ammenities')
    def compute_acreage(self):
        if self.total_acreage>0:
            self.useful_acreage = self.total_acreage - self.allocation_to_ammenities
        else:
            self.useful_acreage = 0

    @api.one
    @api.depends('line_ids')
    def compute_allocation(self):
        total = 0
        for line in self.line_ids:
            total += line.allocation_percentage
        self.percentage_allocation = total

    @api.one
    @api.depends('costing_from','vendor_quotation','vendor_invoice')
    def compute_purchase_cost(self):
        order = self.env['purchase.order'].search([('id','=',self.vendor_quotation.id)])
        self.purchase_cost = order.amount_total
        self.vendor = order.partner_id
        
            
    @api.one
    @api.constrains('percentage_allocation')
    def check_allocations(self):
        if self.percentage_allocation>100:
            raise ValidationError("Your allocations exceed 100%")

class project_costing_lines(models.Model):
    _name = 'investment.project.costing.lines'   

    no = fields.Char()
    
    #useful_acreage = fields.Float()
    #unit_price = fields.Float()
    unit_of_measure = fields.Selection([('acre',"Acre"),('hectare',"Hectare")])  
    size_of_plots = fields.Float()
    allocation_percentage = fields.Float()
    no_of_plots = fields.Integer(readonly = True)
    #total_acreage = fields.Float()
    #useful_acreage = fields.Float()
    land_purchase_cost = fields.Float(readonly = True)
    land_cost_per_plot = fields.Float(readonly = True)
    overheads = fields.Float()
    total_cost = fields.Float(readonly = True)
    margin = fields.Float(readonly = True)
    price = fields.Float(readonly = True)
    overhead_ids = fields.One2many('investment.land.overheads','no')

    
    @api.one
    @api.onchange('size_of_plots','allocation_percentage')
    def compute_no_of_plots(self):
        if (self.size_of_plots > 0) and (self.allocation_percentage>0):
            project = self.env['investment.project.costing.header'].search([('id','=',self.no)])
                        

class land_overheads(models.Model):
    _name = 'investment.land.overheads'

    no = fields.Many2one('investment.project.costing.header')
    code = fields.Many2one('investment.land.transactions')
    fee_charged = fields.Float()
    vat = fields.Float()
    total_cost = fields.Float()
    profit_margin = fields.Float()
    overhead_price = fields.Float(string = "Total Cost + Profit Margin")

class monthly_penalties(models.Model):
    _name = 'sale.investment.monthly.penalty'
    name = fields.Char()
    date = fields.Date()
    amount = fields.Float()
    created = fields.Boolean(default = False)
    posted = fields.Boolean(default = False)
    line_ids = fields.One2many('sale.investment.monthly.penalty.lines','no')


class monthly_penalty_lines(models.Model):
    _name = 'sale.investment.monthly.penalty.lines'
    no = fields.Char()
    investor_no = fields.Char()
    investor_name = fields.Char()
    invoice_no = fields.Char()
    invoice_amount = fields.Float()
    monthly_amount = fields.Float()
    

class plot_transactions(models.Model):
    _name = 'investment.land.transactions'

    name = fields.Char(string = 'Code')
    description = fields.Char()
    attracts_vat = fields.Boolean()
    attracts_margin = fields.Boolean()

class land_overheads_setup(models.Model):
    _name = 'investment.land.transaction.costs'

    overhead = fields.Many2one('investment.land.transactions')
    description = fields.Char(readonly = True)
    based_on = fields.Selection([('flat',"Flat Rate"),('percentage',"Percentage")], default = 'flat')
    percentage = fields.Float()
    cost = fields.Float()
    

class land_overheads_setup_local(models.Model):
    _name = 'investment.land.transaction.costs.local'
    _inherit = 'investment.land.transaction.costs'

    no = fields.Char()




