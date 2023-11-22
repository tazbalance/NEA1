import tkinter as tk
from tkinter.ttk import *
from database import *
import database
from typing import Dict, List, Optional

global qNumber
qNumber = 1
myDb = database.Database("NEAdatabase.db")

class NEAprogram(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.minsize(width=450, height=200)

        self.db = Database("NEAdatabase.db")

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.ents: Dict[str, tk.Entry] = {}
        self.btns: Dict[str, tk.Button] = {}
        self.rbtns: Dict[str, tk.Radiobutton] = {}

        self.create_frames()
        self.create_label_widgets(qNumber)
        self.create_radio_buttons()


    def create_frames(self):
        
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["entry"] = tk.Frame(self.frms["parent"])
        self.frms["entry"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)


    def create_label_widgets(self, qNumber):

        Questions = myDb.get_questions(qNumber)
        Question = Questions[0]

        self.lbls["Question"] = tk.Label(self.frms["entry"], text=Question)
        self.lbls["Question"].grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    

    def update_label_widgets(self, qNumber):
        
        Questions = myDb.get_questions(qNumber)
        Question = Questions[0]
        
        self.lbls["Question"].config(text=Question)
    

    def create_radio_buttons(self):

        global var
        var = tk.IntVar()
 
        def next_question():
            
            global qNumber
            if qNumber < 13:
                radioValue = var.get()
                myDb.insert_answer(qNumber, radioValue)
                qNumber += 1
                var.set(None)
                self.update_label_widgets(qNumber)
                if qNumber == 2:
                    self.create_prev_button()
            else:
                self.lbls["Question"].config(text="finished")

        values = {"Strongly Disagree": 1,
          "Disagree": 2,
          "Neutral": 3,
          "Agree": 4,
          "Strongly Agree": 5}

        for (text, value) in values.items():
            tk.Radiobutton(self.frms["entry"], text=text, variable=var, value=value, command=next_question).grid(column=0, padx=50, sticky=tk.W)
        

    def create_prev_button(self):
        def prev_question():
            global qNumber
            qNumber -= 1
            answers = myDb.get_answers(qNumber)
            answer = answers[0][3]
            global var
            var.set(answer)
            if qNumber == 1:
                PrevButton.grid_remove()
            self.update_label_widgets(qNumber)

        PrevButton = tk.Button(self.frms["entry"], text='Previous', command=prev_question)
        PrevButton.grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)


def run():
    root = tk.Tk()
    root.geometry("450x200")
    NEAprogram(root).grid()
    root.mainloop()


run()