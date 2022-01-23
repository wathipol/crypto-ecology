import requests
import re
from bs4 import BeautifulSoup



# Средне значение за 2019 (Ичтоник: https://www.iea.org/reports/global-energy-co2-status-report-2019/emissions)
KWH_TO_CO2_CONST = 475



def get_single_transaction_description_data():
	""" Получить текстовый блок о цене одной транзакции по данным digiconomist """
	url = 'https://digiconomist.net/bitcoin-energy-consumption/'
	try:
		response = requests.get(url)
	except:
		return False
	soup = BeautifulSoup(response.text, 'html.parser')
	quotes = soup.find_all('div', class_='rpt_plan')
	for d in quotes:
		if str(d.text).find("household over") > 0:
			return str(d.text)






def get_single_transaction_energy_price():
	""" Получить цену kWh за одну транзакцию """
	data_text = get_single_transaction_description_data()
	if not data_text:
		return False
	start_ind = int(data_text.find(" kWh")) - 1
	data = []

	for i in range(1,100):
		tmp_val = str(data_text[start_ind])
		try:
			tmp = int(tmp_val)
			data.append(tmp_val)
			start_ind -= 1
		except:
			if tmp_val == ".":
				data.append(".")
				start_ind -= 1
			else:
				break
	data.reverse()
	full_string = "".join(data)
	try:
		data = float(full_string)
		return data
	except:
		return False



def get_co2_from_single_transaction():
	''' Получить средний след kgCO2 за одну транзакцию '''
	energy_price = get_single_transaction_energy_price()
	if not energy_price:
		return False
	return (energy_price * KWH_TO_CO2_CONST) / 1000





