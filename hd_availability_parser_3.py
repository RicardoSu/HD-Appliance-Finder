from functools import cache
import requests,json,re,urllib


def json_finder(folder_name,json_file):
    path = f"data/{folder_name}/{json_file}.json"

    with open(path) as json_file:
        appliance_json = json.load(json_file)
    return appliance_json
  
def url_decoder(url_encoded):
    # uses urllib to open json file and read
    with urllib.request.urlopen(url_encoded) as url:
        # decodes json file
        json_response = json.loads(url.read().decode())
    return json_response    


def availability_checker(folder_name,json_file, zip_code):
    mydict = json_finder(folder_name,json_file)
    list_to_iterate = list(mydict.values())[0]

    in_stock_dict = dict()

    for my_product_id in list_to_iterate:
        print(my_product_id)
        my_product_id = int(my_product_id)
        appliance_url = f"https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{my_product_id}/zipCode/{zip_code}"
        json_response = url_decoder(appliance_url)

        if "earliestAvailabilityDate" in json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]:
            in_stock_dict[my_product_id] = {}
            shortned_response = json_response["DeliveryAvailabilityResponse"]["deliveryAvailability"]
            in_stock_dict[my_product_id]["product_id"] = my_product_id
            in_stock_dict[my_product_id]["status"] = shortned_response["availability"][0]["status"]
            in_stock_dict[my_product_id]["earliestAvailabilityDate"] = shortned_response["earliestAvailabilityDate"]
        else:
            print("OOS")

    json_dumper(in_stock_dict,json_file)

def json_dumper(my_dict,json_file):
    try:
        json_key = f"temp/{json_file}.json"

        with open(json_key, 'w') as fp:
            json.dump(my_dict, fp,indent=4, ensure_ascii=False)

    except IOError:
        print("I/O error")

availability_checker("cooktops","radiant_30",33315)