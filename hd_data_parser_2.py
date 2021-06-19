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

def json_finder(folder_name,json_file):
    path = f"data/{folder_name}/{json_file}.json"

    with open(path) as json_file:
        appliance_json = json.load(json_file)
    return appliance_json

# json_finder("cooktops","radiant_36_white")

def availability_checker(folder_name,json_file, zip_code):
    mydict = json_finder(folder_name,json_file)
    dict3 = mydict.copy()
    print(mydict)

    start = 0
    stop = len(mydict[json_file])

    for i,(k,dict_values) in enumerate(dict3.items()):
        print(f"counter: {i}")
        print(f"product_id: {dict_values[i]}")

        appliance_url = f"https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{dict_values[i]}/zipCode/{zip_code}"
        description_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{dict_values[i]}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

        # uses url decode function to loop through url and extract data
        json_response = url_decoder(appliance_url)
        json_response_descr = url_decoder(description_url)

        # if key deliveryAvailability is on the json reponse returns true
        if "deliveryAvailability" in json_response["DeliveryAvailabilityResponse"]:

            mydict[dict_values[i]] = {}

            # shortned path
            shortned_response = json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]

            mydict[dict_values[i]]["product_id"] = dict_values[i]
            mydict[dict_values[i]]["modelNbr"] = shortned_response["availability"][0]["modelNbr"]
            mydict[dict_values[i]]["status"] = shortned_response["availability"][0]["status"]

            # checks if product is out of stock
            if "earliestAvailabilityDate" in json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]:
                print("It stoped on the if")  
                mydict[dict_values[i]]["earliestAvailabilityDate"] = shortned_response["earliestAvailabilityDate"]
                description_parser(mydict, dict_values[i])
                bs4_decoder(mydict,dict_values[i])
                print("It stoped on the if") 
                
            elif "en_US" in json_response_descr["Locale"]:
                print("It stoped on the elif")
                print(f"{dict_values[i]} DNE")
                print("It stoped on the elif")
                
            else:
                print("It stoped on the else")
                description_parser(mydict, dict_values[i])
                bs4_decoder(mydict,dict_values[i])
                print("It stoped on the else")
                    
        else:
            print(f"{dict_values[i]} is not an Appliance")

    json_dumper(mydict)


def csv_file(dict):

    csv_columns = ['product_id', "Category", "Brand", "Type1", "Type2", 'modelNbr', "ApplType", 'reviewCount', 'height',  'depth', 'width', 'ratingValue', 'priceValidUntil', 'price',
                   'status', "earliestAvailabilityDate",  "Discontinued", "Title", "ImageUrl", "ProductPageUrl", "Description"]

    csv_file = "appliances_status.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            # lineterminator removes extra space on each line on csv
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in dict.values():
                writer.writerow(data)
    except IOError:
        print("I/O error")

#store data in a json file
def json_dumper(dict):

    data_json = "data.json"
    try:
        with open(data_json, 'w') as fp:
            json.dump(dict, fp,  indent=4)
    except IOError:
        print("I/O error")


def bs4_decoder(dict,my_product_id):

    #temp dict

    details_url = f"https://www.homedepot.com/s/{my_product_id}"

    with urllib.request.urlopen(details_url) as url:
        # decodes json file
        soup = BeautifulSoup(url, "html.parser")

    res = soup.find('script',id="thd-helmet__script--productStructureData")

    try:
        json_object = json.loads(res.contents[0])
        print(json_object)

    except AttributeError:
        print("Empty")
        dict[my_product_id]["Discontinued"] = True
        
    try:
        if "offers" in json_object:

            dict[my_product_id]["depth"] = json_object["depth"]
            dict[my_product_id]["height"] = json_object["height"]
            dict[my_product_id]["width"] = json_object["width"]
            dict[my_product_id]["ratingValue"] = json_object["aggregateRating"]["ratingValue"]
            dict[my_product_id]["reviewCount"] = json_object["aggregateRating"]["reviewCount"]
            dict[my_product_id]["price"] = json_object["offers"]["price"]
            dict[my_product_id]["priceValidUntil"] = json_object["offers"]["priceValidUntil"]
            
    except Exception as e:
        print(getattr(e, 'message', repr(e)))
        print(getattr(e, 'message', str(e)))
    # Logs the error appropriately. 


@cache
def url_decoder(url_encoded):
    # uses urllib to open json file and read
    with urllib.request.urlopen(url_encoded) as url:
        # decodes json file
        json_response = json.loads(url.read().decode())

    return json_response


def description_parser(dict, my_product_id):
    print(dict,my_product_id)

    description_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{my_product_id}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

    json_response_descr = url_decoder(description_url)

    try:
        for key, value in json_response_descr["Includes"]["Products"].items():
            print(key)
    except KeyError:
        print("Bad key")

    if my_product_id != key:
        my_product_id = key
    

    # item number is diferent from imput

    short_response_descr = json_response_descr[
        "Includes"]["Products"][f"{my_product_id}"]

    item_category = short_response_descr["Attributes"]["Category"]["Values"][0]["Value"].split()[
        0].rstrip(">")

    if item_category == "APPLIANCES":

        dict[my_product_id]["Category"] = item_category
        dict[my_product_id]["ApplType"] = short_response_descr["Attributes"]["THDClass_name"]["Values"][0]["Value"]
        dict[my_product_id]["Type1"] = short_response_descr["Attributes"]["THDSubClass_name"]["Values"][0]["Value"]
        try:
            dict[my_product_id]["Type2"] = short_response_descr["Attributes"]["THD_SubSubClass_name"]["Values"][0]["Value"]
        except KeyError:
            print('Can not find "something"')
        dict[my_product_id]["Title"] = short_response_descr["Name"]
        dict[my_product_id]["Brand"] = short_response_descr["Brand"]["Name"]
        dict[my_product_id]["ImageUrl"] = short_response_descr["ImageUrl"]
        dict[my_product_id]["ProductPageUrl"] = short_response_descr["ProductPageUrl"]
        dict[my_product_id]["Description"] = short_response_descr["Description"]

availability_checker("cooktops","radiant_36_white",33315)