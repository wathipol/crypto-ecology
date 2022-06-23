from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from ecology_data_sdk import (
    get_co2_from_all_transaction, KWH_TO_CO2_CONST,
    total_btc_transaction_count, get_single_transaction_energy_price)
from datetime import datetime
from models import AllTransactionCO2
from flask_pymongo import PyMongo
import os
import time


app = Flask(__name__)
load_dotenv()
DEBUG_MODE = True
MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI is None:
    print("App not initialized...")
    exit()
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


def get_co_data():
    co2_data = get_co2_from_all_transaction()
    while not co2_data:
        time.sleep(0.3)
        co2_data = get_co2_from_all_transaction()
    return co2_data


def get_domain(request):
    return str(request.url_root)[7:][0:-1]


def get_saved_values(only_first_month_day=False):
    out = []
    for v in mongo.db["co_values"].find():
        out.append(AllTransactionCO2(**v))
    if only_first_month_day:
        for v in out:
            d = str(v.stamp).split(".")[0]
            if d != "01" and d != "1":
                del out[out.index(v)]
    return out


def get_month_label_from_num(num):
    m_label = str(num)
    if m_label == "01" or m_label == "1":
        m_label = "Січень"
    elif m_label == "02" or m_label == "2":
        m_label = "Лютий"
    elif m_label == "03" or m_label == "3":
        m_label = "Березень"
    elif m_label == "04" or m_label == "4":
        m_label = "Квітень"
    elif m_label == "05" or m_label == "5":
        m_label = "Травень"
    elif m_label == "06" or m_label == "6":
        m_label = "Червень"
    elif m_label == "07" or m_label == "7":
        m_label = "Липень"
    elif m_label == "08" or m_label == "8":
        m_label = "Серпень"
    elif m_label == "09" or m_label == "9":
        m_label = "Вересень"
    elif m_label == "10":
        m_label = "Жовтень"
    elif m_label == "11":
        m_label = "Листопад"
    elif m_label == "12":
        m_label = "Грудень"
    return m_label


@app.route("/")
def index():
    domain = str(request.url_root)[7:][0:-1]
    chart_map = {}
    for v in get_saved_values(only_first_month_day=True):
        m_label = get_month_label_from_num(str(v.stamp).split(".")[1])
        chart_map[m_label] = v.co2_value

    return render_template(
        "index.html", co2_data=get_co_data(),
        date=datetime.now().strftime("%d.%m.%Y"), domain=get_domain(request),
        chart_labels=list(chart_map.keys()), chart_data=list(chart_map.values()))


@app.route("/info")
def info():
    return render_template(
        "info.html", energy_co2=KWH_TO_CO2_CONST,
        transaction_count=total_btc_transaction_count(),
        single_transaction_energy_price=get_single_transaction_energy_price(),
        co2_data=get_co_data(), date=datetime.now().strftime("%d.%m.%Y"), domain=get_domain(request))


@app.route("/do")
def do():
    return render_template(
        "do.html", co2_data=get_co_data(),
        date=datetime.now().strftime("%d.%m.%Y"), domain=get_domain(request))


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    print("START")
