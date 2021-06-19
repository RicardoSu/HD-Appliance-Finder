from bs4 import BeautifulSoup
import requests
import urllib
import json
import csv
from functools import cache
import requests
import json
import re
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


def hd_sku_parser(filename):
    #JSON reader
    json_opener = open(f'{filename}', "r")
    json_data = json.loads(json_opener.read())
    return json_data
    # return json_data

def folder_creator(filename):
    try:
        json_file = hd_sku_parser(filename)
        for i,(father_keys,values) in enumerate(json_file.items()):
            os.makedirs(f"data/{father_keys}")
    except FileExistsError:
            print("File already exists")

def load_dinamically(father_keys,keys,values):
    print(father_keys,keys,values)

    res = urllib.request.urlopen(f'https://www.homedepot.com/b/N-{values}')
    base_url = res.geturl()
    print(base_url)

    driver = webdriver.Chrome('./chromedriver')

    product_skus = set()
    base_url += '?experienceName=default&Nao=%s'

    for page_num in range(0, 1000):
        url = base_url % (page_num*24)

        driver.get(url)
        driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        father_meta = soup.find_all(
            'div', "class:browse-search__pod col__6-12 col__6-12--xs col__4-12--sm col__4-12--md col__3-12--lg")
        meta = soup.find_all('meta', attrs={"data-prop": "productID"})

        try:
            if meta in father_meta:
                return meta
        except AttributeError:
            print("meta is not a child of father")

        prev_len = len(product_skus)
        for state in meta:
            product_skus.add(state['content'].split(".")[0])

        if len(product_skus) == prev_len: break
        # this line is optional and can determine when you want to break
    driver.close()  # closing the webdriver
    
    print(f"{len(product_skus)} SKU'S")
 
    product_skus = tuple(product_skus)

    final_dict = dict()
    final_dict[keys] = (product_skus)
    print(f" my dict ={final_dict}")

    product_skus = final_dict

    try:
        json_key = f"data/{father_keys}/{keys}.json"

        with open(json_key, 'w') as fp:
            json.dump(product_skus, fp,indent=4, ensure_ascii=False)

    except IOError:
        print("I/O error")

def reader(filename):
    json_file = hd_sku_parser(filename)
    json_list = list(json_file.keys())

    for i,(father_keys,values) in enumerate(json_file.items()):
        # print(f"dic_keys = {father_keys}")
        # print(f"dic_values={values}")
        for i2,(appl_key,appl_value) in enumerate(values.items()):
            # print(f"appl_key = {appl_key}")
            # print(f"appl_value = {appl_value}")
            folder_creator(filename)
            load_dinamically(father_keys,appl_key,appl_value)

 
print(reader("appliances.json"))