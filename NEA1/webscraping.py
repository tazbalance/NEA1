import urllib3
import json
import databaseChars


myDb = databaseChars.Database()
ids = [1, 2, 3, 4]

myDb.delete_table()


for id in ids:

    url = f"https://api.personality-database.com/api/v1/profile/{id}"
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    resp = json.loads(resp.data)

    name = resp["mbti_profile"]
    series = resp["subcategory"]
    image = resp["profile_image_url"]

    myDb.insert_character(id, name, series, image)


def get_mbti_values(id):

    MBTIvalues = {'ISFJ':0, 'ESFJ':0, 'INTP':0, 'ENTP':0,
                  'ISTJ':0, 'ESTJ':0, 'INFP':0, 'ENFP':0,
                  'INFJ':0, 'ENFJ':0, 'ISTP':0, 'ESTP':0,
                  'INTJ':0, 'ENTJ':0, 'ISFP':0, 'ESFP':0}

    # getting url data
    url = f"https://api.personality-database.com/api/v1/profile/{id}"
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    resp = json.loads(resp.data)

    # getting parts from data
    MBTIlist = resp["breakdown_systems"]["1"]
    votenum = resp["systems"][0]["system_vote_count"]

    # assigning mbtis
    for i in range(len(MBTIlist)):
        mbti = resp["breakdown_systems"]["1"][i]["personality_type"]
        count = resp["breakdown_systems"]["1"][i]["theCount"]
        count /= votenum
        MBTIvalues[mbti] = count
    
    return MBTIvalues