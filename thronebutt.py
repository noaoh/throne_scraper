from urllib.parse import urljoin
from api_interpreter import decode_thronebutt_data
from client_async_sem import *
from bs4 import BeautifulSoup
import json
import aiohttp
import asyncio

with open("stream-api.json","r") as f:
    api = json.load(f)

def get_id(text):
    return text[1].split('-')[1]

def parse_alltime_data(entry):
    rank = entry.find("td", {"class" : "scoreboard-rank"}).text
    name = entry.find("a").text.strip()
    score = entry.find("td",{"class" : "score"}).text
    processed_entry 

def parse_board_data(entry):
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

    ultra_mutation_search = detail_data.find_all("span", {"class" : "ultra"})
    if len(ultra_mutation_search) > 0:
        ultra_mutation_id = get_id(ultra_mutation_search[0]['class'])

    else:
        ultra_mutation_id = "0"

    mutation_ids = []
    mutations_search = detail_data.find_all("span", {"class" : "mutation"})
    if len(mutations_search) > 0:
        for mutation in mutations_search:
            mutation_ids.append(get_id(mutation['class']))
    else:
        mutation_ids = []

    weapon_ids = []
    weapons_search = detail_data.find_all("span", {"class" : "weapon"})
    if len(weapons_search) > 0:
        for weapon in weapons_search:
            weapon_ids.append(get_id(weapon['class']))
    else:
        weapon_ids = []

    crown_search = detail_data.find_all("span", {"class" : "crown"})
    if len(crown_search) > 0:
        crown_id = get_id(crown_search[0]['class'])
    else:
        crown_id = "1"

    killed_by_search = detail_data.find_all("img", {"class" : "deathflag"})
    killed_by_id = killed_by_search[0]['src'].split('/')[-1].split(".")[0]

    encoded_entry = {"rank" : rank, "name" : name, "character" : char_used, "loops" : loops,\
            "level" : level, "score" : score, "ultra" : ultra_mutation_id,\
            "mutations" : mutation_ids, "weapons" : weapon_ids,\
            "crown" : crown_id, "lasthit" : killed_by_id}

    return encoded_entry

def process_date_data(page_data,entries):
    processed_page = [] 

    soup = BeautifulSoup(page_data, "html.parser")
    # has data like loop, Stage, Level, Username, character
    basics_data = soup.find_all("tr", {"class" : "scoreboard-entry"})[:entries]
    # has data like mutations, crowns, weapons, and killed by
    details_data = soup.find_all("tr", {"class" : "scoreboard-details-row"})\
            [:entries]
    # list of lists with first element being entries_data and second element
    # being details_data
    for entry in zip(basics_data,details_data):
        processed_page.append(parse_board_data(entry))

    return processed_page

def process_all_data(page_data,entries):
    processed_page = []
    soup = BeautifulSoup(page_data, "html.parser")
    entries_data=soup.find_all("tr", {"class" : "scoreboard-entry"})[:entries]
    for entry in entries_data:
        processed_page.append(parse_alltime_data(entry))

    return processed_page

def leaderboard_crawler(date, entries=0, pages=1):
    website = "https://www.thronebutt.com/archive/"
    date_url = urljoin(website,date+"/")
    entries_per_page = 30
    number_of_entries = entries or pages * entries_per_page
    full_pages, last_page = divmod(number_of_entries,entries_per_page)
    entry_list = [entries_per_page] * full_pages 
    if last_page != 0:
        entry_list.append(last_page)    


    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession() as session:
        future = asyncio.ensure_future(fetch_pages(date_url,pages,session))
        date_html = loop.run_until_complete(future)

    processed_pages = {}

    for page, num_entries in enumerate(entry_list,1):
        page_data =  date_html[page]
        processed_pages[str(page)] = process_date_data(page_data,num_entries)


    leaderboard_data = {date : processed_pages} 
    return leaderboard_data

def alltime_leaderboard(entries=0,pages=1):
    website = "https://www.thronebutt.com/all-time/"

    entries_per_page = 30
    number_of_entries = entries or pages * entries_per_page
    full_pages, last_page = divmod(number_of_entries,entries_per_page)
    entry_list = [entries_per_page] * full_pages
    if last_page != 0:
        entry_list.append(last_page)

    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession() as session:
        future = asyncio.ensure_future(fetch_pages(website,pages,session))
        alltime_html = loop.run_until_complete(future)

    processed_pages = {}
    
    for page, num_entries in enumerate(entry_list,1):
        page_data = alltime_html[page]
        processed_pages[str(page)] =
        process_alltime_data(page_data,num_entries)

def weekly_leaderboard(week, year, entries=0, pages=1):
    weekly_date = "{0:02d}{1}".format(week, year)
    return leaderboard_crawler(weekly_date,entries,pages)

def daily_leaderboard(day, month, year, entries=0, pages=1):
    daily_date = "{0:02d}{1:02d}{2}".format(day, month, year) 
    return leaderboard_crawler(daily_date, entries, pages)

