import tkinter as tk
from tkinter import *
from tkinter.ttk import *

from typing import Dict
from PIL import Image, ImageTk
import urllib.request

from NEA import get_types
from webscraping import *
from database import *
import database


global qNumber
qNumber = 1
myDb = database.Database("NEAdatabase.db")


class NEAselection(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.minsize(width=450, height=400)

        self.db = Database("NEAdatabase.db")

        self.wgts: Dict[str] = {}
        self.imgs: Dict[str] = {}

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.ents: Dict[str, tk.Entry] = {}
        self.btns: Dict[str, tk.Button] = {}
        self.rbtn: Dict[str, tk.Radiobutton] = {}

        self.create_frames()
        self.create_labels()
        self.create_buttons()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["entry"] = tk.Frame(self.frms["parent"])
        self.frms["entry"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)


    def create_labels(self):
        image_list = [['Batman', 'https://static1.personality-database.com/profile_images/79843d9575884e8d8bec216709f82464.png'],
                      ['Superman', 'https://static1.personality-database.com/profile_images/52eab3736f274e819b56274ed64ed6c6.png'],
                      ['Spider-Man', 'https://static1.personality-database.com/profile_images/12a8e090cb17461b9c40adf614255124.png']]

        for image in image_list:
            filename = f'Images{image[0]}.png'
            
            urllib.request.urlretrieve(image[1], filename)
            img = Image.open(filename)
            img = img.resize((75, 75))
            img.save(filename)
            img = ImageTk.PhotoImage(img)
            
            self.imgs[image[0]] = img

        character_lists = []
        character_list = [['Batman', 'DC Comics', self.imgs['Batman']],
                          ['Superman', 'DC Comics', self.imgs['Superman']],
                          ['Spider-Man', 'Marvel Comics', self.imgs['Spider-Man']]]

        for item in character_list:
            char_list = []
            char_list.append(item[0])
            char_list.append(item[1])
            char_list.append(item[2])
            character_lists.append(char_list)

        def deselect_character(name):
            for i in range(len(self.wgts[name])):
                self.wgts[name][i].config(bg='#cccccc')
            self.btns[name].config(text='Select', command=lambda n=name:select_character(n))

        def select_character(name):
            for i in range(len(self.wgts[name])):
                self.wgts[name][i].config(bg='#666666')
            self.btns[name].config(text='Deselect', command=lambda n=name:deselect_character(n))

        for num, item in enumerate(character_lists):
            name = item[0]
            series = item[1]
            pic = item[2]

            self.frms[name] = tk.Frame(self.frms["entry"], bg='#cccccc')
            self.frms[name].grid(row=num, column=0, columnspan=50, pady=5, sticky=tk.W)
            self.frms[name].config(height=90, width=350)
            self.frms[name].grid_propagate(0)

            self.frms[f'{name} Button'] = tk.Frame(self.frms["entry"], bg='#cccccc')
            self.frms[f'{name} Button'].grid(row=num, column=51, pady=5, sticky=tk.W)
            self.frms[f'{name} Button'].config(height=90, width=65)
            self.frms[f'{name} Button'].grid_propagate(0)

            self.lbls[f'{name} Picture'] = tk.Label(self.frms[name], image=pic, bg='#cccccc')
            self.lbls[f'{name} Picture'].grid(row=num, rowspan=2, column=0, padx=5, pady=5, sticky=tk.W)
            self.lbls[f'{name} Picture'].image=pic

            self.lbls[name] = tk.Label(self.frms[name], text=name, font=('Helvetica', 18), bg='#cccccc')
            self.lbls[name].grid(row=num, column=1, padx=5, sticky=tk.W)

            self.lbls[f'{name} Series'] = tk.Label(self.frms[name], text=series, bg='#cccccc')
            self.lbls[f'{name} Series'].grid(row=num+1, column=1, padx=5, sticky=tk.W)

            self.btns[name] = tk.Button(self.frms[f'{name} Button'], text='Select', height=4, command=lambda n=name:select_character(n))
            self.btns[name].grid(row=num, rowspan=2, column=2, pady=10, sticky=tk.E)

            self.wgts[name] = [self.frms[name],
                               self.frms[f'{name} Button'],
                               self.lbls[f'{name} Picture'],
                               self.lbls[name],
                               self.lbls[f'{name} Series']]


    def create_buttons(self):
        def destroy_window():
            global root
            root.destroy()

        self.btns["Quiz"] = tk.Button(self.frms["entry"], text='Finished', command=destroy_window)
        self.btns["Quiz"].grid(column=0, padx=5, pady=5, sticky=tk.W)



class NEAquiz(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.minsize(width=450, height=200)

        self.db = Database("NEAdatabase.db")

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}
        self.ents: Dict[str, tk.Entry] = {}
        self.btns: Dict[str, tk.Button] = {}
        self.rbtn: Dict[str, tk.Radiobutton] = {}

        self.create_frames()
        self.create_labels(qNumber)
        self.create_radio_buttons()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["entry"] = tk.Frame(self.frms["parent"])
        self.frms["entry"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.frms["finished"] = tk.Frame(self.frms["parent"])
        self.frms["finished"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)


    def create_labels(self, qNumber):
        Questions = myDb.get_questions(qNumber)
        Question = Questions[0]

        self.lbls["Question"] = tk.Label(self.frms["entry"], text=Question)
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
            rb = tk.Radiobutton(self.frms["entry"], text=text, variable=var, value=num, command=next_question)
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

        self.btns["Previous"] = tk.Button(self.frms["entry"], text='Previous', command=prev_question)
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

        self.db = Database("NEAdatabase.db")

        self.frms: Dict[str, tk.Frame] = {}
        self.lbls: Dict[str, tk.Label] = {}

        self.create_frames()
        self.create_labels()


    def create_frames(self):
        self.frms["parent"] = tk.Frame(self.parent)
        self.frms["parent"].grid(sticky=tk.W)

        self.frms["entry"] = tk.Frame(self.frms["parent"])
        self.frms["entry"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    
    def create_labels(self):
        label = tk.Label(self.frms["entry"], text='Results:')
        label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        label = tk.Label(self.frms["entry"])
        
        types = get_types()
        MBTI = types[0]
        Enneagram = types[1]
        BigFive = types[2]
            
        results = [f'MBTI: {MBTI}', f'Enneagram: {Enneagram}', f'Big Five: {BigFive}']
        
        for text in results:
            lbl = tk.Label(self.frms["entry"], text=text)
            lbl.grid(column=0, padx=5, sticky=tk.W)


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