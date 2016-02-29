#This file is part gestmag_sga module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.rpc import RPC
from itertools import groupby
from xml.dom.minidom import parseString
import os
import operator
import logging
import datetime
import tempfile

__all__ = ['Gestmag']


class Gestmag(ModelSQL, ModelView):
    'Gestmag'
    __name__ = 'gestmag'
    name = fields.Char('Name', required=True)
    warehouse = fields.Many2One('stock.location', "Warehouse",
        domain=[('type', '=', 'warehouse')],
        help='System Logics Warehouse', required=True)
    path = fields.Char('Path', required=True)
    active = fields.Boolean('Active', select=True)

    @classmethod
    def default_warehouse(cls):
        Location = Pool().get('stock.location')
        locations = Location.search(cls.warehouse.domain)
        if locations:
            return locations[0].id

    @staticmethod
    def default_path():
        return os.path.dirname(__file__)

    @staticmethod
    def default_active():
        return True

    @classmethod
    def check_xml_record(cls, records, values):
        return True

    @classmethod
    def import_shipments(self, shipments):
        '''Export shipments'''
        # TODO + watch dir

    @classmethod
    def export_shipments(self, shipments):
        '''Export shipments'''
        # TODO

    @classmethod
    def export_products(self, products):
        '''Export products'''
        # TODO
