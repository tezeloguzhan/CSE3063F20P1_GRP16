
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
