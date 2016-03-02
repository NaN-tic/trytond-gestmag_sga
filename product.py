#This file is part gestmag_sga module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from datetime import datetime
from trytond.model import ModelView, fields

from trytond.pool import Pool, PoolMeta
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction

__all__ = ['Product', 'GestmagProduct', 'GestmagProductResult']
__metaclass__ = PoolMeta


class Product:
    __name__ = 'product.product'

    @classmethod
    def create(cls, vlist):
        products = super(Product, cls).create(vlist)
        cls.generate_gestmag_sga(products)
        return products

    @classmethod
    def write(cls, *args):
        super(Product, cls).write(*args)
        actions = iter(args)
        for products, _ in zip(actions, actions):
            cls.generate_gestmag_sga(products)

    @classmethod
    def generate_gestmag_sga(cls, products):
        pool = Pool()
        Gestmag = pool.get('gestmag')
        Company = pool.get('company.company')

        company = Company(Transaction().context.get('company'))
        company_code = company.party.code
        today = datetime.today().strftime('%d%m%Y')

        gestmags = Gestmag.search([
            ('name', '=', 'EXPORT_PRODUCT'),
            ])
        if gestmags:
            gestmag = gestmags[0]
            headers = [
                'EMPRESA',
                'CODFAM',
                'CODSUBFAM',
                'CODART',
                'DESCR',
                'EAN_ART',
                'EAN_UV',
                'TIPO_UT',
                'UTxUV',
                'T_PAL',
                'UxP',
                'PBxU',
                'C_ALTO',
                'C_ANCHO',
                'C_FONDO',
                'F_ACT',
                ]
            rows = []
            for product in products:
                template = product.template
                rows.append([
                        company_code.encode('utf-8'),
                        template.category.parent.name.encode('utf-8')
                            if template.category and template.category.parent
                            else '',
                        template.category.name.encode('utf-8')
                            if template.category else '',
                        product.code.encode('utf-8') if product.code else '',
                        template.name.encode('utf-8'),
                        product.code_ean13 or ''
                        '',  # Not implemented
                        template.default_uom.name,
                        template.sale_uom.factor
                            if template.sale_uom and template.sale_uom.factor
                            else '',
                        template.sale_uom.name
                            if template.sale_uom else '',
                        0,  # Not implemented
                        0,  # Not implemented
                        0,  # Not implemented
                        0,  # Not implemented
                        0,  # Not implemented
                        0,  # Not implemented
                        today,
                        ])
            gestmag.export_file(rows, headers)


class GestmagProductResult(ModelView):
    'Gestmag Product Result'
    __name__ = 'gestmag.product.result'
    info = fields.Text('Info', readonly=True)


class GestmagProduct(Wizard):
    'Gestmag Product'
    __name__ = 'gestmag.product'
    start_state = 'export'

    export = StateTransition()
    result = StateView('gestmag.product.result',
        'gestmag_sga.gestmag_product_result', [
            Button('Close', 'end', 'tryton-close'),
            ])

    @classmethod
    def __setup__(cls):
        super(GestmagProduct, cls).__setup__()
        cls._error_messages.update({
                'export_info': 'Exported %s product/s to Gestmat SGA',
                })

    def transition_export(self):
        pool = Pool()
        Product = pool.get('product.product')

        products = Product.browse(Transaction().context['active_ids'])
        Product.generate_gestmag_sga(products)

        self.result.info = self.raise_user_error('export_info',
            (len(products)), raise_exception=False)
        return 'result'

    def default_result(self, fields):
        info_ = self.result.info
        return {
            'info': info_,
            }
