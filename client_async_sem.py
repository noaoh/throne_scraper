from urllib.parse import urljoin
import aiohttp
import asyncio

LIMIT = 5

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def bound_fetch(url, session, sem):
    # Getter function with semaphore
    async with sem:
        return await fetch(url,session)

async def fetch_pages(url,pages,session):
    tasks = []
    sem = asyncio.Semaphore(LIMIT)

    for page in range(pages+1):
        task_url = urljoin(url,str(page))
        task = asyncio.ensure_future(bound_fetch(task_url, session, sem))
        tasks.append(task)

    return await asyncio.gather(*tasks)
