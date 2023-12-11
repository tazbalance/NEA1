from pathlib import Path
import sqlite3


class Database():

    def __init__(self):
        self.path = Path(__file__).with_name('NEAcharacterDB.db')


    def insert_character(self, name, series, image):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'INSERT INTO Characters (Name, Series, Image) VALUES ("{name}", "{series}", "{image}");'
        cur.execute(query)

        conn.commit()


    def get_character_info(self, number):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"SELECT Name, Series, Image FROM Characters WHERE CharacterID = {number};"
        cur.execute(query)
        results = cur.fetchall()

        conn.close()
        return results
