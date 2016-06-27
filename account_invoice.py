from openerp import fields, api, models
from openerp.exceptions import ValidationError
from datetime import datetime

class invoice(models.Model):

    _inherit = 'account.invoice'

    schedule_ids = fields.One2many('account.invoice.repayment.schedule','invoice_id', readonly = True)
    installments = fields.Integer(default = 1)
    amount_due = fields.Float(compute = 'compute_dues')

    @api.one
    def generate_schedule(self):
        self.schedule_ids.unlink()
        installment_amount = 0.0
        schedule = []
        installment_amount = self.amount_total/self.installments
        schedule = [installment_amount for installment in range(1,self.installments + 1)]
        due_date = self.date_due
        installment = 0
        balance = self.amount_total
        repayment_schedule = self.env['account.invoice.repayment.schedule']
        for entry in schedule:
            installment += 1
            due_date = next_date(due_date)
            repayment_schedule.create({'invoice_id':self.id,'installment':installment, 'date_due':due_date,
                'balance':balance, 'installment_amount':entry})
            balance -= entry

    @api.one
    @api.depends('schedule_ids')
    def compute_dues(self):
        total = 0.0
        paid = self.amount_total - self.residual
        due = 0.0
        for line in self.schedule_ids:
            total += line.installment_amount
            #if total < paid:
            #    line.paid = True
            #else:
            #    line.paid = False

            #calculate dues
            if datetime.strptime(line.date_due, '%Y-%m-%d') <= datetime.now():# and line.paid == False
                due += line.installment_amount
                line.due = True
        if ((due-paid)>0):
            self.amount_due = due - paid #this is the true due amount




    @api.multi
    def check_product_state(self):
        for line in self.invoice_line:
            if line.product_id:#avoid singleton error when no product is selected on lines
                if line.product_id.product_category == 'land':
                    line.product_id.sale_ok = False
                    line.product_id.purchase_ok = False
                    line.product_id.status = 'sold'

class account_invoice_repayment_schedule(models.Model):
    _name = 'account.invoice.repayment.schedule'

    invoice_id = fields.Many2one('account.invoice')
    installment = fields.Integer()
    date_due = fields.Date()
    balance = fields.Float()
    installment_amount = fields.Float()
    due = fields.Boolean(compute = 'mark_as_paid')
    paid = fields.Boolean(compute = 'mark_as_paid')#

    @api.one
    @api.depends('invoice_id')
    def mark_as_paid(self):
        total = 0.0
        paid = self.invoice_id.amount_total - self.invoice_id.residual
        for line in self.invoice_id.schedule_ids:
            total += line.installment_amount
            if total < paid:
                line.paid = True
            else:
                line.paid = False

            if datetime.strptime(line.date_due, '%Y-%m-%d') <= datetime.now():
                line.due = True


def next_date(startdate_param):
        """
        This next function calculates the next month with same date. If that date is larger than available dates for the
        following month, it gets the maximum date for that month:::>>>Author:dennokorir
        """
        #we create a dictionary for months against their max days
        months_structure = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        #start calculation
        start_date = datetime.strptime(str(startdate_param),'%Y-%m-%d').date()#start_date
        current_month = start_date.month
        current_year = start_date.year
        next_month = 0
        next_year = current_year
        if current_month == 12:
            next_month = 1
            next_year += 1
        else:
            next_month = current_month + 1

        #routine to ensure we do not exceed the number of days in the next month
        end_day = start_date
        current_day = start_date.day
        if current_day < months_structure[next_month]:
            end_day = start_date.replace(month = next_month, year = next_year)
        else:
            end_day = start_date.replace(day=months_structure[next_month],month=next_month, year = next_year)#months_structure[next_month] returns max days of next month
            #end_day = start_date.replace(month=next_month)
        return end_day
