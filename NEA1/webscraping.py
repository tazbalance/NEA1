from bs4 import BeautifulSoup
import re
from pathlib import Path

p = Path(__file__).with_name('HTML_batman.html')

def find_types():
    with p.open('r') as f:
        soup = BeautifulSoup(f)
        text = soup.find(string=re.compile(r'INTJ\('))
        return text