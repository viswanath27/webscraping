import string
import time
from scrape import InvestopediaScrape

if __name__ == '__main__':
    crawler = InvestopediaScrape()
    total_start_time = time.time()
    for alphabet in list(string.ascii_lowercase):
        #print("Fetching words starting with: {}".format(alphabet), flush=True)
        start = time.time()
        crawler.scrape(alphabet)
        end = time.time()
        print(f"Fetching words starting with: {alphabet} has taken :{end-start} secs of time")

    crawler.close()
    total_end_time = time.time()
    print(f'Done! total execution time :{total_end_time-total_start_time} secs')