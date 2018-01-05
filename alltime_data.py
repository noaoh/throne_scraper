from bs4 import BeautifulSoup
from urllib.parse import urljoin
import aiohttp
import asyncio

def parse_entry_data(entry):
    rank = entry.find("td", {"class" : "scoreboard-rank"}).text
    name = entry.find("a").text.strip()
    score = entry.find("td",{"class" : "score"}).text
    processed_entry = [rank, name, score]
    return processed_entry

def process_page_data(page_data,entries):
    processed_page = []
    soup = BeautifulSoup(urlopen(url), "html.parser")
    entries_data = soup.find_all("tr", {"class" : "scoreboard-entry"})[:entries]
    for entry in entries_data:
        processed_page.append(parse_entry_data(entry))

    return processed_page


async def get_page_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

def chunk(array,n):
    return [array[x:x+n] for x in range(0,len(array),n)]

async def alltime_leaderboard(entries=0,pages=1):
    website = "https://www.thronebutt.com/all-time/"
    loop = asyncio.get_event_loop()
    
    entries_per_page = 30
    number_of_entries = entries or pages * entries_per_page
    entry_list = [*range(1,number_of_entries+1)]

    processed_pages_data = dict(enumerate(chunk(entry_list,30),1))
    for page, processed_entries in processed_pages_data.items():
        page_url = urljoin(website,str(page))
        processed_entries[:] = get_page_data(page_url,len(processed_entries))

    return processed_pages_data
