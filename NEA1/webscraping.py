import urllib3
import json
import databaseChars
import data


# store information about related characters
# calculate information from existing data


def find_info():
    myDb = databaseChars.Database()
    myDb.delete_table()

    theData = data.Data()
    ids = theData.get_ids()

    for id in ids:

        if not myDb.in_database(id):

            url = f"https://api.personality-database.com/api/v1/profile/{id}"
            http = urllib3.PoolManager()
            resp = http.request('GET', url)
            resp = json.loads(resp.data)

            name = resp["mbti_profile"]
            series = resp["subcategory"]
            image = resp["profile_image_url"]

            typedata = json.dumps(resp["breakdown_systems"])
            votedata = json.dumps(resp["systems"])

            myDb.insert_character(id, name, series, image, typedata, votedata)


def get_type_values(id):

    myDb = databaseChars.Database()

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

    typedata = myDb.get_character_data(id)
    typedata = json.loads(typedata)

    MBTIlist = typedata["1"]
    EnneaList = typedata["2"]
    BigFiveList = typedata["9"]

    votedata = myDb.get_vote_data(id)
    votedata = json.loads(votedata)

    for i in range(len(MBTIlist)):
        mbti = MBTIlist[i]["personality_type"]
        count = MBTIlist[i]["theCount"]
        count /= votedata[0]["system_vote_count"]
        MBTIvalues[mbti] += count
    
    for i in range(len(EnneaList)):
        ennea = EnneaList[i]["personality_type"]
        count = EnneaList[i]["theCount"]
        count /= votedata[1]["system_vote_count"]
        EnneaValues[ennea[0]] += count

    for i in range(len(BigFiveList)):
        bigfive = BigFiveList[i]["personality_type"]
        count = BigFiveList[i]["theCount"]
        count /= votedata[6]["system_vote_count"]
        for i in range(5):
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
            if celebNumber > 2:
                return celebList

            name = resp["profiles"][i]["mbti_profile"]
            image = resp["profiles"][i]["profile_image_url"]
            info = name + '|||' + image
            celebList.add(info)

