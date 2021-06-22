import time
import requests
import urllib
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import asyncio
import re
import aiohttp
import ssl

URLs = []

def json_finder(folder_name, json_file, zip_code):
    path = f"data/{folder_name}/{json_file}.json"
    with open(path) as json_file:
        appliance_json = json.load(json_file)
        sku_list = list(appliance_json.values())[0]
        print(sku_list)
    hd_url = "https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"
    for sku in sku_list:
        URLs.append(hd_url.format(sku))

print(json_finder("cooktops", "radiant_36_white", 33315))

async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    urls = URLs
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    print(htmls)

