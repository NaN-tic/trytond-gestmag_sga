#This file is part gestmag_sga module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
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
        Gestmag = Pool().get('gestmag')

        products = super(Product, cls).create(vlist)

        gestmag_products = []
        for product in products:
            if product.code:
                gestmag_products.append(product)
        if gestmag_products:
            Gestmag.export_products(gestmag_products)
        return products

    @classmethod
    def write(cls, *args):
        Gestmag = Pool().get('gestmag')

        super(Product, cls).write(*args)

        gestmag_products = []
        actions = iter(args)
        for products, values in zip(actions, actions):
            # generate xml if code or codes changed
            if values.get('code') or values.get('codes'):
                gestmag_products = products

        if gestmag_products:
            Gestmag.export_products(gestmag_products)


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
        Gestmag = pool.get('gestmag')

        products = Product.browse(Transaction().context['active_ids'])
        Gestmag.export_products(products)
        print "ara aqui"
        self.result.info = self.raise_user_error('export_info',
            (len(products)), raise_exception=False)
        return 'result'

    def default_result(self, fields):
        info_ = self.result.info
        return {
            'info': info_,
            }
