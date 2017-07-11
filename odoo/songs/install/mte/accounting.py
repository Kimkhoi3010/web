# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update
from . import mte_vars
from ...common import load_chart_of_accounts


@anthem.log
def set_fiscalyear(ctx):
    for year in ['2010', '2011', '2012', '2013', '2014', '2015', '2016',
                 '2017', '2018']:
        values = {'date_start': year + '-01-01',
                  'name': year,
                  'date_end': year + '-12-31',
                  'type_id': 1,
                  'company_id': ctx.env.ref('__setup__.company_mte').id,
                  'active': True,
                  }
        create_or_update(ctx, 'date.range',
                         '__setup__.date_range_mte_' + year, values)


@anthem.log
def configure_chart_of_account(ctx):
    """Configure COA for companies"""
    account_settings = ctx.env['account.config.settings']

    for company_xml_id, coa in mte_vars.coa_dict.iteritems():
        company = ctx.env.ref(company_xml_id)
        with ctx.log("Import basic CoA for %s:" % company.name):
            vals = {'company_id': company.id,
                    'chart_template_id': ctx.env.ref(coa).id,
                    }
            acs = account_settings.create(vals)
            acs.onchange_chart_template_id()
            acs.execute()


@anthem.log
def import_chart_of_account(ctx):
    """ Customize accounts """
    load_chart_of_accounts(ctx, '__setup__.company_mte',
                           'data/install/mte/account.account.csv')


@anthem.log
def set_currency_update(ctx):
    """ Configure currency update """
    ctx.env['account.config.settings'].create(
        {'currency_interval_unit': 'monthly',
         'currency_provider': 'ecb',
         }
    ).execute()


@anthem.log
def main(ctx):
    """ Configuring accounting """
    set_fiscalyear(ctx)
    configure_chart_of_account(ctx)
    import_chart_of_account(ctx)
    set_currency_update(ctx)
