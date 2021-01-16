from CommonUtils import CommonUtils


class Poll:
    def __init__(self):
        self.date = ""
        self.name = ""
        self.questions = []
        self.question_list = []
        self.students = {}
        self.answerkey = []
        self.marked = []
        self.selected_options = []
        self.utils = CommonUtils()

    def set_name(self, name):
        self.name = name

    def set_date(self, date):
        self.date = date