#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect
from ecology_data_sdk import get_co2_from_all_transaction,KWH_TO_CO2_CONST,total_btc_transaction_count,get_single_transaction_energy_price
from datetime import datetime
import os
import time



app = Flask(__name__)
DEBUG_MODE = True
#app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


import time

def get_co_data():
	co2_data = get_co2_from_all_transaction()
	while not co2_data:
		time.sleep(0.3)
		co2_data = get_co2_from_all_transaction()
	return co2_data


def get_domain(request):
	return  str(request.url_root)[7:][0:-1]


@app.route("/")
def index():
	domain = str(request.url_root)[7:][0:-1]
	return render_template("index.html",co2_data=get_co_data(),date=datetime.now().strftime("%d.%m.%Y"),domain=get_domain(request))


@app.route("/info")
def info():
	return render_template("info.html",energy_co2=KWH_TO_CO2_CONST,transaction_count=total_btc_transaction_count(),single_transaction_energy_price=get_single_transaction_energy_price() ,co2_data=get_co_data(),date=datetime.now().strftime("%d.%m.%Y"),domain=get_domain(request))


@app.route("/do")
def do():
	return render_template("do.html",co2_data=get_co_data(),date=datetime.now().strftime("%d.%m.%Y"),domain=get_domain(request))




# Получаем новые сообщения
if __name__ == "__main__":	
	app.run(host="0.0.0.0",debug=DEBUG_MODE,port=int(os.environ.get('PORT', 5000))) 
	print("START")


