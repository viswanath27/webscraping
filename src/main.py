import string
import time
from scrape import InvestopediaScrape
from concurrent.futures import ThreadPoolExecutor
from db_util import db_ops

if __name__ == '__main__':
    crawler = InvestopediaScrape()
    crawler.scrape_content('a', 'actuarial-science')
    # total_start_time = time.time()
    # executor = ThreadPoolExecutor(30)
    #
    # for alphabet in list(string.ascii_lowercase):
    #     print("Fetching words starting with: {}".format(alphabet), flush=True)
    #     #start = time.time()
    #     executor.submit(crawler.scrape, (alphabet))
    #     #crawler.scrape(alphabet)
    #     #end = time.time()
    #     #print(f"Fetching words starting with: {alphabet} has taken :{end-start} secs of time")
    #
    crawler.close()
    # total_end_time = time.time()
    # print(f'Done! total execution time :{total_end_time-total_start_time} secs')
    db_obj = db_ops()
    #db_obj.get_table_data('fin_data_definition')
    data = {}
    data['Term'] = 'Actuarial'
    data['definition'] = '''An actuarial life table is a table or spreadsheet that shows the probability of a person at 
    a certain age dying before their next birthday. It's often used by life insurance companies to calculate the 
    remaining life expectancy for people at different ages and stages, and the probability of surviving a 
    particular year of age.'''
    db_obj.insert_data('fin_data_definition', data)
    db_obj.get_table_data('fin_data_definition')

