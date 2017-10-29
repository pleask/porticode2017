from flask import Flask, render_template, request, jsonify, make_response
from resources import twittersentiment, stocklist, stocks
from json import dumps

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/browser")
def browser():
    return render_template("browser.html")

@app.route("/sentiment")
def sentiment():
    return render_template("sentiment.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/twitter', methods = ['POST'])
def get_twitter():
    jsdata = request.get_json()
    print(jsdata)
    try:
        data = jsonify(twittersentiment.maintwitter(jsdata['data']))
    except TypeError:
        data = "Twitter is dead"
    return data

import json
@app.route('/stocklist')
def get_stocks():
    print(stocklist.getlist())
    return make_response(dumps(stocklist.getlist()))

@app.route("/stockdata", methods = ['POST'])
def stock_data():
    jsdata = request.get_json()

    return(jsonify(stocks.getdata(jsdata['symbol'])))

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
