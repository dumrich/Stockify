from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


class Stockify:
    """Stockify class to scrape EGDAR and get data"""
    headers = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.CIK = self.get_CIK()
        self.base_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self.CIK}&type=10-K&dateb=&owner=include&count=40&search_text="
    def get_CIK(self):
        """Get the SEC CIK"""
        url = f"https://sec.report/Ticker/{self.ticker}"
        request = {'url': url, }
        soup = BeautifulSoup(requests.get(request['url'], \
                                          headers={'User-Agent':Stockify.headers}).content, 'lxml')

        return (soup.h2.text.split()[-1].lstrip('0'))

    def get_10K_links(self):
        """Get all 10K links"""
        request = {'url': self.base_url, 'User-Agent': Stockify.headers}
        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')

        url_list = [a.get('href') for a in soup.find_all('a', id='interactiveDataBtn')]

        if len(url_list) <= 10:
            url_list = url_list[:10]

        return {f"year +{i}": 'https://www.sec.gov'+url_list[i] for i in range(len(url_list))}

    def get_operating_statement(self):
        """Get operating statement numbers from SEC"""
        OperatingDict = {'Ticker':self.ticker}
        for i, url in enumerate(list(self.get_10K_links().values())[0:-1:3]):
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                
                if '12 months ended' and 'earningspersharebasic' not in soup.prettify().lower():
                    raise IndexError('Incorrect URL. Trying R3 Form')

                all_data = []
                for tr in soup.select('tr'):
                    tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                    if len(tds) == 4:
                        tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                        tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                        all_data.append(tds)
                
                for row in all_data:
                    if i==0:
                        if (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and 'defref_us-gaap_SalesRevenueNet' not in OperatingDict):
                            row[0] = 'defref_us-gaap_SalesRevenueNet'
                            OperatingDict[row[0]] = row[1:]
                        elif (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                            OperatingDict[row[0]] = row[1:]
                        

                        else:
                            OperatingDict[row[0]] = row[1:]
                    else:
                        try:

                            if (row[0]=='defref_us-gaap_Revenues' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                OperatingDict['defref_us-gaap_SalesRevenueNet'].extend(row[1:])
                            else:
                                OperatingDict[row[0]].extend(row[1:])
                        except KeyError:
                            OperatingDict[row[0]] = row[1:]                 
            except IndexError:
                try:
                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                    request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                    
                    if '12 months ended' and 'earningspersharebasic' not in soup.prettify().lower():
                        raise IndexError('Incorrect URL. Trying R4 Form')


                    all_data = []
                    for tr in soup.select('tr'):
                        tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                        if len(tds) == 4:
                            tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                            tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                            all_data.append(tds)
                    
                    for row in all_data:
                        if i==0:
                            if (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and 'defref_us-gaap_SalesRevenueNet' not in OperatingDict):
                                row[0] = 'defref_us-gaap_SalesRevenueNet'
                                OperatingDict[row[0]] = row[1:]
                            elif (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                OperatingDict[row[0]] = row[1:]
                            else:
                                OperatingDict[row[0]] = row[1:]
                        else:
                            try:

                                if (row[0]=='defref_us-gaap_Revenues' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                    OperatingDict['defref_us-gaap_SalesRevenueNet'].extend(row[1:])
                                else:
                                    OperatingDict[row[0]].extend(row[1:])
                            except KeyError:
                                OperatingDict[row[0]] = row[1:]             

                except IndexError:
                    try:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R4.htm"
                        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')

                        if '12 months ended' and 'earningspersharebasic' not in soup.prettify().lower():
                            raise IndexError('Incorrect URL. Trying R5 form')

                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 4:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            if i==0:
                                if (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and 'defref_us-gaap_SalesRevenueNet' not in OperatingDict):
                                    row[0] = 'defref_us-gaap_SalesRevenueNet'
                                    OperatingDict[row[0]] = row[1:]
                                elif (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                    OperatingDict[row[0]] = row[1:]
                                else:
                                    OperatingDict[row[0]] = row[1:]
                            else:
                                try:

                                    if (row[0]=='defref_us-gaap_Revenues' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                        OperatingDict['defref_us-gaap_SalesRevenueNet'].extend(row[1:])
                                    else:
                                        OperatingDict[row[0]].extend(row[1:])
                                except KeyError:
                                    OperatingDict[row[0]] = row[1:]     

                    except IndexError:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R5.htm"
                        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if '12 months ended' and 'earningspersharebasic' not in soup.prettify().lower():
                            continue
                        all_data = []
                        for tr in soup.select('tr'):
                            tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                            if len(tds) == 4:
                                tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                all_data.append(tds)

                        for row in all_data:
                            if i==0:
                                if (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and 'defref_us-gaap_SalesRevenueNet' not in OperatingDict):
                                    row[0] = 'defref_us-gaap_SalesRevenueNet'
                                    OperatingDict[row[0]] = row[1:]
                                elif (row[0] == 'defref_us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                    OperatingDict[row[0]] = row[1:]
                                else:
                                    OperatingDict[row[0]] = row[1:]
                            else:
                                try:

                                    if (row[0]=='defref_us-gaap_Revenues' and len(OperatingDict['defref_us-gaap_SalesRevenueNet'])!=0):
                                        OperatingDict['defref_us-gaap_SalesRevenueNet'].extend(row[1:])
                                    else:
                                        OperatingDict[row[0]].extend(row[1:])
                                except KeyError:
                                    OperatingDict[row[0]] = row[1:] 


        return OperatingDict

    def get_balance_sheet(self):
        """Get operating statement numbers from SEC"""
        BalanceDict = {'Ticker':self.ticker}

        for i, url in enumerate(list(self.get_10K_links().values())[0:-1:2]):
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R4.htm"
                request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                
                    

                if  'cashandcash' not in soup.prettify().lower():
                    raise IndexError("File not found. Trying R6 Form")

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
                    else:
                        try:
                            BalanceDict[row[0]].extend(row[1:])
                        except KeyError:
                            BalanceDict[row[0]] = row[1:]             
            except IndexError:
                try:
                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R6.htm"
                    request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                    
                    if 'cashandcash' not in soup.prettify().lower():
                        raise KeyError('Incorrect URL. Trying R1 Form')


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
                        else:
                            try:
                                BalanceDict[row[0]].extend(row[1:])
                            except KeyError:
                                BalanceDict[row[0]] = row[1:]              

                except KeyError:
                    try:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R1.htm"
                        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if 'cashandcash' not in soup.prettify().lower():
                            raise IndexError('Incorrect URL. Trying R2 form')
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
                            else:
                                try:
                                    BalanceDict[row[0]].extend(row[1:])
                                except KeyError:
                                    BalanceDict[row[0]] = row[1:]           
                    except IndexError:
                        try:

                            BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                            request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                            soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                            if 'cashandcash' not in soup.prettify().lower():
                                raise IndexError("Invalid URL. Trying R5 form")

                            all_data = []
                            for tr in soup.select('tr'):
                                tds = [td for td in tr.select('td') if td.get_text(strip=True)]
                                if len(tds) == 3:
                                    tds[0] = re.search(r"'(.*?)'", tds[0].a['onclick']).group(1)
                                    tds[1:] = [td.get_text(strip=True) for td in tds[1:]]
                                    all_data.append(tds)

                            for row in all_data:

                                print('{:<90} {:<10} {:<10} {:<10}'.format(*row))
                                if i==0:
                                    
                                    BalanceDict[row[0]] = row[1:]
                                else:
                                    try:
                                        BalanceDict[row[0]].extend(row[1:])
                                    except KeyError:
                                        BalanceDict[row[0]] = row[1:]
                        except IndexError:
                            try:
                                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R5.htm"
                                request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                if 'cashandcash' not in soup.prettify().lower():
                                    raise IndexError("Invalid URL. Trying R3 form")

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
                                    else:
                                        try:
                                            BalanceDict[row[0]].extend(row[1:])
                                        except KeyError:
                                            BalanceDict[row[0]] = row[1:]
                            except IndexError:
                                try:
                                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                                    request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                    if 'cashandcash' not in soup.prettify().lower():
                                        raise IndexError('Trying R7 form')
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
                                        else:
                                            try:
                                                BalanceDict[row[0]].extend(row[1:])
                                            except KeyError:
                                                BalanceDict[row[0]] = row[1:]
                                except IndexError:
                                    try:
                                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R7.htm"
                                        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                        if 'cashandcash' not in soup.prettify().lower():
                                            raise IndexError("Trying R8 form")
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
                                            else:
                                                try:
                                                    BalanceDict[row[0]].extend(row[1:])
                                                except KeyError:
                                                    BalanceDict[row[0]] = row[1:]
                                    except IndexError:
                                    
                                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R7.htm"
                                        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                        if 'cashandcash' not in soup.prettify().lower():
                                            raise IndexError("Trying R8 form")
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
                                            else:
                                                try:
                                                    BalanceDict[row[0]].extend(row[1:])
                                                except KeyError:
                                                    BalanceDict[row[0]] = row[1:]





        return BalanceDict    

    def get_cash_flow(self):
        """Get operating statement numbers from SEC"""
        CashFlowDict = {'Ticker':self.ticker}

        for i, url in enumerate(list(self.get_10K_links().values())[0:-1:3]):
            accession_number = url.split('&')[2][17:].replace('-', '')
            try:
                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R6.htm"
                request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                
                if '12 months ended' and 'cash flows' not in soup.prettify().lower():
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
                        CashFlowDict[row[0]] = row[1:]
                    try:
                        CashFlowDict[row[0]].extend(row[1:])
                    except KeyError:
                        CashFlowDict[row[0]] = row[1:]
            
            except IndexError:
                try:
                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R7.htm"
                    request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                    
                    if '12 months ended' and 'cash flows' not in soup.prettify().lower():
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
                            CashFlowDict[row[0]] = row[1:]
                        try:
                            CashFlowDict[row[0]].extend(row[1:])
                        except KeyError:
                            CashFlowDict[row[0]] = row[1:]                

                except IndexError:
                    try:
                        BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R4.htm"
                        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                        if '12 months ended' and 'cash flows' not in soup.prettify().lower():
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
                                CashFlowDict[row[0]] = row[1:]
                            try:
                                CashFlowDict[row[0]].extend(row[1:])
                            except KeyError:
                                CashFlowDict[row[0]] = row[1:] 

                    except IndexError:
                        try:
                            BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R8.htm"
                            request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                            soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                            if '12 months ended' and 'cash flows' not in soup.prettify().lower():
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
                                    CashFlowDict[row[0]] = row[1:]
                                try:
                                    CashFlowDict[row[0]].extend(row[1:])
                                except KeyError:
                                    CashFlowDict[row[0]] = row[1:]
                        except NameError:
                            try:
                                BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R3.htm"
                                request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                if '12 months ended' and 'cash flows' not in soup.prettify().lower():
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
                                        CashFlowDict[row[0]] = row[1:]
                                    try:
                                        CashFlowDict[row[0]].extend(row[1:])
                                    except KeyError:
                                        CashFlowDict[row[0]] = row[1:]
                            except NameError:
                                try:
                                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R1.htm"
                                    request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                    if '12 months ended' and 'cash flows' not in soup.prettify().lower():
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
                                            CashFlowDict[row[0]] = row[1:]
                                        try:
                                            CashFlowDict[row[0]].extend(row[1:])
                                        except KeyError:
                                            CashFlowDict[row[0]] = row[1:]
                                except NameError:
                                    BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{self.get_CIK().strip('0')}/{accession_number}/R2.htm"
                                    request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
                                    soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')
                                    if '12 months ended' and 'cash flows' not in soup.prettify().lower():
                                        continue
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
                                            CashFlowDict[row[0]] = row[1:]
                                        try:
                                            CashFlowDict[row[0]].extend(row[1:])
                                        except KeyError:
                                            CashFlowDict[row[0]] = row[1:]



    


        return CashFlowDict
            

    def get_company_profile(self):
        BASE_URL = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}"
        request = {'url': BASE_URL, 'User-Agent': Stockify.headers}
        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')

        

        ProfileDict = {'symbol': self.ticker, 'Profile':\
                {'Price': float(soup.find('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text.replace(',', '')),\
                'Beta (5Y M)': float(soup.find('span', {'data-reactid':'144'}).text),
                'Volume (Avg.)': float(soup.find('span', {'data-reactid': '131'}).text.replace(',', '')),
                'Volume':float(soup.find('span', {'data-reactid': '126'}).text.replace(',', '')),
                'Market Cap':soup.find('span', {'data-reactid': '139'}).text.replace(',', ''),
                '52 Week Range':soup.find('td', {'data-reactid': '121'}).text,
                'PE Ratio (TTM)':soup.find('span', {'data-reactid': '149'}).text.replace(',', ''),
                'Earnings Date':soup.find('span', {'data-reactid': '161'}).text,
                'Forward Dividend & Yield':soup.find('td', {'data-reactid': '165'}).text,
                'Ex-Dividend Date':soup.find('span', {'data-reactid': '170'}).text,
                '1y Target Est':float(soup.find('span', {'data-reactid': '175'}).text.replace(',', '')),
                'Previous Close':float(soup.find('span', {'data-reactid': '98'}).text.replace(',', '')),
                'Open':float(soup.find('span', {'data-reactid': '103'}).text.replace(',', '')),
                'Bid':soup.find('span', {'data-reactid': '108'}).text,
                'Ask':soup.find('span', {'data-reactid': '113'}).text,
}}
            



        

        return ProfileDict

    def get_historical_stock_values(self):
        pass







