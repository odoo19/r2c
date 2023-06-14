from odoo import fields, models, api, _


class CheckIn(models.Model):
    _name = 'check.in'
# class CheckIn(models.Model):
#     _inherit = 'hr.leave'

#     date_from = fields.Date()
#     date_to = fields.Date()

#     @api.onchange('date_from','date_to')
#     def _onchange_date_from_to(self):
#     	super(CheckIn, slef)._onchange_date_from_to()