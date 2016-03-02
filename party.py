# This file is part of gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


__all__ = ['Party', 'Address']
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'

    @classmethod
    def generate_gestmag_sga(cls, parties, role):
        pool = Pool()
        Gestmag = pool.get('gestmag')
        Company = pool.get('company.company')

        company = Company(Transaction().context.get('company'))
        company_code = company.party.code

        gestmags = Gestmag.search([
            ('name', '=', role),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = [
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
            rows = []
            for party in parties:
                address = (getattr(party, 'addresses', None)
                    and party.addresses[0])
                rows.append([
                        company_code.encode('utf-8'),
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
            gestmag.export_file(rows, headers)


class Address:
    __name__ = 'party.address'

    @classmethod
    def generate_gestmag_sga(cls, addresses):
        pool = Pool()
        Gestmag = pool.get('gestmag')
        Company = pool.get('company.company')

        company = Company(Transaction().context.get('company'))
        company_code = company.party.code

        gestmags = Gestmag.search([
            ('name', '=', 'EXPORT_ADDRESS'),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = [
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
            rows = []
            for address in addresses:
                rows.append([
                        company_code.encode('utf-8'),
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
            gestmag.export_file(rows, headers)
