# See LICENSE file for full copyright and licensing details
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class safety_certificate(models.AbstractModel):
    _name = 'report.property_management.report_safety_certificate'
    _description = 'Safety Certificate'

    def get_details(self, start_date, end_date):
        data_1 = []
        certificate_obj = self.env["property.safety.certificate"]
        certificate_ids = certificate_obj.search(
            [('expiry_date', '>=', start_date),
             ('expiry_date', '<=', end_date)])
        for data in certificate_ids:
            user_lang = self.env.user.lang
            lang = self.env['res.lang'].search(
                [('code', '=', user_lang)])
            if data.expiry_date:
                date = data.expiry_date.strftime(lang.date_format)
            data_1.append({
                'name': data.name,
                'property_id': data.property_id.name,
                'contact_id': data.contact_id.name,
                'expiry_date': date,
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

        data_res = self.with_context(
            data['form'].get('used_context', {})).get_details(
                start_date, end_date)
        docargs = {
            'doc_ids': docids,
            'doc_model':'account.asset.asset',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_details': data_res,
            'date_format': self.date_format,
        }
        docargs['data'].update({
            'end_date': self.date_format(docargs.get('data').get('end_date')),
            'start_date': self.date_format(docargs.get('data').get(
                'start_date'))})
        return docargs
