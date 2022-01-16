import requests

from bs4 import BeautifulSoup

index = int(input())  # Obtain the index of the subtitle is the first
r = requests.get(input())  # Obtain html address from input and sends a connection request


if r.status_code == 200:  # if status_code of connection is "200", connection successful, 'ERROR' otherwise
    soup = BeautifulSoup(r.content, 'html.parser')  # retrieving HTML content
    subtitles_list = soup.find_all('h2')  # tag must be parsed in quotes without angle brackets
    print(subtitles_list[index].text)  # print content of the given element using .text method
else:
    print("ERROR")
