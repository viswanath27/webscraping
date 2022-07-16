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
        print(cur.fetchall())
        self.con.close()
    def insert_data(self, table_name,  data):
        self.con = sqlite3.connect(DB_NAME)
        cur = self.con.cursor()
        # print(f"data: {data['Term']} ,{data['definition']}")
        sqlite_insert_query = f"""INSERT INTO {table_name}
                              (Term, definition)
                               VALUES
                              ("{data['Term']}", "{data['definition']}")"""
        # print(f"query:{sqlite_insert_query}")
        cur.execute(sqlite_insert_query)
        self.con.commit()
        self.con.close()
