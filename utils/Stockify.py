from bs4 import BeautifulSoup
import requests



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

    def get_CIK(self):
        url = f"https://sec.report/Ticker/{self.ticker}"
        request = {'url': url, }
        soup = BeautifulSoup(requests.get(request['url'], \
                                          headers={'User-Agent':self.headers}).content, 'lxml')

        return(soup.h2.text.split()[-1])

    def get_10K_links(self):
        request = {'url': self.base_url, 'User-Agent': self.headers}
        soup = BeautifulSoup(requests.get(request['url'], headers={'User-Agent': request['User-Agent']}).content, 'lxml')

        url_list = [a.get('href') for a in soup.find_all('a', id='interactiveDataBtn')][:10]
        return {self.url_keys[i]: url_list[i] for i in range(len(self.url_keys))}

    def get_EPS(self):
        for url in self.url_dict.
        return {self.url_keys[i]: }

    def get_historical_stock_prices(self):
        pass

print(Stockify('ko').get_EPS())
