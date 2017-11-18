from bs4 import BeautifulSoup
from urllib.request import urlopen
from json import dump
from pprint import pprint
from itertools import chain

# enemy_ids works
enemy_ids = {}
url = "https://nuclear-throne.wikia.com/wiki/Stream_Keys"
soup = BeautifulSoup(urlopen(url),"html.parser")
enemy_id_table = soup.find_all("table",{"class" : "article-table"})[-1].find_all("tr")

for row in enemy_id_table[2:]:
    id_number, enemy = row.stripped_strings
    enemy_ids[int(id_number)] = enemy

# ultra mutations
ultra_mutations_url = "https://nuclear-throne.wikia.com/wiki/Mutations"

ultra_mutations_soup = BeautifulSoup(urlopen(ultra_mutations_url),"html.parser")

# The data format is yx where x = 1 or 2 (or 3 if horror), and y is 1,2,..,15
# y means which character, x means which mutation
# They correspond directly with the order in the wiki
id_numbers = ['{0}1 {0}2'.format(y).split(' ') for y in range(1,16) if y != 13]

# this flattens the list
keys = list(chain(*id_numbers))
# Horror has 3 ultra mutation choices, so 11 is his character # and 3 is the 3rd
keys.insert(-6,'113')

ultra_mutations_table = ultra_mutations_soup.find_all("span", {"class" : "mw-headline"})
# 31 is the start of ultra mutations, and the last 3 are co-op ultra mutations
values = [x.text for x in ultra_mutations_table[31:-3]]

ultra_mutation_ids = {}
for id_number, ultra_mutation in zip(keys,values):
    ultra_mutation_ids[int(id_number)] = ultra_mutation
    ultra_mutation_ids[ultra_mutation] = int(id_number)

# weapon_ids
weapon_ids = {}
weapon_id_table = soup.find_all("table",{"class" : "article-table"})[-2].find_all("tr")

for row in weapon_id_table[2:]:
    id_number, weapon = row.stripped_strings
    weapon_ids[int(id_number)] = weapon
    weapon_ids[weapon] = int(id_number)

# world_ids
world_ids = {}
world_id_table = soup.find_all("table",{"class" : "article-table"})[-3].find_all("tr")

for row in world_id_table[2:]:
    id_number, world = row.stripped_strings
    world_ids[int(id_number)] = world
    world_ids[world] = int(id_number)

# crown_ids
crown_ids = {}
crown_id_table = soup.find_all("table",{"class" : "article-table"})[-4].find_all("tr")

for row in crown_id_table[1:]:
    id_number, crown = row.stripped_strings
    crown_ids[int(id_number)] = crown
    crown_ids[crown] = int(id_number)

# mutation_ids
mutation_ids = {}
mutation_id_table = soup.find_all("table",{"class" : "article-table"})[-5].find_all("tr")

for row in mutation_id_table[2:]:
        id_number, mutation = row.stripped_strings
        mutation_ids[int(id_number)] = mutation
        mutation_ids[mutation] = int(id_number)

# character_ids
character_ids = {}
character_id_table = soup.find_all("table",{"class" : "article-table"})[-6].find_all("tr")

for row in character_id_table[1:]:
        id_number, character = row.stripped_strings
        character_ids[int(id_number)] = character
        character_ids[character] = int(id_number)

stream_api = {"characters" : character_ids, "mutations" : mutation_ids,\
 "ultra-mutations" : ultra_mutation_ids, "crowns" : crown_ids, "worlds" : world_ids,\
 "enemies" : enemy_ids, "weapons" : weapon_ids}

with open("stream-api.json","w") as f:
     dump(stream_api,f)
