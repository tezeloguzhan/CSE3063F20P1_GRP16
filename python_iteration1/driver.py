from ZoomPollAnalyzer import ZoomPollAnalyzer
from tkinter import Tk, Listbox, Label, Button, ttk, Toplevel
import pandas as pd
from PIL import Image, ImageTk
import glob
import os

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
        if os.name == 'darwin':
            self.names = glob.glob(os.getcwd() + "/output/**/*.xlsx", recursive=True)

            for i in self.names:
                if "Poll" in i.split("/")[-1]:
                    self.listee.insert(0, i.split("/")[-1])
                elif "attendance" in i.split("/")[-1]:
                    self.listee.insert(0, i.split("/")[-1])
        else:

            self.names = glob.glob(os.getcwd() + "\output/*.xlsx", recursive=True)
            for i in self.names:
                if "Poll" in i.split("\\")[-1]:
                    self.listee.insert(0, i.split("\\")[-1])
                elif "attendance" in i.split("\\")[-1]:
                    self.listee.insert(0, i.split("\\")[-1])

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

    def imagewindow(self):
        self.imagewindoww = Toplevel(bg='yellow')
        self.imagewindoww.title("Histograms With Reports")
        self.imagewindoww.geometry("1000x600")
        self.combo = ttk.Combobox(self.imagewindoww)
        self.combo.place(x=50, y=50)
        path = (os.getcwd() + "/output/Histograms " + self.listee.get(self.listee.curselection())).split(".xlsx")[0]
        self.png_dict = {}
        combo_values = []
        self.name = glob.glob(path[:-1] + str(int(path[-1]) - 1) + "/*.png", recursive=True)
        for qe in self.name:
            png = qe.split("/")[-1]
            combo_values.append(png.split(".")[0])
            self.png_dict[png.split(".")[0]] = qe
        combo_values.sort()
        self.combo["values"] = combo_values
        self.combo.bind("<<ComboboxSelected>>", lambda event: self.imageshow1(event))

    def imageshow1(self, event):
        png_file = self.combo.get()
        self.image = Image.open(self.png_dict[png_file])
        self.resized = self.image.resize((500, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.resized)
        self.showimage = Label(self.imagewindoww, image=self.photo)
        self.showimage.resized = self.photo
        self.showimage.place(x=50, y=100)
        excel = self.png_dict[png_file].split(".png")[0]+".xlsx"
        xls = pd.ExcelFile(excel)
        sheetData = pd.read_excel(xls, 'Sheet1')
        headings = sheetData.columns
        data = list(headings.values.tolist())
        rows = len(sheetData)
        tree = ttk.Treeview(self.imagewindoww, columns=data, show=["headings"], selectmode='browse')
        tree.place(x=600, y=100)
        for heading in headings:
            heading = str(heading)
            tree.column(heading, width=200, anchor='center')
            tree.heading(heading, text=heading)
        for rownumber in range(rows):
            rowvalue = sheetData.values[rownumber]
            rowdata = tuple(rowvalue)
            tree.insert('', 'end', values=rowdata)

root = Tk()
my_gui = GUI(root)
root.mainloop()