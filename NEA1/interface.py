import tkinter as tk
from tkinter import *
from tkinter.ttk import *

from typing import Dict
from PIL import Image, ImageTk
import urllib.request
import os

from NEA import get_types, get_char_types, get_difference
import database
import databaseChars
from webscraping import ids, get_celebs


global qNumber
qNumber = 1

global chars
chars = []

myDb = database.Database()
myCharDb = databaseChars.Database()


class NEAselection(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.minsize(width=450, height=400)

        self.db = myCharDb

        self.wgts: Dict[str] = {}

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.btns: Dict[str, tk.Button] = {}

        self.create_frames()
        self.create_labels()
        self.create_select_label()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["frame"] = tk.Frame(self.frms["parent"])
        self.frms["frame"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)


    def create_labels(self):
        def deselect_character(name):
            for i in range(len(self.wgts[name])-1):
                self.wgts[name][i+1].config(bg='#cccccc')
            self.btns[name].config(text='Select', command=lambda n=name:select_character(n))
            id = self.wgts[name][0]
            global chars
            chars.remove(id)
            if len(chars) == 0:
                self.create_select_label()
                self.btns["Quiz"].grid_forget()

        def select_character(name):
            for i in range(len(self.wgts[name])-1):
                self.wgts[name][i+1].config(bg='#666666')
            self.btns[name].config(text='Deselect', command=lambda n=name:deselect_character(n))
            id = self.wgts[name][0]
            global chars
            chars.append(id)
            if len(chars) == 1:
                self.create_buttons()
                self.lbls["Select"].grid_forget()
                

        for row,id in enumerate(ids):
            char_info = myCharDb.get_character_info(id)[0]

            name = char_info[0]
            series = char_info[1]
            image = char_info[2]

            urllib.request.urlretrieve(image, f'{id}.png')
            img = Image.open(f'{id}.png')
            img = img.resize((75, 75))
            img = ImageTk.PhotoImage(img)
            os.remove(f'{id}.png')

            self.frms[name] = tk.Frame(self.frms["frame"], bg='#cccccc')
            self.frms[name].grid(row=row, column=0, columnspan=50, pady=5, sticky=tk.W)
            self.frms[name].config(height=90, width=350)
            self.frms[name].grid_propagate(0)

            self.frms[f'{name} Frame'] = tk.Frame(self.frms["frame"], bg='#cccccc')
            self.frms[f'{name} Frame'].grid(row=row, column=51, pady=5, sticky=tk.W)
            self.frms[f'{name} Frame'].config(height=90, width=65)
            self.frms[f'{name} Frame'].grid_propagate(0)

            self.lbls[f'{name} Picture'] = tk.Label(self.frms[name], image=img, bg='#cccccc')
            self.lbls[f'{name} Picture'].grid(row=row, rowspan=2, column=0, padx=5, pady=5, sticky=tk.W)
            self.lbls[f'{name} Picture'].image=img

            self.lbls[f'{name} Label'] = tk.Label(self.frms[name], text=name, font=('TkDefaultFont', 12), bg='#cccccc')
            self.lbls[f'{name} Label'].grid(row=row, column=1, padx=5, sticky=tk.W)

            self.lbls[f'{name} Series'] = tk.Label(self.frms[name], text=series, bg='#cccccc')
            self.lbls[f'{name} Series'].grid(row=row+1, column=1, padx=5, sticky=tk.W)

            self.btns[name] = tk.Button(self.frms[f'{name} Frame'], text='Select', height=4, command=lambda n=name:select_character(n))
            self.btns[name].grid(row=row, rowspan=2, column=2, pady=10, sticky=tk.E)

            self.wgts[name] = [id,
                               self.frms[name],
                               self.frms[f'{name} Frame'],
                               self.lbls[f'{name} Picture'],
                               self.lbls[f'{name} Label'],
                               self.lbls[f'{name} Series']]


    def create_buttons(self):
        def destroy_window():
            global root
            root.destroy()

        self.btns["Quiz"] = tk.Button(self.frms["frame"], text='Finished', command=destroy_window)
        self.btns["Quiz"].grid(column=0, padx=5, pady=5, sticky=tk.W)

    
    def create_select_label(self):
        self.lbls["Select"] = tk.Label(self.frms["frame"], text='Select at least 1 character')
        self.lbls["Select"].grid(column=0, padx=5, pady=5, sticky=tk.W)





class NEAquiz(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.minsize(width=450, height=200)

        self.db = myDb

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.btns: Dict[str, tk.Button] = {}
        self.rbtn: Dict[str, tk.Radiobutton] = {}

        self.create_frames()
        self.create_labels(qNumber)
        self.create_radio_buttons()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["frame"] = tk.Frame(self.frms["parent"])
        self.frms["frame"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.frms["finished"] = tk.Frame(self.frms["parent"])
        self.frms["finished"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)


    def create_labels(self, qNumber):
        Questions = myDb.get_questions(qNumber)
        Question = Questions[0]

        self.lbls["Question"] = tk.Label(self.frms["frame"], text=Question)
        self.lbls["Question"].grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    

    def update_labels(self, qNumber):
        Questions = myDb.get_questions(qNumber)
        Question = Questions[0]
        
        self.lbls["Question"].config(text=Question)
    

    def create_radio_buttons(self):
        global var
        var = tk.IntVar()

        qAmount = myDb.get_amount_of_questions()
        qHighest = qAmount[0]

        def next_question():
            global qNumber
            if qNumber == qHighest:
                    self.create_finished_button()
            elif qNumber < qHighest:
                radioValue = var.get()
                myDb.insert_answer(radioValue, qNumber)
                qNumber += 1
                var.set(None)
                self.update_labels(qNumber)
                if qNumber == 2:
                    self.create_prev_button()

        options = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
        options_list = []

        for num,text in enumerate(options):
            rb = tk.Radiobutton(self.frms["frame"], text=text, variable=var, value=num, command=next_question)
            rb.grid(column=0, padx=50, sticky=tk.W)
            options_list.append(rb)        


    def create_prev_button(self):
        def prev_question():
            global qNumber
            qNumber -= 1
            answers = myDb.get_answers(qNumber)
            answer = answers[0][3]
            global var
            var.set(answer)
            if qNumber == 1:
                self.btns["Previous"].grid_remove()
            self.update_labels(qNumber)

        self.btns["Previous"] = tk.Button(self.frms["frame"], text='Previous', command=prev_question)
        self.btns["Previous"].grid(row=50, column=0, padx=5, pady=5, sticky=tk.W)

    
    def create_finished_button(self):
        def destroy_window():
            global root
            root.destroy()
        
        self.btns["Finished"] = tk.Button(self.frms["finished"], text='Finished', command=destroy_window)
        self.btns["Finished"].grid(row=50, column=1, padx=5, pady=5, sticky=tk.W)



class NEAresults(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.minsize(width=450, height=200)

        self.db = myDb

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}

        self.create_frames()
        self.create_labels()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        for num,frame in enumerate(["char", "quiz", "diff"]):
            self.frms[frame] = tk.Frame(self.frms["parent"])
            self.frms[frame].grid(column=num, row=0, padx=10, sticky=tk.W)

        self.frms["like"] = tk.Frame(self.frms["parent"])
        self.frms["like"].grid(row=1, columnspan=4, pady=10, padx=10, sticky=tk.W)

    
    def create_labels(self):

        # Selection
        
        label = tk.Label(self.frms["char"], text='Selection Results:')
        label.grid(pady=10, sticky=tk.W)

        global chars
        for id in chars:
            CharMBTI, CharEnnea, CharBig5 = get_char_types(id)
        
        char_results = [f'MBTI: {CharMBTI}', f'Enneagram: {CharEnnea}', f'Big Five: {CharBig5}']

        for text in char_results:
            lbl = tk.Label(self.frms["char"], text=text)
            lbl.grid(sticky=tk.W)
        

        # Quiz
        
        label = tk.Label(self.frms["quiz"], text='Quiz Results:')
        label.grid(pady=10, sticky=tk.W)

        MBTItype, Enneagram, BigFive = get_types()
        results = [f'MBTI: {MBTItype}', f'Enneagram: {Enneagram}', f'Big Five: {BigFive}']

        for text in results:
            lbl = tk.Label(self.frms["quiz"], text=text)
            lbl.grid(sticky=tk.W)
        

        # Difference
        
        label = tk.Label(self.frms["diff"], text='Percentage Difference:')
        label.grid(pady=10, sticky=tk.W)

        DiffMBTI, DiffEnnea, DiffBig5 = get_difference([CharMBTI,CharEnnea,CharBig5], [MBTItype,Enneagram,BigFive])
        diff_results = [f'MBTI: {DiffMBTI}', f'Enneagram: {DiffEnnea}', f'Big Five: {DiffBig5}']

        for text in diff_results:
            lbl = tk.Label(self.frms["diff"], text=text)
            lbl.grid(sticky=tk.W)


        # Celebs

        label = tk.Label(self.frms["like"], text='You are similar to:')
        label.grid(pady=10, sticky=tk.W)

        charCelebs = get_celebs(CharMBTI, CharEnnea)
        quizCelebs = get_celebs(MBTItype, Enneagram)

        grid = 0

        for info in (charCelebs | quizCelebs):
            name = info.split('|||')[0]
            image = info.split('|||')[1]

            urllib.request.urlretrieve(image, f'celeb.png')
            img = Image.open(f'celeb.png')
            img = img.resize((25, 25))
            img = ImageTk.PhotoImage(img)
            os.remove(f'celeb.png')

            lbl = tk.Label(self.frms["like"], text=name, image=img, compound='left')
            lbl.grid(column=grid, row=1, sticky=tk.W)
            lbl.image=img

            grid += 1



def runSelection():
    global root
    root = tk.Tk()
    NEAselection(root).grid()
    root.mainloop()


def runQuiz():
    global root
    root = tk.Tk()
    NEAquiz(root).grid()
    root.mainloop()


def runResults():
    root = tk.Tk()
    NEAresults(root).grid()
    root.mainloop()


runSelection()
runQuiz()
runResults()