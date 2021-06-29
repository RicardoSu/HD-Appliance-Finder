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
    hd_url = "https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{}/zipCode/{}"
    for sku in sku_list:
        URLs.append(hd_url.format(sku, zip_code))


json_finder("refrigerators", "french_door_refrigerator", 33315)


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
            print("OOS")

    print(available_app)
