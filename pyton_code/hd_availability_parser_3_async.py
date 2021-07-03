from concurrent.futures import ProcessPoolExecutor, as_completed
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
import urllib
import time
import json
import ssl
import re


"""
Home depot AVAILABILITY Parser:
This code uses the data stored data from Home depot DATA Parser
to ckeck if the products are available on give zip code
returns a dictionary with earliestAvailabilityDate and if products
are availabe or backordered, out of stock products are not diplayed

Code is run during flask apliaction
"""


URLs = []

def json_finder(folder_name, json_file, zip_code):
    path = f"data/{folder_name}/{json_file}.json"

    with open(path) as json_file:
        appliance_json = json.load(json_file)
        sku_list = list(appliance_json.values())[0]
    hd_url = "https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{}/zipCode/{}"

    for sku in sku_list:
        URLs.append(hd_url.format(sku, zip_code))


# json_finder("refrigerators", "french_door_refrigerator", 33315)

async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


def finder():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    urls = URLs
    htmls = loop.run_until_complete(fetch_all(urls, loop))

    available_app = dict()
    for i, url in enumerate(htmls):
        if "errorData" in htmls[i]["DeliveryAvailabilityResponse"]:
            print("Not a major appliance")

        elif htmls[i]["DeliveryAvailabilityResponse"]["deliveryAvailability"]["availability"][0]["status"] != "OOS_ETA_UNAVAILABLE":
            my_product_id = htmls[i]["DeliveryAvailabilityResponse"]["deliveryAvailability"]["availability"][0]["itemId"]

            available_app[my_product_id] = {}
            available_app[my_product_id]["product_id"] = my_product_id
            available_app[my_product_id]["status"] = htmls[i]["DeliveryAvailabilityResponse"]["deliveryAvailability"]["availability"][0]["status"]
            available_app[my_product_id]["earliestAvailabilityDate"] = htmls[i][
                "DeliveryAvailabilityResponse"]["deliveryAvailability"]["earliestAvailabilityDate"]
        else:
            pass
            

    return available_app


# print(finder())
