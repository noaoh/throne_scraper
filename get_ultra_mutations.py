from bs4 import BeautifulSoup
from urllib.request import urlopen
from itertools import chain

url = "https://nuclear-throne.wikia.com/wiki/Mutations"

soup = BeautifulSoup(urlopen(url),"html.parser")

# The data format is yx where x = 1 or 2 (or 3 if horror), and y is 1,2,..,15
# y means which character, x means which mutation
# They correspond directly with the order in the wiki
id_numbers = ['ultra-{0}1 ultra-{0}2'.format(y).split(' ') for y in range(1,16) if y != 13]

# this flattens the list
keys = list(chain(*id_numbers))
# Horror has 3 ultra mutation choices, so 11 is his character # and 3 is the 3rd
keys.insert(-6,'ultra-113')

ultra_mutations_search = soup.find_all("span", {"class" : "mw-headline"})
# 31 is the start of ultra mutations, and the last 3 are co-op ultra mutations
values = [x.text for x in ultra_mutations_search[31:-3]]

ultra_mutations = dict(zip(keys,values))
