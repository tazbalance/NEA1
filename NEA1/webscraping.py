from bs4 import BeautifulSoup, SoupStrainer
import re

def find_types():
    with open("HTML_batman.html") as fp:
        soup = BeautifulSoup(fp)
        text = soup.find(string=re.compile("INTJ("))
        return text