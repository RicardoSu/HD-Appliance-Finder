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
import os


def json_finder(folder_name, json_file):
    path = f"data/{folder_name}/{json_file}.json"

    with open(path) as json_file:
        appliance_json = json.load(json_file)
    return appliance_json


def availability_checker(folder_name, json_file):
    mydict = json_finder(folder_name, json_file)
    functional_dict = dict()

    list_to_iterate = list(mydict.values())[0]

    for my_product_id in list_to_iterate:

        my_product_id = int(my_product_id)

        description_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{my_product_id}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

        # uses url decode function to loop through url and extract data

        json_response_descr = url_decoder(description_url)

        # if key deliveryAvailability is on the json reponse returns true
        if "Products" in json_response_descr["Includes"]:
            new_id = list(
                json_response_descr["Includes"]["Products"].keys())[0]
            if my_product_id != new_id:
                my_product_id = int(new_id)

            functional_dict[my_product_id] = {}
            functional_dict[my_product_id]["product_id"] = my_product_id
            functional_dict[my_product_id]["modelNbr"] = json_response_descr[
                "Includes"]["Products"][f"{my_product_id}"]["ModelNumbers"][0]
            description_parser(functional_dict, my_product_id)
            bs4_decoder(functional_dict, my_product_id)

        elif "Products" in json_response_descr["Includes"]:
            print(f"{my_product_id} DNE")

        else:
            print(f"{my_product_id} is not an Appliance or OOS")

    try:
        json_key = f"specs/{folder_name}/{json_file}.json"

        with open(json_key, 'w') as fp:
            json.dump(functional_dict, fp, indent=4, ensure_ascii=False)

    except IOError:
        print("I/O error")


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


def bs4_decoder(my_dict, my_product_id):
    my_product_id = int(my_product_id)
    # temp dict
    details_url = f"https://www.homedepot.com/s/{my_product_id}"

    with urllib.request.urlopen(details_url) as url:
        # decodes json file
        soup = BeautifulSoup(url, "html.parser")

    res = soup.find('script', id="thd-helmet__script--productStructureData")

    try:
        json_object = json.loads(res.contents[0])

    except AttributeError:
        print("Empty")
        my_dict[my_product_id]["Discontinued"] = True

    try:
        if "offers" in json_object:
            my_dict[my_product_id]["depth"] = json_object["depth"]
            my_dict[my_product_id]["height"] = json_object["height"]
            my_dict[my_product_id]["width"] = json_object["width"]
            my_dict[my_product_id]["ratingValue"] = json_object["aggregateRating"]["ratingValue"]
            my_dict[my_product_id]["reviewCount"] = json_object["aggregateRating"]["reviewCount"]
            my_dict[my_product_id]["price"] = json_object["offers"]["price"]
            my_dict[my_product_id]["priceValidUntil"] = json_object["offers"]["priceValidUntil"]
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


def description_parser(my_dict, my_product_id):
    my_product_id = int(my_product_id)

    description_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{my_product_id}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

    json_response_descr = url_decoder(description_url)

    try:
        for key, value in json_response_descr["Includes"]["Products"].items():
            print(f"Key:{key}")
    except KeyError:
        print(f"Bad key")

    print(f"my_product_id1:{my_product_id}")

    if my_product_id != key:
        my_product_id = key
    print(f"my_product_id2:{my_product_id}")
    # item number is diferent from imput
    my_product_id = int(my_product_id)

    short_response_descr = json_response_descr["Includes"]["Products"][f"{my_product_id}"]

    item_category = short_response_descr["Attributes"]["Category"]["Values"][0]["Value"].split()[
        0].rstrip(">")

    print(f"my_product_id3:{my_product_id}")

    if item_category == "APPLIANCES":
        try:
            my_dict[my_product_id]["Category"] = str(item_category)
            my_dict[my_product_id]["ApplType"] = short_response_descr["Attributes"]["THDClass_name"]["Values"][0]["Value"]
            my_dict[my_product_id]["Type1"] = short_response_descr["Attributes"]["THDSubClass_name"]["Values"][0]["Value"]
            try:
                my_dict[my_product_id]["Type2"] = short_response_descr["Attributes"]["THD_SubSubClass_name"]["Values"][0]["Value"]
            except KeyError:
                print('Can not find "something"')

            try:
                my_dict[my_product_id]["Title"] = short_response_descr["Name"]
                my_dict[my_product_id]["Brand"] = short_response_descr["Brand"]["Name"]
            except KeyError:
                print('Can not find "something"')

            my_dict[my_product_id]["ImageUrl"] = short_response_descr["ImageUrl"]

            try:
                my_dict[my_product_id]["ProductPageUrl"] = short_response_descr["ProductPageUrl"]
            except KeyError:
                my_dict[my_product_id][
                    "ProductPageUrl"] = f"https://homedepot.com/s/{my_product_id}"

            my_dict[my_product_id]["Description"] = short_response_descr["Description"]
        except KeyError:
            print('Can not find Description')
            print(json_response_descr["Includes"]["Products"])
            print(f"my_dict:{my_dict}")


@cache
def folder_creator(data):
    try:
        if not os.path.exists(""):
            os.makedirs(f"specs/{data}")
    except FileExistsError:
        print("File data already exists")


def subdirectory_finder():
    directory = "./data"
    for root, subdirectories, files in os.walk(directory):
        for subdirectory in subdirectories:
            data = (os.path.join(subdirectory))
            folder_creator(data)


def files_subdirectory_finder():
    directory = "./data"
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            folder_name = (os.path.join(root.replace(f"./data\\", "")))
            file_name = (os.path.join(file.replace(".json", "")))
            availability_checker(folder_name, file_name)


files_subdirectory_finder()
# availability_checker("dryers","non_stackable_eletric")
