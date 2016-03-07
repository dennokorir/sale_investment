from openerp import models, fields, api

class investor_next_of_kin(models.Model):
	_inherit = 'next.of.kin'

	investor_id = fields.Many2one('res.partner')

class investor(models.Model):
	_inherit = 'res.partner'

	next_of_kin_ids = fields.One2many('next.of.kin','investor_id')

