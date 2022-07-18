import sqlite3

DB_NAME = "fin_data.db"

#con = sqlite3.connect(DB_NAME)

class db_ops:
    def __init__(self):
        pass
        #self.con = sqlite3.connect(DB_NAME)
    # def get_tables(self):
    #     cur = self.con.cursor()
    #     cur.execute(
    def get_table_data(self, table_name):
        self.con = sqlite3.connect(DB_NAME)
        cur = self.con.cursor()
        cur.execute(f'select * from {table_name}')
        result = cur.fetchall()
        self.con.close()
        return result
    def insert_data(self, table_name,  data):
        self.con = sqlite3.connect(DB_NAME)
        cur = self.con.cursor()
        print(f"data: {data}")
        print(f"data: {data[0]} ,{data[1]}")
        sqlite_insert_query = f"""INSERT INTO {table_name}
                              (Word, link)
                               VALUES
                              ("{data[0]}", "{data[1]}")"""
        # print(f"query:{sqlite_insert_query}")
        cur.execute(sqlite_insert_query)
        self.con.commit()
        self.con.close()

    def insert_word_def(self, word, word_question, word_def, link):
        self.con = sqlite3.connect(DB_NAME)
        cur = self.con.cursor()
        print(f"word: {word} ,question:{word_question}, answer:{word_def}, link:{link} ")
        sqlite_insert_query = f"""INSERT INTO word_definition
                              (Word, Word_Question, Word_Definition, Link)
                               VALUES
                              ("{word}", "{word_question}", "{word_def}", "{link}")"""
        # print(f"query:{sqlite_insert_query}")
        cur.execute(sqlite_insert_query)
        self.con.commit()
        self.con.close()
