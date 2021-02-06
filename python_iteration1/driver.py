from ZoomPollAnalyzer import ZoomPollAnalyzer
from tkinter import Tk, Listbox, Label, Button, filedialog, ttk, Toplevel, PhotoImage, Canvas
import shutil, os, pathlib
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
import glob
import time


class GUI:
    def __init__(self, master):
        self.master = master

        master.title("Zoom Poll Analyzer")
        master.geometry("1200x800")
        master.configure(bg="red3")
        self.listee = Listbox(master, width=80, height=35)
        self.listee.place(x=50, y=140)
        self.header = Label(master, text="ZOOM POLL ANALYZER", width=30, height=2, font=30).place(x=500, y=50)

        self.buton4 = Button(master, text="Start", width=35, height=2, command=self.start).place(x=850, y=475)
        self.buton5 = Button(master, text="Show Result", width=35, height=2, command=self.newwindow).place(x=850, y=550)
        self.buton6 = Button(master, text="Show Histograms", width=35, height=2, command=self.imagewindow).place(x=850,
                                                                                                                 y=625)

    def start(self):
        driver = ZoomPollAnalyzer("answer-keys-directory", "students-list-directory", "polls-directory", "output")
        driver.start()
        self.names = glob.glob(os.getcwd() + "/output/*/.xlsx", recursive=True)
        for i in self.names:
            if "Poll" in i.split("/")[-1]:
                self.listee.insert(0, i.split("/")[-1])
            elif "attendance" in i.split("/")[-1]:
                self.listee.insert(0, i.split("/")[-1])

    def newwindow(self):
        self.window = Tk()
        self.window.title("Student List")
        self.window.geometry("1000x600")
        xls = pd.ExcelFile(os.getcwd() + "/output/" + self.listee.get(self.listee.curselection()))
        sheetData = pd.read_excel(xls, 'Sheet1')
        headings = sheetData.columns
        data = list(headings.values.tolist())
        rows = len(sheetData)
        tree = ttk.Treeview(self.window, columns=data, show=["headings"], selectmode='browse')
        tree.place(x=0, y=100)

        for heading in headings:
            heading = str(heading)
            tree.column(heading, width=120, anchor='center')
            tree.heading(heading, text=heading)
        for rownumber in range(rows):
            rowvalue = sheetData.values[rownumber]
            rowdata = tuple(rowvalue)
            tree.insert('', 'end', values=rowdata)