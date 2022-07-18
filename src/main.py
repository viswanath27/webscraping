from src.scraping.scrape import InvestopediaScrape
from src.db.db_util import db_ops

if __name__ == '__main__':
    crawler = InvestopediaScrape()
    # total_start_time = time.time()
    # executor = ThreadPoolExecutor(30)
    # word_info = {}
    # for alphabet in list(string.ascii_lowercase):
    #     print("Fetching words starting with: {}".format(alphabet), flush=True)
    #     start = time.time()
    #     #executor.submit(crawler.scrape_terms(), (alphabet))
    #     word_data = crawler.scrape_terms(alphabet)
    #     #href_data = crawler.get_herf(alphabet)
    #     #print(alphabet, href_data)
    #     end = time.time()
    #     print(f"Fetching words starting with: {alphabet} has taken :{end-start} secs of time")
    #     word_info[alphabet] = word_data
    #
    # print(word_info)
    #remove_unrelated_words(word_info)
    # terms = ['actuarial-science', 'advaloremtax']
    # for term in terms:
    #     question, answer = crawler.scrape_content('a', term)
    #     print(question, answer)
    # crawler.close()
    # total_end_time = time.time()
    # print(f'Done! total execution time :{total_end_time-total_start_time} secs')
    db_obj = db_ops()
    # db_obj.get_table_data('word_index')
    # # data = {}
    # # data['Term'] = 'Actuarial'
    # # data['definition'] = '''An actuarial life table is a table or spreadsheet that shows the probability of a person at
    # # a certain age dying before their next birthday. It's often used by life insurance companies to calculate the
    # # remaining life expectancy for people at different ages and stages, and the probability of surviving a
    # # particular year of age.'''
    # for key, values in word_info.items():
    #     for record in values:
    #         db_obj.insert_data('word_index', record)
    # db_obj.get_table_data('word_index')
    data = db_obj.get_table_data('word_index')
    for each in data:
        try:
            print(f"index:{each[0]}, word:{each[1]}, first letter:{each[1][0]},link:{each[2]}")
            question, answer = crawler.scrape_content(each[2])
            print(f"question:{question} and answer:{answer}")
            db_obj.insert_word_def(each[1], question, answer, each[2])
        except Exception as e:
            print(f"Exception:{e}")
            db_obj.insert_word_def(each[1], "", "", each[2])

