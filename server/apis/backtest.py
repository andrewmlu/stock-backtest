import requests
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os

load_dotenv()

baseurl = 'https://sandbox.iexapis.com/stable'
api_key = os.getenv('SANDBOX_KEY')

class Backtest(Resource):
	def get (self, ticker, startdate, enddate, freq, init_amnt=100, rec_amnt=0):
		
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
				res = response.json()
				return res
			except requests.RequestException:
				return None
