import csv
import urllib.request
from os import path


class MarketAnalysis:
    """Analyze a market index vs a Stock"""
    DATA_PATH = None

    @classmethod
    def get_historical_monthly_data(cls):
        """Get CSV monthly stock data"""
        BASE_URL = "https://query1.finance.yahoo.com/v7/finance/download/%5EGSPC?period1=1440374400&period2=1598227200&interval=1mo&events=history"
        urllib.request.urlretrieve(
            BASE_URL, './utils/data.csv')

        if path.isfile('./utils/data.csv'):
            cls.DATA_PATH = './utils/data.csv'
            return cls.DATA_PATH

        else:
            return False

    def get_csv_dict(self):
        with open(self.get_historical_monthly_data(), 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            CSV_DATA = [line[1] for line in csv_reader]

            return {f"Month {i}": CSV_DATA[i] for i in range(len(CSV_DATA))}

    def get_market_average(self):
        Percentage_Over_60_Months = []
        prices = [float(i) for i in list(
            MarketAnalysis().get_csv_dict().values())[1:]]

        TotalPrices = 0
        for i in [100 * (b-a) / a for a, b in zip(prices[::1], prices[1::1])]:
            TotalPrices += i
        
        return TotalPrices/len([100 * (b-a) / a for a, b in zip(prices[::1], prices[1::1])])

    def find_recession_patterns(self):
        pass


print(MarketAnalysis().get_market_average())
