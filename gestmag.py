# This file is part of gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from csv import writer, QUOTE_MINIMAL
from datetime import datetime
from trytond.model import ModelView, ModelSQL, fields
import os

from trytond.pool import Pool


__all__ = ['Gestmag']


class Gestmag(ModelSQL, ModelView):
    'Gestmag'
    __name__ = 'gestmag'
    name = fields.Char('Name', required=True)
    warehouse = fields.Many2One('stock.location', "Warehouse",
        domain=[('type', '=', 'warehouse')],
        help='Gestmag SGA Warehouse Manager', required=True)
    path = fields.Char('Path', required=True)
    active = fields.Boolean('Active', select=True)

    @classmethod
    def create(cls, vlist):
        for value in vlist:
            if 'path' in value and not value['path'].endswith('/'):
                value['path'] = '%s/' % value['path']
        return super(Gestmag, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for gestmags, values in zip(actions, actions):
            if 'path' in values and not values['path'].endswith('/'):
                values['path'] = '%s/' % values['path']
            args.extend((gestmags, values))
        super(Gestmag, cls).write(*args)

    @classmethod
    def default_warehouse(cls):
        Location = Pool().get('stock.location')
        locations = Location.search(cls.warehouse.domain)
        if locations:
            return locations[0].id

    @staticmethod
    def default_path():
        return os.path.dirname(__file__) + '/'

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
        file_name = '%s%s_%s.csv' % (self.path, self.name.lower(),
            datetime.today().strftime('%Y%m%d%H%M%S%f'))
        with open(file_name, 'w') as csv_file:
            csv = writer(csv_file, quoting=QUOTE_MINIMAL, delimiter=';')
            if headers:
                csv.writerow(headers)
            csv.writerows(rows)
