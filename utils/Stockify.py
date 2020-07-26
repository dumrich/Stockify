from bs4 import BeautifulSoup
import requests
import re


class Stockify:
    """Stockify class to scrape EGDAR and get data"""
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.headers = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
        self.CIK = self.get_CIK()
        self.base_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self.CIK}&type=10-K&dateb=&owner=include&count=40&search_text="
        self.url_keys = ['year 1','year 2','year 3','year 4','year 5','year 6','year 7','year 8',\
                   'year 9','year 10',]
        self.url_dict = self.get_10K_links()
        self.EPSList = self.get_EPS()
        self.OperationStatement = self.get_operation_statement_numbers()
        self.NetSalesID = 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax'
        self.CostOfSalesID = 'defref_us-gaap_CostOfGoodsAndServicesSold'
        self.NetMarginID = 'defref_us-gaap_GrossProfit'
        self.NetIncomeID = 'defref_us-gaap_NetIncomeLoss'
        self.ResearchDevelopmentID = 'defref_us-gaap_ResearchAndDevelopmentExpense'
        self.SGAID = 'defref_us-gaap_SellingGeneralAndAdministrativeExpense'
        self.OperatingExpensesID = 'defref_us-gaap_OperatingExpenses'
        self.OperatingIncome = 'defref_us-gaap_OperatingIncomeLoss'
        self.OtherIncome = 'defref_us-gaap_NonoperatingIncomeExpense'
        self.IncomeBeforeProvisionIncomeTaxesID = 'defref_us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'
        self.ProvisionFOrIncomeTaxesID = 'defref_us-gaap_IncomeTaxExpenseBenefit'
        self.NetIncomeId = 'defref_us-gaap_NetIncomeLoss'
        self.DilutedEPSID = 'defref_us-gaap_EarningsPerShareDiluted'
        self.TotalNetSalesID = 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax'
        
    def get_CIK(self):
        """Get the SEC CIK"""
        url = f"https://sec.report/Ticker/{self.ticker}"
        request = {'url': url, }
        soup = BeautifulSoup(requests.get(request['url'], \
                                          headers={'User-Agent':self.headers}).content, 'lxml')

        return(soup.h2.text.split()[-1])

    def get_10K_links(self):
        """Get all 10K links"""
        request = {'url': self.base_url, 'User-Agent': self.headers}
        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')

        url_list = [a.get('href') for a in soup.find_all('a', id='interactiveDataBtn')][:10]
        return {self.url_keys[i]: 'https://www.sec.gov'+url_list[i] for i in range(len(self.url_keys))}

    def get_EPS(self):
        """Get the EPS"""
        EPSList = []

        for url in list(self.url_dict.values())[:9]:
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')\
                        .prettify().split('defref_us-gaap_EarningsPerShareBasic')[1].split("\n")[5].strip()
                EPSList.append(soup.strip(' '))
            except:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')\
                       .prettify().split('defref_us-gaap_EarningsPerShareBasic')[1].split("\n")[5].strip()

                EPSList.append(soup.strip(' '))


        return [item for item in EPSList if item[0] == '$']

    def get_operation_statement_numbers(self):
        NetSalesID = 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax'
        CostOfSalesID = 'defref_us-gaap_CostOfGoodsAndServicesSold'
        NetMarginID = 'defref_us-gaap_GrossProfit'
        NetIncomeID = 'defref_us-gaap_NetIncomeLoss'
        ResearchDevelopmentID = 'defref_us-gaap_ResearchAndDevelopmentExpense'
        SGAID = 'defref_us-gaap_SellingGeneralAndAdministrativeExpense'
        OperatingExpensesID = 'defref_us-gaap_OperatingExpenses'
        OperatingIncome = 'defref_us-gaap_OperatingIncomeLoss'
        OtherIncome = 'defref_us-gaap_NonoperatingIncomeExpense'
        IncomeBeforeProvisionIncomeTaxesID = 'defref_us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'
        ProvisionFOrIncomeTaxesID = 'defref_us-gaap_IncomeTaxExpenseBenefit'
        NetIncomeId = 'defref_us-gaap_NetIncomeLoss'
        DilutedEPSID = 'defref_us-gaap_EarningsPerShareDiluted'
        TotalNetSalesID = 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax'
        

        for url in list(self.url_dict.values())[:9]:
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')\
                        .prettify().split()[1].split("\n")[5].strip()
                EPSList.append(soup.strip(' '))
            except:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')\
                        .prettify().split((NetSalesID, CostOfSalesID, NetMarginID, NetIncomeId, ResearchDevelopmentID, SGAID, OperatingExpensesID, OperatingIncome, OtherIncome, IncomeBeforeProvisionIncomeTaxesID, ProvisionFOrIncomeTaxesID, NetIncomeId, DilutedEPSID, TotalNetSalesID))[1].split("\n")[5].strip()

                EPSList.append(soup.strip(' '))

        return [item for item in EPSList if item[0] == '$']
9



    def get_historical_stock_prices(self):
        pass


print(Stockify('amzn').get_EPS())

