from flask import Flask, render_template, url_for, request, Response, jsonify
from concurrent.futures import ProcessPoolExecutor, as_completed
from flask_sqlalchemy import SQLAlchemy
from console_log import ConsoleLog
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging
import aiohttp
import asyncio
import pprint
import json
import sys
import ssl


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    conpleted = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


URLs = []


def json_finder(folder_name, json_file, zip_code):

    path = f"data/{folder_name}/{json_file}.json"

    with open(path) as json_file:
        appliance_json = json.load(json_file)
        sku_list = list(appliance_json.values())[0]
    hd_url = "https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{}/zipCode/{}"

    for sku in sku_list:
        URLs.append(hd_url.format(sku, zip_code))


async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def fetch_all(urls, loop):
    # If code doe not run and have error ValueError: too many file descriptors in select()
    # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


def finder():
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    urls = URLs
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    available_app = dict()
    for i, url in enumerate(htmls):
        if "errorData" in htmls[i]["DeliveryAvailabilityResponse"]:
            # print("Not a major appliance")
            pass
        elif htmls[i]["DeliveryAvailabilityResponse"]["deliveryAvailability"]["availability"][0]["status"] != "OOS_ETA_UNAVAILABLE":
            my_product_id = htmls[i]["DeliveryAvailabilityResponse"]["deliveryAvailability"]["availability"][0]["itemId"]

            available_app[my_product_id] = {}
            available_app[my_product_id]["product_id"] = my_product_id
            available_app[my_product_id]["status"] = htmls[i]["DeliveryAvailabilityResponse"]["deliveryAvailability"]["availability"][0]["status"]
            try:
                available_app[my_product_id]["earliestAvailabilityDate"] = htmls[i][
                    "DeliveryAvailabilityResponse"]["deliveryAvailability"]["earliestAvailabilityDate"]
            except KeyError:
                available_app[my_product_id]["earliestAvailabilityDate"] = "OOS"
        else:
            # print("OOS")
            pass

    return available_app
# End functions to process zipcode with data


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/appliances')
def appliances():
    return render_template("appliances.html")


@app.route('/appliances/products')
def products():
    return render_template("products.html")


@app.route('/appliances/refrigerators', methods=['GET', 'POST'])
def refrigerators():
    if request.method == 'POST':
        # Grabs user input
        fridge = (request.form.get("fridge_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))

        # file_to_open = (f"{fridge}_{color}.json")
        file_to_open = (f"{fridge}.json")

        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/refrigerators/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("refrigerators", fridge, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('refrigerators.html')


@app.route('/appliances/ranges', methods=['GET', 'POST'])
def ranges():
    if request.method == 'POST':
        # Grabs user input
        appl_range = (request.form.get("range_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{appl_range}_{color}.json")
        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/ranges/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("ranges", appl_range, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('ranges.html')


@app.route('/appliances/cooktops', methods=['GET', 'POST'])
def cooktops():
    if request.method == 'POST':
        # Grabs user input
        cooktops = (request.form.get("cooktops_type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{cooktops}.json")
        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/cooktops/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("cooktops", cooktops, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('cooktops.html')


@app.route('/appliances/dishwashers', methods=['GET', 'POST'])
def dishwashers():
    if request.method == 'POST':
        # Grabs user input
        dishwasher = (request.form.get("dishwasher_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{dishwasher}_{color}.json")
        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/dishwashers/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("dishwashers", dishwasher, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('dishwashers.html')


@app.route('/appliances/microwaves', methods=['GET', 'POST'])
def microwaves():
    if request.method == 'POST':
        # Grabs user input
        microwaves = (request.form.get("microwaves_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{microwaves}_{color}.json")
        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/microwaves/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("microwaves", microwaves, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('microwaves.html')


@app.route('/appliances/washer', methods=['GET', 'POST'])
def washer():
    if request.method == 'POST':
        # Grabs user input
        washer = (request.form.get("washer_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{washer}_{color}.json")
        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/washing_machine/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("washing_machine", washer, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('washing_machine.html')


@app.route('/appliances/dryer', methods=['GET', 'POST'])
def dryer():
    if request.method == 'POST':
        # Grabs user input
        dryers = (request.form.get("dryers_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{dryers}_{color}.json")
        print(f"file to open = {(file_to_open)}")

        # Grabs appliance data from files  - (STORED DATA)
        json_key = f"specs/dryers/{file_to_open}"
        with open(json_key) as data_dict:
            new_data_dict = json.load(data_dict)

        # Prints only available appliances - (NEW DATA)
        URLs = []
        json_finder("dryers", dryers, zip_code)
        json_data = finder()

        for k in new_data_dict:
            if k in json_data.keys():
                new_data_dict[k].update(json_data.get(k, {}))

        final_dict = dict()
        for i, (k, v) in enumerate(new_data_dict.items()):
            if "status" in v:
                final_dict[k] = v

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('dryers.html')


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
