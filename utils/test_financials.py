from . import Stockify
import unittest


class TestFinancials(unittest.TestCase):

    def test_income_statement(self):
        """Test getting the income statement is successful"""
        Stockify = Stockify('AAPL')
        Financials = Stockify.get_operating_statement()
        self.assertEqual(len(Financials['defref_us-gaap_EarningsPerShareBasic']), 9)
