import database


class Data:

    def __init__(self):

        self.ids = [1,2,3,4]

        self.myDb = database.Database()
        self.chars = []
        self.qNumber = 1

    # ========================== ids ==========================

    def get_ids(self):
        return self.ids

    # =================== question database ===================

    def get_db(self):
        return self.myDb

    def insert_answer(self, radioValue, qNumber):
        self.myDb.insert_answer(radioValue, qNumber)

    def get_answers(self):
        return self.myDb.get_answers(self.qNumber)

    def get_questions(self):
        return self.myDb.get_questions(self.qNumber)

    def get_amount_of_questions(self):
        return self.myDb.get_amount_of_questions()

    # =================== character database ===================

    def get_char_db(self):
        return self.myDb

    def get_character_info(self, id):
        return self.myDb.get_character_info(id)
    
    def get_character_genre(self, id):
        return self.myDb.get_character_genre(id)
    
    # ================== selected characters ==================

    def get_chars(self):
        return self.chars

    def remove_char(self, id):
        self.chars.remove(id)
        return self.chars

    def append_char(self, id):
        self.chars.append(id)
        return self.chars

    # =================== question number ===================

    def get_qnumber(self):
        return self.qNumber

    def increase_qnumber(self):
        self.qNumber += 1
        return self.qNumber

    def decrease_qnumber(self):
        self.qNumber -= 1
        return self.qNumber