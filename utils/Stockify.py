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
       # self.OperationStatement = self.get_operation_statement_numbers()
        
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
        NetSalesID = 'Revenue'
        CostOfSalesID = 'us-gaap_CostOfGoodsAndServicesSold'
        NetMarginID = 'us-gaap_GrossProfit'
        NetIncomeID = 'us-gaap_NetIncomeLoss'
        ResearchDevelopmentID = 'us-gaap_ResearchAndDevelopmentExpense'
        SGAID = 'us-gaap_SellingGeneralAndAdministrativeExpense'
        OperatingExpensesID = "us-gaap_OperatingExpenses'"
        OperatingIncomeID = 'us-gaap_OperatingIncomeLoss'
        OtherIncomeID = 'us-gaap_NonoperatingIncomeExpense'
        IncomeBeforeProvisionIncomeTaxesID = 'us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'
        ProvisionForIncomeTaxesID = 'us-gaap_IncomeTaxExpenseBenefit'
        NetIncomeID = 'us-gaap_NetIncomeLoss'
        DilutedEPSID = 'us-gaap_EarningsPerShareDiluted'

        tag = [NetSalesID, CostOfSalesID, NetMarginID, NetIncomeID, ResearchDevelopmentID, SGAID,\
                OperatingExpensesID, OperatingIncomeID, IncomeBeforeProvisionIncomeTaxesID, ProvisionForIncomeTaxesID, NetIncomeID,DilutedEPSID]

        OperatingDict = {'StockName': self.ticker, 'EPS':self.EPSList, NetSalesID:[], CostOfSalesID:[], NetMarginID: [], NetIncomeID:[], ResearchDevelopmentID:[],\
                SGAID: [], OperatingExpensesID:[], OperatingIncomeID: [], IncomeBeforeProvisionIncomeTaxesID:[], ProvisionForIncomeTaxesID:[], NetIncomeID:[], DilutedEPSID:[], \
                }
        for url in list(self.url_dict.values())[:9]:
            accession_number = url.split('&')[2][17:].replace('-', '')
            
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')\
                        .prettify()



                for i in tag:
                   
                    OperatingDict[i].append(soup.split(i)[1].split("\n")[5].strip())
            except:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')\
                        .prettify()



                for i in tag:
                    OperatingDict[i].append(soup.split(i)[1].split("\n")[5].strip())

        return OperatingDict 
        




    def get_historical_stock_prices(self):
        pass


print(Stockify('msft').get_10K_links())

