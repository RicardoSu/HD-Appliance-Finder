from hd_data_parser_2 import json_finder, url_decoder
from bs4 import BeautifulSoup
import requests
import urllib
import json
import csv
from functools import cache
import requests,json,re,urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def availability_checker(folder_name,json_file, zip_code):
    mydict = json_finder(folder_name,json_file)
    
    functional_dict = dict()
    list_to_iterate = list(mydict.values())[0]

    for my_product_id in list_to_iterate:
        my_product_id = int(my_product_id)
        appliance_url = f"https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{my_product_id}/zipCode/{zip_code}"
        json_response = url_decoder(appliance_url)

        if "deliveryAvailability" in json_response["DeliveryAvailabilityResponse"]:
            functional_dict[my_product_id] = {}
            shortned_response = json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]

        if "earliestAvailabilityDate" in json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]:
            functional_dict[my_product_id]["earliestAvailabilityDate"] = shortned_response["earliestAvailabilityDate"]
            description_parser(functional_dict, my_product_id)
            bs4_decoder(functional_dict, my_product_id)
