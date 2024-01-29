from re import A
import data
import database
from webscraping import get_type_values
import difflib


class Types():


    def instantiate_types(self):

        self.MBTIfuncs = {'Si':0, 'Se':0, 'Ni':0, 'Ne':0,
                          'Fi':0, 'Fe':0, 'Ti':0, 'Te':0}

        self.Enneas = {'1':0, '2':0, '3':0,
                       '4':0, '5':0, '6':0,
                       '7':0, '8':0, '9':0}

        self.BigFives = {'R':0, 'S':0,
                         'L':0, 'C':0,
                         'U':0, 'O':0,
                         'E':0, 'A':0,
                         'N':0, 'I':0}

        self.MBTIlist = [['Si', 'Fe', 'Ti', 'Ne'], ['Fe', 'Si', 'Ne', 'Ti'], ['Ti', 'Ne', 'Si', 'Fe'], ['Ne', 'Ti', 'Fe', 'Si'],
                         ['Si', 'Te', 'Fi', 'Ne'], ['Te', 'Si', 'Ne', 'Fi'], ['Fi', 'Ne', 'Si', 'Te'], ['Ne', 'Fi', 'Te', 'Si'],
                         ['Ni', 'Fe', 'Ti', 'Se'], ['Fe', 'Ni', 'Se', 'Ti'], ['Ti', 'Se', 'Ni', 'Fe'], ['Se', 'Ti', 'Fe', 'Ni'],
                         ['Ni', 'Te', 'Fi', 'Se'], ['Te', 'Ni', 'Se', 'Fi'], ['Fi', 'Se', 'Ni', 'Te'], ['Se', 'Fi', 'Te', 'Ni']]


    def get_char_types(self, id):

        MBTIvalues, EnneaValues, BigFiveValues = get_type_values(id)

        for CharMBTI, Function in zip(MBTIvalues.values(), self.MBTIlist):
            self.MBTIfuncs[Function[0]] += 8 * CharMBTI
            self.MBTIfuncs[Function[1]] += 4 * CharMBTI
            self.MBTIfuncs[Function[2]] += 2 * CharMBTI
            self.MBTIfuncs[Function[3]] += 1 * CharMBTI

        for key, value in EnneaValues.items():
            self.Enneas[key] += value
    
        for key, value in BigFiveValues.items():
            self.BigFives[key] += value

        HighestMBTI, HighestEnnea, HighestBigFive = self.calculate_types(self.MBTIfuncs, self.Enneas, self.BigFives)
        return HighestMBTI, HighestEnnea, HighestBigFive


    def get_types(self):

        myDb = database.Database()
        theData = data.Data()

        qAmount = theData.get_amount_of_questions()
        qHighest = qAmount[0]

        for i in range(qHighest):
            answers = myDb.get_answers(i+1)

            if answers[0][0] != '/':
                self.MBTIfuncs[answers[0][0]] += answers[0][3]
            if answers[0][1] != '/':
                self.Enneas[answers[0][1]] += answers[0][3]
            if answers[0][2] != '/':
                self.BigFives[answers[0][2]] += answers[0][3]

        HighestMBTI, HighestEnnea, HighestBigFive = self.calculate_types(self.MBTIfuncs, self.Enneas, self.BigFives)
        return HighestMBTI, HighestEnnea, HighestBigFive


    def calculate_types(self, MBTI, Enneagram, Big5):

        # Calculating MBTI

        Quad = {'SiNeTiFe': MBTI['Si'] + MBTI['Ne'] + MBTI['Ti'] + MBTI['Fe'],
                'SeNiTiFe': MBTI['Se'] + MBTI['Ni'] + MBTI['Ti'] + MBTI['Fe'],
                'SiNeTeFi': MBTI['Si'] + MBTI['Ne'] + MBTI['Te'] + MBTI['Fi'],
                'SeNiTeFi': MBTI['Se'] + MBTI['Ni'] + MBTI['Te'] + MBTI['Fi']}
        Quadra = max(Quad, key=Quad.get)

        perceivingFuncs = [MBTI[Quadra[0:2]], MBTI[Quadra[2:4]]]
        judgingFuncs = [MBTI[Quadra[4:6]], MBTI[Quadra[6:8]]]

        perceivingDiff = abs(perceivingFuncs[0] - perceivingFuncs[1])
        judgingDiff = abs(judgingFuncs[0] - judgingFuncs[1])

        if Quadra == 'SiNeTiFe':
            if perceivingDiff > judgingDiff:
                DomInf = {'ISFJ': MBTI['Si'], 'ENTP': MBTI['Ne']}
            else:
                DomInf = {'ESFJ': MBTI['Fe'], 'INTP': MBTI['Ti']}

        elif Quadra == 'SeNiTiFe':
            if perceivingDiff > judgingDiff:
                DomInf = {'ESTP': MBTI['Se'], 'INFJ': MBTI['Ni']}
            else:
                DomInf = {'ISTP': MBTI['Ti'], 'ENFJ': MBTI['Fe']}

        elif Quadra == 'SiNeTeFi':
            if perceivingDiff > judgingDiff:
                DomInf = {'ISTJ': MBTI['Si'], 'ENFP': MBTI['Ne']}
            else:
                DomInf = {'ESTJ': MBTI['Te'], 'INFP': MBTI['Fi']}

        elif Quadra == 'SeNiTeFi':
            if perceivingDiff > judgingDiff:
                DomInf = {'ESTP': MBTI['Se'], 'INFJ': MBTI['Ni']}
            else:
                DomInf = {'ISFP': MBTI['Fe'], 'ENTJ': MBTI['Te']}
    
        HighestMBTI = max(DomInf, key=DomInf.get)


        # Calculating Enneagram

        HighestEnnea = max(Enneagram, key=Enneagram.get)

        if HighestEnnea == '1':
            Wings = {'2':Enneagram['2'], '9':Enneagram['9']}
        elif HighestEnnea == '2':
            Wings = {'1':Enneagram['1'], '3':Enneagram['3']}
        elif HighestEnnea == '3':
            Wings = {'2':Enneagram['2'], '4':Enneagram['4']}
        elif HighestEnnea == '4':
            Wings = {'3':Enneagram['3'], '5':Enneagram['5']}
        elif HighestEnnea == '5':
            Wings = {'4':Enneagram['4'], '6':Enneagram['6']}
        elif HighestEnnea == '6':
            Wings = {'5':Enneagram['5'], '7':Enneagram['7']}
        elif HighestEnnea == '7':
            Wings = {'6':Enneagram['6'], '8':Enneagram['8']}
        elif HighestEnnea == '8':
            Wings = {'7':Enneagram['7'], '9':Enneagram['9']}
        elif HighestEnnea == '9':
            Wings = {'8':Enneagram['8'], '1':Enneagram['1']}

        HighestEnnea += 'w' + max(Wings, key=Wings.get)


        # Calculating BigFive

        BigFive = ''
        BigFive += max({'R':Big5['R'], 'S':Big5['S']}, key=Big5.get)
        BigFive += max({'L':Big5['L'], 'C':Big5['C']}, key=Big5.get)
        BigFive += max({'U':Big5['U'], 'O':Big5['O']}, key=Big5.get)
        BigFive += max({'E':Big5['E'], 'A':Big5['A']}, key=Big5.get)
        BigFive += max({'N':Big5['N'], 'I':Big5['I']}, key=Big5.get)

        return HighestMBTI, HighestEnnea, BigFive


    def get_difference(gchar, gquiz):

        # MBTI

        FuncList = {'ISFJ': 'Si Fe Ti Ne', 'ESFJ': 'Fe Si Ne Ti',
                    'INTP': 'Ti Ne Si Fe', 'ENTP': 'Ne Ti Fe Si',
                    'ISTJ': 'Si Te Fi Ne', 'ESTJ': 'Te Si Ne Fi',
                    'INFP': 'Fi Ne Si Te', 'ENFP': 'Ne Fi Te Si',
                    'INFJ': 'Ni Fe Ti Se', 'ENFJ': 'Fe Ni Se Ti',
                    'ISTP': 'Ti Se Ni Fe', 'ESTP': 'Se Ti Fe Ni',
                    'INTJ': 'Ni Te Fi Se', 'ENTJ': 'Te Ni Se Fi',
                    'ISFP': 'Fi Se Ni Te', 'ESFP': 'Se Fi Te Ni'}

        char = FuncList[gchar[0]]
        quiz = FuncList[gquiz[0]]

        diff = list(difflib.Differ().compare(char.split(), quiz.split()))
        mbtiDiff = percentage(4, diff)


        # Enneagram

        EnneaList = {'2': {'Compliant', 'Positive', 'Rejection'},
                     '3': {'Assertive', 'Attachment', 'Competent'},
                     '4': {'Frustration', 'Reactive', 'Withdrawn'},
             
                     '5': {'Competent', 'Rejection', 'Withdrawn'},
                     '6': {'Attachment', 'Compliant', 'Reactive'},
                     '7': {'Assertive', 'Frustration', 'Positive'},
             
                     '8': {'Assertive', 'Reactive', 'Rejection'},
                     '9': {'Attachment', 'Positive', 'Withdrawn'},
                     '1': {'Competent', 'Compliant', 'Frustration'}}

        char = EnneaList[gchar[1][0]].union(EnneaList[gchar[1][2]])
        quiz = EnneaList[gquiz[1][0]].union(EnneaList[gquiz[1][2]])

        enneaPercent = round(len(char&quiz)/len(quiz&quiz)*100)
        enneaPercent = 5 * round(enneaPercent/5)

        if gchar[1][2] == gquiz[1][0]:
            enneaPercent = 80
        if gchar[1][0] == gquiz[1][2]:
            enneaPercent = 85
        if enneaPercent == 100 and gchar[1] != gquiz[1]:
            enneaPercent = 90
        if enneaPercent != 100 and gchar[1][0] == gquiz[1][0]:
            enneaPercent = 95

        enneaDiff = f'{enneaPercent}%'


        # Big Five

        diff = list(difflib.Differ().compare([*gchar[2]], [*gquiz[2]]))
        big5Diff = percentage(5, diff)

        return mbtiDiff, enneaDiff, big5Diff


    def percentage(amt, diff):
        pos = amt

        for item in diff:
            if item[0] == '-':
                pos -= 1

        return f'{round(pos/amt*100)}%'


"""
List = ['1w9','1w2','2w1','2w3','3w2','3w4','4w3','4w5','5w4','5w6','6w5','6w7','7w6','7w8','8w7','8w9','9w8','9w1']

for mbti in List:
    for mbti2 in List:
        diff = get_difference(['ISFJ', mbti, 'RLOAN'], ['ISFJ', mbti2, 'RLOAN'])
        mbtidiff = diff[1]
        print(f'{mbti} & {mbti2}: {mbtidiff}')
        
for mbti in List:
    highest = []
    for mbti2 in List:
        diff = get_difference(['ISFJ', mbti, 'RLOAN'], ['ISFJ', mbti2, 'RLOAN'])
        mbtidiff = diff[1]
        if mbtidiff >= 85:
            highest.append(mbti2)
    print(highest)
"""


mbtiGraph = {'ISFJ': ['ESFJ', 'INTP', 'ISTJ', 'ESTJ', 'INFJ', 'ENFJ'],
             'ESFJ': ['ISFJ', 'ENTP', 'ISTJ', 'ESTJ', 'INFJ', 'ENFJ'],
             'INTP': ['ISFJ', 'ENTP', 'INFP', 'ENFP', 'ISTP', 'ESTP'],
             'ENTP': ['ESFJ', 'INTP', 'INFP', 'ENFP', 'ISTP', 'ESTP'],
             'ISTJ': ['ISFJ', 'ESFJ', 'ESTJ', 'INFP', 'INTJ', 'ENTJ'],
             'ESTJ': ['ISFJ', 'ESFJ', 'ISTJ', 'ENFP', 'INTJ', 'ENTJ'],
             'INFP': ['INTP', 'ENTP', 'ISTJ', 'ENFP', 'ISFP', 'ESFP'],
             'ENFP': ['INTP', 'ENTP', 'ESTJ', 'INFP', 'ISFP', 'ESFP'],
             'INFJ': ['ISFJ', 'ESFJ', 'ENFJ', 'ISTP', 'INTJ', 'ENTJ'],
             'ENFJ': ['ISFJ', 'ESFJ', 'INFJ', 'ESTP', 'INTJ', 'ENTJ'],
             'ISTP': ['INTP', 'ENTP', 'INFJ', 'ESTP', 'ISFP', 'ESFP'],
             'ESTP': ['INTP', 'ENTP', 'ENFJ', 'ISTP', 'ISFP', 'ESFP'],
             'INTJ': ['ISTJ', 'ESTJ', 'INFJ', 'ENFJ', 'ENTJ', 'ISFP'],
             'ENTJ': ['ISTJ', 'ESTJ', 'INFJ', 'ENFJ', 'INTJ', 'ESFP'],
             'ISFP': ['INFP', 'ENFP', 'ISTP', 'ESTP', 'INTJ', 'ESFP'],
             'ESFP': ['INFP', 'ENFP', 'ISTP', 'ESTP', 'ENTJ', 'ISFP']}

enneaGraph = {'1w9': ['9w1','1w2','2w1'],
              '1w2': ['9w1','1w9','2w1'],
              '2w1': ['1w2','2w3','3w2'],
              '2w3': ['1w2','2w1','3w2'],
              '3w2': ['2w3','3w4','4w3'],
              '3w4': ['2w3','3w2','4w3'],
              '4w3': ['3w4','4w5','5w4'],
              '4w5': ['3w4','4w3','5w4'],
              '5w4': ['4w5','5w6','6w5'],
              '5w6': ['4w5','5w4','6w5'],
              '6w5': ['5w6','6w7','7w6'],
              '6w7': ['5w6','6w5','7w6'],
              '7w6': ['6w7','7w8','8w7'],
              '7w8': ['6w7','7w6','8w7'],
              '8w7': ['7w8','8w9','9w8'],
              '8w9': ['7w8','8w7','9w8'],
              '9w8': ['8w9','9w1','1w9'],
              '9w1': ['8w9','9w8','1w9']}

"""
def BFS_SP(graph, start, goal):
    explored = []
     
    # Queue for traversing the 
    # graph in the BFS
    queue = [[start]]
     
    # If the desired node is 
    # reached
    if start == goal:
        print("Same Node")
        return
     
    # Loop to traverse the graph 
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]
         
        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]
             
            # Loop to iterate over the 
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                 
                # Condition to check if the 
                # neighbour node is the goal
                if neighbour == goal:
                    print("Shortest path = ", *new_path)
                    return
            explored.append(node)

BFS_SP(mbtiGraph, 'ISFJ', 'ISFP')"""