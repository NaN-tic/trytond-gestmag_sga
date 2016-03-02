# This file is part gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentIn', 'ShipmentOut']
__metaclass__ = PoolMeta


class ShipmentIn:
    __name__ = 'stock.shipment.in'

    @classmethod
    def receive(cls, shipments):
        Party = Pool().get('party.party')

        super(ShipmentIn, cls).receive(shipments)

        Party.generate_gestmag_sga([s.supplier for s in shipments],
            'EXPORT_SUPPLIER')
        for shipment in shipments:
            shipment.generate_gestmag_sga()

    def generate_gestmag_sga(self):
        Gestmag = Pool().get('gestmag')

        gestmags = Gestmag.search([
            ('name', '=', 'EXPORT_SHIPMENT_IN'),
            ('warehouse', '=', self.warehouse),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = [
                'EMPRESA',
                'NUMPED',
                'NUMLIN',
                'CODALM',
                'FECHA',
                'CODART',
                'UNIDADES',
                'NUMLOTE',
                ]
            rows = [
                [
                    self.company.party.code,
                    self.code,
                    move.id,
                    self.warehouse.name.encode('utf-8'),
                    self.effective_date
                        and self.effective_date.strftime('%d%m%Y') or '',
                    move.product.code,
                    move.quantity,
                    '',  # Not implemented
                    ] for move in self.incoming_moves]
            gestmag.export_file(rows, headers)


class ShipmentOut:
    __name__ = 'stock.shipment.out'

    @classmethod
    def assign(cls, shipments):
        Party = Pool().get('party.party')

        super(ShipmentOut, cls).assign(shipments)

        Party.generate_gestmag_sga([s.customer for s in shipments],
            'EXPORT_CUSTOMER')
        for shipment in shipments:
            shipment.generate_gestmag_sga()

    def generate_gestmag_sga(self):
        Gestmag = Pool().get('gestmag')

        gestmags = Gestmag.search([
            ('name', '=', 'EXPORT_SHIPMENT_OUT'),
            ('warehouse', '=', self.warehouse),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = [
                'EMPRESA',
                'NUMENV',
                'NUMPED',
                'NUMLIN',
                'CODALM',
                'CODART',
                'UNIDADES',
                'CODCLI',
                'CODDIR',
                'EXPE',
                'PEDCLI',
                'F_PEDIDO',
                'F_ENTREGA',
                ]
            rows = [
                [
                    self.company.party.code,
                    getattr(move, 'origin', '')
                        and getattr(move.origin, 'reference', ''),
                    self.code,
                    move.id,
                    self.warehouse.name.encode('utf-8'),
                    move.product.code,
                    move.quantity,
                    self.customer.code,
                    self.delivery_address.name,
                    '',  # Not implemented
                    '',  # Not implemented
                    self.create_date.strftime('%d%m%Y'),
                    self.effective_date
                        and self.effective_date.strftime('%d%m%Y') or '',
                    ] for move in self.outgoing_moves]
            gestmag.export_file(rows, headers)
