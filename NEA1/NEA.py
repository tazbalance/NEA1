import data
import database
from webscraping import get_type_values
import difflib


class Types():

    def __init__(self):

        self.myDb = database.Database()
        self.theData = data.Data()


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

        return self.calculate_types(self.MBTIfuncs, self.Enneas, self.BigFives)


    def get_types(self):

        qAmount = self.theData.get_amount_of_questions()
        qHighest = qAmount[0]

        for i in range(qHighest):
            answers = self.myDb.get_answers(i+1)

            if answers[0][0] != '/':
                self.MBTIfuncs[answers[0][0]] += answers[0][3]
            if answers[0][1] != '/':
                self.Enneas[answers[0][1]] += answers[0][3]
            if answers[0][2] != '/':
                self.BigFives[answers[0][2]] += answers[0][3]

        return self.calculate_types(self.MBTIfuncs, self.Enneas, self.BigFives)


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
        
        Type = {'SiNeTiFe': ['ISFJ Si', 'ENTP Ne', 'ESFJ Fe', 'INTP Ti'],
                'SeNiTiFe': ['ESTP Se', 'INFJ Ni', 'ISTP Ti', 'INTP Ti'],
                'SiNeTeFi': ['ISTJ Si', 'ENFP Ne', 'ESTJ Te', 'INFP Fi'],
                'SeNiTeFi': ['ESFP Se', 'INFJ Ni', 'ISFP Fi', 'ENTJ Te']}

        if perceivingDiff > judgingDiff:
            if MBTI[Type[Quadra][0][5:7]] > MBTI[Type[Quadra][1][5:7]]:
                Highest = 0
            else:
                Highest = 1
        else:
            if MBTI[Type[Quadra][2][5:7]] > MBTI[Type[Quadra][3][5:7]]:
                Highest = 2
            else:
                Highest = 3
            
        HighestMBTI = Type[Quadra][Highest][0:4]
        

        # Calculating Enneagram

        HighestEnnea = max(Enneagram, key=Enneagram.get)

        WingList = {'1':['2','9'], '2':['1','3'], '3':['2','4'],
                    '4':['3','5'], '5':['4','6'], '6':['5','7'],
                    '7':['6','8'], '8':['7','9'], '9':['8','1']}

        if Enneagram[WingList[HighestEnnea][0]] > Enneagram[WingList[HighestEnnea][1]]:
            HighestEnnea += 'w' + WingList[HighestEnnea][0]
        else:
            HighestEnnea += 'w' + WingList[HighestEnnea][1]


        # Calculating BigFive

        BigFive = ''
        BigFive += max({'R':Big5['R'], 'S':Big5['S']}, key=Big5.get)
        BigFive += max({'L':Big5['L'], 'C':Big5['C']}, key=Big5.get)
        BigFive += max({'U':Big5['U'], 'O':Big5['O']}, key=Big5.get)
        BigFive += max({'E':Big5['E'], 'A':Big5['A']}, key=Big5.get)
        BigFive += max({'N':Big5['N'], 'I':Big5['I']}, key=Big5.get)

        return HighestMBTI, HighestEnnea, BigFive


    def get_difference(self, gchar, gquiz):

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
        mbtiDiff = self.percentage(4, diff)


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
        big5Diff = self.percentage(5, diff)

        return mbtiDiff, enneaDiff, big5Diff


    def percentage(self, amt, diff):
        pos = amt

        for item in diff:
            if item[0] == '-':
                pos -= 1

        return f'{round(pos/amt*100)}%'
    

    def build_graph(self):

        info = self.myDb.graph_info()

        self.mbtiDB = {}  # eg. {'ISFJ': [1,2], 'ESFJ': [3,4],...}

        for i in range(len(info)): 
            IDlist = info[i][1]
            if IDlist: # if there is information for this type
                self.mbtiDB[f'{info[i][0]}'] = IDlist.split(', ')
            else:
                self.mbtiDB[f'{info[i][0]}'] = None

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
        
        removeNodes = []
        removeEdges = []

        # remove nodes that there is no information for
        for node, edges in mbtiGraph.items():
            if not self.mbtiDB[node]:
                removeNodes.append(node)
            else:
                for edge in edges:
                    if not self.mbtiDB[edge]:
                        removeEdges.append([node,edge])

        for node in removeNodes:
            mbtiGraph.pop(node)

        for node, edge in removeEdges:
            mbtiGraph[node].remove(edge)

        print(mbtiGraph)
        return mbtiGraph
    

    def find_path(self, startNode, endNode):
        mbtiGraph = self.build_graph()
        explored = []
        queue = [[startNode]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                neighbours = mbtiGraph[node]

                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if neighbour == endNode:
                        middle = round((len(new_path)-1)/2+0.1)
                        return new_path[middle]
                    
                explored.append(node)


    def find_characters(self, start, end):
        middletype = self.find_path(start, end)
        print(self.mbtiDB[middletype])  # this prints character ids that are the type

        # add these characters to list so that they can show up in results (interface)
        # make it so it chooses characters from same genre first, then other genres
        # try to use multi-database search

            
if __name__ == "__main__":
    typeos = Types()
    #print(typeos.build_graph())
    typeos.find_characters('INTP','ENTP')



"""
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
              '9w1': ['8w9','9w8','1w9']}"""