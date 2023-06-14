# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
