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
        self.buton1 = Button(master, text="Add Students List Files", width=35, height=2,
                             command=self.addstudent_file).place(x=850, y=250)
        self.buton2 = Button(master, text="Add Poll Files", width=35, height=2, command=self.addpoll_files).place(x=850,
                                                                                                                  y=325)
        self.buton3 = Button(master, text="Add Answers Files", width=35, height=2,
                             command=self.addanswers_files).place(x=850, y=400)
        self.buton4 = Button(master, text="Start", width=35, height=2, command=self.start).place(x=850, y=475)
        self.buton5 = Button(master, text="Show Result", width=35, height=2, command=self.newwindow).place(x=850, y=550)
        self.buton6 = Button(master, text="Show Histograms", width=35, height=2, command=self.imagewindow).place(x=850,
                                                                                                                 y=625)
