# This file is part of gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


__all__ = ['Party', 'Address']


class Party:
    __metaclass__ = PoolMeta
    __name__ = 'party.party'

    @classmethod
    def gestmag_sga_headers(cls):
        'Return header CSV'
        return [
            'EMPRESA',
            'CODCLI',
            'NOMCOM',
            'NOMFISCAL',
            'NIF',
            'DIR',
            'CP',
            'POBL',
            'PROV',
            'PAIS',
            ]

    @classmethod
    def gestmag_sga_rows(cls, company, parties):
        'Return rows CSV'
        rows = []
        for party in parties:
            address = (getattr(party, 'addresses', None)
                and party.addresses[0])
            rows.append([
                    company.party.code.encode('utf-8'),
                    party.code.encode('utf-8'),
                    party.name.encode('utf-8'),
                    '',
                    party.vat_code if party.vat_code else '',
                    address.street.encode('utf-8')
                        if address and address.street else '',
                    address.zip.encode('utf-8')
                        if address and address.zip else '',
                    address.city.encode('utf-8')
                        if address and address.city else '',
                    address.subdivision.name.encode('utf-8')
                        if address and address.subdivision
                            and address.subdivision.name else '',
                    address.country.name.encode('utf-8')
                        if address and address.country
                            and address.country.name else '',
                    ])
        return rows

    @classmethod
    def generate_gestmag_sga(cls, parties, role='EXPORT_CUSTOMER'):
        pool = Pool()
        Gestmag = pool.get('gestmag')
        Company = pool.get('company.company')

        company = Company(Transaction().context.get('company'))

        gestmags = Gestmag.search([
            ('name', '=', role),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = cls.gestmag_sga_headers()
            rows = cls.gestmag_sga_rows(company, parties)
            gestmag.export_file(rows, headers)


class Address:
    __metaclass__ = PoolMeta
    __name__ = 'party.address'

    @classmethod
    def gestmag_sga_headers(cls):
        'Return header CSV'
        return [
            'EMPRESA',
            'CODCLI',
            'CODDIR',
            'NOMCOM',
            'DIR',
            'CP',
            'POBL',
            'PROV',
            'PAIS',
            ]

    @classmethod
    def gestmag_sga_rows(cls, company, addresses):
        'Return rows CSV'
        rows = []
        for address in addresses:
            rows.append([
                    company.party.code.encode('utf-8'),
                    address.party.code.encode('utf-8'),
                    address.name.encode('utf-8'),
                    address.party.name.encode('utf-8'),
                    address.street.encode('utf-8')
                        if address and address.street else '',
                    address.zip.encode('utf-8')
                        if address and address.zip else '',
                    address.city.encode('utf-8')
                        if address and address.city else '',
                    address.subdivision.name.encode('utf-8')
                        if address and address.subdivision
                            and address.subdivision.name else '',
                    address.country.name.encode('utf-8')
                        if address and address.country
                            and address.country.name else '',
                    ])
        return rows

    @classmethod
    def generate_gestmag_sga(cls, addresses):
        pool = Pool()
        Gestmag = pool.get('gestmag')
        Company = pool.get('company.company')

        company = Company(Transaction().context.get('company'))

        gestmags = Gestmag.search([
            ('name', '=', 'EXPORT_ADDRESS'),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = cls.gestmag_sga_headers()
            rows = cls.gestmag_sga_rows(company, addresses)
            gestmag.export_file(rows, headers)
