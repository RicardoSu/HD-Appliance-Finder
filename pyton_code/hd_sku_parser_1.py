from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from functools import cache
import requests
import urllib
import json
import time
import os

"""
Home depot SKU Parser:
This code uses the selenium web driver to scrape home depot SKUS
SKUS or Stock keeping unit are numbers given to merchandise to
easily track and categorize products, this code reads a JSON file
and scrapes the home depot website with the provided N-value that Home
Depot uses to order similar products, and return organized JSON files
 with the new data.

4092.004 seconds
"""


@cache
def json_reader(filename):
    file_to_open = open(f'pyton_code/{filename}', "r")
    json_data = json.loads(file_to_open.read())
    return json_data


@cache
def folder_creator(filename):
    try:
        if not os.path.exists(""):
            os.makedirs("data")
    except FileExistsError:
        print("File data already exists")

    try:
        json_file = json_reader(filename)
        for i, (father_keys, values) in enumerate(json_file.items()):
            os.makedirs(f"data/{father_keys}")
    except FileExistsError:
        print(f"File  already exists")


def load_dinamically(father_keys, keys, values):
    res = urllib.request.urlopen(f'https://www.homedepot.com/b/N-{values}')
    base_url = res.geturl()

    driver = webdriver.Chrome('./chromedriver')

    # set list to remove duplicates
    product_skus = set()
    base_url += '?experienceName=default&Nao=%s'

    for page_num in range(0, 1000):
        url = base_url % (page_num*24)

        driver.get(url)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # Change loading time for javascript to load properlly
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # Edited since it was grabbing all colors
        # lxml_father = soup.find_all(
        #     'div', attrs={"data-automation-id": "podnode"})

        # Only grabs specific N value color
        lxml_father = soup.find_all(
            'div', class_="desktop product-pod")

        # checks len to break code after there is no more results
        prev_len = len(product_skus)
        try:
            for result in lxml_father:
                # location where skus are stored
                meta = result.find('meta', attrs={'data-prop': 'productID'})
                # removes the extra data
                product_skus.add(int(meta['content'].split(".")[0]))

        except AttributeError:
            print("meta is not a child of lxml_father")

        # this line is optional and can determine when you want to break
        if len(product_skus) == prev_len:
            break

    driver.close()

    print(f"{len(product_skus)} SKU'S")

    product_skus = tuple(product_skus)

    final_dict = dict()
    final_dict[keys] = (product_skus)
    print(f" my dict = {final_dict}")

    product_skus = final_dict

    # Stores data
    try:
        json_key = f"data/{father_keys}/{keys}.json"

        with open(json_key, 'w') as fp:
            json.dump(product_skus, fp, indent=4, ensure_ascii=False)

    except IOError:
        print("I/O error")


def reader(filename):
    json_file = json_reader(filename)

    for i, (father_keys, values) in enumerate(json_file.items()):
        for i2, (appl_key, appl_value) in enumerate(values.items()):
            folder_creator(filename)
            load_dinamically(father_keys, appl_key, appl_value)


reader("appliances.json")
