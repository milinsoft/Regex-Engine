import requests

from bs4 import BeautifulSoup
article_address = requests.get(input())
soap = BeautifulSoup(article_address.content, "html.parser")
header = soap.find('h1')
print(header.text)
