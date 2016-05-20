# -*- coding: utf-8 -*-
@depiltech @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @no_login
  Scenario: CREATE DATABASE
    Given I find or create database from config file

  @company
  Scenario: SETUP company informations
    Given I need a "res.company" with oid: base.main_company
    And having
       | key        | value      |
       | name       | Depil'Tech |
    # Given the company has the "images/logo.png" logo

  @lang
  Scenario: install lang
   Given I install the following language :
      | lang  |
      | fr_FR |
    Then the language should be available
   Given I find a "res.lang" with code: fr_FR
    And having:
      | key         | value    |
      | grouping    | [3,0]    |
      | date_format | %d/%m/%Y |

  @modules
  Scenario: install modules
    Given I install the required modules with dependencies:
        | name                    |
        # oca/ocb
        | document                |
        | account                 |
        | sale                    |
        | sale_stock              |
        | stock                   |
        | purchase                |
        # OCA/server-tools
        #| disable_openerp_online  |
        # local-src
