#This file is part gestmag_sga module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import  ModelView, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.wizard import Wizard, StateView, Button, StateTransition

__all__ = ['ShipmentIn', 'ShipmentOut', 'ShipmentInternal']
__metaclass__ = PoolMeta


class ShipmentIn:
    __name__ = 'stock.shipment.in'

    @classmethod
    def assign(cls, shipments):
        super(ShipmentOut, cls).assign(shipments)
        # control generate systemlogics module with context
        if Transaction().context.get('generate_gestmag_sga', True):
            cls.generate_gestmag_sga(shipments)

    @classmethod
    def generate_gestmag_sga(cls, shipments):
        '''Create Gestmag SGA Shipment IN CSV'''
        Gestmag = Pool().get('gestmag')
        Gestmag.import_shipments(products)

    @classmethod
    def receive(cls, shipments):
        super(ShipmentOut, cls).receive(shipments)
        cls.generate_gestmag_sga(shipments)


class ShipmentOut:
    __name__ = 'stock.shipment.out'

    @classmethod
    def generate_gestmag_sga(cls, shipments):
        '''Create Gestmag SGA Shipment OUT CSV'''
        Gestmag = Pool().get('gestmag')
        Gestmag.export_shipments(products)

    @classmethod
    def assign(cls, shipments):
        super(ShipmentOut, cls).assign(shipments)
        # control generate systemlogics module with context
        if Transaction().context.get('generate_gestmag_sga', True):
            cls.generate_gestmag_sga(shipments)


class ShipmentInternal:
    __name__ = 'stock.shipment.internal'

    @classmethod
    def generate_gestmag_sga(cls, shipments):
        '''Create Gestmag SGA Shipment Internal CSV'''
        Gestmag = Pool().get('gestmag')
        Gestmag.export_shipments(products)

    @classmethod
    def assign(cls, shipments):
        super(ShipmentInternal, cls).assign(shipments)
        cls.generate_gestmag_sga(shipments)
