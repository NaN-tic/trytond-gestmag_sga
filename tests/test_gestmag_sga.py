# This file is part of gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import (doctest_setup, doctest_teardown,
    doctest_checker)


class GestmagSGATestCase(ModuleTestCase):
    'Test Gestmag SGA module'
    module = 'gestmag_sga'

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            GestmagSGATestCase))
    suite.addTests(doctest.DocFileSuite('scenario_gestmag_sga.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
