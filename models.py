# -*- coding: utf-8 -*-

from openerp import models, fields, api

class investor_registration(models.Model):
    _name = 'investment.investor.registration'
    _inherit = 'res.partner'

    investor = fields.Boolean(default = True)

    @api.one
    def create_investor(self):
        pass #create a duplicate entry on res.partner


class investor(models.Model):
    _inherit = 'res.partner'

    investor = fields.Boolean()

