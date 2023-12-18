from os import MFD_HUGE_64KB
from webbrowser import get
import database
from webscraping import get_mbti_values
import re


myDb = database.Database()
MBTI = {'Si':0, 'Se':0, 'Ni':0, 'Ne':0,
        'Fi':0, 'Fe':0, 'Ti':0, 'Te':0}


def get_char_types(id):

    MBTIvalues = get_mbti_values(id)

    MBTIlist = [['Si', 'Fe', 'Ti', 'Ne'], ['Fe', 'Si', 'Ne', 'Ti'], ['Ti', 'Ne', 'Si', 'Fe'], ['Ne', 'Ti', 'Fe', 'Si'],
                ['Si', 'Te', 'Fi', 'Ne'], ['Te', 'Si', 'Ne', 'Fi'], ['Fi', 'Ne', 'Si', 'Te'], ['Ne', 'Fi', 'Te', 'Si'],
                ['Ni', 'Fe', 'Ti', 'Se'], ['Fe', 'Ni', 'Se', 'Ti'], ['Ti', 'Se', 'Ni', 'Fe'], ['Se', 'Ti', 'Fe', 'Ni'],
                ['Ni', 'Te', 'Fi', 'Se'], ['Te', 'Ni', 'Se', 'Fi'], ['Fi', 'Se', 'Ni', 'Te'], ['Se', 'Fi', 'Te', 'Ni']]

    for CharMBTI, Function in zip(MBTIvalues.values(), MBTIlist):
        MBTI[Function[0]] += 8 * CharMBTI
        MBTI[Function[1]] += 4 * CharMBTI
        MBTI[Function[2]] += 2 * CharMBTI
        MBTI[Function[3]] += 1 * CharMBTI


def get_types():

    MBTI_list = {'Si':0, 'Se':0, 'Ni':0, 'Ne':0,
                 'Fi':0, 'Fe':0, 'Ti':0, 'Te':0}

    Enneagram_list = {'1':0, '2':0, '3':0,
                      '4':0, '5':0, '6':0,
                      '7':0, '8':0, '9':0}

    BigFive_list = {'R':0, 'S':0,
                    'L':0, 'C':0,
                    'U':0, 'O':0,
                    'E':0, 'A':0,
                    'N':0, 'I':0}

    for i in range(13):
        answers = myDb.get_answers(i+1)
        MBTI = answers[0][0]
        Enneagram = answers[0][1]
        BigFive = answers[0][2]

        MBTI_list[MBTI] += answers[0][3]
        Enneagram_list[Enneagram] += answers[0][3]
        BigFive_list[BigFive] += answers[0][3]

        HighestMBTI, HighestEnnea, HighestBigFive = calculate_types(MBTI_list, Enneagram_list, BigFive_list)
        return HighestMBTI, HighestEnnea, HighestBigFive


def calculate_types(MBTI, Enneagram, BigFive):

    Quadra = {'SiNeTiFe': MBTI['Si'] + MBTI['Ne'] + MBTI['Ti'] + MBTI['Fe'],
              'SeNiTiFe': MBTI['Se'] + MBTI['Ni'] + MBTI['Ti'] + MBTI['Fe'],
              'SiNeTeFi': MBTI['Si'] + MBTI['Ne'] + MBTI['Te'] + MBTI['Fi'],
              'SeNiTeFi': MBTI['Se'] + MBTI['Ni'] + MBTI['Te'] + MBTI['Fi']}
    HighestQuadra = max(Quadra, key=Quadra.get)

    if HighestQuadra == 'SiNeTiFe':
        # SI NE TI FE

        perceivingDiff = abs(Si - Ne)
        judgingDiff = abs(Ti - Fe)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ISFJ': Si, 'ENTP': Ne}
            HighestMBTI = max(DomInf, key=DomInf.get)
        elif HighestPJ == 'Judging':
            DomInf = {'ESFJ': Fe, 'INTP': Ti}
            HighestMBTI = max(DomInf, key=DomInf.get)


    elif HighestQuadra == 'SeNiTiFe':
        # SE NI TI FE
        
        perceivingDiff = abs(Se - Ni)
        judgingDiff = abs(Ti - Fe)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ESTP': Se, 'INFJ': Ni}
            HighestMBTI = max(DomInf, key=DomInf.get)
        elif HighestPJ == 'Judging':
            DomInf = {'ISTP': Ti, 'ENFJ': Fe}
            HighestMBTI = max(DomInf, key=DomInf.get)


    elif HighestQuadra == 'SiNeTeFi':
        # SI NE TE FI

        perceivingDiff = abs(Si - Ne)
        judgingDiff = abs(Te - Fi)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ISTJ': Si, 'ENFP': Ne}
            HighestMBTI = max(DomInf, key=DomInf.get)
        elif HighestPJ == 'Judging':
            DomInf = {'ESTJ': Te, 'INFP': Fi}
            HighestMBTI = max(DomInf, key=DomInf.get)


    elif HighestQuadra == 'SeNiTeFi':
        # SE NI TE FI

        perceivingDiff = abs(Se - Ni)
        judgingDiff = abs(Te - Fi)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ESFP': Se, 'INTJ': Ni}
            HighestMBTI = max(DomInf, key=DomInf.get)
        elif HighestPJ == 'Judging':
            DomInf = {'ISFP': Fi, 'ENTJ': Te}
            HighestMBTI = max(DomInf, key=DomInf.get)


    # Calculating Enneagram

    HighestEnnea = max(Enneagram, key=Enneagram.get)

    if HighestEnnea == '1':
        Wings = {'w2': Enneagram['2'], 'w9': Enneagram['9']}
    elif HighestEnnea == '2':
        Wings = {'w1': Enneagram['1'], 'w3': Enneagram['3']}
    elif HighestEnnea == '3':
        Wings = {'w2': Enneagram['2'], 'w4': Enneagram['4']}
    elif HighestEnnea == '4':
        Wings = {'w3': Enneagram['3'], 'w5': Enneagram['5']}
    elif HighestEnnea == '5':
        Wings = {'w4': Enneagram['4'], 'w6': Enneagram['6']}
    elif HighestEnnea == '6':
        Wings = {'w5': Enneagram['5'], 'w7': Enneagram['7']}
    elif HighestEnnea == '7':
        Wings = {'w6': Enneagram['6'], 'w8': Enneagram['8']}
    elif HighestEnnea == '8':
        Wings = {'w7': Enneagram['7'], 'w9': Enneagram['9']}
    elif HighestEnnea == '9':
        Wings = {'w8': Enneagram['8'], 'w1': Enneagram['1']}

    HighestWing = max(Wings, key=Wings.get)
    HighestEnnea += HighestWing


    # Calculating BigFive

    HighestRS = max(BigFive['R'], BigFive['S'])
    HighestLC = max(LC, key=LC.get)
    HighestUO = max(UO, key=UO.get)
    HighestEA = max(EA, key=EA.get)
    HighestIN = max(IN, key=IN.get)

    BigFive = ""

    if HighestRS == 'Reserved':
        BigFive += 'R'
    else:
        BigFive += 'S'

    if HighestLC == 'Limbic':
        BigFive += 'L'
    else:
        BigFive += 'C'

    if HighestUO == 'Unstructured':
        BigFive += 'U'
    else:
        BigFive += 'O'

    if HighestEA == 'Egocentric':
        BigFive += 'E'
    else:
        BigFive += 'A'

    if HighestIN == 'Inquisitive':
        BigFive += 'I'
    else:
        BigFive += 'N'

    return HighestMBTI, HighestEnnea, BigFive

