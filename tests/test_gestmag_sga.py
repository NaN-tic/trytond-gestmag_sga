# This file is part of the gestmag_sga module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class GestmagSGATestCase(ModuleTestCase):
    'Test Gestmag SGA module'
    module = 'gestmag_sga'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        GestmagSGATestCase))
    return suite
