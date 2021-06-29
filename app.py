from flask import Flask, render_template, url_for, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging, sys
from console_log import ConsoleLog


console = logging.getLogger('console')
console.setLevel(logging.DEBUG)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    conpleted = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def home():
    console.error('Error logged from Python')
    return render_template("index.html")
    
app.wsgi_app = ConsoleLog(app.wsgi_app, console)

@app.route('/appliances')
def appliances():
    return render_template("appliances.html")


@app.route('/appliances/refrigerators', methods=['GET', 'POST'])
def refrigerators():
    if request.method == 'POST':
        fridge = (request.form.get("fridge_type"))
        color = (request.form.get("Color_Type"))
        zip_code = (request.form.get("customer_zip_code"))
        file_to_open = (f"{fridge}_{color}.json")
        print(f"json file  ={file_to_open}")
        print(f"zip code = {zip_code}")
        return products()
    return render_template("refrigerators.html")

@app.route('/appliances/products')
def products():
    return render_template("products.html")


if __name__ == '__main__':
    app.run(debug=True)
