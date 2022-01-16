# solution with regexp
import re

import requests

from bs4 import BeautifulSoup
pattern_word = input()
r = requests.get(input())

soup = BeautifulSoup(r.content, "html.parser")
paragraphs = soup.find_all("p")

for par in paragraphs:
    result = re.search(pattern_word, par.text)
    if result:
        print(par.text)
        break
