import requests

from bs4 import BeautifulSoup

index = int(input())
r = requests.get(input())

if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html.parser')
    all_links = soup.find_all("a")
    link = all_links[index - 1]
    print(link.get('href'))

else:
    print("Site does not respond")
