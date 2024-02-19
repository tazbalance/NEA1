from pathlib import Path
import sqlite3


class Database():

    def __init__(self):
        self.path = Path(__file__).with_name('NEAdatabase.db')


    # QUIZ

    def get_amount_of_questions(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = "SELECT QuestionNumber FROM Questions ORDER BY QuestionNumber DESC;"
        cur.execute(query)
        result = cur.fetchone()

        conn.close()
        return result


    def get_questions(self, number):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"SELECT Question FROM Questions WHERE QuestionNumber = {number};"
        cur.execute(query)
        result = cur.fetchone()

        conn.close()
        return result


    def insert_answer(self, answer, number):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"UPDATE Questions SET Answer = {answer} WHERE QuestionNumber = {number};"
        cur.execute(query)

        conn.commit()


    def get_answers(self, number):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"SELECT MBTI, Enneagram, BigFive, Answer FROM Questions WHERE QuestionNumber = {number};"
        cur.execute(query)
        results = cur.fetchall()

        conn.close()
        return results


    # CHARACTERS

    def add_types(self):
        types = ['ISFJ', 'ESFJ', 'INTP', 'ENTP', 'ISTJ', 'ESTJ', 'INFP', 'ENFP', 'INFJ', 'ENFJ', 'ISTP', 'ESTP', 'INTJ', 'ENTJ', 'ISFP', 'ESFP']
        
        for i in types:

            conn = sqlite3.connect(self.path)
            cur = conn.cursor()

            cur.execute(f'INSERT INTO Types(MBTI) VALUES ("{i}")')

            conn.commit()


    def delete_table(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"DELETE FROM Characters;"
        cur.execute(query)

        query = f"DELETE FROM Types WHERE CharacterIDs;"
        cur.execute(query)

        conn.commit()


    def insert_character(self, id, name, series, image, typedata, votedata, mbti, enneagram):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute('INSERT INTO Characters (ID, Name, Series, Image, Data, VoteData, MBTI, Enneagram) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', (id, name, series, image, typedata, votedata, mbti, enneagram,))

        conn.commit()

        self.insert_types(id, mbti)


    def insert_types(self, id, mbti):
        IDlist = self.find_type(id, mbti)
        
        if IDlist:

            conn = sqlite3.connect(self.path)
            cur = conn.cursor()

            cur.execute(f'UPDATE Types SET CharacterIDs = "{IDlist}" WHERE MBTI = "{mbti}";')

            conn.commit()


    def find_type(self, id, mbti):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f'SELECT CharacterIDs FROM Types WHERE MBTI = "{mbti}";'
        cur.execute(query)

        result = cur.fetchone()

        if not result:  # if list empty, return id by itself
            return id

        conn.close()
        
        result = result[0]
        IDlist = result.split(', ')

        for dbID in IDlist:  # if id in list, no change
            if dbID == id:
                return None
        
        result += f', {id}'  # if id not in list, add it
        return result


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

        query = f'SELECT Data FROM Characters WHERE ID = {id};'
        cur.execute(query)
        result = cur.fetchone()

        conn.close()
        return result