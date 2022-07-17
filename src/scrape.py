from urllib import request
import requests
from bs4 import BeautifulSoup


class InvestopediaScrape:
    def __init__(self):
        print("Starting...", flush=True)
        self.fh = open('output.txt', 'w', encoding="utf-8")

    def get_herf(self, alphabet):
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
            link_list = [a['href'] for a in soup.find_all('a', href=True) if len(a['href']) >= 4 and a['href'][-4:] == ".asp"]
        return link_list


    def scrape_terms(self, alphabet):
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
            data = soup.find_all('a', {'class': "mntl-text-link"})
            #for each in data:
            #    print(each.get("href"))
            for each in data:
                print(each.text.strip())
            text = [(term.text.strip(), term.get("href")) for term in data if term.text.strip()[0].lower() == alphabet]
            #print(text)
        return text
            # self.fh.write(','.join(text))
            # self.fh.write('\n')

    def get_question(self, soup):
        return soup.find('span', {'class': 'mntl-sc-block-heading__text'}).get_text()

    def get_answer(self, soup):
        return soup.find('p',{'class':'mntl-sc-block-html'}).get_text()

    def scrape_content(self, link):
        print(f"{link}")
        r = requests.get(link)
        #r = requests.get('https://www.investopedia.com/terms/{}/{}.asp'.format(alphabet, term))
        encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(r.content, "html5lib", from_encoding=encoding)
        #print(soup)
        data = soup.find('div', {'class':"loc article-content"})
        #new_data = BeautifulSoup(data, 'html.parser')
        question = self.get_question(soup)
        answer = self.get_answer(soup)
        return question, answer
        # print(f"question:{question.get_text()}")
        #
        # answer = soup.find('p',{'class':'mntl-sc-block-html'})
        # print(f"answer:{answer.get_text()}")
        # # for data in soup.find_all("p"):
        #     print(data.get_text())
        #print(question)
        #text = [term.text.strip() for term in data]
        #print(text)

    def close(self):
        self.fh.close()
