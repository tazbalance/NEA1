import requests
from bs4 import BeautifulSoup


def getHTMLdocument(url): 
    
    response = requests.get(url) 
    return response.text 


characterID = 129385
scrapingURL = f"https://www.personality-database.com/profile/{characterID}/"

html_doc = getHTMLdocument(scrapingURL) 

soup = BeautifulSoup(html_doc, 'html.parser') 

def printText():
    text = soup.find('h1').get_text()
    return text
    # --> 'Hello!'
