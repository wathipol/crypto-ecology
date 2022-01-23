#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect
import os



app = Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


import time



@app.route("/")
def index():
	return render_template("index.html")




# Получаем новые сообщения
if __name__ == "__main__":	
	app.run(host='0.0.0.0')
	print("START")


