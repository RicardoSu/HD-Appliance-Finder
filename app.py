from flask import Flask, render_template, url_for, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import sys
import pprint
import json
import requests
import aiohttp
import ssl
import asyncio
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from console_log import ConsoleLog


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


# Functions to porcess zipcode with data
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
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


def finder():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
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
# End functions to porcess zipcode with data


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/appliances')
def appliances():
    return render_template("appliances.html")


@app.route('/appliances/refrigerators', methods=['GET', 'POST'])
def refrigerators():
    if request.method == 'POST':
        # Grabs user input
        fridge = (request.form.get("fridge_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{fridge}_{color}.json")
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

        # parent_list  = [final_dict]
        # print(parent_list)

        return render_template('products.html', title="page",
                               jsonfile=final_dict.items())
    else:
        return render_template('refrigerators.html')


@app.route('/appliances/products')
def products():
    return render_template("products.html")


if __name__ == '__main__':
    app.run(debug=True)
