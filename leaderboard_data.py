from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from json import load
import asyncio
import aiohttp

with open("killed_by.json","r") as f:
    deathflags = load(f)

with open("ultra_mutations.json","r") as f:
    ultra_mutations = load(f)

def parse_entry_data(entry):
    basic_data = entry[0]
    detail_data = entry[1]

    rank = basic_data.find("td", {"class" : "scoreboard-rank"}).text

    name = basic_data.find("span", {"class" : "scoreboard-user"}).text
    name = name.strip().replace('b','')

    char_used_class = basic_data.find("span", {"class" : "character"})['class']
    char_used = char_used_class[1].split('-')[1].title()

    raw_level = basic_data.find("div", {"class" : "daily-level"}).text
    loops, level = raw_level[0:2],raw_level[2:]

    score = basic_data.find("td", {"class" : "scoreboard-score"}).text

    # can't really easily include ultra mutation, has numbers and picture
    ultra_mutation_search = detail_data.find_all("span", {"class" : "ultra"})
    if len(ultra_mutation_search) > 0:
        key_id = ultra_mutation_search[0]['class'][1]
        ultra_mutation = ultra_mutations[key_id]

    else:
        ultra_mutation = "N/A"

    mutations = [ultra_mutation]
    mutations_search = detail_data.find_all("span", {"class" : "mutation"})
    if len(mutations_search) > 0:
        for mutation in mutations_search:
            mutations.append(mutation['title'].title())
    else:
        mutations = "N/A"

    weapons = []
    weapons_search = detail_data.find_all("span", {"class" : "weapon"})
    if len(weapons_search) > 0:
        for weapon in weapons_search:
            weapons.append(weapon['title'])
    else:
        weapons = "N/A"

    crown_search = detail_data.find_all("span", {"class" : "crown"})
    if len(crown_search) > 0:
        crown = crown_search[0]['title']
    else:
        crown = "N/A"
    # can't really get who killed them that easily, it's a picture w
    # no name, located at https://www.thronebutt.com/img/deathflags/0.gif thru 105.gif
    killed_by_search = detail_data.find_all("img", {"class" : "deathflag"})
    if len(killed_by_search) > 0:
        killed_by_id = killed_by_search[0]['src'].split('/')[-1].split(".")[0]
        killed_by = deathflags[killed_by_id]

    processed_entry = [rank, name, char_used, loops, level,\
     score, mutations, weapons, crown, killed_by]
    return processed_entry

def get_page_data(url,entries):
    processed_page = []
    soup = BeautifulSoup(urlopen(url), "html.parser")
    # has data like loop, Stage, Level, Username, character
    basics_data = soup.find_all("tr", {"class" : "scoreboard-entry"})[:entries]
    # has data like mutations, crowns, weapons, and killed by
    details_data = soup.find_all("tr", {"class" : "scoreboard-details-row"})\
    [:entries]
    # list of lists with first element being entries_data and second element
    # being details_data
    for entry in zip(basics_data,details_data):
        processed_page.append(parse_entry_data(entry))

    return processed_page

def chunk(array,n):
    return [array[x:x+n] for x in range(0,len(array),n)]

def leaderboard_crawler(date, entries=0, pages=1):
    website = "https://www.thronebutt.com/archive/"
    date_url = urljoin(website,date+"/")

    entries_per_page = 30
    number_of_entries = entries or pages * entries_per_page
    entry_list = [*range(1,number_of_entries+1)]

    processed_pages_data = dict(enumerate(chunk(entry_list,30),1))
    leaderboard_data = {"{0}".format(date) : processed_pages_data}

    for page, processed_entries in processed_pages_data.items():
        page_url = urljoin(date_url,str(page))
        processed_entries[:] = get_page_data(page_url,len(processed_entries))

    return leaderboard_data

def weekly_leaderboard(week, year, entries=0, pages=1):
    weekly_date = "{0:02d}{1}".format(week, year)
    return leaderboard_crawler(weekly_date, entries, pages)

def daily_leaderboard(day, month, year, entries=0, pages=1):
    daily_date = "{0:02d}{1:02d}{2}".format(day, month, year)
    return leaderboard_crawler(daily_date, entries, pages)

def list_string(item):
    if type(item) is list:
        return ', '.join(item)
    else:
        return item

def pretty_print(entry):
    description = ["Rank","Player","Character","Loop","Stage","Score",
    "Mutations","Weapons","Crown","Killed By"]
    for item, desc in zip(entry,description):
        print("{0} : {1}".format(desc.ljust(9), list_string(item)))
