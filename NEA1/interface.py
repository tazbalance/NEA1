import tkinter as tk 
from tkinter import * 
from tkinter.ttk import * 
from typing import Dict 
from PIL import Image, ImageTk 
import urllib.request 
import os 
from webscraping import find_info 
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
 

    def deselect_character(self, id): 
        for i in range(len(self.wgts[id])): 
            self.wgts[id][i].config(bg='#cccccc') 
        self.btns[id].config(text='Select', command=lambda n=id:self.select_character(n)) 
        chars = self.theData.remove_char(id) 
        if len(chars) == 0: 
            self.create_select_label() 
            self.btns["Quiz"].grid_forget() 

 
    def select_character(self, id): 
        for i in range(len(self.wgts[id])): 
            self.wgts[id][i].config(bg='#666666') 
        self.btns[id].config(text='Deselect', command=lambda n=id:self.deselect_character(n)) 
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

            self.frms[id] = tk.Frame(self.frms["frame"], bg='#cccccc') 
            self.frms[id].grid(row=row, column=0, columnspan=50, pady=5, sticky=tk.W) 
            self.frms[id].config(height=90, width=350) 
            self.frms[id].grid_propagate(0) 

            self.frms[f'{id} Frame'] = tk.Frame(self.frms["frame"], bg='#cccccc') 
            self.frms[f'{id} Frame'].grid(row=row, column=51, pady=5, sticky=tk.W) 
            self.frms[f'{id} Frame'].config(height=90, width=65) 
            self.frms[f'{id} Frame'].grid_propagate(0) 

            self.lbls[f'{id} Picture'] = tk.Label(self.frms[id], image=img, bg='#cccccc') 
            self.lbls[f'{id} Picture'].grid(row=row, rowspan=2, column=0, padx=5, pady=5, sticky=tk.W) 
            self.lbls[f'{id} Picture'].image=img 

            self.lbls[f'{id} Label'] = tk.Label(self.frms[id], text=name, font=(12), bg='#cccccc') 
            self.lbls[f'{id} Label'].grid(row=row, column=1, padx=5, sticky=tk.W) 

            self.lbls[f'{id} Series'] = tk.Label(self.frms[id], text=series, bg='#cccccc') 
            self.lbls[f'{id} Series'].grid(row=row+1, column=1, padx=5, sticky=tk.W) 

            self.btns[id] = tk.Button(self.frms[f'{id} Frame'], text='Select', height=4, command=lambda n=id:self.select_character(n)) 
            self.btns[id].grid(row=row, rowspan=2, column=2, pady=10, sticky=tk.E) 

            self.wgts[id] = [self.frms[id], 
                               self.frms[f'{id} Frame'], 
                               self.lbls[f'{id} Picture'], 
                               self.lbls[f'{id} Label'], 
                               self.lbls[f'{id} Series']] 

 

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
        NEAgraph = NEA.Graph()

        # Selection
        
        label = tk.Label(self.frms["char"], text='Selection Results:')
        label.grid(pady=10, sticky=tk.W)

        NEAtypes.instantiate_types()
        selectedChars = self.theData.get_chars()
        selectedGenres = []

        for id in selectedChars:
            genre = self.theData.get_character_genre(id)
            selectedGenres.append([id, genre])
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


        # Similar
            
        label = tk.Label(self.frms["like"], text='You are similar to:')
        label.grid(pady=10, sticky=tk.W)

        similarList = NEAgraph.find_characters(CharMBTI, MBTItype)

        grid = 0
        genreDict = {}

        for id, genre in selectedGenres:
            if genre in genreDict:
                genreDict.update({genre: genreDict[genre]+1})
            else:
                genreDict.update({genre: 1})

        priorityList = []

        for id in similarList:
            priorityList.append([id, genreDict[self.theData.get_character_genre(id)]])
        
        priorityList.sort(key=lambda x:x[1],reverse=True)

        for id, genre in priorityList:
            if int(id) not in selectedChars:

                character = self.theData.get_character_info(id)[0]
                name = character[0]
                image = character[2]

                urllib.request.urlretrieve(image, f'similar.png')
                img = Image.open(f'similar.png')
                img = img.resize((25, 25))
                img = ImageTk.PhotoImage(img)
                os.remove(f'similar.png')

                lbl = tk.Label(self.frms["like"], text=name, image=img, compound='left')
                lbl.grid(column=grid, row=1, sticky=tk.W)
                lbl.image=img

                grid += 1


if __name__ == "__main__":
    root = tk.Tk()
    NEAselection(root).grid()
    root.mainloop()