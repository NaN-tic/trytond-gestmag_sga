# This file is part of gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
from csv import writer, QUOTE_MINIMAL
from datetime import datetime
from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields
from trytond.config import config as config_
from trytond import backend

__all__ = ['Gestmag']

GESTMAG_PATH = config_.get('gestmag_sga', 'path', default='/tmp')


class Gestmag(ModelSQL, ModelView):
    'Gestmag'
    __name__ = 'gestmag'
    name = fields.Char('Name', required=True)
    warehouse = fields.Many2One('stock.location', "Warehouse",
        domain=[('type', '=', 'warehouse')],
        help='Gestmag SGA Warehouse Manager', required=True)
    path = fields.Char('Path',
        help='Use other directory path that global configuration')
    active = fields.Boolean('Active', select=True)

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        table = TableHandler(cls, module_name)

        super(Gestmag, cls).__register__(module_name)
        table.not_null_action('path', 'remove')

    @classmethod
    def default_warehouse(cls):
        Location = Pool().get('stock.location')
        locations = Location.search(cls.warehouse.domain)
        if locations:
            return locations[0].id

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

    def export_file(self, rows, headers=None):
        '''
        :param rows: List of lists with values of the csv file
        :param headers: List of column headers of the csv file
        '''
        path = self.path if self.path else GESTMAG_PATH
        file_name = '%s/%s_%s.csv' % (path, self.name.lower(),
            datetime.today().strftime('%Y%m%d%H%M%S%f'))
        with open(file_name, 'w') as csv_file:
            csv = writer(csv_file, quoting=QUOTE_MINIMAL, delimiter=';')
            if headers:
                csv.writerow(headers)
            csv.writerows(rows)
