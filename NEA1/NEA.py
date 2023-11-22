import random
import database
import interface

myDb = database.Database("NEAdatabase.db")

# Defining MBTI, Enneagram and Big Five

Si = 0
Se = 0
Ni = 0
Ne = 0
Fe = 0
Fi = 0
Ti = 0
Te = 0

One = 0
Two = 0
Three = 0
Four = 0
Five = 0
Six = 0
Seven = 0
Eight = 0
Nine = 0

Reserved = 0
Social = 0
Limbic = 0
Calm = 0
Unstructured = 0
Organised = 0
Egocentric = 0
Accomodating = 0
Noncurious = 0
Inquisitive = 0

"""
# Assigning answers to each question

for i in range(13):
    answer = random.randint(-4,4)
    myDb.insert_answer(answer,i+1)
"""

# Adding MBTI results together

def get_answers():

    for i in range(13):
        answers = myDb.get_answers(i+1)
        MBTI = answers[0][0]
        Enneagram = answers[0][1]
        BigFive = answers[0][2]

        if MBTI == 'Si':
            Si += answers[0][3]
        elif MBTI == 'Se':
            Se += answers[0][3]
        elif MBTI == 'Ni':
            Ni += answers[0][3]
        elif MBTI == 'Ne':
            Ne += answers[0][3]
        elif MBTI == 'Fi':
            Fi += answers[0][3]
        elif MBTI == 'Fe':
            Fe += answers[0][3]
        elif MBTI == 'Ti':
            Ti += answers[0][3]
        elif MBTI == 'Te':
            Te += answers[0][3]

        # Adding Enneagram results together

        if Enneagram == '1':
            One += answers[0][3]
        elif Enneagram == '2':
            Two += answers[0][3]
        elif Enneagram == '3':
            Three += answers[0][3]
        elif Enneagram == '4':
            Four += answers[0][3]
        elif Enneagram == '5':
            Five += answers[0][3]
        elif Enneagram == '6':
            Six += answers[0][3]
        elif Enneagram == '7':
            Seven += answers[0][3]
        elif Enneagram == '8':
            Eight += answers[0][3]
        elif Enneagram == '9':
            Nine += answers[0][3]

        # Adding Big Five results together

        if BigFive == 'R':
            Reserved += answers[0][3]
        elif BigFive == 'S':
            Social += answers[0][3]
        elif BigFive == 'L':
            Limbic += answers[0][3]
        elif BigFive == 'C':
            Calm += answers[0][3]
        elif BigFive == 'U':
            Unstructured += answers[0][3]
        elif BigFive == 'O':
            Organised += answers[0][3]
        elif BigFive == 'E':
            Egocentric += answers[0][3]
        elif BigFive == 'A':
            Accomodating += answers[0][3]
        elif BigFive == 'N':
            Noncurious += answers[0][3]
        elif BigFive == 'I':
            Inquisitive += answers[0][3]


def calculate_types():

    # Calculating MBTI
    # Quadra

    SiNeTiFe = Si + Ne + Ti + Fe
    SeNiTiFe = Se + Ni + Ti + Fe
    SiNeTeFi = Si + Ne + Te + Fi
    SeNiTeFi = Se + Ni + Te + Fi

    Quadra = {'SiNeTiFe': SiNeTiFe, 'SeNiTiFe': SeNiTiFe, 'SiNeTeFi': SiNeTeFi, 'SeNiTeFi': SeNiTeFi}
    HighestQuadra = max(Quadra, key=Quadra.get)
    print(HighestQuadra)


    if HighestQuadra == 'SiNeTiFe':
        # SI NE TI FE

        perceivingDiff = abs(Si - Ne)
        judgingDiff = abs(Ti - Fe)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ISFJ': Si, 'ENTP': Ne}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)
        elif HighestPJ == 'Judging':
            DomInf = {'ESFJ': Fe, 'INTP': Ti}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)


    elif HighestQuadra == 'SeNiTiFe':
        # SE NI TI FE
        
        perceivingDiff = abs(Se - Ni)
        judgingDiff = abs(Ti - Fe)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ESTP': Se, 'INFJ': Ni}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)
        elif HighestPJ == 'Judging':
            DomInf = {'ISTP': Ti, 'ENFJ': Fe}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)


    elif HighestQuadra == 'SiNeTeFi':
        # SI NE TE FI

        perceivingDiff = abs(Si - Ne)
        judgingDiff = abs(Te - Fi)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ISTJ': Si, 'ENFP': Ne}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)
        elif HighestPJ == 'Judging':
            DomInf = {'ESTJ': Te, 'INFP': Fi}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)


    elif HighestQuadra == 'SeNiTeFi':
        # SE NI TE FI

        perceivingDiff = abs(Se - Ni)
        judgingDiff = abs(Te - Fi)

        PerceivingJudging = {'Perceiving': perceivingDiff, 'Judging': judgingDiff}
        HighestPJ = max(PerceivingJudging, key=PerceivingJudging.get)

        if HighestPJ == 'Perceiving':
            DomInf = {'ESFP': Se, 'INTJ': Ni}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)
        elif HighestPJ == 'Judging':
            DomInf = {'ISFP': Fi, 'ENTJ': Te}
            FinalType = max(DomInf, key=DomInf.get)
            print(FinalType)

    print(f"Si: {Si}, Se: {Se}, Ne: {Ne}, Ni: {Ni}, Fi: {Fi}, Fe: {Fe}, Ti: {Ti}, Te: {Te}")



    # Calculating Enneagram

    Ennea = {'1': One, '2': Two, '3': Three, '4': Four, '5': Five, '6': Six, '7': Seven, '8': Eight, '9': Nine}
    HighestEnnea = max(Ennea, key=Ennea.get)

    EnneaIndex = list(Ennea.keys()).index(HighestEnnea)

    if HighestEnnea == '1':
        Wings = {'w2': Two, 'w9': Nine}
    elif HighestEnnea == '2':
        Wings = {'w1': One, 'w3': Three}
    elif HighestEnnea == '3':
        Wings = {'w2': Two, 'w4': Four}
    elif HighestEnnea == '4':
        Wings = {'w3': Three, 'w5': Five}
    elif HighestEnnea == '5':
        Wings = {'w4': Four, 'w6': Six}
    elif HighestEnnea == '6':
        Wings = {'w5': Five, 'w7': Seven}
    elif HighestEnnea == '7':
        Wings = {'w6': Six, 'w8': Eight}
    elif HighestEnnea == '8':
        Wings = {'w7': Seven, 'w9': Nine}
    elif HighestEnnea == '9':
        Wings = {'w8': Eight, 'w1': One}

    HighestWing = max(Wings, key=Wings.get)
    HighestEnnea += HighestWing


    print(HighestEnnea)


    # Calculating BigFive

    RS = {'Reserved': Reserved, 'Social': Social}
    LC = {'Limbic': Limbic, 'Calm': Calm}
    UO = {'Unstructured': Unstructured, 'Organised': Organised}
    EA = {'Egocentric': Egocentric, 'Accomodating': Accomodating}
    IN = {'Inquisitive': Inquisitive, 'Noncurious': Noncurious}

    HighestRS = max(RS, key=RS.get)
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

    print(BigFive)

