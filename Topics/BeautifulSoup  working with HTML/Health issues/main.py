import requests

from bs4 import BeautifulSoup

letter = 'S'

r = requests.get(input())

if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    all_a_tags = tuple(soup.find_all('a'))

    selected_a_tags = []
    for tag in all_a_tags:
        if len(tag.text) > 1:
            if tag.text.startswith(letter):
                if "entity" in tag.get('href') or "topics" in tag.get('href'):
                    selected_a_tags.append(tag.text)

    print(selected_a_tags)
