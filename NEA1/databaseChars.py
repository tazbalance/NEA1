from pathlib import Path
import sqlite3


class Database():

    def __init__(self):
        self.path = Path(__file__).with_name('NEAcharacterDB.db')
        self.reset_visibility()


    def reset_visibility(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'UPDATE Characters SET Visible = 0'
        cur.execute(query)

        conn.commit()


    def set_visibility(self, id):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'UPDATE Characters SET Visible = 1 WHERE ID = {id};'
        cur.execute(query)

        conn.commit()


    def delete_table(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"DELETE FROM Characters;"
        cur.execute(query)

        conn.commit()


    def insert_character(self, id, name, series, image, typedata):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute('INSERT INTO Characters (ID, Name, Series, Image, Data) VALUES (?, ?, ?, ?, ?);', (id, name, series, image, typedata,))

        conn.commit()


    def get_character_info(self, id):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'SELECT Name, Series, Image FROM Characters WHERE ID = {id};'
        cur.execute(query)
        results = cur.fetchall()

        conn.close()
        return results


    def get_character_data(self, id):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'SELECT Data FROM Characters WHERE ID = {id};'
        cur.execute(query)
        results = cur.fetchone()

        conn.close()
        return results[0]


    def in_database(self, id):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'SELECT ID FROM Characters WHERE ID = {id};'
        cur.execute(query)
        result = cur.fetchone()

        conn.close()
        return result



conn = sqlite3.connect(Path(__file__).with_name('NEAcharacterDB.db'))
cur = conn.cursor()

query = f'ALTER TABLE Characters ADD VoteData Text;'
cur.execute(query)

conn.commit()