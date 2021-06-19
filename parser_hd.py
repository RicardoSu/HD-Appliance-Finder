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

all_finder = "?NCNI-5&catStyle=ShowProducts"
appl_link = "https://www.homedepot.com/b/N-{id}"

dict_id = {
    "refrigerators":{
    "french_door_refrigerator": "5yc1vZc3oo",
    "side_by_side_refrigerator": "5yc1vZc3q0",
    "top_freezer_refrigerator" : "5yc1vZc3ns",
    "botton_freezer_refrigerator" : "5yc1vZc3p6",
    "mini_fridges" : "5yc1vZc4mo",
    "freezer": "5yc1vZc3p2",
    "commercial_refrigerators" : "5yc1vZc3oe",
    "freezerless_refrigerators" : "5yc1vZc3p9"
    },

    "dishwashers":{
    "front_control_24":"5yc1vZc3njZ1z0zbkpZ1z10atj",
    "top_control_24":"5yc1vZc3njZ1z0zbkpZ1z10atb",
    "compact":"5yc1vZc3poZ1z1dgdn",
    "portable":"5yc1vZc3p1",
    },

    "ranges":{
    "eletric_30_slide_in":"5yc1vZc3obZ1z0yhyoZ1z127ec",
    "eletric_30_freestanding":"5yc1vZc3obZ1z0yhyoZ1z127eh",
    "gas_30_slide_in":"5yc1vZc3oyZ1z0yhyoZ1z127ec",
    "gas_30_freestanding":"5yc1vZc3oyZ1z0yhyoZ1z127eh",
    "induction":"5yc1vZc9px0",
    "ranges_20_in":"5yc1vZc3obZ1z0yhyn",
    "ranges_24_in":"5yc1vZc3obZ1z0yhyq",
    },

    "microwaves":{   
    "over_the_range":"5yc1vZc3pa",
    "countertop":"5yc1vZc3p7",
    },

    "washing_machine":{
    "front_load_washers": "5yc1vZc3pj",
    "top_load_washers" : "5yc1vZc3oc",
    "top_load_washers" : "5yc1vZc3oc",
    "top_load_washers" : "5yc1vZc3ocZ1z17rwr",
    "Top Load Washers" : "5yc1vZc3ocZ1z17ryq"
    },

    "dryers":{
    "electric_dryers" : "5yc1vZc3q1",
    "gas_dryers": "5yc1vZc3o3",
    "stackable":"5yc1vZc3q1Z1z17ic0",
    "non_stackable":"5yc1vZc3q1Z1z17ibr",
    },
    "cooktops":{
    "radiant_30":"5yc1vZc3qaZ1z103g6Z1z1bjpg",
    "radiant_36":"5yc1vZc3qaZ1z1042gZ1z1bjpg",
    "induction_30":"5yc1vZc5lxZ1z103g6",
    "induction_36":"5yc1vZc5lxZ1z1042g",
    }
}


"""
availability checker uses start online product_id number from hd.com
stop product_id and zip code that locates nearest home depot
to provide information if an appliance is in stock
"""

def availability_checker(start, stop, zip_code):

    mydict = dict()

    for product_id in range(start, stop):

        print(product_id)

        appliance_url = f"https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{product_id}/zipCode/{zip_code}"
        description_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{product_id}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

        # uses url decode function to loop through url and extract data
        json_response = url_decoder(appliance_url)
        json_response_descr = url_decoder(description_url)

        # if key deliveryAvailability is on the json reponse returns true
        if "deliveryAvailability" in json_response["DeliveryAvailabilityResponse"]:

            mydict[product_id] = {}

            # shortned path
            shortned_response = json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]

            mydict[product_id]["product_id"] = product_id
            mydict[product_id]["modelNbr"] = shortned_response["availability"][0]["modelNbr"]
            mydict[product_id]["status"] = shortned_response["availability"][0]["status"]

            # checks if product is out of stock
            if "earliestAvailabilityDate" in json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]:

                mydict[product_id]["earliestAvailabilityDate"] = shortned_response["earliestAvailabilityDate"]
                description_parser(mydict, product_id)
                bs4_decoder(mydict,product_id)
                print(mydict)
                
            elif "en_US" in json_response_descr["Locale"]:
                print(f"{product_id} DNE")
                
            else:
                description_parser(mydict, product_id)
                bs4_decoder(mydict,product_id)
                print(mydict)
                
                

        else:
            print(f"{product_id} is not an Appliance")

        # cut code 1

        # CSV
        # csv file runs on each iteration
        # saves code until runs into a error
        json_dumper(mydict)
    csv_file(mydict)

#store data in a csv excel file
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

    data_json = "appliancesjson"
    try:
        with open(data_json, 'w') as fp:
            json.dump(dict, fp,  indent=4)
    except IOError:
        print("I/O error")

json_dumper(dict_id)

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

    description_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{my_product_id}&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

    json_response_descr = url_decoder(description_url)

    try:
        for key, value in json_response_descr["Includes"]["Products"].items():
            print(key)

    except KeyError:
        print("Bad key")
    
    
    if my_product_id != key:
        new_product_id = key

    # item number is diferent from imput

    short_response_descr = json_response_descr[
        "Includes"]["Products"][f"{new_product_id}"]

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


def redirect_link(param):
    res = urllib.request.urlopen(f'https://www.homedepot.com/b/N-{param}')
    finalurl = res.geturl()
    return finalurl


def load_dinamically(param):

    base_url = redirect_link(param)
    print(base_url)
    
    
    driver = webdriver.Chrome('./chromedriver')
    tags_dict = dict() 
    product_skus = set()
    base_url += '?experienceName=default&Nao=%s'
    
   
    for page_num in range(0,1000):
        url = base_url % (page_num*24)

        driver.get(url)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        father_meta = soup.find_all('div',"class:browse-search__pod col__6-12 col__6-12--xs col__4-12--sm col__4-12--md col__3-12--lg")
        meta = soup.find_all('meta',attrs={"data-prop":"productID"})

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
    
    driver.close() # closing the webdriver
    print(f"{len(product_skus)} SKU'S")
    return product_skus

# print(load_dinamically("5yc1vZc3ns"))


def sku_finder(param):

    product_skus = set()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    
    base_url = redirect_link(param)
    base_url += '?experienceName=default&Nao=%s'

   
    for page_num in range(0,1000):
        url = base_url % (page_num*24)

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as url:
            
            soup = BeautifulSoup(url, "lxml")  
        res = soup.find_all('meta',attrs={"data-prop":"productID"})

        prev_len = len(product_skus)

        for state in res:
            product_skus.add(state['content'].split(".")[0])
        if len(product_skus) == prev_len: break # this line is optional and can determine when you want to break

    return product_skus

# print(sku_finder("5yc1vZc3q0"))


def reader(my_dict_json,appliance_number,appliance_shape,*args,**kwargs):
  json_list = list(my_dict_json.keys())
  print(json_list)
  n_string = my_dict_json[json_list[appliance_number]]
  return n_string.get((list(n_string)[appliance_shape]))
  
print(reader(dict_id,1,0))


def json_storer_products(dict,appliance_number):
    data_json = f"{list(dict.keys()[appliance_number])}.json"
    try:
        with open(data_json, 'w') as fp:
            json.dump(dict, fp,  indent=4)
    except IOError:
        print("I/O error")

def dict_to_json(dict):
  app_json = json.dumps(dict)
  print(app_json)






















# cut code 1
# checks is key have an error
# elif "errorData" in json_response["DeliveryAvailabilityResponse"]:

#     mydict[product_id] = {}
#     mydict[product_id]["product_id"] = product_id

#     # shortned path
#     error = json_response["DeliveryAvailabilityResponse"]["errorData"]["errors"]["error"]["errorCode"]

#     mydict[product_id]["error"] = error

# elif "en_US" in json_response_descr["Locale"]:
#     print("DNE")

# else:
#     shortned_response_descr = json_response_descr[
#         "Includes"]["Products"][f"{product_id}"]
#     print(shortned_response_descr["Description"])
