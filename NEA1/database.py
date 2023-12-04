import sqlite3


class Database():

    def __init__(self, path):
        self.path = path


    def get_amount_of_questions(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = "Select QuestionNumber FROM Questions ORDER BY QuestionNumber DESC;"
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