from pathlib import Path
import sqlite3


class Database():

    def __init__(self):
        self.path = Path(__file__).with_name('NEAcharacterDB.db')


    def delete_table(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"DELETE FROM Characters;"
        cur.execute(query)

        conn.commit()


    def insert_character(self, id, name, series, image, typedata, votedata):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute('INSERT INTO Characters (ID, Name, Series, Image, Data, VoteData) VALUES (?, ?, ?, ?, ?, ?);', (id, name, series, image, typedata, votedata,))

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


    def get_vote_data(self, id):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'SELECT VoteData FROM Characters WHERE ID = {id};'
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
