from decimal import Decimal
from twython import TwythonStreamer
import json
import os
import requests
import re

settings = {
    #'twitter_userid': "12137672", # gorillamania (for testing)
    'twitter_userid': "961445378", # officialmcafee
    'exchange_key': os.getenv("EXCHANGE_KEY"), # your Bittrex API key
    'exchange_secret': os.getenv("EXCHANGE_SECRET"), # your Bittrex API secret
    'buy_amount_btc': Decimal(2), # Amount to buy
    'limit_multiplier': Decimal(1.075), # How much over the current ticker to set the limit order
    'twitter_app_key': os.getenv("TWITTER_APP_KEY"),
    'twitter_app_secret': os.getenv("TWITTER_APP_SECRET"),
    'twitter_oauth_token': os.getenv("TWITTER_OAUTH_TOKEN"),
    'twitter_oauth_secret': os.getenv("TWITTER_OAUTH_SECRET"),
}

"""
Flow
1. Set up the streamer to listen to all tweets from twitter_username
2. When a tweet is found, parse for symbol
3. Is it a valid symbol for Bittrex?
4. BUY!
"""

def get_markets():
    # Fetch the current markets so we know if it is a valid symbol
    response = requests.get("https://bittrex.com/api/v1.1/public/getmarkets")
    assert response.status_code == 200 
    markets = []
    for m in response.json()["result"]:
        markets.append(m["MarketCurrency"])
    return markets
MARKETS = get_markets()


def handle_tweet(tweet):
    match = re.search("[A-Z]{3,5}", tweet)
    if not match:
        print("No symbol found in tweet: '%s'" % tweet)
        return

    symbol = match.group(0)
    if symbol not in MARKETS:
        print("%s is not tradeable on Bittrex" % symbol)
        return

    buy_crypto(symbol)


def buy_crypto(symbol):
    from bitex import Bittrex
    e = Bittrex(settings["exchange_key"], settings["exchange_secret"])

    pair = "BTC-" + symbol
    print("Fetching current quote for %s" % pair)
    quote = e.ticker(pair).formatted
    current_price = Decimal(quote[6])

    price = current_price * settings["limit_multiplier"]
    amount = settings["buy_amount_btc"] / price
    print("Buying %s of %s at %s" % (amount, symbol, price))
    response = e.bid(pair, price, amount, False)
    print(response.json())



## Set up the streamer
# https://twython.readthedocs.io/en/latest/usage/streaming_api.html
class OurStreamer(TwythonStreamer):

    def on_success(self, data):
        if "user" in data and data["user"]["id_str"] == settings["twitter_userid"]:
            print(json.dumps(data, indent=2))
            if 'text' in data:
                handle_tweet(data["text"])

    def on_error(self, status_code, data):
        print("Error:", status_code, data)
        self.disconnect()

print("Setting up Twitter feed listener")
stream = OurStreamer(
        settings["twitter_app_key"],
        settings["twitter_app_secret"],
        settings["twitter_oauth_token"],
        settings["twitter_oauth_secret"])
stream.statuses.filter(follow=settings["twitter_userid"])
print("Listening...")
