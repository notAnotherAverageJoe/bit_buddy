
import os
from flask import request
import requests


def get_bitcoin_data():
    # Retrieve API key from environment variable
    api_key = os.getenv('COINMARKETCAP_API_KEY')
    if not api_key:
        print('Error: CoinMarketCap API key not found.')
        return None
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': '1', 'limit': '10', 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}

    response = requests.get(url, headers=headers, params=parameters)
    if response.status_code == 200:
        data = response.json()
        bitcoin_data = data['data'][0]

        # Format the price to two decimal places
        bitcoin_price = bitcoin_data['quote']['USD']['price']
        bitcoin_data['quote']['USD']['price'] = round(bitcoin_price, 2)

        return bitcoin_data
    else:
        print('Error:', response.status_code)
        return None



def get_blockchain_info():
    url = 'https://blockchain.info/latestblock'
    response = requests.get(url)
    
    if response.status_code == 200:
        blockchain_info = response.json()
        return blockchain_info
    else:
        print('Error:', response.status_code)
        return None
    