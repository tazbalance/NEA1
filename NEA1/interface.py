import tkinter as tk
from tkinter import *
from tkinter.ttk import *

from typing import Dict
from PIL import Image, ImageTk
import urllib.request
import os

from webscraping import find_info, get_celebs
import NEA
import data


class NEAselection(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Selection")
        parent.minsize(width=450, height=400)

        self.theData = data.Data()
        find_info()

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


    def deselect_character(self, name):
        for i in range(len(self.wgts[name])-1):
            self.wgts[name][i+1].config(bg='#cccccc')
        self.btns[name].config(text='Select', command=lambda n=name:self.select_character(n))
        id = self.wgts[name][0]
        chars = self.theData.remove_char(id)
        if len(chars) == 0:
            self.create_select_label()
            self.btns["Quiz"].grid_forget()


    def select_character(self, name):
            for i in range(len(self.wgts[name])-1):
                self.wgts[name][i+1].config(bg='#666666')
            self.btns[name].config(text='Deselect', command=lambda n=name:self.deselect_character(n))
            id = self.wgts[name][0]
            chars = self.theData.append_char(id)
            if len(chars) == 1:
                self.create_buttons()
                self.lbls["Select"].grid_forget()


    def create_labels(self):
        ids = self.theData.get_ids()

        for row,id in enumerate(ids):
            name, series, image = self.theData.get_character_info(id)[0]

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

            self.lbls[f'{name} Label'] = tk.Label(self.frms[name], text=name, font=(12), bg='#cccccc')
            self.lbls[f'{name} Label'].grid(row=row, column=1, padx=5, sticky=tk.W)

            self.lbls[f'{name} Series'] = tk.Label(self.frms[name], text=series, bg='#cccccc')
            self.lbls[f'{name} Series'].grid(row=row+1, column=1, padx=5, sticky=tk.W)

            self.btns[name] = tk.Button(self.frms[f'{name} Frame'], text='Select', height=4, command=lambda n=name:self.select_character(n))
            self.btns[name].grid(row=row, rowspan=2, column=2, pady=10, sticky=tk.E)

            self.wgts[name] = [id,
                               self.frms[name],
                               self.frms[f'{name} Frame'],
                               self.lbls[f'{name} Picture'],
                               self.lbls[f'{name} Label'],
                               self.lbls[f'{name} Series']]


    def create_buttons(self):
        self.btns["Quiz"] = tk.Button(self.frms["frame"], text='Finished', command=self.destroy_window)
        self.btns["Quiz"].grid(column=0, padx=5, pady=5, sticky=tk.W)

    
    def create_select_label(self):
        self.lbls["Select"] = tk.Label(self.frms["frame"], text='Select at least 1 character')
        self.lbls["Select"].grid(column=0, padx=5, pady=5, sticky=tk.W)


    def destroy_window(self):
        self.parent.destroy()
        root = tk.Tk()
        NEAquiz(root, self.theData).grid()
        root.mainloop()





class NEAquiz(tk.Frame):
    
    def __init__(self, parent, theData, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Quiz")
        parent.minsize(width=450, height=200)

        self.theData = theData

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.btns: Dict[str, tk.Button] = {}
        self.rbtn: Dict[str, tk.Radiobutton] = {}

        self.create_frames()
        self.create_labels()
        self.create_radio_buttons()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["frame"] = tk.Frame(self.frms["parent"])
        self.frms["frame"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.frms["finished"] = tk.Frame(self.frms["parent"])
        self.frms["finished"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)


    def create_labels(self):
        Questions = self.theData.get_questions()
        Question = Questions[0]

        self.lbls["Question"] = tk.Label(self.frms["frame"], text=Question)
        self.lbls["Question"].grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    

    def create_radio_buttons(self):
        var = tk.IntVar()

        options = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
        options_list = []

        for num,text in enumerate(options):
            rb = tk.Radiobutton(self.frms["frame"], text=text, variable=var, value=num, command=lambda n=var:self.next_question(n))
            rb.grid(column=0, padx=50, sticky=tk.W)
            options_list.append(rb)


    def next_question(self, var):
        qAmount = self.theData.get_amount_of_questions()
        qHighest = qAmount[0]
        qNumber = self.theData.get_qnumber()

        if qNumber == qHighest:
            self.create_finished_button()
        elif qNumber < qHighest:
            radioValue = var.get()
            self.theData.insert_answer(radioValue, qNumber)
            qNumber = self.theData.increase_qnumber()
            var.set(None)
            self.update_labels()
            if qNumber == 2:
                self.create_prev_button(var)       


    def prev_question(self, var):
        qNumber = self.theData.decrease_qnumber()
        answer = self.theData.get_answers()[0][3]
        var.set(answer)
        if qNumber == 1:
            self.btns["Previous"].grid_remove()
        self.update_labels()


    def create_prev_button(self, var):
        self.btns["Previous"] = tk.Button(self.frms["frame"], text='Previous', command=lambda n=var:self.prev_question(n))
        self.btns["Previous"].grid(row=50, column=0, padx=5, pady=5, sticky=tk.W)


    def update_labels(self):
        Questions = self.theData.get_questions()
        Question = Questions[0]
        
        self.lbls["Question"].config(text=Question)
    

    def create_finished_button(self):
        self.btns["Finished"] = tk.Button(self.frms["finished"], text='Finished', command=self.destroy_window)
        self.btns["Finished"].grid(row=50, column=1, padx=5, pady=5, sticky=tk.W)


    def destroy_window(self):
        self.parent.destroy()
        root = tk.Tk()
        NEAresults(root, self.theData).grid()
        root.mainloop()



class NEAresults(tk.Frame):
    
    def __init__(self, parent, theData, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Results")
        parent.minsize(width=450, height=200)

        self.theData = theData

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

        NEAtypes = NEA.Types()

        # Selection
        
        label = tk.Label(self.frms["char"], text='Selection Results:')
        label.grid(pady=10, sticky=tk.W)

        NEAtypes.instantiate_types()
        for id in self.theData.get_chars():
            CharMBTI, CharEnnea, CharBig5 = NEAtypes.get_char_types(id)
        
        char_results = [f'MBTI: {CharMBTI}', f'Enneagram: {CharEnnea}', f'Big Five: {CharBig5}']

        for text in char_results:
            lbl = tk.Label(self.frms["char"], text=text)
            lbl.grid(sticky=tk.W)
        

        # Quiz
        
        label = tk.Label(self.frms["quiz"], text='Quiz Results:')
        label.grid(pady=10, sticky=tk.W)

        NEAtypes.instantiate_types()
        MBTItype, Enneagram, BigFive = NEAtypes.get_types()
        results = [f'MBTI: {MBTItype}', f'Enneagram: {Enneagram}', f'Big Five: {BigFive}']

        for text in results:
            lbl = tk.Label(self.frms["quiz"], text=text)
            lbl.grid(sticky=tk.W)
        

        # Difference
        
        label = tk.Label(self.frms["diff"], text='Percentage Difference:')
        label.grid(pady=10, sticky=tk.W)

        DiffMBTI, DiffEnnea, DiffBig5 = NEAtypes.get_difference([CharMBTI,CharEnnea,CharBig5], [MBTItype,Enneagram,BigFive])
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


if __name__ == "__main__":
    root = tk.Tk()
    NEAselection(root).grid()
    root.mainloop()