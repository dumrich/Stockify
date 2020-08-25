from .Stockify import Stockify
import unittest


class TestFinancials(unittest.TestCase):
    """Test getting financial data works"""

    def setUp(self):
        self.Stock = Stockify("aApL")

    def test_IncomeStatement(self):
        """Test getting the income statement is successful"""
        Financials = self.Stock.get_operating_statement()
        self.assertIn(Financials, 'defref_us-gaap_EarningsPerShareBasic')

    def test_BalanceSheet(self):
        """Test getting the balance sheet is successful"""
        Financials = self.Stock.get_balance_sheet()
        self.assertIn(Financials, 'defref_us-gaap_NetIncomeLoss')
    

if __name__ == '__main__':
    unittest.main()
