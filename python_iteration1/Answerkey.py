from Question import Question


class Answerkey:
    def __init__(self, name):
        self.name = name
        self.question_list = []

    def insert_question(self, question, answer):
        q1 = Question(question, answer)
        self.question_list.append(q1)

    def get_name(self):
        return self.name

    def is_question_present(self, que):
        check = 0
        for q in que:
            for question in self.question_list:
                if question.get_question().split() == str(q.question).split():
                    check += 1
                    break
        return check == len(que)

    def get_answer(self, que):
        for question in self.question_list:
            if question.get_question() == que:
                return question.get_answer()
