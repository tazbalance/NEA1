sample_doc = """
<html>
 <body>
  <li class="zone even open day">
   <label for="srr-1-1397046600">
    Room 225 8:30 AM
   </label>
   <input id="srr-1-1397046600" name="srr-1-1397046600" type="checkbox" value="Y"/>
   <span class="drag-handle">
   </span>
  </li>
  ,
  <li class="zone even open day">
   <label for="srr-1-1397068200">
    Room 225 2:30 PM
   </label>
   <input id="srr-1-1397068200" name="srr-1-1397068200" type="checkbox" value="Y"/>
   <span class="drag-handle">
   </span>
  </li>
 </body>
</html>
"""

pdb_doc3 = """
<html>
 <body>
  <div class="personality-vote-item">
   <label>ENFP(327)</label>
   <span style="width:100%"></span>
  </div>
 </body>
</html>
"""

# import requests
# from selenium import webdriver
import urllib.request
from requests_html import HTMLSession
from bs4 import BeautifulSoup, SoupStrainer

characterID = 129385
url = "https://www.personality-database.com/profile/129385/"
# url = f"https://www.personality-database.com/profile/{characterID}/"

# SELENIUM
# driver = webdriver.Firefox()
# driver.get(url)

# REQUESTS_HTML
session = HTMLSession()
pdb_ses = session.get(url)
about = pdb_ses.html.search('{}')[0][0]

r = session.get('https://python.org/')
about2 = r.html.search('Python is a {} language')[0]

# URLLIB.REQUEST
# html = urllib.request.urlopen(url).read()

# BEAUTIFULSOUP
pdb_parse = SoupStrainer('div',{'class': 'personality-vote-item'})
pdb = BeautifulSoup(pdb_doc3, 'html.parser', parse_only=pdb_parse) 

sample_parse = SoupStrainer('li',{'class': 'zone even open day'})
sample = BeautifulSoup(sample_doc, 'html.parser', parse_only=sample_parse) 


def printText():
    text = pdb.find('label')
    return about2
    # trying to return label text
