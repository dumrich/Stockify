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
    #    self.url_dict = self.get_10K_links()
        self.OperatingDict = {'Ticker': self.ticker, 'DilutedEPS': [], 'BasicEPS':[], 'TotalNetSales':[], 'TotalCostOfSales':[], 'TotalMargin':[], \
                'R&D':[], 'SG&A':[], 'TotalOperatingExpenses':[], 'OperatingIncome':[], 'IncomeBeforeTaxes': [], 'IncomeAfterTaxes':[]}
        self.BalanceDict = {'Ticker':self.ticker}
        self.CashFlowDict = {'Ticker':self.ticker}

    def get_CIK(self):
        """Get the SEC CIK"""
        url = f"https://sec.report/Ticker/{self.ticker}"
        request = {'url': url, }
        soup = BeautifulSoup(requests.get(request['url'], \
                                          headers={'User-Agent':self.headers}).content, 'lxml')

        return (soup.h2.text.split()[-1].lstrip('0'))

    def get_10K_links(self):
        """Get all 10K links"""
        request = {'url': self.base_url, 'User-Agent': self.headers}
        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')

        url_list = [a.get('href') for a in soup.find_all('a', id='interactiveDataBtn')][:11]
        return {self.url_keys[i]: 'https://www.sec.gov'+url_list[i] for i in range(len(self.url_keys))}

    def get_operating_statement(self):
        """Get operating statement numbers from SEC"""
        OperatingDict = {'Ticker':self.ticker}

        for i, url in enumerate(list(self.get_10K_links().values())[0:-1:3]):
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                
                if '12 months ended' not in soup.prettify().lower():
                    raise IndexError('Incorrect URL. Trying R3 Form')

                all_data = []
                for tr in soup.select('tr'):
                    tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                    if len(tds) == 4:
                        tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                        tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                        all_data.append(tds)

                for row in all_data:
                    print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                    if i==0:
                        OperatingDict[row[0]] = row[1:]
                    try:
                        OperatingDict[row[0]].extend(row[1:])
                    except KeyError:
                        OperatingDict[row[0]] = row[1:]
            
            except IndexError:
                try:
                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                    request = {'url': BASE_URL, 'User-Agent': self.headers}
                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                    
                    if '12 months ended' not in soup.prettify().lower():
                        raise ValueError('Incorrect URL. Trying R4 Form')


                    all_data = []
                    for tr in soup.select('tr'):
                        tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                        if len(tds) == 4:
                            tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                            tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                            all_data.append(tds)

                    for row in all_data:
                        print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                        if i==0:
                            OperatingDict[row[0]] = row[1:]
                        try:
                            OperatingDict[row[0]].extend(row[1:])
                        except KeyError:
                            OperatingDict[row[0]] = row[1:]                

                except IndexError:
                    try:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R4.htm"
                        request = {'url': BASE_URL, 'User-Agent': self.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if '12 months ended' not in soup.prettify().lower():
                            raise NameError('Incorrect URL. Trying R5 form')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 4:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                            if i==0:
                                OperatingDict[row[0]] = row[1:]
                            try:
                                OperatingDict[row[0]].extend(row[1:])
                            except KeyError:
                                OperatingDict[row[0]] = row[1:] 

                    except IndexError:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R5.htm"
                        request = {'url': BASE_URL, 'User-Agent': self.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if '12 months ended' not in soup.prettify().lower():
                            raise NameError('Incorrect URL. File Not Found')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 4:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                            if i==0:
                                OperatingDict[row[0]] = row[1:]
                            try:
                                OperatingDict[row[0]].extend(row[1:])
                            except KeyError:
                                OperatingDict[row[0]] = row[1:] 


        return OperatingDict

    def get_balance_sheet_numbers(self):
        """Get operating statement numbers from SEC"""
        BalanceDict = {'Ticker':self.ticker}

        for i, url in enumerate(list(self.get_10K_links().values())[0:-1:2]):
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R4.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                
                if 'balance sheets' not in soup.prettify().lower():
                    raise IndexError('Incorrect URL. Trying R1 Form')



                all_data = []
                for tr in soup.select('tr'):
                    tds = [td for td in tr.select('td') if td.get_text(strip=True)]

                    if len(tds) == 3:
                        tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                        tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                        all_data.append(tds)

                for row in all_data:
                    print('{:<90} {:<10} {:<10}'.format(*row))
                    if i==0:
                        BalanceDict[row[0]] = row[1:]
                    try:
                        BalanceDict[row[0]].extend(row[1:])
                    except KeyError:
                        BalanceDict[row[0]] = row[1:]
            
            except IndexError:
                try:
                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R5.htm"
                    request = {'url': BASE_URL, 'User-Agent': self.headers}
                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                    
                    if 'balance sheet' not in soup.prettify().lower():
                        raise IndexError('Incorrect URL. Trying R6 Form')


                    all_data = []
                    for tr in soup.select('tr'):
                        tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                        if len(tds) == 3:
                            tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                            tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                            all_data.append(tds)

                    for row in all_data:
                        print('{:<90} {:<10} {:<10}'.format(*row))
                        if i==0:
                            BalanceDict[row[0]] = row[1:]
                        try:
                            BalanceDict[row[0]].extend(row[1:])
                        except KeyError:
                            BalanceDict[row[0]] = row[1:]                

                except IndexError:
                    try:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R1.htm"
                        request = {'url': BASE_URL, 'User-Agent': self.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if 'balance sheet' not in soup.prettify().lower():
                            raise IndexError('Incorrect URL. Trying R5 form')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 3:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            print('{:<90} {:<10} {:<10}'.format(*row))
                            if i==0:
                                BalanceDict[row[0]] = row[1:]
                            try:
                                BalanceDict[row[0]].extend(row[1:])
                            except KeyError:
                                BalanceDict[row[0]] = row[1:] 

                    except IndexError:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R6.htm"
                        request = {'url': BASE_URL, 'User-Agent': self.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if 'balance sheet' not in soup.prettify().lower():
                            raise NameError('Incorrect URL. File Not Found')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 3:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            print('{:<90} {:<10} {:<10}'.format(*row))
                            if i==0:
                                BalanceDict[row[0]] = row[1:]
                            try:
                                BalanceDict[row[0]].extend(row[1:])
                            except KeyError:
                                BalanceDict[row[0]] = row[1:] 


        return BalanceDict
    

    def get_cash_flow_numbers(self):
        """Get operating statement numbers from SEC"""
        OperatingDict = {'Ticker':self.ticker}

        for i, url in enumerate(list(self.get_10K_links().values())[0:-1:3]):
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R6.htm"
                request = {'url': BASE_URL, 'User-Agent': self.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                
                if '12 months ended' not in soup.prettify().lower():
                    raise IndexError('Incorrect URL. Trying R3 Form')

                all_data = []
                for tr in soup.select('tr'):
                    tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                    if len(tds) == 4:
                        tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                        tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                        all_data.append(tds)

                for row in all_data:
                    print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                    if i==0:
                        OperatingDict[row[0]] = row[1:]
                    try:
                        OperatingDict[row[0]].extend(row[1:])
                    except KeyError:
                        OperatingDict[row[0]] = row[1:]
            
            except IndexError:
                try:
                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R7.htm"
                    request = {'url': BASE_URL, 'User-Agent': self.headers}
                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                    
                    if '12 months ended' not in soup.prettify().lower():
                        raise IndexError('Incorrect URL. Trying R4 Form')


                    all_data = []
                    for tr in soup.select('tr'):
                        tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                        if len(tds) == 4:
                            tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                            tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                            all_data.append(tds)

                    for row in all_data:
                        print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                        if i==0:
                            OperatingDict[row[0]] = row[1:]
                        try:
                            OperatingDict[row[0]].extend(row[1:])
                        except KeyError:
                            OperatingDict[row[0]] = row[1:]                

                except IndexError:
                    try:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R4.htm"
                        request = {'url': BASE_URL, 'User-Agent': self.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if '12 months ended' not in soup.prettify().lower():
                            raise IndexError('Incorrect URL. Trying R5 form')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 4:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                            if i==0:
                                OperatingDict[row[0]] = row[1:]
                            try:
                                OperatingDict[row[0]].extend(row[1:])
                            except KeyError:
                                OperatingDict[row[0]] = row[1:] 

                    except IndexError:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R6.htm"
                        request = {'url': BASE_URL, 'User-Agent': self.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if '12 months ended' not in soup.prettify().lower():
                            raise NameError('Incorrect URL. File Not Found')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 4:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                            if i==0:
                                OperatingDict[row[0]] = row[1:]
                            try:
                                OperatingDict[row[0]].extend(row[1:])
                            except KeyError:
                                OperatingDict[row[0]] = row[1:] 


        return OperatingDict


    def get_daily_quote(self):
        pass


print(Stockify('aapl').get_cash_flow_numbers())





