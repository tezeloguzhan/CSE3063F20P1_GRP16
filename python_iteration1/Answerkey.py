from Question import Question


class Answerkey:
    def init(self, name):
        self.name = name
        self.question_list = []

    def insert_question(self, question, answer):
        q1 = Question(question, answer)
        self.question_list.append(q1)

    def get_name(self):
        return self.name