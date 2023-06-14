# See LICENSE file for full copyright and licensing details

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Account Entry"

    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')
    new_tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy ')
    schedule_date = fields.Date(
        string='Schedule Date',
        help='Rent Schedule Date.')
    source = fields.Char(
        string='Account Source',
        help='Source from where account move created.')

    def assert_balanced(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        if self.ids:
            self._cr.execute("""
                SELECT move_id FROM account_move_line WHERE move_id in %s
                GROUP BY move_id HAVING abs(sum(debit) - sum(credit)) > %s
                """, (tuple(self.ids), 10 ** (-max(5, prec))))
            if self._cr.fetchall():
                raise UserError(_("Cannot create unbalanced journal entry."))
        return True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Tenancy',
        help='Tenancy Name.')


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy',
        help='Tenancy Name.')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')
    is_deposit = fields.Boolean(
        string='Is Deposit Received?')
    is_return = fields.Boolean(
        string='Is Deposit Returned?')

    @api.model
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        context = dict(self._context) or {}
        active_id = self.env[context.get('active_model')].browse(
            context.get('active_id'))
        if active_id:
            res['property_id'] = active_id.property_id.id or False
            res['tenancy_id'] = active_id.new_tenancy_id.id or False
        return res

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super()._create_payment_vals_from_wizard(batch_result)
        context = dict(self._context) or {}
        if 'return' in context and context.get('return') and self.is_return:
            res.update({
                'is_return': self.is_return
            })
            
        if 'return' not in context and not context.get('return'):
            res.update({
                'property_id': self.property_id.id,
                'tenancy_id': self.tenancy_id.id,
                'is_deposit': self.is_deposit,
                })
        return res


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy',
        help='Tenancy Name.')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')
    amount_due = fields.Monetary(
        comodel_name='res.partner',
        related='partner_id.credit',
        readonly=True,
        help='Display Due amount of Customer')
    is_deposit = fields.Boolean(
        string='Is Deposit Received?')
    is_return = fields.Boolean(
        string='Is Deposit Returned?')

    def action_post(self):
        res = super().action_post()
        invoice_obj = self.env['account.move']
        context = dict(self._context) or {}
        for rec in self:
            if context.get('return'):
                invoice_browse = invoice_obj.browse(
                    context.get('active_id')).new_tenancy_id
                invoice_browse.write({'amount_return': rec.amount})
            if context.get('deposite_received'):
                tenancy_active_id = \
                    self.env['account.analytic.account'].browse(
                        context.get('active_id'))
                tenancy_active_id.write({'amount_return': rec.amount})
        return res

    @api.model
    def create(self, vals):
        res = super(AccountPayment, self).create(vals)
        context = dict(self._context) or {}
        if res and res.id and res.tenancy_id and res.tenancy_id.id:
            if res.payment_type == 'inbound' and context.get('deposite_received'):
                res.tenancy_id.write({'acc_pay_dep_rec_id': res.id})
            if res.payment_type == 'outbound' and (context.get('return') or context.get('deposite_pay')):
                res.tenancy_id.write({'acc_pay_dep_ret_id': res.id})
        return res

    def _prepare_move_line_default_vals(self, write_off_line_vals):
        result = super()._prepare_move_line_default_vals(write_off_line_vals)
        context = dict(self._context) or {}
        for line in result:
            if not self.move_id.property_id:
                self.move_id.property_id = self.property_id.id or False
            if context.get('deposit_received') and line.get('debit') > 0 and self.tenancy_id.id:
                if self.payment_type in ('inbound', 'outbound'):
                    line.update({
                        'analytic_account_id': self.tenancy_id.id,
                        'property_id': self.property_id.id
                        })
        return result

    def _seek_for_lines(self):
        rec = super(AccountPayment, self)._seek_for_lines()
        if rec and rec[1] and self.tenancy_id and self.tenancy_id.id:
            if self.payment_type in ('inbound', 'outbound'):
                rec[1].update({'analytic_account_id': self.tenancy_id.id, 'property_id': self.property_id.id})
        return rec
