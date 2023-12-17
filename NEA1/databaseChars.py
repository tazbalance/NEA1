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


    def insert_character(self, id, name, series, image):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"INSERT INTO Characters (ID, Name, Series, Image) VALUES ('{id}', '{name}', '{series}', '{image}');"
        cur.execute(query)

        conn.commit()


    def get_character_info(self, id):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'SELECT Name, Series, Image FROM Characters WHERE ID = {id};'
        cur.execute(query)
        results = cur.fetchall()

        conn.close()
        return results
