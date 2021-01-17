
import glob
import os
import numpy as np
import pandas

from Answerkey import Answerkey
from CommonUtils import CommonUtils
from ExcelWriter import ExcelWriter
from Poll import Poll
from Question import Question
from Student import Student


class ZoomPollAnalyzer:
    def __init__(self, answer_dir, students_dir,
                 polls_dir, out_dir):
        self.answer_dir = answer_dir
        self.students_dir = students_dir
        self.polls_dir = polls_dir
        self.out_dir = out_dir
        self.utils = CommonUtils()

    def populate_answer_keys(self, directory):
        count = 1
        answer_keys = []
        for file_name in glob.iglob('{}/*.csv'.format(directory), recursive=True):
            cols = []
            df = pandas.read_csv(file_name)
            for col in df.columns:
                cols.append(col)
            answer_key = Answerkey(cols[0])
            for i, j in df.iterrows():
                answer_key.insert_question("".join(j[0].split()), "".join(j[1].split()))
            answer_keys.append(answer_key)
            count += 1
        return answer_keys

    def populate_students_list(self, directory):
        students = []
        for file_name in glob.iglob('{}/*.xls'.format(directory), recursive=True):
            start = False
            df = pandas.read_excel(file_name)
            for i in df.itertuples():
                arr = np.asarray(i)
                cleaned_row = np.asarray([x for x in arr if str(x) != 'nan'])
                if cleaned_row.size < 2:
                    start = False
                if start:
                    if cleaned_row.size < 6:
                        exp = " "
                    else:
                        exp = cleaned_row[5]
                    st = Student(cleaned_row[2], self.utils.strip_accents(cleaned_row[3]),
                                 self.utils.strip_accents(cleaned_row[4]),
                                 exp)
                    students.append(st)
                if np.isin("Öğrenci No", cleaned_row):
                    start = True
        return students
        
    def populate_polls(self, directory):
        count = 1
        polls = []
        for file_name in glob.iglob('{}/*.csv'.format(directory), recursive=True):
            df = pandas.read_csv(file_name)
            poll = Poll()
            for i in df.itertuples():
                if len(i[0]) > 3:
                    data = [np.asarray(i[0])]
                    for j in range(1, len(i)):
                        if str(i[j]) != "nan":
                            data.append(i[j])
                    tup = []
                    for obj in data[0]:
                        tup.append(obj)
                else:
                    tup = [i[0][0], i[0][1]]
                for index in range(1, len(i)):
                    tup.append(i[index])
                tup = np.asarray([x for x in tup if str(x) != 'nan'])
                if poll.if_student_exists(tup[1]):
                    polls.append(poll)
                    poll = Poll()
                for q in range(4, len(tup), 2):
                    question = Question("".join(tup[q].split()), "".join(tup[q + 1].split()))
                    poll.insert_question(question)
                poll.insert_student(self.utils.strip_accents(tup[1]))
            polls.append(poll)
            count += 1
        return polls

    def identify_poll(self, polls, answer_keys):
        return_polls = []
        for pl in polls:
            for ak in answer_keys:
                if ak.is_question_present(pl.question_list):
                    pl.name = ak.name
                    pl.answerkey = ak
                    return_polls.append(pl)
                    break
        return return_polls

    def mark_attendance(self, students, polls):
        for st in students:
            for pl in polls:
                if pl.if_student_exists(st.fname + " " + st.lname):
                    st.attended_polls += 1
        return students

    def mark_quiz(self, poll):
        students = poll.students
        answer_key = poll.answerkey
        marked_students = []
        for st in students:
            marks = []
            question_list = students[st]
            for q in question_list:
                if answer_key.get_answer(str(q.question)) == q.get_answer():
                    marks.append(1)
                else:
                    marks.append(0)
            marked_students.append(marks)
        q_iter = 0
        chosen_answers = []
        for ak in answer_key.question_list:
            qa = {}
            for st in students:
                if not q_iter >= len(students[st]):
                    st_answer = students[st][q_iter].get_answer()
                    if st_answer in qa:
                        qa[st_answer] += 1
                    else:
                        qa[st_answer] = 1
            qa["correct"] = ak.get_answer()
            chosen_answers.append(qa)
            q_iter += 1
        return marked_students, chosen_answers
