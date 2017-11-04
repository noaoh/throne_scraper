from bs4 import BeautifulSoup
from urllib.request import urlopen
from json import dump

enemy_ids = {}
url = "https://nuclear-throne.wikia.com/wiki/Stream_Keys"
soup = BeautifulSoup(urlopen(url),"html.parser")
enemy_id_table = soup.find_all("table",{"class" : "article-table"})[-1].find_all("tr")

for row in enemy_id_table[2:]:
    id_number, enemy = row.stripped_strings
    enemy_ids[int(id_number)] = enemy
