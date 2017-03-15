===================
Getmag SGA Scenario
===================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()
    >>> yesterday = today - relativedelta(days=1)

Create database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install stock Module::

    >>> Module = Model.get('ir.module')
    >>> module, = Module.find([('name', '=', 'gestmag_sga')])
    >>> module.click('install')
    >>> Wizard('ir.module.install_upgrade').execute('upgrade')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Reload the context::

    >>> User = Model.get('res.user')
    >>> config._context = User.get_preferences(True, config.context)

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']

    >>> Journal = Model.get('account.journal')
    >>> cash_journal, = Journal.find([('type', '=', 'cash')])
    >>> cash_journal.credit_account = cash
    >>> cash_journal.debit_account = cash
    >>> cash_journal.save()

Create Customer and Supplier party::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'Product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal('20')
    >>> template.cost_price = Decimal('8')
    >>> template.save()
    >>> product.template = template
    >>> product.save()

Get stock locations::

    >>> Location = Model.get('stock.location')
    >>> warehouse_loc, = Location.find([('code', '=', 'WH')])
    >>> supplier_loc, = Location.find([('code', '=', 'SUP')])
    >>> customer_loc, = Location.find([('code', '=', 'CUS')])
    >>> output_loc, = Location.find([('code', '=', 'OUT')])
    >>> input_loc, = Location.find([('code', '=', 'IN')])
    >>> storage_loc, = Location.find([('code', '=', 'STO')])

Create Gestmag::

    >>> Gestmag = Model.get('gestmag')
    >>> gestmag_export = Gestmag(name='EXPORT_SHIPMENT_OUT', warehouse=warehouse_loc)
    >>> gestmag_export.save()
    >>> gestmag_import = Gestmag(name='EXPORT_SHIPMENT_IN', warehouse=warehouse_loc)
    >>> gestmag_import.save()

Create an Inventory::

    >>> Inventory = Model.get('stock.inventory')
    >>> Location = Model.get('stock.location')
    >>> storage, = Location.find([
    ...         ('code', '=', 'STO'),
    ...         ])
    >>> inventory = Inventory()
    >>> inventory.location = storage
    >>> inventory_line = inventory.lines.new(product=product)
    >>> inventory_line.quantity = 100.0
    >>> inventory_line.expected_quantity = 0.0
    >>> inventory.click('confirm')
    >>> inventory.state
    u'done'

Create Shipment Out::

    >>> ShipmentOut = Model.get('stock.shipment.out')
    >>> StockMove = Model.get('stock.move')
    >>> shipment_out = ShipmentOut()
    >>> shipment_out.planned_date = today
    >>> shipment_out.customer = customer
    >>> shipment_out.warehouse = warehouse_loc
    >>> shipment_out.company = company
    >>> outgoing_move = StockMove()
    >>> shipment_out.outgoing_moves.append(outgoing_move)
    >>> outgoing_move.product = product
    >>> outgoing_move.uom = unit
    >>> outgoing_move.quantity = 1
    >>> outgoing_move.from_location = output_loc
    >>> outgoing_move.to_location = customer_loc
    >>> outgoing_move.company = company
    >>> outgoing_move.unit_price = Decimal('1')
    >>> outgoing_move.currency = company.currency
    >>> shipment_out.save()
    >>> shipment_out.click('wait')
    >>> shipment_out.click('assign_try')
    True

Create Shipment In::

    >>> ShipmentIn = Model.get('stock.shipment.in')
    >>> StockMove = Model.get('stock.move')
    >>> shipment_in = ShipmentIn()
    >>> shipment_in.planned_date = today
    >>> shipment_in.supplier = supplier
    >>> shipment_in.warehouse = warehouse_loc
    >>> shipment_in.company = company
    >>> incoming_move = StockMove()
    >>> shipment_in.incoming_moves.append(incoming_move)
    >>> incoming_move.product = product
    >>> incoming_move.uom = unit
    >>> incoming_move.quantity = 1
    >>> incoming_move.from_location = input_loc
    >>> incoming_move.to_location = storage_loc
    >>> incoming_move.company = company
    >>> incoming_move.unit_price = Decimal('1')
    >>> incoming_move.currency = company.currency
    >>> shipment_in.save()
    >>> shipment_in.click('receive')
