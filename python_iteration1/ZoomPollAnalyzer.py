
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