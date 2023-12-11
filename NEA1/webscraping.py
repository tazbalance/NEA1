from types import NoneType
from bs4 import BeautifulSoup
import re
from pathlib import Path
# lxml

def find_types():
    with p.open('r') as f:
        soup = BeautifulSoup(f, features="html.parser")
        text = soup.find(string=re.compile(r'INTJ\('))
        return text

# https://www.personality-database.com/profile/{ID}

characterIDs = [1984, 1985, 1986]

MBTIvalues = {'ISFJ':0,
              'INFJ':0,
              'ESFJ':0,
              'ENFJ':0,

              'ISTJ':0,
              'INTJ':0,
              'ESTJ':0,
              'ENTJ':0,

              'ISTP':0,
              'INTP':0,
              'ESTP':0,
              'ENTP':0,
              
              'ISFP':0,
              'INFP':0,
              'ESFP':0,
              'ENFP':0}

for ID in characterIDs:
    print(f"-------- {ID} -----------")
    p = Path(__file__).with_name(f'HTML_{ID}.html')
    page = p.open('r')
    soup = BeautifulSoup(page, features="html.parser")

    for MBTI, MBTIvalue in MBTIvalues.items():
        MBTI_HTML = soup.find(string=re.compile(rf'{MBTI}\('))
        print(f'{MBTI}: {MBTI_HTML}')
        """ RegexSearch = re.search(r'\((.*)\)', MBTI_HTML)
        if RegexSearch == NoneType:
            MBTIvalue = 0
        else:
            MBTIvalue = RegexSearch.group(1)"""

    print('-------')

        

