import tkinter as tk
from tkinter.ttk import *
from database import *
import database
from NEA import qNumber
from typing import Dict, List, Optional

myDb = database.Database("NEAdatabase.db")


class NEAprogram(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.db = Database("NEAdatabase.db")

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.ents: Dict[str, tk.Entry] = {}
        self.btns: Dict[str, tk.Button] = {}
        self.rbtns: Dict[str, tk.Radiobutton] = {}

        self.create_frames()
        self.create_label_widgets(qNumber)
        self.create_radio_buttons(qNumber)
        self.create_buttons()


    def create_frames(self):
        
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid()

        self.frms["entry"] = tk.Frame(self.frms["parent"])
        self.frms["entry"].grid(row=0, column=0, padx=5, pady=5)


    def create_label_widgets(self, qNumber):

        Questions = myDb.get_questions(qNumber)
        Question = Questions[0]

        self.lbls["Question"] = tk.Label(self.frms["entry"], text=Question)
        self.lbls["Question"].grid(row=0, column=0, padx=5, pady=5)


    def create_radio_buttons(self, qNumber):

        var = tk.IntVar()
        # radioLabel = tk.Label(self, bg='white', width=20, text='empty')
        # radioLabel.pack()
 
        def print_selection():
            radioValue = var.get()
            myDb.insert_answer(qNumber, radioValue)
            next_question()
            # radioLabel.config(text=f'you have selected {radioValue}')
 
        StrongDis = tk.Radiobutton(self, text='Strongly Disagree', variable=var, value=-4, command=print_selection)
        StrongDis.pack()

        Disagree = tk.Radiobutton(self, text='Disagree', variable=var, value=-2, command=print_selection)
        Disagree.pack()

        Neutral = tk.Radiobutton(self, text='Neutral', variable=var, value=0, command=print_selection)
        Neutral.pack()

        Agree = tk.Radiobutton(self, text='Agree', variable=var, value=2, command=print_selection)
        Agree.pack()

        StrongAgree = tk.Radiobutton(self, text='Strongly Agree', variable=var, value=4, command=print_selection)
        StrongAgree.pack()


    def create_buttons(self):
        PrevButton = tk.Button(self, text='Next', command=prev_question)
        PrevButton.pack()


def run():
    root = tk.Tk()
    NEAprogram(root).grid()
    root.mainloop()


run()