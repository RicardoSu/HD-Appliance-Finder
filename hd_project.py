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

# imports json dictionary





# def json_reader(self, filename):
#     f = open(f'{filename}', "r")
#     # Reading from file
#     data = json.loads(f.read())
#     return data

def json_storer_products(self, filename):
    self.json_reader(filename)

    dictionary = json_reader(filename)
    dictionary_keys = list(dictionary.keys())

    for number, keys in enumerate(dictionary.keys()):
        data_json = f"{dictionary_keys[number]}.json"
        try:
            with open(f"data/{data_json}", 'w') as fp:
                json.dump(dictionary, fp,  indent=4)
        except IOError:
            print("I/O error")

# def redirect_link(self, parameter):
#     res = urllib.request.urlopen(f'https://www.homedepot.com/b/N-{parameter}')
#     finalurl = res.geturl()
#     return finalurl



# def reader(self, filename, appliance_type, appliance_shape):
#     self.json_reader(filename)
    
#     json_list = list(json_reader(filename).keys())
#     n_string = json_reader(filename)[json_list[appliance_type]]
#     return n_string.get((list(n_string)[appliance_shape]))


appl = GrabAllAppliances("appliances.json", "1", "0")
print(appl.load_dinamically("appliances.json", "1", "0"))
