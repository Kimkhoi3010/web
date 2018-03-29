# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    import html2text
except ImportError:
    _logger.warning('could not import html2text')
    html2text = None


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    comment_text = fields.Text(
        string='Description as text',
        compute='_compute_comment_text',
        readonly=True,
    )

    @api.depends('comment')
    def _compute_comment_text(self):
        if html2text is None:
            return
        for invoice in self:
            invoice.comment_text = html2text.HTML2Text().handle(
                invoice.comment or ''
            ).strip()

    @api.multi
    def action_invoice_sent(self):
        template = self.env.ref(
            'mtsmte_reports.email_template_edi_invoice_specific'
        )
        res = super(AccountInvoice, self).action_invoice_sent()
        ctx = res.get('context', {})
        ctx['default_template_id'] = template.id
        res['context'] = ctx
        return res
