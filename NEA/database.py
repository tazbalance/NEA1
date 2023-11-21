import sqlite3


class Database():
    """
    store reference to database file
    """

    def __init__(self, path):
        self.path = path


    def get_questions(self, system, number):
        system = system
        number = number
        
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"SELECT {system} FROM Questions WHERE QuestionNumber = {number}"
        cur.execute(query)
        result = cur.fetchone()

        conn.close()
        return result


    def insert_answer(self, answer, number):
        answer = answer
        number = number
        
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"UPDATE Questions SET Answer = {answer} WHERE QuestionNumber = {number};"
        cur.execute(query)

        conn.commit()


    def get_answers(self, number):
        number = number
        
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        query = f"SELECT MBTI, Enneagram, BigFive, Answer FROM Questions WHERE QuestionNumber = {number}"
        cur.execute(query)
        results = cur.fetchall()

        conn.close()
        return results