import requests
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

baseurl = 'https://sandbox.iexapis.com/stable'
api_key = os.getenv('SANDBOX_KEY')

class Backtest(Resource):

	def calculate(self, series, init_amnt, rec_amnt):
		historical_prices = [price['close'] for price in series]
		holdings = [init_amnt/historical_prices[0]]
		investments = [init_amnt]
		for price in historical_prices[1:]:
			if not rec_amnt == 0:
				holdings.append(holdings[-1]+rec_amnt/price)
				investments.append(investments[-1]+rec_amnt)
			else:
				holdings.append(holdings[0])
				investments.append(investments[0])
		for holding, investment, series_datapoint in zip(holdings, investments, series):
			series_datapoint['value'] = series_datapoint['close'] * holding
			series_datapoint['invested'] = investment
			series_datapoint['holdings'] = holding
		return series

	def get (self, ticker, startdate, enddate, freq, init_amnt, rec_amnt):
		
		# check valid arguments
		if int(enddate) < int(startdate) or int(freq) < 0:
			return None

		# check if ticker exists
		try:
			url = f'{baseurl}/ref-data/iex/symbols?token={api_key}'
			response = requests.get(url)
			response.raise_for_status()
		except requests.RequestException:
			return None

		try:
			res = response.json()
			symbols = [stock['symbol'] for stock in res]
		except (KeyError, TypeError, ValueError):
			return None

		# get historical prices
		if ticker in symbols:
			url = f'{baseurl}/time-series/HISTORICAL_PRICES/{ticker}?token={api_key}&filter=date,close&interval={freq}&from={startdate}&to={enddate}'
			try:
				response = requests.get(url)
				response.raise_for_status()
				res = response.json() # IEX provides chronologically most recent first
				res.reverse()
				for series_datapoint in res:
					series_datapoint['date'] = datetime.utcfromtimestamp(series_datapoint['date']/1000).strftime('%Y-%m-%d')
				return self.calculate(res, float(init_amnt), float(rec_amnt))
			except requests.RequestException:
				return None
