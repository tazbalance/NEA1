import urllib3
import json
import databaseChars


myDb = databaseChars.Database()
myDb.delete_table()

ids = [141259]


for id in ids:

    url = f"https://api.personality-database.com/api/v1/profile/{id}"
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    resp = json.loads(resp.data)

    name = resp["mbti_profile"]
    series = resp["subcategory"]
    image = resp["profile_image_url"]

    myDb.insert_character(id, name, series, image)


def get_type_values(id):

    MBTIvalues = {'ISFJ':0, 'ESFJ':0, 'INTP':0, 'ENTP':0,
                  'ISTJ':0, 'ESTJ':0, 'INFP':0, 'ENFP':0,
                  'INFJ':0, 'ENFJ':0, 'ISTP':0, 'ESTP':0,
                  'INTJ':0, 'ENTJ':0, 'ISFP':0, 'ESFP':0}

    EnneaValues = {'1':0, '2':0, '3':0,
                   '4':0, '5':0, '6':0,
                   '7':0, '8':0, '9':0}

    BigFiveValues = {'R':0, 'S':0,
                     'L':0, 'C':0,
                     'U':0, 'O':0,
                     'E':0, 'A':0,
                     'N':0, 'I':0}

    url = f"https://api.personality-database.com/api/v1/profile/{id}"
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    resp = json.loads(resp.data)

    MBTIlist = resp["breakdown_systems"]["1"]
    EnneaList = resp["breakdown_systems"]["2"]
    BigFiveList = resp["breakdown_systems"]["9"]

    for i in range(len(MBTIlist)):
        mbti = resp["breakdown_systems"]["1"][i]["personality_type"]
        count = resp["breakdown_systems"]["1"][i]["theCount"]
        count /= resp["systems"][0]["system_vote_count"]
        MBTIvalues[mbti] += count
    
    for i in range(len(EnneaList)):
        ennea = resp["breakdown_systems"]["2"][i]["personality_type"]
        count = resp["breakdown_systems"]["2"][i]["theCount"]
        count /= resp["systems"][1]["system_vote_count"]
        EnneaValues[ennea[0]] += count

    for i in range(len(BigFiveList)):
        bigfive = resp["breakdown_systems"]["9"][i]["personality_type"]
        count = resp["breakdown_systems"]["9"][i]["theCount"]
        count /= resp["systems"][6]["system_vote_count"]
        for i in range(4):
            BigFiveValues[bigfive[i]] += count
    
    return MBTIvalues, EnneaValues, BigFiveValues


def get_celebs(mbti, ennea):
    celebNumber = 0
    celebList = set({})

    url = 'https://api.personality-database.com/api/v1/profiles?offset=0&limit=100&cid=1&pid=1&sort=top&cat_id=1&property_id=1'
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    resp = json.loads(resp.data)
    
    for i in range(len(resp["profiles"])):
        celebType = resp["profiles"][i]["personality_type"]
        celebMBTI = celebType.split()[0]
        celebEnnea = celebType.split()[1]

        if celebMBTI == mbti or celebEnnea[0] == ennea[0]:
            celebNumber += 1
            name = resp["profiles"][i]["mbti_profile"]
            image = resp["profiles"][i]["profile_image_url"]
            info = name + '|||' + image
            celebList.add(info)

            if celebNumber > 2:
                return celebList

