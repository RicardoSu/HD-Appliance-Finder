from concurrent.futures import ProcessPoolExecutor, as_completed
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
import urllib
import json
import time
import ssl
import sys
import re
import os

"""
Home depot DATA Parser Asynchronous:
This code uses the data stored data from Home depot SKU Parser
and creates JSON a file from specified imput runs faster than
Home depot DATA Parser, needs to be implemented multi file
reader
"""


URLs = []

def json_finder(folder_name, json_file):
    path = f"data/{folder_name}/{json_file}.json"
    with open(path) as json_file:
        appliance_json = json.load(json_file)
        sku_list = list(appliance_json.values())[0]
    hd_url = "https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"
    for sku in sku_list:
        URLs.append(hd_url.format(sku))
    
# json_finder("cooktops","induction_30_black")
# print(URLs)

def files_subdirectory_finder():
    directory = "./data"

    for root, subdirectories, files in os.walk(directory):
        for file in files:
            folder_name = (os.path.join(root.replace(f"./data\\", "")))
            file_name = (os.path.join(file.replace(".json", "")))
            json_finder(folder_name, file_name)
                 
files_subdirectory_finder()

async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

def json_saver(folder_name, json_file):
    try:
        json_key = f"data_async/{folder_name}/{json_file}.json"

        with open(json_key, 'w') as fp:
            json.dump(functional_dict, fp, indent=4, ensure_ascii=False)
    except IOError:
        print("I/O error")

if __name__ == '__main__':
    print(URLs)
    loop = asyncio.get_event_loop()
    urls = URLs
    htmls = loop.run_until_complete(fetch_all(urls, loop))

    functional_dict = dict()

    for i, url in enumerate(htmls):
        print(i)
        try:
            if "Products" in htmls[i]["Includes"]:
                json_response_descr = htmls[i]
                my_product_id = list(
                    htmls[i]["Includes"]["Products"].keys())[0]
                print(my_product_id)
                short_response_descr = htmls[i]["Includes"]["Products"][f"{my_product_id}"]

                functional_dict[my_product_id] = {}
                functional_dict[my_product_id]["product_id"] = my_product_id
                functional_dict[my_product_id]["modelNbr"] = json_response_descr[
                    "Includes"]["Products"][f"{my_product_id}"]["ModelNumbers"][0]

                item_category = short_response_descr["Attributes"]["Category"]["Values"][0]["Value"].split()[
                    0].rstrip(">")
                if item_category == "APPLIANCES":
                    try:
                        functional_dict[my_product_id]["Category"] = str(
                            item_category)
                        functional_dict[my_product_id]["ApplType"] = short_response_descr[
                            "Attributes"]["THDClass_name"]["Values"][0]["Value"]
                        functional_dict[my_product_id]["Type1"] = short_response_descr[
                            "Attributes"]["THDSubClass_name"]["Values"][0]["Value"]
                        try:
                            functional_dict[my_product_id]["Type2"] = short_response_descr[
                                "Attributes"]["THD_SubSubClass_name"]["Values"][0]["Value"]
                        except KeyError:
                            print('Can not find "something"')

                        try:
                            functional_dict[my_product_id]["Title"] = short_response_descr["Name"]
                            functional_dict[my_product_id]["Brand"] = short_response_descr["Brand"]["Name"]
                        except KeyError:
                            print('Can not find "something"')

                        functional_dict[my_product_id]["ImageUrl"] = short_response_descr["ImageUrl"]

                        try:
                            functional_dict[my_product_id]["ProductPageUrl"] = short_response_descr["ProductPageUrl"]
                        except KeyError:
                            functional_dict[my_product_id][
                                "ProductPageUrl"] = f"https://homedepot.com/s/{my_product_id}"

                        functional_dict[my_product_id]["Description"] = short_response_descr["Description"]
                    except KeyError:
                        print('Can not find Description')
                        print(f"my_dict:{functional_dict}")
        except UnicodeEncodeError:
            print("UnicodeEncodeError")
    print(functional_dict)


# Creates folders

# def folder_creator(data):
#     try:
#         if not os.path.exists(""):
#             os.makedirs(f"data_async/{data}")
#     except FileExistsError:
#         print("File data already exists")

# def subdirectory_finder():
#     directory = "./data"
#     for root, subdirectories, files in os.walk(directory):
#         for subdirectory in subdirectories:
#             data = (os.path.join(subdirectory))
#             folder_creator(data)

# folder_creator("appliances.json")
# subdirectory_finder()
