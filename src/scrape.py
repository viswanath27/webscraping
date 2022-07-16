from urllib import request
import requests
from bs4 import BeautifulSoup


class InvestopediaScrape:
    def __init__(self):
        print("Starting...", flush=True)
        self.fh = open('output.txt', 'w', encoding="utf-8")

    def scrape(self, alphabet):
        r = requests.get('https://www.investopedia.com/terms/{}/'.format(alphabet))
        soup = BeautifulSoup(r.text, "html5lib")
        try:
            page = soup.find('li', {'class': 'pager-last last'}).find('a')['href'].split('=')[1]
        except:
            page = 1
            pass
        for page_number in range(0, int(page)):
            print(f"page_number:{page_number}")
            r = requests.get('https://www.investopedia.com/terms/{}/?page={}'.format(alphabet, page_number))
            encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
            soup = BeautifulSoup(r.content, "html5lib", from_encoding=encoding)
            data = soup.find_all('a', {'class': "dictionary-top300-list__list mntl-text-link"})
            text = [term.text.strip() for term in data]
            print(text)
            self.fh.write(','.join(text))
            self.fh.write('\n')
    
    def scrape_content(self, aplhabet, term):
        r = requests.get('https://www.investopedia.com/terms/{}/{}.asp'.format(aplhabet, term))
        encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(r.content, "html5lib", from_encoding=encoding)
        data = soup.find_all('id', {'class':"comp mntl-sc-block-callout-body mntl-text-block"})
        text = [term.text.strip() for term in data]
        print(text)
        
    def close(self):
        self.fh.close()
