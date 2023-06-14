# See LICENSE file for full copyright and licensing details
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.tools import ustr


class TenancyDetailProperty(models.AbstractModel):
    _name = 'report.property_management.report_tenancy_by_property'
    _description = 'Tenancy by Property'

    def get_details(self, start_date, end_date, property_id):
        data_1 = []
        tenancy_obj = self.env["account.analytic.account"]
        tenancy_ids = tenancy_obj.search([
            ('property_id', '=', property_id[0]),
            ('date_start', '>=', start_date),
            ('date', '<=', end_date),
            ('resident_type', '=', 'tenant_tenancy')])
        for data in tenancy_ids:
            if data.currency_id:
                cur = data.currency_id.symbol
            user_lang = self.env.user.lang
            lang = self.env['res.lang'].search(
                [('code', '=', user_lang)])
            if data.date_start:
                date_start = data.date_start.strftime(lang.date_format)
            if data.date:
                date = data.date.strftime(lang.date_format)
            data_1.append({
                'name': data.name,
                'tenant_id': data.tenant_id.name,
                'date_start': date_start,
                'date': date,
                'rent': cur + ustr(data.rent),
                'rent_type_id': data.rent_type_id.name,
                'rent_type_month': data.rent_type_id.renttype,
                'state': data.state
            })
        return data_1

    def date_format(self, date):
        from_date = datetime.strptime(date, '%Y-%m-%d')
        user_lang = self.env.user.lang
        lang = self.env['res.lang'].search(
            [('code', '=', user_lang)])
        if from_date:
            final_from_date = from_date.strftime(lang.date_format)
        return final_from_date

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.asset.asset'].browse(docids)
        start_date = data['form'].get('start_date', fields.Date.today())
        end_date = data['form'].get(
            'end_date', str(datetime.now() + relativedelta(
                months=+1, day=1, days=-1))[:10])
        property_id = data['form'].get('property_id')

        detail_res = self.with_context(
            data['form'].get('used_context', {})).get_details(
            start_date, end_date, property_id)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.asset.asset',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_details': detail_res,
        }
        docargs['data'].update({
            'end_date': self.date_format(docargs.get('data').get('end_date')),
            'start_date': self.date_format(docargs.get('data').get(
                'start_date'))})
        return docargs
