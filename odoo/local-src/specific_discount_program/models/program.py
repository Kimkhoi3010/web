# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class Program(models.Model):
    _inherit = 'sale.discount.program'

    allowed_company_ids = fields.Many2many(
        comodel_name='res.company',
    )

    @api.model
    def create(self, vals):
        """ Set promo code not combinable
        """
        if vals.get('promo_code'):
            vals['combinable'] = False
        return super(Program, self).create(vals)

    @api.multi
    def check_voucher_limits(self, sale):
        super(Program, self).check_voucher_limits(sale)

        max_vouchers = int(self.env['ir.config_parameter'].get_param(
            'voucher_max_count', '0'
        ))
        if max_vouchers:
            nb_vouchers = len(sale.program_code_ids.filtered(
                lambda p: p.voucher_amount
            ))

            if nb_vouchers > max_vouchers:
                raise UserError(
                    _("Number of vouchers is limited to %s")
                    % max_vouchers
                )

    @api.model
    def get_automatic_program(self):
        domain = [
            '&',
            ('automatic', '=', True),
            '|',
            ('allowed_company_ids', '=', False),
            ('allowed_company_ids', 'parent_of', self.env.user.company_id)
        ]

        return self.search(domain)
